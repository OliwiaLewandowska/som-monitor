"""
Theme Analyzer - Extract narrative insights from LLM responses
Uses LLM to identify themes, attributes, and competitive narratives
"""
import re
from typing import Dict, List, Tuple, Set, Optional
from collections import defaultdict, Counter
from dataclasses import dataclass
import json

from models import QueryResult


@dataclass
class ThemeInsight:
    """A thematic insight about brand positioning"""
    theme: str
    brand: str
    frequency: float  # 0-1
    example_quotes: List[str]
    sentiment: str  # positive, neutral, negative
    
    def __str__(self):
        return f"{self.brand} → {self.theme}: {self.frequency:.0%} ({self.sentiment})"


@dataclass
class NarrativeAnalysis:
    """Analysis of competitive narratives"""
    attribute: str
    brand_ownership: Dict[str, float]  # brand -> ownership score
    leader: str
    leader_score: float
    gap_analysis: Dict[str, float]  # brand -> gap to leader
    example_quotes: Dict[str, List[str]]  # brand -> quotes


class ThemeAnalyzer:
    """Analyze themes and narratives in LLM responses"""
    
    # Premium mobile provider attributes
    ATTRIBUTES = [
        'reliability', 'network_quality', 'coverage', '5g',
        'price', 'value', 'affordable', 'cheap',
        'customer_service', 'support', 'service',
        'innovation', 'technology', 'modern',
        'speed', 'fast', 'performance',
        'international', 'roaming', 'global',
        'business', 'enterprise', 'corporate',
        'flexibility', 'contract', 'prepaid',
        'data', 'unlimited', 'volume',
        'premium', 'quality', 'best'
    ]
    
    # Attribute groupings for analysis
    ATTRIBUTE_GROUPS = {
        'Network Excellence': ['reliability', 'network_quality', 'coverage', '5g', 'speed', 'fast', 'performance'],
        'Value Proposition': ['price', 'value', 'affordable', 'cheap'],
        'Customer Experience': ['customer_service', 'support', 'service'],
        'Innovation': ['innovation', 'technology', 'modern', '5g'],
        'Global Reach': ['international', 'roaming', 'global'],
        'Data & Performance': ['data', 'unlimited', 'volume', 'speed', 'fast'],
        'Premium Positioning': ['premium', 'quality', 'best', 'reliability']
    }
    
    def __init__(self, brands: List[str]):
        self.brands = brands
        self._attribute_patterns = self._compile_patterns()
    
    def _compile_patterns(self) -> Dict[str, re.Pattern]:
        """Compile regex patterns for efficient attribute detection"""
        patterns = {}
        for attr in self.ATTRIBUTES:
            # Match word boundaries to avoid partial matches
            pattern = re.compile(r'\b' + re.escape(attr) + r'\w*\b', re.IGNORECASE)
            patterns[attr] = pattern
        return patterns
    
    def extract_themes(self, results: List[QueryResult]) -> Dict[str, Dict[str, ThemeInsight]]:
        """
        Extract themes for each brand from query results
        
        Returns:
            {brand: {theme: ThemeInsight}}
        """
        brand_themes = {brand: defaultdict(lambda: {'count': 0, 'quotes': []}) 
                       for brand in self.brands}
        
        for result in results:
            response_lower = result.response.lower()
            
            # For each brand mentioned
            for brand in self.brands:
                if not result.mentions[brand].mentioned:
                    continue
                
                # Extract surrounding context for this brand
                contexts = self._extract_brand_contexts(result.response, brand)
                
                # Check for attributes in contexts
                for context in contexts:
                    context_lower = context.lower()
                    for attr in self.ATTRIBUTES:
                        if self._attribute_patterns[attr].search(context_lower):
                            brand_themes[brand][attr]['count'] += 1
                            if len(brand_themes[brand][attr]['quotes']) < 5:
                                brand_themes[brand][attr]['quotes'].append(context[:200])
        
        # Convert to ThemeInsight objects
        insights = {}
        total_mentions = {brand: sum(1 for r in results if r.mentions[brand].mentioned) 
                         for brand in self.brands}
        
        for brand in self.brands:
            insights[brand] = {}
            if total_mentions[brand] == 0:
                continue
                
            for theme, data in brand_themes[brand].items():
                frequency = data['count'] / total_mentions[brand]
                if frequency > 0:  # Only include if mentioned
                    insights[brand][theme] = ThemeInsight(
                        theme=theme,
                        brand=brand,
                        frequency=frequency,
                        example_quotes=data['quotes'][:3],
                        sentiment=self._estimate_sentiment(data['quotes'])
                    )
        
        return insights
    
    def _extract_brand_contexts(self, text: str, brand: str, 
                               window: int = 150) -> List[str]:
        """
        Extract text context around brand mentions
        
        Args:
            text: Full response text
            brand: Brand name to find
            window: Characters to include before/after mention
            
        Returns:
            List of context strings
        """
        contexts = []
        brand_lower = brand.lower()
        text_lower = text.lower()
        
        # Find all occurrences
        start = 0
        while True:
            pos = text_lower.find(brand_lower, start)
            if pos == -1:
                break
            
            # Extract context window
            context_start = max(0, pos - window)
            context_end = min(len(text), pos + len(brand) + window)
            context = text[context_start:context_end]
            
            contexts.append(context)
            start = pos + 1
        
        return contexts
    
    def _estimate_sentiment(self, quotes: List[str]) -> str:
        """
        Estimate sentiment from quotes (simple heuristic)
        Could be enhanced with LLM-based sentiment analysis
        """
        positive_words = ['best', 'excellent', 'great', 'good', 'recommended', 
                         'strong', 'leading', 'top', 'superior', 'outstanding']
        negative_words = ['poor', 'bad', 'worst', 'avoid', 'limited', 
                         'weak', 'lacking', 'disappointing', 'issues']
        
        if not quotes:
            return 'neutral'
        
        text = ' '.join(quotes).lower()
        positive_count = sum(1 for word in positive_words if word in text)
        negative_count = sum(1 for word in negative_words if word in text)
        
        if positive_count > negative_count * 2:
            return 'positive'
        elif negative_count > positive_count * 2:
            return 'negative'
        else:
            return 'neutral'
    
    def analyze_narratives(self, 
                          theme_insights: Dict[str, Dict[str, ThemeInsight]]) -> List[NarrativeAnalysis]:
        """
        Analyze competitive narratives - who owns which attributes
        
        Returns:
            List of narrative analyses by attribute group
        """
        analyses = []
        
        for group_name, attributes in self.ATTRIBUTE_GROUPS.items():
            # Calculate aggregate scores for this attribute group
            brand_scores = {}
            brand_quotes = defaultdict(list)
            
            for brand in self.brands:
                if brand not in theme_insights:
                    brand_scores[brand] = 0.0
                    continue
                
                # Sum frequencies across attributes in group
                total_score = 0.0
                for attr in attributes:
                    if attr in theme_insights[brand]:
                        insight = theme_insights[brand][attr]
                        total_score += insight.frequency
                        brand_quotes[brand].extend(insight.example_quotes[:2])
                
                brand_scores[brand] = total_score / len(attributes) if attributes else 0.0
            
            # Find leader
            if brand_scores:
                leader = max(brand_scores.items(), key=lambda x: x[1])
                leader_brand, leader_score = leader
                
                # Calculate gaps
                gaps = {brand: leader_score - score 
                       for brand, score in brand_scores.items()}
                
                analyses.append(NarrativeAnalysis(
                    attribute=group_name,
                    brand_ownership=brand_scores,
                    leader=leader_brand,
                    leader_score=leader_score,
                    gap_analysis=gaps,
                    example_quotes=dict(brand_quotes)
                ))
        
        # Sort by leader score (most contested narratives first)
        analyses.sort(key=lambda x: x.leader_score, reverse=True)
        
        return analyses
    
    def generate_insights_text(self, 
                              narratives: List[NarrativeAnalysis],
                              your_brand: str) -> List[str]:
        """
        Generate human-readable strategic insights
        
        Returns:
            List of insight strings for display
        """
        insights = []
        
        for narrative in narratives:
            if your_brand not in narrative.brand_ownership:
                continue
            
            your_score = narrative.brand_ownership[your_brand]
            gap = narrative.gap_analysis[your_brand]
            
            # Skip if you're the leader
            if narrative.leader == your_brand:
                insights.append(
                    f"✅ **{narrative.attribute}**: You own this narrative "
                    f"({your_score:.0%} association rate)"
                )
            # Flag if you're significantly behind
            elif gap > 0.15:
                insights.append(
                    f"⚠️ **{narrative.attribute}**: {narrative.leader} dominates "
                    f"({narrative.leader_score:.0%} vs your {your_score:.0%}). "
                    f"Gap: {gap:.0%}"
                )
            # Flag opportunities (contested narratives)
            elif gap > 0.05 and narrative.leader_score < 0.50:
                insights.append(
                    f"🎯 **{narrative.attribute}**: Opportunity to own this narrative. "
                    f"Current leader {narrative.leader} at {narrative.leader_score:.0%}, "
                    f"you at {your_score:.0%}"
                )
        
        return insights[:5]  # Top 5 insights
    
    def extract_competitive_quotes(self, 
                                   results: List[QueryResult],
                                   brand: str,
                                   limit: int = 10) -> List[Dict[str, str]]:
        """
        Extract notable quotes about a specific brand
        
        Returns:
            List of {quote, category, brands_mentioned}
        """
        quotes = []
        
        for result in results:
            if not result.mentions[brand].mentioned:
                continue
            
            # Extract sentences mentioning the brand
            sentences = self._split_into_sentences(result.response)
            
            for sentence in sentences:
                if brand.lower() in sentence.lower():
                    # Check if it's a substantive mention (not just in a list)
                    if len(sentence.split()) > 10:
                        quotes.append({
                            'quote': sentence.strip(),
                            'category': result.category,
                            'brands_mentioned': ', '.join(result.mention_order),
                            'query': result.query[:80] + '...'
                        })
                    
                    if len(quotes) >= limit:
                        break
            
            if len(quotes) >= limit:
                break
        
        return quotes
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences (simple approach)"""
        # Split on periods, question marks, exclamation marks
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if len(s.strip()) > 20]
    
    def create_narrative_matrix(self,
                               narratives: List[NarrativeAnalysis]) -> Dict[str, Dict[str, float]]:
        """
        Create a matrix suitable for heatmap visualization
        
        Returns:
            {attribute: {brand: score}}
        """
        matrix = {}
        
        for narrative in narratives:
            matrix[narrative.attribute] = narrative.brand_ownership
        
        return matrix