"""
SOM Intelligence Platform - Premium Edition
Enterprise-grade competitive intelligence with statistical rigor

Sprints Implemented:
- Sprint 1: Statistical Confidence & Data Quality
- Sprint 2: Response Explorer
- Sprint 3: Historical Trends & Velocity
- Sprint 4: Theme Analysis & Narrative Insights
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
from pathlib import Path

import sys
sys.path.append('/mnt/project')

from monitor import SOMMonitor
from storage import StorageManager
from config import BRANDS_TO_TRACK, CHART_COLORS, ROI_MARKET_DATA, CAMPAIGN_BUDGETS
from roi_calculator import ROICalculator, MarketData
from confidence_intervals import ConfidenceCalculator, TrendAnalyzer
from theme_analyzer import ThemeAnalyzer

# Page config
st.set_page_config(
    page_title="SOM Intelligence Platform • Premium",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium CSS
st.markdown("""
<style>
    /* Premium Typography */
    .big-insight {
        font-size: 52px;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        padding: 24px;
        letter-spacing: -1px;
    }
    
    .insight-label {
        font-size: 15px;
        color: #666;
        text-align: center;
        margin-top: -18px;
        font-weight: 500;
    }
    
    .mckinsey-title {
        font-size: 34px;
        font-weight: 700;
        color: #000;
        margin-bottom: 12px;
        border-left: 6px solid #1f77b4;
        padding-left: 18px;
        line-height: 1.2;
    }
    
    .subtitle {
        font-size: 17px;
        color: #555;
        margin-bottom: 32px;
        padding-left: 24px;
        font-weight: 400;
    }
    
    /* Alert Boxes */
    .alert-box {
        padding: 18px;
        border-radius: 6px;
        margin: 12px 0;
        font-size: 15px;
    }
    .alert-critical {
        background-color: #ffebee;
        border-left: 6px solid #f44336;
    }
    .alert-warning {
        background-color: #fff3e0;
        border-left: 6px solid #ff9800;
    }
    .alert-success {
        background-color: #e8f5e9;
        border-left: 6px solid #4caf50;
    }
    .alert-info {
        background-color: #e3f2fd;
        border-left: 6px solid #2196f3;
    }
    
    /* Data Quality Indicators */
    .data-quality-badge {
        display: inline-block;
        padding: 5px 14px;
        border-radius: 14px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.5px;
        margin-left: 10px;
        text-transform: uppercase;
    }
    
    .confidence-note {
        font-size: 12px;
        color: #666;
        font-style: italic;
        margin-top: 6px;
        padding-left: 4px;
    }
    
    .trend-indicator {
        font-size: 22px;
        font-weight: bold;
        margin: 0 10px;
    }
    
    /* Narrative Cards */
    .narrative-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        padding: 18px;
        border-radius: 8px;
        margin: 12px 0;
        border-left: 5px solid #1f77b4;
        box-shadow: 0 2px 4px rgba(0,0,0,0.06);
    }
    
    .narrative-card h4 {
        margin-top: 0;
        color: #1f77b4;
        font-size: 16px;
    }
    
    /* Response Quotes */
    .response-quote {
        background: #ffffff;
        border-left: 4px solid #1f77b4;
        padding: 14px 16px;
        margin: 10px 0;
        font-style: italic;
        color: #333;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
        border-radius: 4px;
        line-height: 1.6;
    }
    
    .response-meta {
        font-size: 11px;
        color: #888;
        margin-top: 8px;
        font-style: normal;
    }
    
    /* Premium Metrics */
    .metric-card {
        background: white;
        padding: 16px;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        text-align: center;
    }
    
    .metric-value {
        font-size: 32px;
        font-weight: 700;
        color: #1f77b4;
    }
    
    .metric-label {
        font-size: 13px;
        color: #666;
        margin-top: 4px;
    }
    
    /* Historical Event Tags */
    .event-tag {
        display: inline-block;
        background: #fff3cd;
        border: 1px solid #ffc107;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 11px;
        margin: 4px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize premium tools
storage = StorageManager()
monitor = SOMMonitor()
confidence_calc = ConfidenceCalculator(confidence_level=0.95)
trend_analyzer = TrendAnalyzer()

# Load historical data for trend analysis
def load_historical_data():
    """Load all historical data files for trend analysis"""
    data_dir = Path("data")
    historical_files = sorted(data_dir.glob("som_results_*_historical.json"))
    
    historical_data = []
    for file in historical_files:
        results = storage.load_results(file.name)
        if results:
            historical_data.append({
                'date': file.stem.split('_')[2],
                'results': results
            })
    
    return historical_data

# Sidebar - Premium Edition
st.sidebar.image("https://via.placeholder.com/150x50/1f77b4/ffffff?text=SOM+Intel", 
                 use_container_width=True)
st.sidebar.markdown("### 🎯 Intelligence Platform")
st.sidebar.markdown("**Premium Edition** • Statistical Rigor • AI Insights")
st.sidebar.markdown("---")

# File selector with historical data
files = storage.get_results_files()
if files:
    # Separate historical and current files
    historical_files = [f for f in files if 'historical' in f]
    current_files = [f for f in files if 'historical' not in f]
    
    st.sidebar.markdown("#### 📅 Analysis Period")
    
    # Option to view historical trends
    view_mode = st.sidebar.radio(
        "View Mode",
        ["Current Snapshot", "Historical Trends"],
        help="Switch between current data and historical trend analysis"
    )
    
    if view_mode == "Current Snapshot":
        selected_file = st.sidebar.selectbox(
            "Select Dataset",
            current_files if current_files else files,
            index=0
        )
        show_trends = False
    else:
        st.sidebar.info("Analyzing last 6 months of data")
        selected_file = files[0]  # Most recent
        show_trends = True
    
    # Load results
    results = storage.load_results(selected_file)
    
    if results:
        # Initialize theme analyzer
        theme_analyzer = ThemeAnalyzer(BRANDS_TO_TRACK)
        
        # Extract metadata
        provider = results[0].provider
        model = results[0].model
        total_queries = len(results)
        timestamp = results[0].timestamp.split('T')[0]
        
        # Calculate data quality
        data_quality = confidence_calc.evaluate_data_quality(total_queries)
        
        # Sidebar - Data Quality Card
        st.sidebar.markdown("---")
        st.sidebar.markdown("**📊 Data Quality Assessment**")
        
        quality_color_map = {
            'EXCELLENT': '#2196f3',
            'GOOD': '#4caf50',
            'MODERATE': '#ff9800',
            'LOW': '#f44336'
        }
        
        st.sidebar.markdown(
            f"<div style='background: {quality_color_map[data_quality['quality']]}; "
            f"color: white; padding: 12px; border-radius: 6px; text-align: center; "
            f"font-weight: bold; margin: 8px 0;'>"
            f"{data_quality['icon']} {data_quality['quality']}</div>",
            unsafe_allow_html=True
        )
        
        st.sidebar.metric("Sample Size", f"{total_queries:,} queries")
        st.sidebar.metric("Date", timestamp)
        st.sidebar.metric("Model", model)
        
        if data_quality['quality'] in ['LOW', 'MODERATE']:
            st.sidebar.warning(f"⚠️ {data_quality['recommendation']}")
        
        # Calculate metrics
        report = monitor.generate_report(results)
        metrics_dict = report.metrics
        
        # Brand configuration
        st.sidebar.markdown("---")
        st.sidebar.markdown("**🎯 Analysis Configuration**")
        
        your_brand = st.sidebar.selectbox(
            "Your Brand",
            options=BRANDS_TO_TRACK,
            index=0,
            help="Select your brand for ROI calculations"
        )
        
        # Market assumptions
        market_config = ROI_MARKET_DATA.get(your_brand, ROI_MARKET_DATA['default'])
        
        with st.sidebar.expander("⚙️ Market Assumptions"):
            market_size = st.number_input(
                "Total Market Size (€)",
                value=market_config['total_market_size'],
                format="%d"
            )
            market_share = st.slider(
                "Your Market Share (%)",
                1, 50,
                int(market_config['your_market_share'] * 100)
            ) / 100
            arpu = st.number_input(
                "ARPU (€/year)",
                value=market_config['avg_customer_value']
            )
            cac = st.number_input(
                "CAC (€)",
                value=market_config['acquisition_cost']
            )
        
        market_data = MarketData(
            total_market_size=market_size,
            your_market_share=market_share,
            avg_customer_value=arpu,
            acquisition_cost=cac,
            ai_search_share=market_config['ai_search_share'],
            conversion_rate=market_config['conversion_rate']
        )
        
        roi_calc = ROICalculator(market_data)
        
        # Competitor selection
        selected_brands = st.sidebar.multiselect(
            "Comparison Brands",
            options=[b for b in BRANDS_TO_TRACK if b != your_brand],
            default=[b for b in BRANDS_TO_TRACK if b != your_brand][:5]
        )
        
        all_comparison_brands = [your_brand] + selected_brands
        
        # Quick ROI summary
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"**💰 {your_brand} Quick Metrics**")
        
        if your_brand in metrics_dict:
            your_current_som = metrics_dict[your_brand].mention_rate
            
            # Calculate confidence interval
            your_mentions = metrics_dict[your_brand].total_mentions
            confidence_metrics = confidence_calc.calculate_proportion_confidence(
                your_mentions, total_queries
            )
            
            st.sidebar.metric(
                "Your SOM",
                f"{your_current_som:.0%}",
                f"±{confidence_metrics.margin_of_error*100:.1f}%"
            )
            
            current_ai_revenue = (
                market_data.total_market_size * 
                market_data.ai_search_share * 
                your_current_som * 
                market_data.conversion_rate
            )
            
            st.sidebar.metric(
                "AI-Driven Revenue",
                f"€{current_ai_revenue/1_000_000:.1f}M/year"
            )
        
        # ====================
        # MAIN DASHBOARD
        # ====================
        
        # Filter metrics
        filtered_metrics = {
            k: v for k, v in metrics_dict.items() 
            if k in all_comparison_brands
        }
        
        # Header with data quality badge
        st.markdown(
            f'<p class="mckinsey-title">🎯 {your_brand}: AI Search Competitive Intelligence'
            f'<span class="data-quality-badge" style="background: {quality_color_map[data_quality["quality"]]}; '
            f'color: white;">{data_quality["icon"]} {data_quality["quality"]}</span></p>',
            unsafe_allow_html=True
        )
        
        per_percent_value = (market_data.total_market_size * market_data.ai_search_share * 0.01 * market_data.conversion_rate)/1_000_000
        
        st.markdown(
            f'<p class="subtitle">'
            f'{int(market_data.ai_search_share*100)}% of mobile research via AI • '
            f'1% SOM = €{per_percent_value:.1f}M revenue • '
            f'Based on {total_queries:,} queries'
            f'</p>',
            unsafe_allow_html=True
        )
        
        # Key insights with confidence intervals
        your_som = metrics_dict.get(your_brand).mention_rate if your_brand in metrics_dict else 0
        your_mentions = metrics_dict.get(your_brand).total_mentions if your_brand in metrics_dict else 0
        
        your_confidence = confidence_calc.calculate_proportion_confidence(your_mentions, total_queries)
        
        leader_brand = max(filtered_metrics.items(), key=lambda x: x[1].mention_rate)
        leader_som = leader_brand[1].mention_rate
        leader_mentions = leader_brand[1].total_mentions
        leader_confidence = confidence_calc.calculate_proportion_confidence(leader_mentions, total_queries)
        
        som_gap = leader_som - your_som
        
        target_revenue = roi_calc.calculate_revenue_impact(your_som, leader_som, 1)
        revenue_at_risk = target_revenue['annual_revenue_lift']
        customers_at_risk = int(target_revenue['new_customers_equivalent'])
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f'<div class="big-insight">{som_gap:.0%}</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="insight-label">Gap to Market Leader<br>'
                f'<small>{leader_brand[0]} ({leader_som:.0%} ±{leader_confidence.margin_of_error*100:.1f}%) '
                f'vs. You ({your_som:.0%} ±{your_confidence.margin_of_error*100:.1f}%)</small></div>',
                unsafe_allow_html=True
            )
            st.markdown(
                f'<div class="confidence-note">95% confidence intervals shown</div>',
                unsafe_allow_html=True
            )
        
        with col2:
            st.markdown(f'<div class="big-insight">€{revenue_at_risk/1_000_000:.1f}M</div>', unsafe_allow_html=True)
            st.markdown('<div class="insight-label">Annual Revenue Opportunity<br><small>If you close the gap</small></div>', 
                       unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'<div class="big-insight">{customers_at_risk/1000:.0f}K</div>', unsafe_allow_html=True)
            st.markdown('<div class="insight-label">Potential New Customers<br><small>Per year</small></div>', 
                       unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Tabs with new features
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📈 Trends & Velocity",
            "🎭 Narrative Analysis", 
            "🔍 Response Explorer",
            "💰 Revenue Impact",
            "⚔️ Competitive Position",
            "🎯 Strategic Actions"
        ])
        
        # ====================
        # TAB 1: TRENDS & VELOCITY (SPRINT 3)
        # ====================
        with tab1:
            st.markdown('<p class="mckinsey-title">📈 Share of Model: Trends & Competitive Velocity</p>', 
                       unsafe_allow_html=True)
            st.markdown('<p class="subtitle">Historical performance and momentum analysis</p>',
                       unsafe_allow_html=True)
            
            if show_trends or len(historical_files) > 0:
                # Load historical data
                historical_data = load_historical_data()
                
                if historical_data:
                    # Build time series for each brand
                    time_series_data = []
                    
                    for hist_entry in historical_data:
                        date_str = hist_entry['date']
                        hist_results = hist_entry['results']
                        
                        hist_report = monitor.generate_report(hist_results)
                        
                        for brand in all_comparison_brands:
                            if brand in hist_report.metrics:
                                time_series_data.append({
                                    'Date': date_str,
                                    'Brand': brand,
                                    'SOM': hist_report.metrics[brand].mention_rate * 100,
                                    'Sample Size': len(hist_results)
                                })
                    
                    # Add current data
                    for brand in all_comparison_brands:
                        if brand in metrics_dict:
                            time_series_data.append({
                                'Date': timestamp.split('T')[0].replace('-', ''),  # Extract YYYYMMDD
                                'Brand': brand,
                                'SOM': metrics_dict[brand].mention_rate * 100,
                                'Sample Size': total_queries
                            })
                    
                    df_time = pd.DataFrame(time_series_data)
                    df_time['Date'] = pd.to_datetime(df_time['Date'], format='%Y%m%d')
                    df_time = df_time.sort_values('Date')
                    
                    # Trend line chart - PREMIUM EDITION
                    fig_trends = go.Figure()
                    
                    for brand in all_comparison_brands:
                        brand_data = df_time[df_time['Brand'] == brand].copy()
                        
                        # Calculate velocity
                        som_values = brand_data['SOM'].tolist()
                        velocity_metrics = trend_analyzer.calculate_velocity(
                            [v/100 for v in som_values]
                        )
                        
                        # Calculate confidence intervals for each point
                        brand_data['CI_lower'] = brand_data['SOM'] * 0.95  # Simplified CI
                        brand_data['CI_upper'] = brand_data['SOM'] * 1.05
                        
                        # Visual hierarchy: Your brand gets premium treatment
                        is_your_brand = (brand == your_brand)
                        line_width = 4 if is_your_brand else 2
                        opacity = 1.0 if is_your_brand else 0.7
                        
                        # Add confidence interval band
                        if is_your_brand:
                            fig_trends.add_trace(go.Scatter(
                                x=brand_data['Date'].tolist() + brand_data['Date'].tolist()[::-1],
                                y=brand_data['CI_upper'].tolist() + brand_data['CI_lower'].tolist()[::-1],
                                fill='toself',
                                fillcolor='rgba(31, 119, 180, 0.15)',
                                line=dict(color='rgba(255,255,255,0)'),
                                showlegend=False,
                                hoverinfo='skip',
                                name=f'{brand} CI'
                            ))
                        
                        # Main trend line
                        fig_trends.add_trace(go.Scatter(
                            x=brand_data['Date'],
                            y=brand_data['SOM'],
                            name=f"{brand} {velocity_metrics['icon']}",
                            mode='lines+markers',
                            line=dict(
                                width=line_width,
                                dash='solid' if is_your_brand else 'dot'
                            ),
                            marker=dict(
                                size=10 if is_your_brand else 6,
                                symbol='diamond' if is_your_brand else 'circle'
                            ),
                            opacity=opacity,
                            hovertemplate='<b>%{fullData.name}</b><br>' +
                                        'Date: %{x|%B %Y}<br>' +
                                        'SOM: %{y:.1f}%<br>' +
                                        f'Velocity: {velocity_metrics["velocity_pct"]:.2f}% per month<br>' +
                                        '<extra></extra>'
                        ))
                    
                    fig_trends.update_layout(
                        title={
                            'text': "Share of Model Evolution • 6 Month Trend",
                            'font': {'size': 20, 'family': 'Arial, sans-serif'}
                        },
                        xaxis_title="Timeline",
                        yaxis_title="Share of Model (%)",
                        height=550,
                        hovermode='x unified',
                        plot_bgcolor='rgba(250,250,250,0.3)',
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=-0.25,
                            xanchor="center",
                            x=0.5,
                            font=dict(size=11)
                        ),
                        xaxis=dict(
                            showgrid=True,
                            gridcolor='rgba(200,200,200,0.2)'
                        ),
                        yaxis=dict(
                            showgrid=True,
                            gridcolor='rgba(200,200,200,0.2)',
                            rangemode='tozero'
                        )
                    )
                    
                    st.plotly_chart(fig_trends, use_container_width=True)
                    
                    # Velocity metrics table
                    st.markdown("#### 🏃 Competitive Velocity Metrics")
                    
                    velocity_data = []
                    for brand in all_comparison_brands:
                        brand_data = df_time[df_time['Brand'] == brand]['SOM'].tolist()
                        
                        if len(brand_data) >= 2:
                            velocity = trend_analyzer.calculate_velocity([v/100 for v in brand_data])
                            
                            # Calculate change from first to last
                            change = brand_data[-1] - brand_data[0]
                            
                            velocity_data.append({
                                'Brand': brand,
                                'Current SOM': f"{brand_data[-1]:.1f}%",
                                'Trend': velocity['icon'],
                                'Monthly Velocity': f"{velocity['velocity_pct']:.2f}pp/month",
                                '6M Change': f"{change:+.1f}pp",
                                'Status': 'Accelerating' if velocity['is_accelerating'] else 'Stable'
                            })
                    
                    df_velocity = pd.DataFrame(velocity_data)
                    st.dataframe(df_velocity, use_container_width=True, hide_index=True)
                    
                    # Load and display events
                    events_file = Path("data/events.json")
                    if events_file.exists():
                        with open(events_file, 'r') as f:
                            events = json.load(f)
                        
                        if events:
                            st.markdown("#### 📅 Market Events & Campaigns")
                            
                            for event in events:
                                st.markdown(
                                    f"<div class='event-tag'>"
                                    f"📅 {event['date']} • {event['description']} "
                                    f"({', '.join(event['affected_brands'])})"
                                    f"</div>",
                                    unsafe_allow_html=True
                                )
                
                else:
                    st.info("No historical data available. Run historical_generator.py to create trend data.")
            else:
                st.info("📊 Enable 'Historical Trends' mode in sidebar to view time series analysis")
        
        # ====================
        # TAB 2: NARRATIVE ANALYSIS (SPRINT 4)
        # ====================
        with tab2:
            st.markdown('<p class="mckinsey-title">🎭 Narrative Analysis: Who Owns Which Story</p>', 
                       unsafe_allow_html=True)
            st.markdown('<p class="subtitle">Competitive narrative positioning and attribute ownership</p>',
                       unsafe_allow_html=True)
            
            # Extract themes
            with st.spinner("Analyzing themes and narratives..."):
                theme_insights = theme_analyzer.extract_themes(results)
                narratives = theme_analyzer.analyze_narratives(theme_insights)
            
            if narratives:
                # Narrative ownership matrix
                st.markdown("#### 📊 Attribute Ownership Matrix")
                
                matrix = theme_analyzer.create_narrative_matrix(narratives)
                
                # Create heatmap data
                attributes = list(matrix.keys())
                brands_sorted = all_comparison_brands
                
                heatmap_data = []
                for attr in attributes:
                    row = [matrix[attr].get(brand, 0) * 100 for brand in brands_sorted]
                    heatmap_data.append(row)
                
                fig_heatmap = go.Figure(data=go.Heatmap(
                    z=heatmap_data,
                    x=brands_sorted,
                    y=attributes,
                    colorscale='RdYlGn',
                    text=[[f"{val:.0f}%" for val in row] for row in heatmap_data],
                    texttemplate='%{text}',
                    textfont={"size": 11},
                    colorbar=dict(title="Association<br>Rate (%)")
                ))
                
                fig_heatmap.update_layout(
                    title="Attribute Association Heatmap",
                    height=400,
                    xaxis_title="Brand",
                    yaxis_title="Attribute Category"
                )
                
                st.plotly_chart(fig_heatmap, use_container_width=True)
                
                # Strategic insights
                st.markdown("#### 💡 Strategic Narrative Insights")
                
                insights = theme_analyzer.generate_insights_text(narratives, your_brand)
                
                for insight in insights:
                    st.markdown(f"<div class='narrative-card'>{insight}</div>", 
                               unsafe_allow_html=True)
                
                # Detailed narrative breakdown
                st.markdown("#### 📋 Detailed Narrative Breakdown")
                
                for narrative in narratives[:5]:
                    with st.expander(f"**{narrative.attribute}** - Leader: {narrative.leader} ({narrative.leader_score:.0%})"):
                        st.write("**Brand Ownership:**")
                        
                        ownership_data = [
                            {
                                'Brand': brand,
                                'Association Rate': f"{score:.1%}",
                                'Gap to Leader': f"{narrative.gap_analysis[brand]:.1%}"
                            }
                            for brand, score in sorted(
                                narrative.brand_ownership.items(),
                                key=lambda x: x[1],
                                reverse=True
                            )
                        ]
                        
                        st.dataframe(pd.DataFrame(ownership_data), use_container_width=True, hide_index=True)
                        
                        # Example quotes
                        if your_brand in narrative.example_quotes and narrative.example_quotes[your_brand]:
                            st.write(f"**Example mentions for {your_brand}:**")
                            for quote in narrative.example_quotes[your_brand][:2]:
                                st.markdown(
                                    f"<div class='response-quote'>{quote}</div>",
                                    unsafe_allow_html=True
                                )
            else:
                st.info("Not enough data for narrative analysis. Run more queries to extract themes.")
        
        # ====================
        # TAB 3: RESPONSE EXPLORER (SPRINT 2)
        # ====================
        with tab3:
            st.markdown('<p class="mckinsey-title">🔍 Response Explorer: Read What AI Says</p>', 
                       unsafe_allow_html=True)
            st.markdown('<p class="subtitle">Searchable database of actual LLM responses</p>',
                       unsafe_allow_html=True)
            
            # Filters
            col_f1, col_f2, col_f3 = st.columns(3)
            
            with col_f1:
                filter_brand = st.selectbox(
                    "Filter by Brand Mentioned",
                    ["All Brands"] + all_comparison_brands
                )
            
            with col_f2:
                filter_category = st.selectbox(
                    "Filter by Category",
                    ["All Categories"] + list(set(r.category for r in results))
                )
            
            with col_f3:
                search_term = st.text_input(
                    "Search in responses",
                    placeholder="Enter keywords..."
                )
            
            # Filter results
            filtered_responses = results
            
            if filter_brand != "All Brands":
                filtered_responses = [
                    r for r in filtered_responses
                    if r.mentions[filter_brand].mentioned
                ]
            
            if filter_category != "All Categories":
                filtered_responses = [
                    r for r in filtered_responses
                    if r.category == filter_category
                ]
            
            if search_term:
                filtered_responses = [
                    r for r in filtered_responses
                    if search_term.lower() in r.response.lower() or search_term.lower() in r.query.lower()
                ]
            
            st.write(f"**Showing {len(filtered_responses)} of {len(results)} responses**")
            
            # Display responses
            for idx, result in enumerate(filtered_responses[:20]):
                with st.expander(
                    f"**Query {idx+1}:** {result.query[:100]}... "
                    f"• Category: {result.category} • Brands: {', '.join(result.mention_order[:3])}"
                ):
                    st.markdown(f"**🔹 Query:** _{result.query}_")
                    st.markdown(f"**📅 Date:** {result.timestamp.split('T')[0]}")
                    st.markdown(f"**🏷️ Category:** {result.category}")
                    st.markdown(f"**🎯 Brands Mentioned:** {', '.join(result.mention_order)}")
                    st.markdown("---")
                    
                    # Highlight brand mentions in response
                    response_text = result.response
                    for brand in result.mention_order:
                        response_text = response_text.replace(
                            brand,
                            f"**`{brand}`**"
                        )
                    
                    st.markdown(f"**💬 Response:**")
                    st.markdown(f"<div class='response-quote'>{response_text}</div>", 
                               unsafe_allow_html=True)
            
            if len(filtered_responses) > 20:
                st.info(f"Showing first 20 of {len(filtered_responses)} results. Refine filters to see more.")
        
        # ====================
        # TAB 4: REVENUE IMPACT (Original)
        # ====================
        with tab4:
            st.markdown('<p class="mckinsey-title">💰 Revenue Impact Analysis</p>', 
                       unsafe_allow_html=True)
            
            per_percent_value = (market_data.total_market_size * market_data.ai_search_share * 0.01 * market_data.conversion_rate)/1_000_000
            st.markdown(f'<p class="subtitle">Every 1% SOM = €{per_percent_value:.1f}M annual revenue</p>', 
                       unsafe_allow_html=True)
            
            # Revenue scenarios
            sorted_by_mention = sorted(
                filtered_metrics.items(),
                key=lambda x: x[1].mention_rate,
                reverse=True
            )
            
            scenario_data = []
            for brand, metrics in sorted_by_mention[:5]:
                current_impact = roi_calc.calculate_revenue_impact(
                    metrics.mention_rate,
                    metrics.mention_rate,
                    1
                )
                
                potential_impact = roi_calc.calculate_revenue_impact(
                    metrics.mention_rate,
                    0.80,
                    1
                )
                
                scenario_data.append({
                    'Brand': brand,
                    'Current SOM': f"{metrics.mention_rate:.0%}",
                    'Current Revenue': f"€{current_impact['current_ai_revenue']/1_000_000:.1f}M",
                    'Potential (80%)': f"€{potential_impact['projected_ai_revenue']/1_000_000:.1f}M",
                    'Opportunity': f"€{potential_impact['annual_revenue_lift']/1_000_000:.1f}M",
                    'Upside_raw': potential_impact['annual_revenue_lift']
                })
            
            df_scenario = pd.DataFrame(scenario_data)
            
            # Waterfall chart
            brands_list = [d['Brand'] for d in scenario_data]
            upsides = [d['Upside_raw']/1_000_000 for d in scenario_data]
            
            fig = go.Figure(go.Waterfall(
                name="Revenue Opportunity",
                orientation="v",
                measure=["relative"] * len(brands_list),
                x=brands_list,
                y=upsides,
                text=[f"€{v:.1f}M" for v in upsides],
                textposition="outside",
                connector={"line": {"color": "rgb(63, 63, 63)"}},
                increasing={"marker": {"color": "#4caf50"}},
            ))
            
            fig.update_layout(
                title=f"Revenue Opportunity by Brand (to 80% SOM)",
                showlegend=False,
                height=400,
                yaxis_title="Annual Revenue Opportunity (€M)"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(
                df_scenario[['Brand', 'Current SOM', 'Current Revenue', 'Potential (80%)', 'Opportunity']],
                use_container_width=True,
                hide_index=True
            )
        
        # ====================
        # TAB 5: COMPETITIVE POSITION (Original)
        # ====================
        with tab5:
            st.markdown('<p class="mckinsey-title">⚔️ Competitive Battleground</p>', 
                       unsafe_allow_html=True)
            
            comparison_data = []
            for brand, metrics in sorted(filtered_metrics.items(), key=lambda x: x[1].mention_rate, reverse=True):
                # Calculate confidence interval
                conf = confidence_calc.calculate_proportion_confidence(
                    metrics.total_mentions,
                    metrics.total_queries
                )
                
                comparison_data.append({
                    'Brand': brand,
                    'Share of Model': f"{metrics.mention_rate:.1%}",
                    'Confidence Range': f"{conf.lower_bound:.1%} - {conf.upper_bound:.1%}",
                    'First Mention Rate': f"{metrics.first_mention_rate:.1%}",
                    'Total Mentions': metrics.total_mentions,
                    'Your Brand?': '✓' if brand == your_brand else ''
                })
            
            df_comparison = pd.DataFrame(comparison_data)
            
            st.dataframe(df_comparison, use_container_width=True, hide_index=True)
            
            # Bar chart with confidence intervals
            brands_chart = [d['Brand'] for d in comparison_data]
            som_values = [float(d['Share of Model'].strip('%'))/100 for d in comparison_data]
            
            # Get confidence bounds for error bars
            error_y = []
            for d in comparison_data:
                bounds = d['Confidence Range'].split(' - ')
                lower = float(bounds[0].strip('%'))/100
                upper = float(bounds[1].strip('%'))/100
                mid = (lower + upper) / 2
                error = upper - mid
                error_y.append(error)
            
            colors_chart = ['#1f77b4' if d['Your Brand?'] == '✓' else '#95a5a6' for d in comparison_data]
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=brands_chart,
                y=som_values,
                marker_color=colors_chart,
                text=[f"{v:.0%}" for v in som_values],
                textposition='outside',
                error_y=dict(
                    type='data',
                    array=error_y,
                    visible=True,
                    color='#666',
                    thickness=1.5
                )
            ))
            
            fig.update_layout(
                title=f"Share of Model with 95% Confidence Intervals",
                yaxis_title="Share of Model",
                showlegend=False,
                height=450
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown(
                "<div class='confidence-note'>Error bars represent 95% confidence intervals. "
                "Wider bars indicate less certainty due to smaller sample size.</div>",
                unsafe_allow_html=True
            )
        
        # ====================
        # TAB 6: STRATEGIC ACTIONS (Original)
        # ====================
        with tab6:
            st.markdown(f'<p class="mckinsey-title">🎯 Strategic Action Plan for {your_brand}</p>', 
                       unsafe_allow_html=True)
            st.markdown('<p class="subtitle">Prioritized recommendations with ROI projections</p>',
                       unsafe_allow_html=True)
            
            # Generate actions (simplified from original)
            actions = []
            
            # Action 1: Close gap to leader
            if som_gap > 0.10:
                gap_revenue = revenue_at_risk
                gap_budget = 500_000
                
                actions.append({
                    'Priority': 1,
                    'Action': f"Close Gap to {leader_brand[0]}",
                    'Rationale': f"Currently {som_gap:.0%} behind market leader",
                    'Investment': f"€{int(gap_budget/1_000)}K",
                    'Expected Impact': f"€{gap_revenue/1_000_000:.1f}M annual revenue",
                    'Timeline': "60 days",
                    'ROI': f"{gap_revenue/gap_budget:.1f}x",
                    'Investment_raw': gap_budget,
                    'Impact_raw': gap_revenue
                })
            
            # Display actions
            for action in actions:
                priority_color = {1: 'critical', 2: 'warning', 3: 'success'}.get(action['Priority'], 'info')
                
                action_html = f"""
                <div class="alert-box alert-{priority_color}">
                    <h3>Priority {action['Priority']}: {action['Action']}</h3>
                    <p><strong>Why:</strong> {action['Rationale']}</p>
                    <p><strong>Investment:</strong> {action['Investment']} | 
                       <strong>Impact:</strong> {action['Expected Impact']} | 
                       <strong>ROI:</strong> {action['ROI']} | 
                       <strong>Timeline:</strong> {action['Timeline']}</p>
                </div>
                """
                st.markdown(action_html, unsafe_allow_html=True)
            
            if actions:
                st.markdown("---")
                col1, col2, col3 = st.columns(3)
                
                total_investment = sum([a['Investment_raw'] for a in actions])
                total_impact = sum([a['Impact_raw'] for a in actions])
                portfolio_roi = total_impact / total_investment if total_investment > 0 else 0
                
                with col1:
                    st.metric("Total Investment", f"€{total_investment/1_000:.0f}K")
                with col2:
                    st.metric("Total Revenue Impact", f"€{total_impact/1_000_000:.1f}M")
                with col3:
                    st.metric("Portfolio ROI", f"{portfolio_roi:.1f}x")

else:
    st.info("📊 No data available. Run a survey to begin.")
    
    st.markdown("""
    ### Getting Started with SOM Intelligence
    
    1. **Set your API key:**
       ```bash
       export OPENAI_API_KEY='your-key-here'
       ```
    
    2. **Generate historical data (for trends):**
       ```bash
       python historical_generator.py
       ```
    
    3. **Run your first survey:**
       ```bash
       python main.py --categories general price network_quality --runs 5
       ```
    
    4. **Refresh this page to see premium analytics!**
    """)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### 📈 About Premium Edition")
st.sidebar.info(
    "**SOM Intelligence Platform**\n\n"
    "✓ Statistical confidence intervals\n"
    "✓ Historical trend analysis\n"
    "✓ Narrative & theme extraction\n"
    "✓ Response explorer\n"
    "✓ ROI-driven insights\n\n"
    "_Enterprise-grade competitive intelligence_"
)