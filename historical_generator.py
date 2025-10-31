"""
Historical Data Generator - Premium Edition
Generates 6 months of realistic historical SOM data with:
- Seasonal patterns
- Competitive dynamics
- Campaign events
- Realistic noise
"""
import json
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List
import random


class HistoricalDataGenerator:
    """Generate realistic historical SOM data"""
    
    def __init__(self, brands: List[str], categories: List[str]):
        self.brands = brands
        self.categories = categories
        self.random = np.random.RandomState(42)  # Reproducible
        
        # Define brand characteristics (base SOM and growth trajectory)
        self.brand_profiles = {
            'Telekom': {'base_som': 0.78, 'growth_rate': 0.003, 'volatility': 0.02},
            'Vodafone': {'base_som': 0.68, 'growth_rate': -0.002, 'volatility': 0.025},
            'O2': {'base_som': 0.58, 'growth_rate': 0.001, 'volatility': 0.03},
            '1&1': {'base_som': 0.42, 'growth_rate': 0.005, 'volatility': 0.035},
            'Congstar': {'base_som': 0.35, 'growth_rate': 0.002, 'volatility': 0.04},
            'Fraenk': {'base_som': 0.28, 'growth_rate': 0.008, 'volatility': 0.045},
            'Otelo': {'base_som': 0.32, 'growth_rate': -0.001, 'volatility': 0.04},
            'Freenet Mobile': {'base_som': 0.30, 'growth_rate': 0.001, 'volatility': 0.038},
            'Aldi Talk': {'base_som': 0.45, 'growth_rate': 0.002, 'volatility': 0.032},
            'Lidl Connect': {'base_som': 0.38, 'growth_rate': 0.004, 'volatility': 0.036},
            'WinSIM': {'base_som': 0.25, 'growth_rate': 0.003, 'volatility': 0.042},
            'PremiumSIM': {'base_som': 0.27, 'growth_rate': 0.002, 'volatility': 0.04}
        }
        
        # Campaign events (affect specific brands in specific months)
        self.campaign_events = [
            {'month': -5, 'brand': 'Telekom', 'impact': 0.05, 'category': 'network_quality'},
            {'month': -4, 'brand': 'Vodafone', 'impact': -0.03, 'category': 'customer_service'},
            {'month': -3, 'brand': 'O2', 'impact': 0.04, 'category': 'price'},
            {'month': -2, 'brand': '1&1', 'impact': 0.06, 'category': 'general'},
            {'month': -1, 'brand': 'Fraenk', 'impact': 0.08, 'category': 'student'},
        ]
        
        # Seasonal patterns by category
        self.seasonal_patterns = {
            'general': [0, -0.01, -0.02, 0.01, 0.02, 0],  # Slight summer dip
            'price': [0.02, 0.01, -0.01, -0.02, 0, 0.02],  # Higher in winter/year-end
            'network_quality': [0, 0, 0, 0, 0, 0],  # Stable
            'student': [-0.02, -0.02, 0.05, 0.08, -0.03, -0.02],  # Peak in Aug/Sep
            'business': [0.02, 0.01, 0, -0.02, -0.02, 0.01],  # Lower in summer
            'data_heavy': [0, 0.01, 0, 0, 0.01, 0],
            'prepaid': [0.01, 0, -0.01, 0, 0, 0.01],
            '5g': [0.02, 0.02, 0.01, 0.01, 0.01, 0],  # Growing interest
            'customer_service': [0, 0, 0, 0, 0, 0],
            'roaming': [-0.02, -0.02, 0.04, 0.05, 0.02, -0.01]  # Summer travel peak
        }
    
    def generate_month_data(self, month_offset: int, base_date: datetime, queries_per_month: int = 50) -> List[Dict]:
        """
        Generate data for a specific month
        month_offset: -6 to 0 (0 = current month)
        """
        results = []
        timestamp = (base_date + timedelta(days=30 * month_offset)).isoformat()
        
        for category in self.categories:
            # Number of queries per category
            queries_in_category = max(3, queries_per_month // len(self.categories))
            
            for query_idx in range(queries_in_category):
                for run in range(3):  # 3 runs per query
                    # Generate mentions for each brand
                    mentions = {}
                    mention_order = []
                    
                    for brand in self.brands:
                        profile = self.brand_profiles.get(brand, {
                            'base_som': 0.3,
                            'growth_rate': 0,
                            'volatility': 0.03
                        })
                        
                        # Calculate SOM for this month
                        base_som = profile['base_som']
                        growth = profile['growth_rate'] * month_offset
                        seasonal = self.seasonal_patterns.get(category, [0]*6)[month_offset % 6]
                        noise = self.random.normal(0, profile['volatility'])
                        
                        # Check for campaign events
                        campaign_boost = 0
                        for event in self.campaign_events:
                            if event['month'] == month_offset and event['brand'] == brand:
                                if category == event['category'] or event['category'] == 'general':
                                    campaign_boost = event['impact']
                        
                        # Final SOM for this brand/category/month
                        som = np.clip(base_som + growth + seasonal + noise + campaign_boost, 0.05, 0.95)
                        
                        # Determine if mentioned (based on SOM probability)
                        mentioned = self.random.random() < som
                        
                        if mentioned:
                            # Position in response (earlier = better)
                            position = int(self.random.exponential(3)) + 1
                            mention_count = int(self.random.poisson(1.5)) + 1
                            mention_order.append((brand, position))
                            
                            mentions[brand] = {
                                'mentioned': True,
                                'first_position': position * 50,  # Approximate character position
                                'count': mention_count
                            }
                        else:
                            mentions[brand] = {
                                'mentioned': False,
                                'first_position': None,
                                'count': 0
                            }
                    
                    # Sort mention order by position
                    mention_order.sort(key=lambda x: x[1])
                    mention_order_list = [brand for brand, _ in mention_order]
                    
                    # Generate synthetic response text
                    response_text = self._generate_response_text(mention_order_list, category)
                    
                    result = {
                        'timestamp': timestamp,
                        'category': category,
                        'query': self._get_sample_query(category),
                        'run': run,
                        'model': 'gpt-4o',
                        'provider': 'openai',
                        'response': response_text,
                        'mentions': mentions,
                        'mention_order': mention_order_list,
                        'total_mentioned': len(mention_order_list)
                    }
                    
                    results.append(result)
        
        return results
    
    def _generate_response_text(self, mentioned_brands: List[str], category: str) -> str:
        """Generate realistic response text"""
        if not mentioned_brands:
            return "There are several mobile providers in Germany, each with different strengths."
        
        # Templates by category
        templates = {
            'general': [
                f"In Germany, {mentioned_brands[0]} is often considered one of the top choices. ",
                f"Many users recommend {mentioned_brands[0]} for its overall service. "
            ],
            'price': [
                f"For budget-conscious customers, {mentioned_brands[0]} offers competitive pricing. ",
                f"If you're looking for value, {mentioned_brands[0]} has some of the best deals. "
            ],
            'network_quality': [
                f"{mentioned_brands[0]} is known for having excellent network coverage in Germany. ",
                f"The best network quality is typically associated with {mentioned_brands[0]}. "
            ],
            'student': [
                f"For students, {mentioned_brands[0]} offers special discounts and plans. ",
                f"Many students choose {mentioned_brands[0]} for affordable rates. "
            ],
            'business': [
                f"For business customers, {mentioned_brands[0]} provides comprehensive enterprise solutions. ",
                f"{mentioned_brands[0]} is a popular choice among business users. "
            ]
        }
        
        template = self.random.choice(templates.get(category, templates['general']))
        response = template
        
        # Add other mentioned brands
        if len(mentioned_brands) > 1:
            response += f"Other good options include {', '.join(mentioned_brands[1:3])}. "
        
        # Add some context
        context_phrases = [
            "Each provider has its strengths depending on your specific needs.",
            "Consider factors like coverage in your area and contract terms.",
            "It's worth comparing specific plans to find the best fit for you.",
            "Customer service quality can vary, so check recent reviews."
        ]
        response += self.random.choice(context_phrases)
        
        return response
    
    def _get_sample_query(self, category: str) -> str:
        """Get a sample query for the category"""
        queries = {
            'general': "Welcher Mobilfunkanbieter ist am besten in Deutschland?",
            'price': "Welcher ist der günstigste Mobilfunkanbieter?",
            'network_quality': "Welcher Anbieter hat das beste Netz?",
            'student': "Bester Handytarif für Studenten?",
            'business': "Mobilfunk für Unternehmen - welcher Anbieter?",
            'data_heavy': "Welcher Anbieter hat die besten Datentarife?",
            'prepaid': "Beste Prepaid-Karte in Deutschland?",
            '5g': "Welcher Anbieter hat das beste 5G-Netz?",
            'customer_service': "Welcher Mobilfunkanbieter hat den besten Kundenservice?",
            'roaming': "Welcher Anbieter hat die besten Roaming-Konditionen?"
        }
        return queries.get(category, "Welcher Mobilfunkanbieter ist empfehlenswert?")
    
    def generate_six_months(self, output_dir: str = "data") -> List[str]:
        """
        Generate 6 months of historical data
        Returns list of filenames
        """
        Path(output_dir).mkdir(exist_ok=True)
        
        base_date = datetime.now()
        filenames = []
        
        for month_offset in range(-5, 1):  # -5, -4, -3, -2, -1, 0
            month_date = base_date + timedelta(days=30 * month_offset)
            
            # Generate data
            data = self.generate_month_data(month_offset, base_date, queries_per_month=50)
            
            # Save to file
            filename = f"som_results_{month_date.strftime('%Y%m%d')}_historical.json"
            filepath = Path(output_dir) / filename
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            
            filenames.append(filename)
            print(f"✓ Generated {filename}: {len(data)} results")
        
        return filenames


def generate_historical_data():
    """Main function to generate historical data"""
    from config import BRANDS_TO_TRACK, ENABLED_CATEGORIES
    
    # Get enabled categories
    categories = [cat for cat, enabled in ENABLED_CATEGORIES.items() if enabled]
    
    generator = HistoricalDataGenerator(BRANDS_TO_TRACK, categories)
    
    print("Generating 6 months of historical SOM data...")
    print(f"Brands: {len(BRANDS_TO_TRACK)}")
    print(f"Categories: {len(categories)}")
    print()
    
    filenames = generator.generate_six_months()
    
    print()
    print(f"✓ Successfully generated {len(filenames)} months of data")
    print("Files saved to /data directory")
    
    return filenames


if __name__ == "__main__":
    generate_historical_data()