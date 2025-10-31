"""
Response analyzer for extracting brand mentions
"""
from typing import Dict, List, Tuple
from models import BrandMention


class ResponseAnalyzer:
    """Analyzes LLM responses for brand mentions"""
    
    def __init__(self, brands: List[str]):
        self.brands = brands
    
    def extract_mentions(self, text: str) -> Dict[str, BrandMention]:
        """Extract brand mentions and their positions"""
        text_lower = text.lower()
        mentions = {}
        
        for brand in self.brands:
            brand_lower = brand.lower()
            
            if brand_lower in text_lower:
                first_pos = text_lower.find(brand_lower)
                count = text_lower.count(brand_lower)
                mentions[brand] = BrandMention(
                    mentioned=True,
                    first_position=first_pos,
                    count=count
                )
            else:
                mentions[brand] = BrandMention(
                    mentioned=False,
                    first_position=None,
                    count=0
                )
        
        return mentions
    
    def get_mention_order(self, mentions: Dict[str, BrandMention]) -> List[str]:
        """Get brands in order of first mention"""
        mentioned_brands = [
            (brand, data.first_position) 
            for brand, data in mentions.items() 
            if data.mentioned
        ]
        mentioned_brands.sort(key=lambda x: x[1])
        return [brand for brand, _ in mentioned_brands]
    
    def analyze(self, response_text: str) -> Tuple[Dict[str, BrandMention], List[str], int]:
        """
        Analyze a response for brand mentions
        
        Returns:
            mentions: Dict of brand mentions
            mention_order: List of brands in order of appearance
            total_mentioned: Total number of brands mentioned
        """
        mentions = self.extract_mentions(response_text)
        mention_order = self.get_mention_order(mentions)
        total_mentioned = len(mention_order)
        
        return mentions, mention_order, total_mentioned
    
    def calculate_position_score(self, mention_order: List[str], brand: str) -> float:
        """
        Calculate position score (higher is better)
        First position = 1.0, second = 0.5, third = 0.33, etc.
        """
        if brand not in mention_order:
            return 0.0
        
        position = mention_order.index(brand) + 1
        return 1.0 / position
