"""
Unit tests for SOM Monitor
"""
import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import BrandMention, QueryResult
from analyzer import ResponseAnalyzer
from monitor import SOMMonitor


class TestResponseAnalyzer(unittest.TestCase):
    """Test ResponseAnalyzer class"""
    
    def setUp(self):
        self.brands = ["OpenAI", "Anthropic", "Google"]
        self.analyzer = ResponseAnalyzer(self.brands)
    
    def test_extract_mentions_all_brands(self):
        """Test extraction when all brands are mentioned"""
        text = "OpenAI and Anthropic are great. Google is also good."
        mentions = self.analyzer.extract_mentions(text)
        
        self.assertTrue(mentions["OpenAI"].mentioned)
        self.assertTrue(mentions["Anthropic"].mentioned)
        self.assertTrue(mentions["Google"].mentioned)
    
    def test_extract_mentions_case_insensitive(self):
        """Test case-insensitive matching"""
        text = "openai and ANTHROPIC are mentioned"
        mentions = self.analyzer.extract_mentions(text)
        
        self.assertTrue(mentions["OpenAI"].mentioned)
        self.assertTrue(mentions["Anthropic"].mentioned)
    
    def test_extract_mentions_no_brands(self):
        """Test when no brands are mentioned"""
        text = "This text mentions no specific brands."
        mentions = self.analyzer.extract_mentions(text)
        
        for brand in self.brands:
            self.assertFalse(mentions[brand].mentioned)
    
    def test_get_mention_order(self):
        """Test mention order extraction"""
        text = "First Google, then OpenAI, finally Anthropic."
        mentions = self.analyzer.extract_mentions(text)
        order = self.analyzer.get_mention_order(mentions)
        
        self.assertEqual(order, ["Google", "OpenAI", "Anthropic"])
    
    def test_count_mentions(self):
        """Test counting multiple mentions"""
        text = "OpenAI is great. OpenAI also does research. OpenAI leads."
        mentions = self.analyzer.extract_mentions(text)
        
        self.assertEqual(mentions["OpenAI"].count, 3)
    
    def test_position_score(self):
        """Test position score calculation"""
        mention_order = ["OpenAI", "Anthropic", "Google"]
        
        score_first = self.analyzer.calculate_position_score(mention_order, "OpenAI")
        score_second = self.analyzer.calculate_position_score(mention_order, "Anthropic")
        score_third = self.analyzer.calculate_position_score(mention_order, "Google")
        
        self.assertEqual(score_first, 1.0)
        self.assertEqual(score_second, 0.5)
        self.assertAlmostEqual(score_third, 0.333, places=2)


class TestSOMMonitor(unittest.TestCase):
    """Test SOMMonitor class"""
    
    def setUp(self):
        self.brands = ["OpenAI", "Anthropic"]
        self.monitor = SOMMonitor(brands=self.brands)
    
    def test_initialization(self):
        """Test monitor initialization"""
        self.assertEqual(self.monitor.brands, self.brands)
        self.assertIsInstance(self.monitor.analyzer, ResponseAnalyzer)
    
    def test_calculate_som_empty(self):
        """Test SOM calculation with no results"""
        metrics = self.monitor.calculate_som([])
        self.assertEqual(metrics, {})
    
    def test_calculate_som_with_results(self):
        """Test SOM calculation with mock results"""
        # Create mock results
        mentions1 = {
            "OpenAI": BrandMention(mentioned=True, first_position=0, count=1),
            "Anthropic": BrandMention(mentioned=True, first_position=10, count=1)
        }
        
        mentions2 = {
            "OpenAI": BrandMention(mentioned=False, first_position=None, count=0),
            "Anthropic": BrandMention(mentioned=True, first_position=0, count=1)
        }
        
        result1 = QueryResult(
            timestamp="2024-01-01T00:00:00",
            category="general",
            query="Test query 1",
            run=0,
            model="gpt-4o",
            provider="openai",
            response="OpenAI and Anthropic",
            mentions=mentions1,
            mention_order=["OpenAI", "Anthropic"],
            total_mentioned=2
        )
        
        result2 = QueryResult(
            timestamp="2024-01-01T00:00:01",
            category="general",
            query="Test query 2",
            run=0,
            model="gpt-4o",
            provider="openai",
            response="Anthropic is great",
            mentions=mentions2,
            mention_order=["Anthropic"],
            total_mentioned=1
        )
        
        results = [result1, result2]
        metrics = self.monitor.calculate_som(results)
        
        # OpenAI: mentioned in 1/2 = 50%
        self.assertEqual(metrics["OpenAI"].mention_rate, 0.5)
        self.assertEqual(metrics["OpenAI"].first_mention_rate, 0.5)
        
        # Anthropic: mentioned in 2/2 = 100%
        self.assertEqual(metrics["Anthropic"].mention_rate, 1.0)
        self.assertEqual(metrics["Anthropic"].first_mention_rate, 0.5)


class TestBrandMention(unittest.TestCase):
    """Test BrandMention model"""
    
    def test_brand_mention_creation(self):
        """Test BrandMention creation"""
        mention = BrandMention(mentioned=True, first_position=5, count=3)
        
        self.assertTrue(mention.mentioned)
        self.assertEqual(mention.first_position, 5)
        self.assertEqual(mention.count, 3)
    
    def test_brand_mention_to_dict(self):
        """Test BrandMention to_dict conversion"""
        mention = BrandMention(mentioned=True, first_position=5, count=3)
        d = mention.to_dict()
        
        self.assertEqual(d["mentioned"], True)
        self.assertEqual(d["first_position"], 5)
        self.assertEqual(d["count"], 3)


if __name__ == "__main__":
    unittest.main()
