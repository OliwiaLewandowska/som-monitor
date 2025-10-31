"""
Statistical analysis utilities for SOM Monitor
"""
import numpy as np
from scipy import stats
from typing import List, Tuple, Dict, Optional
import pandas as pd
from models import QueryResult


class StatisticalAnalyzer:
    """Performs statistical analysis on SOM data"""
    
    def __init__(self, confidence_level: float = 0.95):
        self.confidence_level = confidence_level
    
    def calculate_confidence_interval(self, 
                                     data: List[float]) -> Tuple[float, float, float]:
        """
        Calculate confidence interval for data
        
        Returns:
            mean, lower_bound, upper_bound
        """
        if not data:
            return 0.0, 0.0, 0.0
        
        mean = np.mean(data)
        if len(data) == 1:
            return mean, mean, mean
        
        se = stats.sem(data)
        ci = stats.t.interval(
            self.confidence_level,
            len(data) - 1,
            mean,
            se
        )
        
        return mean, ci[0], ci[1]
    
    def test_significance(self, 
                         sample1: List[float],
                         sample2: List[float]) -> Tuple[float, float, bool]:
        """
        Test if two samples are significantly different
        
        Returns:
            t_statistic, p_value, is_significant
        """
        if not sample1 or not sample2:
            return 0.0, 1.0, False
        
        t_stat, p_value = stats.ttest_ind(sample1, sample2)
        is_significant = p_value < (1 - self.confidence_level)
        
        return t_stat, p_value, is_significant
    
    def detect_trend(self, time_series: List[float]) -> Dict[str, any]:
        """
        Detect trend in time series data using Mann-Kendall test
        
        Returns:
            Dictionary with trend information
        """
        if len(time_series) < 3:
            return {
                'trend': 'insufficient_data',
                'tau': None,
                'p_value': None,
                'significant': False
            }
        
        time_points = range(len(time_series))
        tau, p_value = stats.kendalltau(time_points, time_series)
        
        is_significant = p_value < (1 - self.confidence_level)
        
        if is_significant:
            if tau > 0:
                trend = 'increasing'
            else:
                trend = 'decreasing'
        else:
            trend = 'stable'
        
        return {
            'trend': trend,
            'tau': tau,
            'p_value': p_value,
            'significant': is_significant
        }
    
    def calculate_effect_size(self,
                            sample1: List[float],
                            sample2: List[float]) -> float:
        """
        Calculate Cohen's d effect size
        
        Returns:
            effect_size (small: 0.2, medium: 0.5, large: 0.8)
        """
        if not sample1 or not sample2:
            return 0.0
        
        mean1 = np.mean(sample1)
        mean2 = np.mean(sample2)
        std1 = np.std(sample1, ddof=1)
        std2 = np.std(sample2, ddof=1)
        
        n1, n2 = len(sample1), len(sample2)
        pooled_std = np.sqrt(((n1 - 1) * std1**2 + (n2 - 1) * std2**2) / (n1 + n2 - 2))
        
        if pooled_std == 0:
            return 0.0
        
        return (mean1 - mean2) / pooled_std
    
    def bootstrap_confidence_interval(self,
                                     data: List[float],
                                     n_iterations: int = 1000) -> Tuple[float, float]:
        """
        Calculate confidence interval using bootstrap
        
        Returns:
            lower_bound, upper_bound
        """
        if not data:
            return 0.0, 0.0
        
        bootstrap_means = []
        for _ in range(n_iterations):
            sample = np.random.choice(data, size=len(data), replace=True)
            bootstrap_means.append(np.mean(sample))
        
        alpha = 1 - self.confidence_level
        lower = np.percentile(bootstrap_means, alpha/2 * 100)
        upper = np.percentile(bootstrap_means, (1 - alpha/2) * 100)
        
        return lower, upper
    
    def compare_brands(self,
                      results: List[QueryResult],
                      brand1: str,
                      brand2: str) -> Dict[str, any]:
        """
        Compare two brands statistically
        
        Returns:
            Dictionary with comparison results
        """
        # Extract mention rates
        brand1_mentions = [1 if r.mentions[brand1].mentioned else 0 for r in results]
        brand2_mentions = [1 if r.mentions[brand2].mentioned else 0 for r in results]
        
        # Calculate rates
        rate1 = np.mean(brand1_mentions)
        rate2 = np.mean(brand2_mentions)
        
        # Test significance
        t_stat, p_value, is_significant = self.test_significance(
            brand1_mentions,
            brand2_mentions
        )
        
        # Effect size
        effect_size = self.calculate_effect_size(
            brand1_mentions,
            brand2_mentions
        )
        
        # Confidence intervals
        ci1_lower, ci1_upper = self.bootstrap_confidence_interval(brand1_mentions)
        ci2_lower, ci2_upper = self.bootstrap_confidence_interval(brand2_mentions)
        
        return {
            'brand1': brand1,
            'brand2': brand2,
            'rate1': rate1,
            'rate2': rate2,
            'difference': rate1 - rate2,
            'ci1': (ci1_lower, ci1_upper),
            'ci2': (ci2_lower, ci2_upper),
            'p_value': p_value,
            'significant': is_significant,
            'effect_size': effect_size,
            'interpretation': self._interpret_comparison(rate1, rate2, is_significant, effect_size)
        }
    
    def _interpret_comparison(self,
                            rate1: float,
                            rate2: float,
                            is_significant: bool,
                            effect_size: float) -> str:
        """Generate human-readable interpretation"""
        diff = rate1 - rate2
        
        if not is_significant:
            return "No significant difference detected"
        
        direction = "higher" if diff > 0 else "lower"
        
        if abs(effect_size) < 0.2:
            magnitude = "negligible"
        elif abs(effect_size) < 0.5:
            magnitude = "small"
        elif abs(effect_size) < 0.8:
            magnitude = "medium"
        else:
            magnitude = "large"
        
        return f"Significantly {direction} with {magnitude} effect size"
    
    def analyze_variance(self,
                        results: List[QueryResult],
                        brands: List[str]) -> Dict[str, any]:
        """
        Perform ANOVA to test if there are significant differences among brands
        
        Returns:
            Dictionary with ANOVA results
        """
        # Prepare data for each brand
        brand_data = []
        for brand in brands:
            mentions = [1 if r.mentions[brand].mentioned else 0 for r in results]
            brand_data.append(mentions)
        
        # Perform one-way ANOVA
        f_stat, p_value = stats.f_oneway(*brand_data)
        
        is_significant = p_value < (1 - self.confidence_level)
        
        return {
            'f_statistic': f_stat,
            'p_value': p_value,
            'significant': is_significant,
            'interpretation': "Significant differences detected among brands" if is_significant else "No significant differences among brands"
        }
    
    def power_analysis(self,
                      effect_size: float,
                      sample_size: int,
                      alpha: float = 0.05) -> float:
        """
        Calculate statistical power
        
        Returns:
            power (0-1)
        """
        from scipy.stats import norm
        
        # Simplified power calculation for two-sample t-test
        ncp = effect_size * np.sqrt(sample_size / 2)
        critical_value = norm.ppf(1 - alpha/2)
        power = 1 - norm.cdf(critical_value - ncp) + norm.cdf(-critical_value - ncp)
        
        return power
    
    def required_sample_size(self,
                            effect_size: float,
                            power: float = 0.8,
                            alpha: float = 0.05) -> int:
        """
        Calculate required sample size for desired power
        
        Returns:
            Required sample size per group
        """
        from scipy.stats import norm
        
        z_alpha = norm.ppf(1 - alpha/2)
        z_beta = norm.ppf(power)
        
        n = 2 * ((z_alpha + z_beta) / effect_size) ** 2
        
        return int(np.ceil(n))
