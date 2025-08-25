"""
E-commerce Business Performance Dashboard

A professional Streamlit dashboard for analyzing e-commerce business metrics
including revenue trends, customer behavior, and operational performance.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings
from data_loader import load_and_prepare_data, create_configurable_date_filter
from business_metrics import (
    calculate_revenue_metrics,
    calculate_monthly_growth_trend,
    calculate_average_order_value,
    calculate_order_metrics,
    calculate_product_category_performance,
    calculate_geographic_performance,
    calculate_customer_satisfaction_metrics
)

warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="E-commerce Business Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 0;
    }
    .kpi-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border: 1px solid #e5e7eb;
        height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .bottom-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border: 1px solid #e5e7eb;
        height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1f2937;
        margin: 0;
    }
    .kpi-label {
        font-size: 0.9rem;
        color: #6b7280;
        margin: 0;
    }
    .trend-positive {
        color: #10b981;
        font-weight: 600;
    }
    .trend-negative {
        color: #ef4444;
        font-weight: 600;
    }
    .bottom-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f2937;
        margin: 0;
    }
    .bottom-label {
        font-size: 1rem;
        color: #6b7280;
        margin-top: 0.5rem;
    }
    .stars {
        color: #fbbf24;
        font-size: 1.5rem;
        margin-left: 0.5rem;
    }
    .stSelectbox label {
        font-weight: 600;
        color: #374151;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and prepare data with caching for better performance."""
    try:
        sales_data, all_datasets = load_and_prepare_data('ecommerce_data')
        return sales_data, all_datasets
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None

def format_currency(value, abbreviated=True):
    """Format currency values with K/M abbreviations."""
    if abbreviated:
        if abs(value) >= 1_000_000:
            return f"${value/1_000_000:.1f}M"
        elif abs(value) >= 1_000:
            return f"${value/1_000:.0f}K"
        else:
            return f"${value:.0f}"
    else:
        return f"${value:,.0f}"

def create_trend_indicator(current_value, previous_value):
    """Create trend indicator with arrow and percentage."""
    if previous_value == 0:
        return "N/A", "trend-positive"
    
    change_pct = ((current_value - previous_value) / previous_value) * 100
    arrow = "↑" if change_pct >= 0 else "↓"
    css_class = "trend-positive" if change_pct >= 0 else "trend-negative"
    return f"{arrow} {abs(change_pct):.2f}%", css_class

def main():
    # Load data
    sales_data, all_datasets = load_data()
    
    if sales_data is None:
        st.error("Failed to load data. Please check your data files.")
        return
    
    # Header with title and date/month filters
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<h1 class="main-header">E-commerce Business Dashboard</h1>', unsafe_allow_html=True)
    
    with col2:
        # Get available years from data
        available_years = sorted(sales_data['year'].unique(), reverse=True)
        
        # Set default to 2023 if available, otherwise first year
        default_year_index = 0
        if 2023 in available_years:
            default_year_index = available_years.index(2023)
        
        # Date range filter
        analysis_year = st.selectbox(
            "Analysis Year",
            options=available_years,
            index=default_year_index,
            key="analysis_year"
        )
        
        # Default comparison year to 2022 if available and different from analysis year
        comparison_years = [year for year in available_years if year != analysis_year]
        comparison_default_index = 0
        if 2022 in comparison_years:
            comparison_default_index = comparison_years.index(2022)
        
        comparison_year = st.selectbox(
            "Comparison Year", 
            options=comparison_years,
            index=comparison_default_index if comparison_years else None,
            key="comparison_year"
        )
        
        # Month filter
        month_options = ["All Months"] + [f"{i:02d} - {['Jan','Feb','Mar','Apr','May','Jun',
                                                       'Jul','Aug','Sep','Oct','Nov','Dec'][i-1]}" 
                                         for i in range(1, 13)]
        selected_months = st.multiselect(
            "Filter by Months",
            options=month_options,
            default=["All Months"],
            key="selected_months"
        )
    
    st.markdown("---")
    
    if analysis_year is None or comparison_year is None:
        st.error("Please ensure you have data for at least two different years.")
        return
    
    # Filter data based on selected years
    filtered_data = sales_data[sales_data['year'].isin([analysis_year, comparison_year])]
    
    # Apply month filtering if specific months are selected
    if selected_months and "All Months" not in selected_months:
        # Extract month numbers from selected options
        selected_month_nums = [int(month.split(' - ')[0]) for month in selected_months]
        filtered_data = filtered_data[filtered_data['month'].isin(selected_month_nums)]
    
    # Calculate metrics
    revenue_metrics = calculate_revenue_metrics(
        filtered_data, 
        current_period_col='year',
        current_period=analysis_year, 
        comparison_period=comparison_year
    )
    
    monthly_growth = calculate_monthly_growth_trend(filtered_data, analysis_year)
    
    aov_metrics = calculate_average_order_value(
        filtered_data,
        current_period_col='year',
        current_period=analysis_year,
        comparison_period=comparison_year
    )
    
    order_metrics = calculate_order_metrics(
        filtered_data,
        current_period_col='year', 
        current_period=analysis_year,
        comparison_period=comparison_year
    )
    
    # KPI Row - 4 cards
    st.markdown("### Key Performance Indicators")
    kpi_cols = st.columns(4)
    
    with kpi_cols[0]:
        trend_text, trend_class = create_trend_indicator(
            revenue_metrics['current_revenue'], 
            revenue_metrics['comparison_revenue']
        )
        st.markdown(f"""
        <div class="kpi-card">
            <div>
                <div class="kpi-value">{format_currency(revenue_metrics['current_revenue'])}</div>
                <div class="kpi-label">Total Revenue</div>
            </div>
            <div class="{trend_class}">{trend_text}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_cols[1]:
        avg_monthly_growth = monthly_growth.mean() * 100
        st.markdown(f"""
        <div class="kpi-card">
            <div>
                <div class="kpi-value">{avg_monthly_growth:.2f}%</div>
                <div class="kpi-label">Monthly Growth</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_cols[2]:
        trend_text, trend_class = create_trend_indicator(
            aov_metrics['current_aov'], 
            aov_metrics['comparison_aov']
        )
        st.markdown(f"""
        <div class="kpi-card">
            <div>
                <div class="kpi-value">{format_currency(aov_metrics['current_aov'])}</div>
                <div class="kpi-label">Average Order Value</div>
            </div>
            <div class="{trend_class}">{trend_text}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_cols[3]:
        trend_text, trend_class = create_trend_indicator(
            order_metrics['current_orders'], 
            order_metrics['comparison_orders']
        )
        st.markdown(f"""
        <div class="kpi-card">
            <div>
                <div class="kpi-value">{order_metrics['current_orders']:,}</div>
                <div class="kpi-label">Total Orders</div>
            </div>
            <div class="{trend_class}">{trend_text}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Charts Grid - 2x2 layout
    st.markdown("### Performance Analytics")
    
    chart_row1 = st.columns(2)
    chart_row2 = st.columns(2)
    
    # Revenue Trend Chart
    with chart_row1[0]:
        # Current year data
        current_monthly = filtered_data[filtered_data['year'] == analysis_year].groupby('month')['price'].sum()
        comparison_monthly = filtered_data[filtered_data['year'] == comparison_year].groupby('month')['price'].sum()
        
        fig_revenue = go.Figure()
        
        # Current year line (solid)
        fig_revenue.add_trace(go.Scatter(
            x=current_monthly.index,
            y=current_monthly.values,
            mode='lines+markers',
            name=f'{analysis_year}',
            line=dict(color='#3B82F6', width=3),
            marker=dict(size=8)
        ))
        
        # Comparison year line (dashed)
        fig_revenue.add_trace(go.Scatter(
            x=comparison_monthly.index,
            y=comparison_monthly.values,
            mode='lines+markers',
            name=f'{comparison_year}',
            line=dict(color='#6B7280', width=2, dash='dash'),
            marker=dict(size=6)
        ))
        
        fig_revenue.update_layout(
            height=400,
            title="Revenue Trend Comparison",
            title_font_size=16,
            showlegend=True,
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
            margin=dict(l=0, r=0, t=40, b=0),
            xaxis=dict(
                title="Month",
                showgrid=True,
                gridwidth=1,
                gridcolor='lightgray'
            ),
            yaxis=dict(
                title="Revenue",
                showgrid=True,
                gridwidth=1,
                gridcolor='lightgray',
                tickformat="$,.0s"
            )
        )
        
        st.plotly_chart(fig_revenue, use_container_width=True)
    
    # Top 10 Categories Bar Chart
    with chart_row1[1]:
        category_performance = calculate_product_category_performance(
            filtered_data, all_datasets['products'], 'year', analysis_year
        )
        
        top_10_categories = category_performance.head(10)
        
        fig_categories = px.bar(
            x=top_10_categories['total_revenue'],
            y=[cat.replace('_', ' ').title() for cat in top_10_categories.index],
            orientation='h',
            color=top_10_categories['total_revenue'],
            color_continuous_scale=['#DBEAFE', '#1D4ED8']
        )
        
        fig_categories.update_layout(
            height=400,
            title="Top 10 Product Categories",
            title_font_size=16,
            margin=dict(l=0, r=0, t=40, b=0),
            showlegend=False,
            coloraxis_showscale=False,
            xaxis=dict(
                title="Revenue",
                tickformat="$,.0s"
            ),
            yaxis=dict(title="")
        )
        
        fig_categories.update_traces(
            texttemplate='%{x:$,.0s}',
            textposition='outside'
        )
        
        st.plotly_chart(fig_categories, use_container_width=True)
    
    # Revenue by State Map
    with chart_row2[0]:
        state_performance = calculate_geographic_performance(
            filtered_data, all_datasets['orders'], all_datasets['customers'], 'year', analysis_year
        )
        
        state_df = state_performance.reset_index()
        state_df = state_df.rename(columns={'customer_state': 'state'})
        
        fig_map = px.choropleth(
            state_df,
            locations='state',
            color='total_revenue',
            locationmode='USA-states',
            scope='usa',
            color_continuous_scale=['#DBEAFE', '#1D4ED8'],
            labels={'total_revenue': 'Revenue ($)'}
        )
        
        fig_map.update_layout(
            height=400,
            title="Revenue by State",
            title_font_size=16,
            margin=dict(l=0, r=0, t=40, b=0),
            coloraxis_colorbar=dict(
                title="Revenue",
                tickformat="$,.0s"
            )
        )
        
        st.plotly_chart(fig_map, use_container_width=True)
    
    # Satisfaction vs Delivery Time
    with chart_row2[1]:
        satisfaction_metrics = calculate_customer_satisfaction_metrics(
            filtered_data, all_datasets['reviews'], 'year', analysis_year
        )
        
        delivery_satisfaction = satisfaction_metrics['satisfaction_by_delivery_speed']
        
        categories = list(delivery_satisfaction.keys())
        scores = list(delivery_satisfaction.values())
        
        fig_satisfaction = px.bar(
            x=categories,
            y=scores,
            color=scores,
            color_continuous_scale=['#DBEAFE', '#1D4ED8']
        )
        
        fig_satisfaction.update_layout(
            height=400,
            title="Customer Satisfaction by Delivery Speed",
            title_font_size=16,
            margin=dict(l=0, r=0, t=40, b=0),
            showlegend=False,
            coloraxis_showscale=False,
            xaxis=dict(title="Delivery Time"),
            yaxis=dict(
                title="Average Review Score",
                range=[3.8, 4.4]
            )
        )
        
        fig_satisfaction.update_traces(
            texttemplate='%{y:.2f}',
            textposition='outside'
        )
        
        st.plotly_chart(fig_satisfaction, use_container_width=True)
    
    st.markdown("---")
    
    # Bottom Row - 2 cards
    st.markdown("### Customer Experience")
    bottom_cols = st.columns(2)
    
    with bottom_cols[0]:
        avg_delivery_time = satisfaction_metrics['avg_delivery_time_days']
        
        st.markdown(f"""
        <div class="bottom-card">
            <div class="bottom-value">{avg_delivery_time:.1f} days</div>
            <div class="bottom-label">Average Delivery Time</div>
        </div>
        """, unsafe_allow_html=True)
    
    with bottom_cols[1]:
        avg_review_score = satisfaction_metrics['avg_review_score']
        stars = "★" * int(round(avg_review_score))
        
        st.markdown(f"""
        <div class="bottom-card">
            <div>
                <span class="bottom-value">{avg_review_score:.2f}</span>
                <span class="stars">{stars}</span>
            </div>
            <div class="bottom-label">Average Review Score</div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()