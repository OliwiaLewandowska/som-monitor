"""
Core SOM Monitor class
"""
import json
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

from config import (
    BRANDS_TO_TRACK, QUERY_TEMPLATES, DATA_DIR, ENABLED_CATEGORIES,
    RUNS_PER_QUERY, TEMPERATURE, MAX_TOKENS
)
from models import QueryResult, SOMMetrics, SOMReport
from llm_client import LLMClientFactory
from analyzer import ResponseAnalyzer
from storage import StorageManager


class SOMMonitor:
    """Main SOM monitoring system"""
    
    def __init__(self, brands: Optional[List[str]] = None):
        self.brands = brands or BRANDS_TO_TRACK
        self.analyzer = ResponseAnalyzer(self.brands)
        self.storage = StorageManager()
        self.results: List[QueryResult] = []
    
    def run_survey(self, 
                   provider: str = "openai",
                   models: Optional[List[str]] = None,
                   categories: Optional[List[str]] = None,
                   runs_per_query: int = RUNS_PER_QUERY,
                   **client_kwargs) -> List[QueryResult]:
        """
        Run a complete SOM survey
        
        Args:
            provider: LLM provider (e.g., "openai")
            models: List of models to query
            categories: Query categories to run
            runs_per_query: Number of times to run each query
            **client_kwargs: Additional arguments for LLM client
        
        Returns:
            List of QueryResult objects
        """
        # Initialize client
        client = LLMClientFactory.create(provider, **client_kwargs)
        
        # Set defaults
        if models is None:
            models = ["gpt-4o"]
            
        # Handle categories based on ENABLED_CATEGORIES
        if categories is None:
            # Use all enabled categories from config
            categories = [cat for cat, enabled in ENABLED_CATEGORIES.items() if enabled]
        else:
            # Filter user-specified categories by enabled ones
            categories = [cat for cat in categories if ENABLED_CATEGORIES.get(cat, False)]
            
        if not categories:
            raise ValueError("No enabled categories found. Check ENABLED_CATEGORIES in config.py")
            
        timestamp = datetime.now().isoformat()
        self.results = []
        
        total_queries = sum(
            len(QUERY_TEMPLATES.get(cat, [])) 
            for cat in categories
        ) * runs_per_query * len(models)
        
        current = 0
        
        for category in categories:
            queries = QUERY_TEMPLATES.get(category, [])
            
            for query in queries:
                print(f"\n[{current}/{total_queries}] Category: {category}")
                print(f"Query: {query[:60]}...")
                
                for run in range(runs_per_query):
                    for model in models:
                        current += 1
                        print(f"  Run {run+1}/{runs_per_query}, Model: {model}...", end=" ")
                        
                        response = client.query(
                            query, 
                            model=model,
                            temperature=TEMPERATURE,
                            max_tokens=MAX_TOKENS
                        )
                        
                        if response:
                            mentions, mention_order, total_mentioned = \
                                self.analyzer.analyze(response)
                            
                            result = QueryResult(
                                timestamp=timestamp,
                                category=category,
                                query=query,
                                run=run,
                                model=model,
                                provider=provider,
                                response=response,
                                mentions=mentions,
                                mention_order=mention_order,
                                total_mentioned=total_mentioned
                            )
                            
                            self.results.append(result)
                            print("âœ“")
                        else:
                            print("âœ— (failed)")
        
        # Save results
        self.storage.save_results(self.results)
        print(f"\nâœ“ Survey complete! {len(self.results)} responses collected.")
        
        return self.results
    
    def calculate_som(self, results: Optional[List[QueryResult]] = None) -> Dict[str, SOMMetrics]:
        """Calculate SOM metrics from results"""
        if results is None:
            results = self.results
        
        if not results:
            return {}
        
        total_queries = len(results)
        som_metrics = {}
        
        for brand in self.brands:
            # Count mentions - handle missing brands gracefully
            mentions = sum(1 for r in results if brand in r.mentions and r.mentions[brand].mentioned)
            mention_rate = mentions / total_queries
            
            # Calculate average position when mentioned
            positions = []
            for r in results:
                if brand in r.mention_order:
                    pos = r.mention_order.index(brand) + 1
                    positions.append(pos)
            
            avg_position = sum(positions) / len(positions) if positions else None
            
            # Count first mentions
            first_mentions = sum(
                1 for r in results 
                if r.mention_order and r.mention_order[0] == brand
            )
            first_mention_rate = first_mentions / total_queries
            
            som_metrics[brand] = SOMMetrics(
                brand=brand,
                mention_rate=mention_rate,
                first_mention_rate=first_mention_rate,
                avg_position=avg_position,
                total_mentions=mentions,
                total_queries=total_queries
            )
        
        return som_metrics
    
    def generate_report(self, results: Optional[List[QueryResult]] = None) -> SOMReport:
        """Generate a complete SOM report"""
        if results is None:
            results = self.results
        
        if not results:
            raise ValueError("No results to generate report from")
        
        metrics = self.calculate_som(results)
        
        report = SOMReport(
            timestamp=datetime.now().isoformat(),
            provider=results[0].provider,
            model=results[0].model,
            total_queries=len(results),
            metrics=metrics
        )
        
        return report
    
    def print_report(self, report: Optional[SOMReport] = None):
        """Print a formatted report to console"""
        if report is None:
            report = self.generate_report()
        
        print("\n" + "="*70)
        print("SHARE OF MODEL REPORT")
        print("="*70)
        print(f"Provider: {report.provider}")
        print(f"Model: {report.model}")
        print(f"Total Queries: {report.total_queries}")
        print(f"Timestamp: {report.timestamp}")
        print("="*70)
        
        # Sort by mention rate
        sorted_metrics = sorted(
            report.metrics.items(),
            key=lambda x: x[1].mention_rate,
            reverse=True
        )
        
        print(f"\n{'Brand':<15} {'Mention Rate':<15} {'First Rate':<15} {'Avg Pos':<10}")
        print("-"*70)
        
        for brand, metrics in sorted_metrics:
            avg_pos_str = f"{metrics.avg_position:.2f}" if metrics.avg_position else "N/A"
            print(f"{brand:<15} {metrics.mention_rate:<15.1%} "
                  f"{metrics.first_mention_rate:<15.1%} {avg_pos_str:<10}")
        
        print("="*70)
    
    def load_results(self, filename: Optional[str] = None) -> List[QueryResult]:
        """Load results from storage"""
        self.results = self.storage.load_results(filename)
        return self.results