"""
Custom visualization functions for SOM Monitor
"""
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict, List
from models import SOMMetrics, QueryResult
from config import CHART_COLORS


def create_comparison_chart(metrics: Dict[str, SOMMetrics],
                           metric_name: str = "mention_rate") -> go.Figure:
    """Create comparison bar chart for any metric"""
    brands = list(metrics.keys())
    
    if metric_name == "mention_rate":
        values = [m.mention_rate * 100 for m in metrics.values()]
        title = "Mention Rate by Brand"
        yaxis_title = "Mention Rate (%)"
    elif metric_name == "first_mention_rate":
        values = [m.first_mention_rate * 100 for m in metrics.values()]
        title = "First Mention Rate by Brand"
        yaxis_title = "First Mention Rate (%)"
    elif metric_name == "avg_position":
        values = [m.avg_position if m.avg_position else 0 for m in metrics.values()]
        title = "Average Position by Brand"
        yaxis_title = "Average Position"
    else:
        values = [m.total_mentions for m in metrics.values()]
        title = "Total Mentions by Brand"
        yaxis_title = "Total Mentions"
    
    # Sort by values
    sorted_pairs = sorted(zip(brands, values), key=lambda x: x[1], reverse=True)
    brands_sorted, values_sorted = zip(*sorted_pairs)
    
    fig = go.Figure(data=[
        go.Bar(
            x=brands_sorted,
            y=values_sorted,
            marker_color=CHART_COLORS[:len(brands_sorted)],
            text=values_sorted,
            texttemplate='%{text:.1f}',
            textposition='outside',
        )
    ])
    
    fig.update_layout(
        title=title,
        xaxis_title="Brand",
        yaxis_title=yaxis_title,
        showlegend=False,
        height=400
    )
    
    return fig


def create_radar_chart(metrics: Dict[str, SOMMetrics]) -> go.Figure:
    """Create radar chart comparing brands across metrics"""
    brands = list(metrics.keys())
    
    # Normalize metrics to 0-100 scale
    categories = ['Mention Rate', 'First Mention', 'Position Score']
    
    fig = go.Figure()
    
    for brand in brands:
        m = metrics[brand]
        position_score = 100 - (m.avg_position * 10 if m.avg_position else 50)
        
        values = [
            m.mention_rate * 100,
            m.first_mention_rate * 100,
            position_score
        ]
        
        fig.add_trace(go.Scatterpolar(
            r=values + [values[0]],  # Close the polygon
            theta=categories + [categories[0]],
            fill='toself',
            name=brand
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=True,
        title="Brand Performance Radar",
        height=500
    )
    
    return fig


def create_heatmap(results: List[QueryResult],
                  brands: List[str]) -> go.Figure:
    """Create co-occurrence heatmap"""
    # Calculate co-occurrence matrix
    n = len(brands)
    matrix = [[0 for _ in range(n)] for _ in range(n)]
    
    for result in results:
        for i, brand1 in enumerate(brands):
            for j, brand2 in enumerate(brands):
                if result.mentions[brand1].mentioned and result.mentions[brand2].mentioned:
                    matrix[i][j] += 1
    
    fig = go.Figure(data=go.Heatmap(
        z=matrix,
        x=brands,
        y=brands,
        colorscale='Blues',
        text=matrix,
        texttemplate='%{text}',
        textfont={"size": 10},
        colorbar=dict(title="Co-occurrences")
    ))
    
    fig.update_layout(
        title="Brand Co-occurrence Matrix",
        xaxis_title="Brand",
        yaxis_title="Brand",
        height=500
    )
    
    return fig


def create_time_series_chart(history_df: pd.DataFrame,
                            brands: List[str]) -> go.Figure:
    """Create time series chart of mention rates"""
    fig = go.Figure()
    
    for brand in brands:
        brand_data = history_df[history_df['brand'] == brand]
        daily_mentions = brand_data.groupby('date')['mentioned'].mean() * 100
        
        fig.add_trace(go.Scatter(
            x=daily_mentions.index,
            y=daily_mentions.values,
            mode='lines+markers',
            name=brand,
            line=dict(width=2),
            marker=dict(size=6)
        ))
    
    fig.update_layout(
        title="Mention Funnel by Brand",
        height=500
    )
    
    return fig


def create_distribution_plot(results: List[QueryResult],
                            brands: List[str]) -> go.Figure:
    """Create distribution plot of mention positions"""
    fig = go.Figure()
    
    for brand in brands:
        positions = []
        for result in results:
            if brand in result.mention_order:
                pos = result.mention_order.index(brand) + 1
                positions.append(pos)
        
        if positions:
            fig.add_trace(go.Box(
                y=positions,
                name=brand,
                boxmean='sd'
            ))
    
    fig.update_layout(
        title="Distribution of Mention Positions",
        yaxis_title="Position",
        xaxis_title="Brand",
        showlegend=False,
        height=400
    )
    
    return fig


def create_category_comparison(results: List[QueryResult],
                              brands: List[str]) -> go.Figure:
    """Create grouped bar chart by category"""
    categories = list(set(r.category for r in results))
    
    fig = go.Figure()
    
    for brand in brands:
        mention_rates = []
        for category in categories:
            cat_results = [r for r in results if r.category == category]
            if cat_results:
                mentions = sum(1 for r in cat_results if r.mentions[brand].mentioned)
                rate = (mentions / len(cat_results)) * 100
                mention_rates.append(rate)
            else:
                mention_rates.append(0)
        
        fig.add_trace(go.Bar(
            name=brand,
            x=categories,
            y=mention_rates,
            text=[f'{r:.1f}%' for r in mention_rates],
            textposition='auto'
        ))
    
    fig.update_layout(
        title="Mention Rates by Category",
        xaxis_title="Category",
        yaxis_title="Mention Rate (%)",
        barmode='group',
        height=400
    )
    
    return fig


def create_sunburst_chart(results: List[QueryResult],
                         brands: List[str]) -> go.Figure:
    """Create sunburst chart showing category -> brand hierarchy"""
    data = []
    
    # Root
    data.append(dict(
        ids=['Total'],
        labels=['All Queries'],
        parents=[''],
        values=[len(results)]
    ))
    
    # Categories
    categories = list(set(r.category for r in results))
    for category in categories:
        cat_count = sum(1 for r in results if r.category == category)
        data.append(dict(
            ids=[category],
            labels=[category.title()],
            parents=['Total'],
            values=[cat_count]
        ))
        
        # Brands within category
        for brand in brands:
            cat_results = [r for r in results if r.category == category]
            brand_mentions = sum(1 for r in cat_results if r.mentions[brand].mentioned)
            if brand_mentions > 0:
                data.append(dict(
                    ids=[f'{category}-{brand}'],
                    labels=[brand],
                    parents=[category],
                    values=[brand_mentions]
                ))
    
    # Combine all data
    ids = [d['ids'][0] for d in data]
    labels = [d['labels'][0] for d in data]
    parents = [d['parents'][0] for d in data]
    values = [d['values'][0] for d in data]
    
    fig = go.Figure(go.Sunburst(
        ids=ids,
        labels=labels,
        parents=parents,
        values=values,
        branchvalues="total"
    ))
    
    fig.update_layout(
        title="Query Distribution: Category → Brand",
        height=600
    )
    
    return fig


def create_waterfall_chart(metrics: Dict[str, SOMMetrics]) -> go.Figure:
    """Create waterfall chart showing cumulative mentions"""
    sorted_metrics = sorted(
        metrics.items(),
        key=lambda x: x[1].total_mentions,
        reverse=True
    )
    
    brands = [brand for brand, _ in sorted_metrics]
    values = [m.total_mentions for _, m in sorted_metrics]
    
    # Calculate cumulative for waterfall
    measure = ['relative'] * len(brands)
    measure[-1] = 'total'
    
    fig = go.Figure(go.Waterfall(
        name="Mentions",
        orientation="v",
        measure=measure,
        x=brands,
        y=values,
        text=values,
        textposition="outside",
        connector={"line": {"color": "rgb(63, 63, 63)"}},
    ))
    
    fig.update_layout(
        title="Cumulative Mentions Waterfall",
        xaxis_title="Brand",
        yaxis_title="Mentions",
        showlegend=False,
        height=400
    )
    
    return fig


def create_scatter_matrix(metrics: Dict[str, SOMMetrics]) -> go.Figure:
    """Create scatter matrix of all metrics"""
    df = pd.DataFrame([
        {
            'Brand': brand,
            'Mention Rate': m.mention_rate * 100,
            'First Mention Rate': m.first_mention_rate * 100,
            'Avg Position': m.avg_position if m.avg_position else 0,
            'Total Mentions': m.total_mentions
        }
        for brand, m in metrics.items()
    ])
    
    fig = px.scatter_matrix(
        df,
        dimensions=['Mention Rate', 'First Mention Rate', 'Avg Position', 'Total Mentions'],
        color='Brand',
        title="Metrics Correlation Matrix"
    )
    
    fig.update_layout(height=700)
    
    return fig


def create_gauge_chart(value: float,
                      title: str,
                      max_value: float = 100) -> go.Figure:
    """Create gauge chart for single metric"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        title={'text': title},
        delta={'reference': max_value * 0.5},
        gauge={
            'axis': {'range': [None, max_value]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, max_value * 0.33], 'color': "lightgray"},
                {'range': [max_value * 0.33, max_value * 0.66], 'color': "gray"},
                {'range': [max_value * 0.66, max_value], 'color': "darkgray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': max_value * 0.9
            }
        }
    ))
    
    fig.update_layout(height=300)
    
    return fig


def create_treemap(results: List[QueryResult],
                  brands: List[str]) -> go.Figure:
    """Create treemap of brand mentions by category"""
    data = []
    
    categories = list(set(r.category for r in results))
    
    for category in categories:
        cat_results = [r for r in results if r.category == category]
        for brand in brands:
            mentions = sum(1 for r in cat_results if r.mentions[brand].mentioned)
            if mentions > 0:
                data.append({
                    'Category': category.title(),
                    'Brand': brand,
                    'Mentions': mentions
                })
    
    df = pd.DataFrame(data)
    
    fig = px.treemap(
        df,
        path=['Category', 'Brand'],
        values='Mentions',
        color='Mentions',
        color_continuous_scale='Blues',
        title="Brand Mentions by Category (Treemap)"
    )
    
    fig.update_layout(height=500)
    
    return fig Rate Trends Over Time",
        xaxis_title="Date",
        yaxis_title="Mention Rate (%)",
        hovermode='x unified',
        height=400
    )
    
    return fig


def create_funnel_chart(metrics: Dict[str, SOMMetrics]) -> go.Figure:
    """Create funnel chart showing mention to first-mention conversion"""
    brands = []
    mentioned = []
    first_mentioned = []
    
    for brand, m in sorted(metrics.items(), key=lambda x: x[1].mention_rate, reverse=True):
        brands.append(brand)
        mentioned.append(m.mention_rate * 100)
        first_mentioned.append(m.first_mention_rate * 100)
    
    fig = go.Figure()
    
    fig.add_trace(go.Funnel(
        name='Mentioned',
        y=brands,
        x=mentioned,
        textinfo="value+percent initial"
    ))
    
    fig.add_trace(go.Funnel(
        name='First Mentioned',
        y=brands,
        x=first_mentioned,
        textinfo="value+percent previous"
    ))
    
    fig.update_layout(
        title="Mention