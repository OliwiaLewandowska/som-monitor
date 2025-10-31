"""
ROI Calculator - Convert SOM metrics to business impact
"""
from typing import Dict, Optional
from dataclasses import dataclass


@dataclass
class MarketData:
    """Market and business context"""
    total_market_size: float  # Annual market size in EUR
    your_market_share: float  # Current market share (0-1)
    avg_customer_value: float  # Annual revenue per customer
    acquisition_cost: float  # Cost to acquire one customer
    ai_search_share: float = 0.35  # % of searches going to AI (default 35%)
    conversion_rate: float = 0.15  # % of AI searchers who convert (default 15%)


class ROICalculator:
    """Calculate business impact of SOM metrics"""
    
    def __init__(self, market_data: MarketData):
        self.market = market_data
    
    def calculate_revenue_impact(self, 
                                 current_som: float,
                                 target_som: float,
                                 time_horizon_years: int = 1) -> Dict:
        """
        Calculate revenue impact of improving SOM
        
        Args:
            current_som: Current share of model (0-1)
            target_som: Target share of model (0-1)
            time_horizon_years: Years to achieve target
            
        Returns:
            Dictionary with revenue projections
        """
        # Calculate addressable market via AI
        ai_influenced_market = (
            self.market.total_market_size * 
            self.market.ai_search_share
        )
        
        # Current revenue from AI-influenced searches
        current_ai_revenue = (
            ai_influenced_market * 
            current_som * 
            self.market.conversion_rate
        )
        
        # Projected revenue with improved SOM
        projected_ai_revenue = (
            ai_influenced_market * 
            target_som * 
            self.market.conversion_rate
        )
        
        # Revenue lift
        annual_revenue_lift = projected_ai_revenue - current_ai_revenue
        total_revenue_lift = annual_revenue_lift * time_horizon_years
        
        # Customer acquisition equivalent
        new_customers = annual_revenue_lift / self.market.avg_customer_value
        
        # CAC savings (organic vs paid)
        cac_savings = new_customers * self.market.acquisition_cost
        
        return {
            'ai_influenced_market': ai_influenced_market,
            'current_ai_revenue': current_ai_revenue,
            'projected_ai_revenue': projected_ai_revenue,
            'annual_revenue_lift': annual_revenue_lift,
            'total_revenue_lift': total_revenue_lift,
            'som_improvement': target_som - current_som,
            'new_customers_equivalent': new_customers,
            'cac_savings': cac_savings,
            'roi_multiplier': total_revenue_lift / self.market.acquisition_cost if self.market.acquisition_cost > 0 else 0
        }
    
    def calculate_competitive_threat(self,
                                    your_som: float,
                                    competitor_som: float,
                                    competitor_growth_rate: float) -> Dict:
        """
        Calculate revenue at risk if competitor maintains growth
        
        Args:
            your_som: Your current SOM (0-1)
            competitor_som: Competitor current SOM (0-1)
            competitor_growth_rate: Monthly growth rate (0-1)
            
        Returns:
            Revenue at risk analysis
        """
        # Project competitor SOM in 6 months if trend continues
        months = 6
        projected_competitor_som = competitor_som * ((1 + competitor_growth_rate) ** months)
        projected_competitor_som = min(projected_competitor_som, 1.0)  # Cap at 100%
        
        # Assume competitor gains come from market leader (you)
        potential_som_loss = projected_competitor_som - competitor_som
        
        # Revenue impact
        ai_market = self.market.total_market_size * self.market.ai_search_share
        revenue_at_risk = (
            ai_market * 
            potential_som_loss * 
            self.market.conversion_rate
        )
        
        return {
            'competitor_current_som': competitor_som,
            'competitor_projected_som': projected_competitor_som,
            'your_potential_som_loss': potential_som_loss,
            'revenue_at_risk_6m': revenue_at_risk,
            'revenue_at_risk_annual': revenue_at_risk * 2,
            'customers_at_risk': revenue_at_risk / self.market.avg_customer_value,
            'market_share_points_at_risk': (potential_som_loss / your_som) * 100 if your_som > 0 else 0
        }
    
    def calculate_campaign_roi(self,
                               campaign_cost: float,
                               som_before: float,
                               som_after: float) -> Dict:
        """
        Calculate ROI of a marketing campaign based on SOM improvement
        
        Args:
            campaign_cost: Total campaign spend
            som_before: SOM before campaign (0-1)
            som_after: SOM after campaign (0-1)
            
        Returns:
            Campaign ROI analysis
        """
        impact = self.calculate_revenue_impact(som_before, som_after, time_horizon_years=1)
        
        roi_percentage = ((impact['annual_revenue_lift'] - campaign_cost) / campaign_cost * 100) if campaign_cost > 0 else 0
        
        payback_months = (campaign_cost / impact['annual_revenue_lift'] * 12) if impact['annual_revenue_lift'] > 0 else float('inf')
        
        return {
            'campaign_cost': campaign_cost,
            'som_improvement': som_after - som_before,
            'annual_revenue_lift': impact['annual_revenue_lift'],
            'net_profit': impact['annual_revenue_lift'] - campaign_cost,
            'roi_percentage': roi_percentage,
            'payback_months': payback_months,
            'new_customers': impact['new_customers_equivalent'],
            'effective_cac': campaign_cost / impact['new_customers_equivalent'] if impact['new_customers_equivalent'] > 0 else 0
        }
    
    def calculate_tool_roi(self,
                          annual_tool_cost: float,
                          som_improvements: Dict[str, float]) -> Dict:
        """
        Calculate ROI of the SOM monitoring tool itself
        
        Args:
            annual_tool_cost: Cost of tool + personnel
            som_improvements: Dict of {period: som_improvement_percentage}
            
        Returns:
            Tool ROI analysis
        """
        total_revenue_impact = 0
        
        for period, improvement in som_improvements.items():
            impact = self.calculate_revenue_impact(0, improvement, time_horizon_years=1)
            total_revenue_impact += impact['annual_revenue_lift']
        
        roi_percentage = ((total_revenue_impact - annual_tool_cost) / annual_tool_cost * 100) if annual_tool_cost > 0 else 0
        
        return {
            'annual_tool_cost': annual_tool_cost,
            'total_revenue_impact': total_revenue_impact,
            'net_benefit': total_revenue_impact - annual_tool_cost,
            'roi_percentage': roi_percentage,
            'payback_months': (annual_tool_cost / total_revenue_impact * 12) if total_revenue_impact > 0 else float('inf'),
            'roi_multiplier': total_revenue_impact / annual_tool_cost if annual_tool_cost > 0 else 0
        }
    
    def segment_value_analysis(self,
                              segment_metrics: Dict[str, Dict]) -> Dict:
        """
        Analyze value of different customer segments
        
        Args:
            segment_metrics: {
                'student': {'som': 0.45, 'market_size': 1000000000, 'avg_value': 120},
                'business': {'som': 0.65, 'market_size': 2000000000, 'avg_value': 600},
                ...
            }
            
        Returns:
            Segment value ranking
        """
        results = {}
        
        for segment, data in segment_metrics.items():
            ai_market = data['market_size'] * self.market.ai_search_share
            current_revenue = ai_market * data['som'] * self.market.conversion_rate
            
            # Potential if we reach 80% SOM in this segment
            potential_revenue = ai_market * 0.80 * self.market.conversion_rate
            upside = potential_revenue - current_revenue
            
            results[segment] = {
                'current_som': data['som'],
                'current_revenue': current_revenue,
                'potential_revenue': potential_revenue,
                'upside': upside,
                'priority_score': upside / data['avg_value']  # Customers we could gain
            }
        
        # Rank by upside
        ranked = sorted(results.items(), key=lambda x: x[1]['upside'], reverse=True)
        
        return {
            'segments': results,
            'ranked_opportunities': [(k, v['upside']) for k, v in ranked],
            'top_priority': ranked[0][0] if ranked else None
        }
    
    def print_business_case(self,
                           current_som: float,
                           target_som: float,
                           campaign_cost: float):
        """Print executive-friendly business case"""
        
        impact = self.calculate_revenue_impact(current_som, target_som)
        campaign = self.calculate_campaign_roi(campaign_cost, current_som, target_som)
        
        print("\n" + "="*70)
        print("BUSINESS CASE: IMPROVING AI VISIBILITY")
        print("="*70)
        
        print(f"\nCURRENT STATE:")
        print(f"  Your Share of Model: {current_som:.1%}")
        print(f"  AI-Influenced Market: €{impact['ai_influenced_market']/1_000_000:.1f}M")
        print(f"  Current AI-Driven Revenue: €{impact['current_ai_revenue']/1_000_000:.1f}M")
        
        print(f"\nTARGET STATE:")
        print(f"  Target Share of Model: {target_som:.1%}")
        print(f"  Projected AI-Driven Revenue: €{impact['projected_ai_revenue']/1_000_000:.1f}M")
        
        print(f"\nREVENUE IMPACT:")
        print(f"  Annual Revenue Lift: €{impact['annual_revenue_lift']/1_000_000:.1f}M")
        print(f"  Equivalent New Customers: {impact['new_customers_equivalent']:,.0f}")
        print(f"  CAC Savings (vs. paid): €{impact['cac_savings']/1_000_000:.1f}M")
        
        print(f"\nCAMPAIGN ROI:")
        print(f"  Investment Required: €{campaign_cost/1_000_000:.1f}M")
        print(f"  Expected Return: €{campaign['annual_revenue_lift']/1_000_000:.1f}M")
        print(f"  Net Profit: €{campaign['net_profit']/1_000_000:.1f}M")
        print(f"  ROI: {campaign['roi_percentage']:.0f}%")
        print(f"  Payback Period: {campaign['payback_months']:.1f} months")
        
        print(f"\nBOTTOM LINE:")
        print(f"  Every 1% increase in SOM = €{(impact['annual_revenue_lift']/((target_som-current_som)*100))/1_000_000:.2f}M annual revenue")
        print("="*70 + "\n")


# Example usage for German Telekom market
if __name__ == "__main__":
    # Example: Mid-size German telekom operator
    market = MarketData(
        total_market_size=10_000_000_000,  # €10B annual market
        your_market_share=0.15,  # 15% market share
        avg_customer_value=300,  # €300 per year per customer
        acquisition_cost=150,  # €150 CAC
        ai_search_share=0.35,  # 35% of searches via AI
        conversion_rate=0.15  # 15% of AI searchers convert
    )
    
    calc = ROICalculator(market)
    
    # Scenario 1: Improve SOM from 45% to 65%
    print("SCENARIO 1: Improve overall visibility")
    calc.print_business_case(
        current_som=0.45,
        target_som=0.65,
        campaign_cost=500_000  # €500K campaign
    )
    
    # Scenario 2: Competitive threat
    print("\nSCENARIO 2: Competitor gaining ground")
    threat = calc.calculate_competitive_threat(
        your_som=0.55,
        competitor_som=0.45,
        competitor_growth_rate=0.05  # Growing 5% per month
    )
    print(f"If competitor maintains 5% monthly growth:")
    print(f"  Revenue at Risk (6 months): €{threat['revenue_at_risk_6m']/1_000_000:.1f}M")
    print(f"  Customers at Risk: {threat['customers_at_risk']:,.0f}")
    print(f"  Market Share Points at Risk: {threat['market_share_points_at_risk']:.1f}%")