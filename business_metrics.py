"""
Business Metrics Module

This module contains functions for calculating key e-commerce business metrics
including revenue analysis, customer behavior, and operational performance.
"""

import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any


def calculate_revenue_metrics(sales_data: pd.DataFrame, 
                            current_period_col: str = 'year',
                            current_period: int = 2023,
                            comparison_period: int = 2022) -> Dict[str, Any]:
    """
    Calculate revenue metrics including total revenue, growth rates, and comparisons.
    
    Args:
        sales_data: DataFrame with sales data including price and period columns
        current_period_col: Column name for the time period (e.g., 'year', 'month')
        current_period: Current period value for analysis
        comparison_period: Previous period value for comparison
        
    Returns:
        Dictionary containing revenue metrics
    """
    current_data = sales_data[sales_data[current_period_col] == current_period]
    comparison_data = sales_data[sales_data[current_period_col] == comparison_period]
    
    current_revenue = current_data['price'].sum()
    comparison_revenue = comparison_data['price'].sum()
    
    revenue_growth = ((current_revenue - comparison_revenue) / comparison_revenue * 100 
                     if comparison_revenue > 0 else 0)
    
    return {
        'current_revenue': current_revenue,
        'comparison_revenue': comparison_revenue,
        'revenue_growth_pct': revenue_growth,
        'current_period': current_period,
        'comparison_period': comparison_period
    }


def calculate_monthly_growth_trend(sales_data: pd.DataFrame, 
                                 target_year: int = 2023) -> pd.Series:
    """
    Calculate month-over-month growth rates for a specific year.
    
    Args:
        sales_data: DataFrame with sales data including price, month, and year columns
        target_year: Year to analyze for monthly trends
        
    Returns:
        Series with monthly growth rates
    """
    yearly_data = sales_data[sales_data['year'] == target_year]
    monthly_revenue = yearly_data.groupby('month')['price'].sum()
    monthly_growth = monthly_revenue.pct_change()
    
    return monthly_growth


def calculate_average_order_value(sales_data: pd.DataFrame,
                                current_period_col: str = 'year',
                                current_period: int = 2023,
                                comparison_period: int = 2022) -> Dict[str, Any]:
    """
    Calculate average order value (AOV) and compare across periods.
    
    Args:
        sales_data: DataFrame with sales data
        current_period_col: Column name for the time period
        current_period: Current period value
        comparison_period: Previous period value for comparison
        
    Returns:
        Dictionary containing AOV metrics
    """
    current_data = sales_data[sales_data[current_period_col] == current_period]
    comparison_data = sales_data[sales_data[current_period_col] == comparison_period]
    
    current_aov = current_data.groupby('order_id')['price'].sum().mean()
    comparison_aov = comparison_data.groupby('order_id')['price'].sum().mean()
    
    aov_growth = ((current_aov - comparison_aov) / comparison_aov * 100 
                 if comparison_aov > 0 else 0)
    
    return {
        'current_aov': current_aov,
        'comparison_aov': comparison_aov,
        'aov_growth_pct': aov_growth
    }


def calculate_order_metrics(sales_data: pd.DataFrame,
                          current_period_col: str = 'year',
                          current_period: int = 2023,
                          comparison_period: int = 2022) -> Dict[str, Any]:
    """
    Calculate order volume metrics and growth rates.
    
    Args:
        sales_data: DataFrame with sales data
        current_period_col: Column name for the time period
        current_period: Current period value
        comparison_period: Previous period value for comparison
        
    Returns:
        Dictionary containing order metrics
    """
    current_data = sales_data[sales_data[current_period_col] == current_period]
    comparison_data = sales_data[sales_data[current_period_col] == comparison_period]
    
    current_orders = current_data['order_id'].nunique()
    comparison_orders = comparison_data['order_id'].nunique()
    
    order_growth = ((current_orders - comparison_orders) / comparison_orders * 100 
                   if comparison_orders > 0 else 0)
    
    return {
        'current_orders': current_orders,
        'comparison_orders': comparison_orders,
        'order_growth_pct': order_growth
    }


def calculate_product_category_performance(sales_data: pd.DataFrame,
                                         products_data: pd.DataFrame,
                                         period_col: str = 'year',
                                         period_value: int = 2023) -> pd.DataFrame:
    """
    Calculate sales performance by product category.
    
    Args:
        sales_data: DataFrame with sales data
        products_data: DataFrame with product information
        period_col: Column name for filtering period
        period_value: Period value to analyze
        
    Returns:
        DataFrame with category performance metrics
    """
    period_data = sales_data[sales_data[period_col] == period_value]
    
    category_sales = pd.merge(
        products_data[['product_id', 'product_category_name']],
        period_data[['product_id', 'price']],
        on='product_id'
    )
    
    category_performance = (category_sales.groupby('product_category_name')['price']
                          .agg(['sum', 'count', 'mean'])
                          .rename(columns={'sum': 'total_revenue', 
                                         'count': 'total_orders',
                                         'mean': 'avg_order_value'})
                          .sort_values('total_revenue', ascending=False))
    
    return category_performance


def calculate_geographic_performance(sales_data: pd.DataFrame,
                                   orders_data: pd.DataFrame,
                                   customers_data: pd.DataFrame,
                                   period_col: str = 'year',
                                   period_value: int = 2023) -> pd.DataFrame:
    """
    Calculate sales performance by geographic region (state).
    
    Args:
        sales_data: DataFrame with sales data
        orders_data: DataFrame with order information
        customers_data: DataFrame with customer information
        period_col: Column name for filtering period
        period_value: Period value to analyze
        
    Returns:
        DataFrame with geographic performance metrics
    """
    period_data = sales_data[sales_data[period_col] == period_value]
    
    # Merge with orders to get customer_id
    sales_customers = pd.merge(
        period_data[['order_id', 'price']],
        orders_data[['order_id', 'customer_id']],
        on='order_id'
    )
    
    # Merge with customers to get state
    sales_states = pd.merge(
        sales_customers,
        customers_data[['customer_id', 'customer_state']],
        on='customer_id'
    )
    
    # Calculate metrics by state
    state_performance = (sales_states.groupby('customer_state')['price']
                        .agg(['sum', 'count', 'mean'])
                        .rename(columns={'sum': 'total_revenue',
                                       'count': 'total_orders',
                                       'mean': 'avg_order_value'})
                        .sort_values('total_revenue', ascending=False))
    
    return state_performance


def calculate_customer_satisfaction_metrics(sales_data: pd.DataFrame,
                                          reviews_data: pd.DataFrame,
                                          period_col: str = 'year',
                                          period_value: int = 2023) -> Dict[str, Any]:
    """
    Calculate customer satisfaction metrics based on reviews and delivery performance.
    
    Args:
        sales_data: DataFrame with sales data including delivery dates
        reviews_data: DataFrame with review scores
        period_col: Column name for filtering period
        period_value: Period value to analyze
        
    Returns:
        Dictionary containing satisfaction metrics
    """
    period_data = sales_data[sales_data[period_col] == period_value].copy()
    
    # Calculate delivery speed
    period_data['order_delivered_customer_date'] = pd.to_datetime(
        period_data['order_delivered_customer_date']
    )
    period_data['delivery_speed'] = (
        period_data['order_delivered_customer_date'] - 
        period_data['order_purchase_timestamp']
    ).dt.days
    
    # Merge with reviews
    satisfaction_data = pd.merge(
        period_data,
        reviews_data[['order_id', 'review_score']],
        on='order_id'
    )
    
    # Remove duplicates for order-level analysis
    order_satisfaction = satisfaction_data[
        ['order_id', 'delivery_speed', 'review_score']
    ].drop_duplicates()
    
    avg_review_score = order_satisfaction['review_score'].mean()
    avg_delivery_time = order_satisfaction['delivery_speed'].mean()
    
    # Categorize delivery speed and calculate satisfaction by category
    def categorize_delivery_speed(days):
        if days <= 3:
            return '1-3 days'
        elif days <= 7:
            return '4-7 days'
        else:
            return '8+ days'
    
    order_satisfaction['delivery_category'] = (
        order_satisfaction['delivery_speed'].apply(categorize_delivery_speed)
    )
    
    satisfaction_by_delivery = (
        order_satisfaction.groupby('delivery_category')['review_score']
        .mean()
        .to_dict()
    )
    
    return {
        'avg_review_score': avg_review_score,
        'avg_delivery_time_days': avg_delivery_time,
        'satisfaction_by_delivery_speed': satisfaction_by_delivery
    }


def calculate_order_status_distribution(orders_data: pd.DataFrame,
                                      period_col: str = 'year',
                                      period_value: int = 2023) -> pd.Series:
    """
    Calculate distribution of order statuses for a given period.
    
    Args:
        orders_data: DataFrame with order information
        period_col: Column name for filtering period
        period_value: Period value to analyze
        
    Returns:
        Series with order status distribution (normalized)
    """
    orders_data_copy = orders_data.copy()
    orders_data_copy[period_col] = pd.to_datetime(
        orders_data_copy['order_purchase_timestamp']
    ).dt.year
    
    period_orders = orders_data_copy[orders_data_copy[period_col] == period_value]
    status_distribution = period_orders['order_status'].value_counts(normalize=True)
    
    return status_distribution


def generate_business_summary(revenue_metrics: Dict,
                            aov_metrics: Dict,
                            order_metrics: Dict,
                            satisfaction_metrics: Dict) -> str:
    """
    Generate a comprehensive business summary from calculated metrics.
    
    Args:
        revenue_metrics: Dictionary from calculate_revenue_metrics
        aov_metrics: Dictionary from calculate_average_order_value
        order_metrics: Dictionary from calculate_order_metrics
        satisfaction_metrics: Dictionary from calculate_customer_satisfaction_metrics
        
    Returns:
        Formatted string with business summary
    """
    summary = f"""
BUSINESS PERFORMANCE SUMMARY
============================

Revenue Analysis:
- Total Revenue: ${revenue_metrics['current_revenue']:,.2f}
- Revenue Growth: {revenue_metrics['revenue_growth_pct']:.2f}%
- Period: {revenue_metrics['current_period']} vs {revenue_metrics['comparison_period']}

Order Metrics:
- Total Orders: {order_metrics['current_orders']:,}
- Order Growth: {order_metrics['order_growth_pct']:.2f}%
- Average Order Value: ${aov_metrics['current_aov']:.2f}
- AOV Growth: {aov_metrics['aov_growth_pct']:.2f}%

Customer Experience:
- Average Review Score: {satisfaction_metrics['avg_review_score']:.2f}/5.0
- Average Delivery Time: {satisfaction_metrics['avg_delivery_time_days']:.1f} days

Key Insights:
"""
    
    # Add insights based on metrics
    if revenue_metrics['revenue_growth_pct'] < 0:
        summary += f"- Revenue declined by {abs(revenue_metrics['revenue_growth_pct']):.1f}%, indicating potential market challenges\n"
    else:
        summary += f"- Revenue grew by {revenue_metrics['revenue_growth_pct']:.1f}%, showing positive business growth\n"
        
    if satisfaction_metrics['avg_review_score'] >= 4.0:
        summary += f"- Customer satisfaction is strong with {satisfaction_metrics['avg_review_score']:.1f}/5.0 average rating\n"
    else:
        summary += f"- Customer satisfaction needs attention with {satisfaction_metrics['avg_review_score']:.1f}/5.0 average rating\n"
        
    if satisfaction_metrics['avg_delivery_time_days'] <= 5:
        summary += "- Delivery performance is excellent with fast shipping times\n"
    elif satisfaction_metrics['avg_delivery_time_days'] <= 10:
        summary += "- Delivery performance is acceptable but could be improved\n"
    else:
        summary += "- Delivery times are slow and may impact customer satisfaction\n"
    
    return summary