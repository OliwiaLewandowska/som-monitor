"""
Statistical Confidence Calculator for SOM Monitor
Provides rigorous statistical validation for enterprise-grade insights
"""
import numpy as np
from scipy import stats
from typing import Dict, Tuple, List, Optional
from dataclasses import dataclass


@dataclass
class ConfidenceMetrics:
    """Statistical confidence metrics for a measurement"""
    value: float
    lower_bound: float
    upper_bound: float
    confidence_level: float
    sample_size: int
    standard_error: float
    is_significant: bool
    margin_of_error: float
    
    def to_display_dict(self) -> Dict:
        """Format for display in UI"""
        return {
            'value': f"{self.value:.1%}",
            'range': f"{self.lower_bound:.1%} - {self.upper_bound:.1%}",
            'confidence': f"{self.confidence_level:.0%}",
            'sample_size': self.sample_size,
            'margin_of_error': f"±{self.margin_of_error:.1%}",
            'reliable': self.is_significant
        }


class ConfidenceCalculator:
    """Calculate statistical confidence for SOM metrics"""
    
    def __init__(self, confidence_level: float = 0.95):
        self.confidence_level = confidence_level
        self.z_score = stats.norm.ppf((1 + confidence_level) / 2)
    
    def calculate_proportion_confidence(self, 
                                       successes: int, 
                                       total: int) -> ConfidenceMetrics:
        """
        Calculate confidence interval for a proportion (e.g., mention rate)
        Uses Wilson score interval for better accuracy with small samples
        
        Args:
            successes: Number of positive outcomes (mentions)
            total: Total number of trials (queries)
            
        Returns:
            ConfidenceMetrics with interval bounds
        """
        if total == 0:
            return ConfidenceMetrics(
                value=0.0,
                lower_bound=0.0,
                upper_bound=0.0,
                confidence_level=self.confidence_level,
                sample_size=0,
                standard_error=0.0,
                is_significant=False,
                margin_of_error=0.0
            )
        
        proportion = successes / total
        
        # Wilson score interval (more accurate than normal approximation)
        z = self.z_score
        denominator = 1 + z**2 / total
        center = (proportion + z**2 / (2 * total)) / denominator
        margin = z * np.sqrt((proportion * (1 - proportion) + z**2 / (4 * total)) / total) / denominator
        
        lower = max(0, center - margin)
        upper = min(1, center + margin)
        
        # Standard error for reference
        se = np.sqrt(proportion * (1 - proportion) / total) if total > 1 else 0
        
        # Check if sample size is sufficient (at least 30 recommended)
        is_significant = total >= 30
        
        return ConfidenceMetrics(
            value=proportion,
            lower_bound=lower,
            upper_bound=upper,
            confidence_level=self.confidence_level,
            sample_size=total,
            standard_error=se,
            is_significant=is_significant,
            margin_of_error=margin
        )
    
    def compare_proportions(self,
                          successes1: int,
                          total1: int,
                          successes2: int,
                          total2: int) -> Tuple[float, bool, str]:
        """
        Compare two proportions statistically
        
        Returns:
            (p_value, is_significant, interpretation)
        """
        if total1 == 0 or total2 == 0:
            return 1.0, False, "Insufficient data"
        
        p1 = successes1 / total1
        p2 = successes2 / total2
        
        # Pooled proportion
        p_pool = (successes1 + successes2) / (total1 + total2)
        
        # Standard error of difference
        se_diff = np.sqrt(p_pool * (1 - p_pool) * (1/total1 + 1/total2))
        
        if se_diff == 0:
            return 1.0, False, "No variance"
        
        # Z-statistic
        z = (p1 - p2) / se_diff
        
        # Two-tailed p-value
        p_value = 2 * (1 - stats.norm.cdf(abs(z)))
        
        alpha = 1 - self.confidence_level
        is_significant = p_value < alpha
        
        # Interpretation
        if not is_significant:
            interpretation = "No significant difference"
        else:
            diff_pct = abs(p1 - p2) * 100
            direction = "higher" if p1 > p2 else "lower"
            interpretation = f"Significantly {direction} by {diff_pct:.1f}pp (p={p_value:.3f})"
        
        return p_value, is_significant, interpretation
    
    def required_sample_size(self,
                            expected_rate: float,
                            margin_of_error: float = 0.05) -> int:
        """
        Calculate required sample size for desired precision
        
        Args:
            expected_rate: Expected proportion (0-1)
            margin_of_error: Desired margin of error (default 5%)
            
        Returns:
            Required sample size
        """
        z = self.z_score
        p = expected_rate
        
        # Conservative estimate uses p=0.5 (maximum variance)
        n = (z**2 * p * (1 - p)) / (margin_of_error**2)
        
        return int(np.ceil(n))
    
    def evaluate_data_quality(self, sample_size: int) -> Dict[str, any]:
        """
        Evaluate overall data quality based on sample size
        
        Returns:
            Quality assessment with recommendations
        """
        if sample_size < 30:
            quality = "LOW"
            color = "#f44336"
            recommendation = f"Collect {30 - sample_size} more samples for statistical significance"
            icon = "⚠️"
        elif sample_size < 100:
            quality = "MODERATE"
            color = "#ff9800"
            recommendation = f"Consider {100 - sample_size} more samples for higher confidence"
            icon = "⚡"
        elif sample_size < 300:
            quality = "GOOD"
            color = "#4caf50"
            recommendation = "Sample size adequate for reliable insights"
            icon = "✓"
        else:
            quality = "EXCELLENT"
            color = "#2196f3"
            recommendation = "Sample size excellent for high-confidence analysis"
            icon = "⭐"
        
        return {
            'quality': quality,
            'color': color,
            'recommendation': recommendation,
            'icon': icon,
            'sample_size': sample_size
        }


class TrendAnalyzer:
    """Analyze trends in time series data"""
    
    @staticmethod
    def calculate_velocity(time_series: List[float]) -> Dict[str, any]:
        """
        Calculate velocity (rate of change) in a metric
        
        Returns:
            Velocity metrics including direction and acceleration
        """
        if len(time_series) < 2:
            return {
                'velocity': 0.0,
                'direction': 'stable',
                'acceleration': 0.0,
                'trend': 'insufficient_data'
            }
        
        # Calculate month-over-month changes
        changes = [time_series[i] - time_series[i-1] for i in range(1, len(time_series))]
        
        avg_change = np.mean(changes)
        
        # Direction
        if avg_change > 0.01:
            direction = 'increasing'
            icon = '↗️'
        elif avg_change < -0.01:
            direction = 'decreasing'
            icon = '↘️'
        else:
            direction = 'stable'
            icon = '→'
        
        # Acceleration (change in velocity)
        if len(changes) >= 2:
            recent_velocity = np.mean(changes[-2:])
            earlier_velocity = np.mean(changes[:-2])
            acceleration = recent_velocity - earlier_velocity
        else:
            acceleration = 0.0
        
        # Trend strength using Mann-Kendall test
        if len(time_series) >= 3:
            tau, p_value = stats.kendalltau(range(len(time_series)), time_series)
            is_trending = p_value < 0.05
            trend_strength = abs(tau)
        else:
            is_trending = False
            trend_strength = 0.0
        
        return {
            'velocity': avg_change,
            'velocity_pct': avg_change * 100,
            'direction': direction,
            'icon': icon,
            'acceleration': acceleration,
            'is_accelerating': abs(acceleration) > 0.005,
            'is_trending': is_trending,
            'trend_strength': trend_strength
        }
    
    @staticmethod
    def format_change_indicator(current: float, 
                               previous: float,
                               format_as_pct: bool = True) -> Dict[str, str]:
        """
        Format a change indicator for display
        
        Returns:
            Formatted change with icon, color, and text
        """
        change = current - previous
        change_pct = (change / previous * 100) if previous != 0 else 0
        
        if abs(change) < 0.001:
            return {
                'icon': '→',
                'color': '#757575',
                'text': 'No change',
                'value': '0.0%' if format_as_pct else '0.0'
            }
        
        if change > 0:
            icon = '↗️'
            color = '#4caf50'
            sign = '+'
        else:
            icon = '↘️'
            color = '#f44336'
            sign = ''
        
        if format_as_pct:
            value_text = f"{sign}{change_pct:.1f}%"
        else:
            value_text = f"{sign}{change:.1%}"
        
        return {
            'icon': icon,
            'color': color,
            'text': f"{icon} {value_text}",
            'value': value_text
        }