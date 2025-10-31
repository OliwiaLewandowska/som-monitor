"""
Data models for SOM Monitor
"""
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
from datetime import datetime


@dataclass
class BrandMention:
    """Represents a brand mention in a response"""
    mentioned: bool
    first_position: Optional[int]
    count: int
    
    def to_dict(self):
        return asdict(self)


@dataclass
class QueryResult:
    """Represents a single query result"""
    timestamp: str
    category: str
    query: str
    run: int
    model: str
    provider: str
    response: str
    mentions: Dict[str, BrandMention]
    mention_order: List[str]
    total_mentioned: int
    
    def to_dict(self):
        return {
            'timestamp': self.timestamp,
            'category': self.category,
            'query': self.query,
            'run': self.run,
            'model': self.model,
            'provider': self.provider,
            'response': self.response,
            'mentions': {k: v.to_dict() for k, v in self.mentions.items()},
            'mention_order': self.mention_order,
            'total_mentioned': self.total_mentioned
        }


@dataclass
class SOMMetrics:
    """Share of Model metrics for a brand"""
    brand: str
    mention_rate: float
    first_mention_rate: float
    avg_position: Optional[float]
    total_mentions: int
    total_queries: int
    
    def to_dict(self):
        return asdict(self)
    
    def __str__(self):
        return (f"{self.brand}: {self.mention_rate:.1%} mention rate, "
                f"{self.first_mention_rate:.1%} first mention rate")


@dataclass
class SOMReport:
    """Complete SOM report"""
    timestamp: str
    provider: str
    model: str
    total_queries: int
    metrics: Dict[str, SOMMetrics]
    
    def to_dict(self):
        return {
            'timestamp': self.timestamp,
            'provider': self.provider,
            'model': self.model,
            'total_queries': self.total_queries,
            'metrics': {k: v.to_dict() for k, v in self.metrics.items()}
        }
