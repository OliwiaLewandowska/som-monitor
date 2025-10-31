"""
Storage manager for SOM results
"""
import json
import pandas as pd
from pathlib import Path
from typing import List, Optional
from datetime import datetime

from config import DATA_DIR, RESULTS_FILE, HISTORY_FILE
from models import QueryResult, BrandMention


class StorageManager:
    """Manages storage of SOM results"""
    
    def __init__(self, data_dir: str = DATA_DIR):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
    
    def save_results(self, results: List[QueryResult], 
                     filename: Optional[str] = None) -> str:
        """Save results to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"som_results_{timestamp}.json"
        
        filepath = self.data_dir / filename
        
        # Convert results to dict
        results_dict = [r.to_dict() for r in results]
        
        with open(filepath, 'w') as f:
            json.dump(results_dict, f, indent=2)
        
        print(f"Results saved to {filepath}")
        
        # Also update history
        self._update_history(results)
        
        return str(filepath)
    
    def load_results(self, filename: Optional[str] = None) -> List[QueryResult]:
        """Load results from JSON file"""
        if filename is None:
            # Load most recent file
            files = list(self.data_dir.glob("som_results_*.json"))
            if not files:
                return []
            filepath = max(files, key=lambda p: p.stat().st_mtime)
        else:
            filepath = self.data_dir / filename
        
        if not filepath.exists():
            print(f"File not found: {filepath}")
            return []
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Convert back to QueryResult objects
        results = []
        for item in data:
            # Convert mentions dict
            mentions = {
                brand: BrandMention(**mention_data)
                for brand, mention_data in item['mentions'].items()
            }
            
            result = QueryResult(
                timestamp=item['timestamp'],
                category=item['category'],
                query=item['query'],
                run=item['run'],
                model=item['model'],
                provider=item['provider'],
                response=item['response'],
                mentions=mentions,
                mention_order=item['mention_order'],
                total_mentioned=item['total_mentioned']
            )
            results.append(result)
        
        return results
    
    def _update_history(self, results: List[QueryResult]):
        """Update historical CSV with new results"""
        filepath = self.data_dir / HISTORY_FILE
        
        # Convert to DataFrame
        rows = []
        for r in results:
            for brand, mention in r.mentions.items():
                rows.append({
                    'timestamp': r.timestamp,
                    'date': r.timestamp.split('T')[0],
                    'provider': r.provider,
                    'model': r.model,
                    'category': r.category,
                    'query': r.query,
                    'run': r.run,
                    'brand': brand,
                    'mentioned': mention.mentioned,
                    'first_position': mention.first_position,
                    'count': mention.count,
                    'in_mention_order': brand in r.mention_order,
                    'mention_rank': r.mention_order.index(brand) + 1 if brand in r.mention_order else None
                })
        
        new_df = pd.DataFrame(rows)
        
        # Append to existing or create new
        if filepath.exists() and filepath.stat().st_size > 0:
            try:
                existing_df = pd.read_csv(filepath)
                df = pd.concat([existing_df, new_df], ignore_index=True)
            except pd.errors.EmptyDataError:
                df = new_df
        else:
            df = new_df
        
        df.to_csv(filepath, index=False)
        print(f"History updated: {filepath}")
    
    def get_history_df(self) -> pd.DataFrame:
        """Load historical data as DataFrame"""
        filepath = self.data_dir / HISTORY_FILE
        
        if not filepath.exists():
            return pd.DataFrame()
        
        return pd.read_csv(filepath)
    
    def get_results_files(self) -> List[str]:
        """Get list of all results files"""
        files = list(self.data_dir.glob("som_results_*.json"))
        return [f.name for f in sorted(files, key=lambda p: p.stat().st_mtime, reverse=True)]
