"""
Data Loader Module

This module handles loading, cleaning, and preprocessing of e-commerce datasets.
It provides functions to load individual datasets and create analysis-ready data structures.
"""

import pandas as pd
import numpy as np
from typing import Tuple, Dict, Optional
import os
import warnings


class EcommerceDataLoader:
    """
    Class for loading and preprocessing e-commerce datasets.
    """
    
    def __init__(self, data_path: str = 'ecommerce_data'):
        """
        Initialize the data loader with the path to data files.
        
        Args:
            data_path: Path to the directory containing CSV files
        """
        self.data_path = data_path
        self.datasets = {}
        
    def load_raw_datasets(self) -> Dict[str, pd.DataFrame]:
        """
        Load all raw datasets from CSV files.
        
        Returns:
            Dictionary containing all loaded datasets
        """
        file_mappings = {
            'orders': 'orders_dataset.csv',
            'order_items': 'order_items_dataset.csv',
            'products': 'products_dataset.csv',
            'customers': 'customers_dataset.csv',
            'reviews': 'order_reviews_dataset.csv',
            'payments': 'order_payments_dataset.csv'
        }
        
        for dataset_name, filename in file_mappings.items():
            file_path = os.path.join(self.data_path, filename)
            try:
                self.datasets[dataset_name] = pd.read_csv(file_path)
                print(f"Loaded {dataset_name}: {len(self.datasets[dataset_name])} rows")
            except FileNotFoundError:
                print(f"Warning: {filename} not found, skipping {dataset_name}")
                continue
        
        return self.datasets
    
    def clean_and_process_data(self) -> Dict[str, pd.DataFrame]:
        """
        Clean and process raw datasets for analysis.
        
        Returns:
            Dictionary containing cleaned datasets
        """
        if not self.datasets:
            self.load_raw_datasets()
        
        # Process orders data
        if 'orders' in self.datasets:
            self.datasets['orders'] = self._process_orders_data(self.datasets['orders'])
        
        # Process order items data
        if 'order_items' in self.datasets:
            self.datasets['order_items'] = self._process_order_items_data(self.datasets['order_items'])
        
        # Process products data
        if 'products' in self.datasets:
            self.datasets['products'] = self._process_products_data(self.datasets['products'])
        
        # Process reviews data
        if 'reviews' in self.datasets:
            self.datasets['reviews'] = self._process_reviews_data(self.datasets['reviews'])
        
        return self.datasets
    
    def _process_orders_data(self, orders: pd.DataFrame) -> pd.DataFrame:
        """
        Process and clean orders dataset.
        
        Args:
            orders: Raw orders DataFrame
            
        Returns:
            Cleaned orders DataFrame
        """
        orders_clean = orders.copy()
        
        # Convert timestamp columns
        timestamp_cols = [
            'order_purchase_timestamp',
            'order_approved_at',
            'order_delivered_carrier_date',
            'order_delivered_customer_date',
            'order_estimated_delivery_date'
        ]
        
        for col in timestamp_cols:
            if col in orders_clean.columns:
                orders_clean[col] = pd.to_datetime(orders_clean[col], errors='coerce')
        
        # Add derived time columns
        if 'order_purchase_timestamp' in orders_clean.columns:
            orders_clean['order_year'] = orders_clean['order_purchase_timestamp'].dt.year
            orders_clean['order_month'] = orders_clean['order_purchase_timestamp'].dt.month
            orders_clean['order_quarter'] = orders_clean['order_purchase_timestamp'].dt.quarter
            orders_clean['order_dayofweek'] = orders_clean['order_purchase_timestamp'].dt.dayofweek
        
        return orders_clean
    
    def _process_order_items_data(self, order_items: pd.DataFrame) -> pd.DataFrame:
        """
        Process and clean order items dataset.
        
        Args:
            order_items: Raw order items DataFrame
            
        Returns:
            Cleaned order items DataFrame
        """
        order_items_clean = order_items.copy()
        
        # Convert shipping limit date
        if 'shipping_limit_date' in order_items_clean.columns:
            order_items_clean['shipping_limit_date'] = pd.to_datetime(
                order_items_clean['shipping_limit_date'], errors='coerce'
            )
        
        # Ensure numeric columns are properly typed
        numeric_cols = ['price', 'freight_value']
        for col in numeric_cols:
            if col in order_items_clean.columns:
                order_items_clean[col] = pd.to_numeric(order_items_clean[col], errors='coerce')
        
        # Add total order value (price + freight)
        if 'price' in order_items_clean.columns and 'freight_value' in order_items_clean.columns:
            order_items_clean['total_value'] = (
                order_items_clean['price'] + order_items_clean['freight_value']
            )
        
        return order_items_clean
    
    def _process_products_data(self, products: pd.DataFrame) -> pd.DataFrame:
        """
        Process and clean products dataset.
        
        Args:
            products: Raw products DataFrame
            
        Returns:
            Cleaned products DataFrame
        """
        products_clean = products.copy()
        
        # Ensure numeric columns are properly typed
        numeric_cols = [
            'product_name_length', 'product_description_length',
            'product_photos_qty', 'product_weight_g',
            'product_length_cm', 'product_height_cm', 'product_width_cm'
        ]
        
        for col in numeric_cols:
            if col in products_clean.columns:
                products_clean[col] = pd.to_numeric(products_clean[col], errors='coerce')
        
        # Calculate product volume if dimensions are available
        dimension_cols = ['product_length_cm', 'product_height_cm', 'product_width_cm']
        if all(col in products_clean.columns for col in dimension_cols):
            products_clean['product_volume_cm3'] = (
                products_clean['product_length_cm'] *
                products_clean['product_height_cm'] *
                products_clean['product_width_cm']
            )
        
        return products_clean
    
    def _process_reviews_data(self, reviews: pd.DataFrame) -> pd.DataFrame:
        """
        Process and clean reviews dataset.
        
        Args:
            reviews: Raw reviews DataFrame
            
        Returns:
            Cleaned reviews DataFrame
        """
        reviews_clean = reviews.copy()
        
        # Convert timestamp columns
        timestamp_cols = ['review_creation_date', 'review_answer_timestamp']
        for col in timestamp_cols:
            if col in reviews_clean.columns:
                reviews_clean[col] = pd.to_datetime(reviews_clean[col], errors='coerce')
        
        # Ensure review_score is numeric
        if 'review_score' in reviews_clean.columns:
            reviews_clean['review_score'] = pd.to_numeric(
                reviews_clean['review_score'], errors='coerce'
            )
        
        return reviews_clean
    
    def create_sales_dataset(self, 
                           filter_status: str = 'delivered',
                           include_cancelled: bool = False) -> pd.DataFrame:
        """
        Create a comprehensive sales dataset by merging relevant tables.
        
        Args:
            filter_status: Order status to filter by (default: 'delivered')
            include_cancelled: Whether to include cancelled orders
            
        Returns:
            Combined sales DataFrame ready for analysis
        """
        if not self.datasets:
            self.clean_and_process_data()
        
        # Start with order items as base
        sales_data = self.datasets['order_items'].copy()
        
        # Merge with orders
        if 'orders' in self.datasets:
            sales_data = pd.merge(
                sales_data,
                self.datasets['orders'][['order_id', 'order_status', 'order_purchase_timestamp',
                                       'order_delivered_customer_date', 'order_year', 'order_month']],
                on='order_id',
                how='left'
            )
        
        # Filter by order status if specified
        if filter_status and not include_cancelled:
            sales_data = sales_data[sales_data['order_status'] == filter_status]
        elif filter_status:
            # Include specified status plus cancelled if requested
            statuses = [filter_status]
            if include_cancelled:
                statuses.append('cancelled')
            sales_data = sales_data[sales_data['order_status'].isin(statuses)]
        
        # Add time-based columns for analysis
        if 'order_purchase_timestamp' in sales_data.columns:
            # Suppress the SettingWithCopyWarning
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                sales_data = sales_data.copy()
                sales_data['year'] = sales_data['order_purchase_timestamp'].dt.year
                sales_data['month'] = sales_data['order_purchase_timestamp'].dt.month
        
        return sales_data
    
    def get_dataset_summary(self) -> Dict[str, Dict]:
        """
        Get summary information about loaded datasets.
        
        Returns:
            Dictionary with summary statistics for each dataset
        """
        summary = {}
        
        for name, df in self.datasets.items():
            summary[name] = {
                'rows': len(df),
                'columns': len(df.columns),
                'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2,
                'missing_values': df.isnull().sum().sum(),
                'dtypes': df.dtypes.value_counts().to_dict()
            }
        
        return summary
    
    def validate_data_quality(self) -> Dict[str, Dict]:
        """
        Perform data quality checks on loaded datasets.
        
        Returns:
            Dictionary with data quality metrics
        """
        quality_report = {}
        
        for name, df in self.datasets.items():
            quality_report[name] = {
                'duplicate_rows': df.duplicated().sum(),
                'missing_percentage': (df.isnull().sum() / len(df) * 100).to_dict(),
                'unique_values': {col: df[col].nunique() for col in df.columns}
            }
        
        return quality_report


def load_and_prepare_data(data_path: str = 'ecommerce_data',
                         target_year: int = 2023,
                         comparison_year: int = 2022) -> Tuple[pd.DataFrame, Dict[str, pd.DataFrame]]:
    """
    Convenience function to load and prepare data for analysis.
    
    Args:
        data_path: Path to data directory
        target_year: Primary year for analysis
        comparison_year: Comparison year for growth calculations
        
    Returns:
        Tuple of (sales_dataset, all_datasets)
    """
    loader = EcommerceDataLoader(data_path)
    datasets = loader.clean_and_process_data()
    sales_data = loader.create_sales_dataset()
    
    print(f"\nData loaded successfully!")
    print(f"Sales data shape: {sales_data.shape}")
    print(f"Date range: {sales_data['order_purchase_timestamp'].min()} to {sales_data['order_purchase_timestamp'].max()}")
    print(f"Years available: {sorted(sales_data['year'].unique())}")
    
    return sales_data, datasets


def create_configurable_date_filter(data: pd.DataFrame,
                                   date_column: str = 'order_purchase_timestamp',
                                   start_year: Optional[int] = None,
                                   end_year: Optional[int] = None,
                                   months: Optional[list] = None,
                                   quarters: Optional[list] = None) -> pd.DataFrame:
    """
    Create a flexible date filter for analysis periods.
    
    Args:
        data: DataFrame to filter
        date_column: Name of the datetime column
        start_year: Start year (inclusive)
        end_year: End year (inclusive)
        months: List of months to include (1-12)
        quarters: List of quarters to include (1-4)
        
    Returns:
        Filtered DataFrame
    """
    filtered_data = data.copy()
    
    if start_year:
        filtered_data = filtered_data[
            filtered_data[date_column].dt.year >= start_year
        ]
    
    if end_year:
        filtered_data = filtered_data[
            filtered_data[date_column].dt.year <= end_year
        ]
    
    if months:
        filtered_data = filtered_data[
            filtered_data[date_column].dt.month.isin(months)
        ]
    
    if quarters:
        filtered_data = filtered_data[
            filtered_data[date_column].dt.quarter.isin(quarters)
        ]
    
    return filtered_data