# E-commerce Business Analysis Framework

A comprehensive, configurable framework for analyzing e-commerce business performance with modular code structure and reusable components.

## Overview

This project provides a refactored and enhanced version of the original EDA notebook with improved code organization, comprehensive documentation, and configurable analysis parameters. The framework enables analysts to efficiently perform business performance analysis across different time periods and business dimensions.

## Project Structure

```
lesson7_files/
├── EDA_Refactored.ipynb          # Main analysis notebook
├── business_metrics.py           # Business metric calculation functions
├── data_loader.py               # Data loading and preprocessing utilities
├── requirements.txt             # Python package dependencies
├── README.md                   # This file
└── ecommerce_data/             # Data directory
    ├── orders_dataset.csv
    ├── order_items_dataset.csv
    ├── products_dataset.csv
    ├── customers_dataset.csv
    ├── order_reviews_dataset.csv
    └── order_payments_dataset.csv
```

## Features

### 🔧 Configurable Analysis
- **Time Period Filtering**: Analyze specific years, months, or quarters
- **Flexible Date Ranges**: Compare any two periods for growth calculations
- **Business Metric Selection**: Focus on specific KPIs as needed

### 📊 Comprehensive Business Metrics
- **Revenue Analysis**: YoY growth, monthly trends, seasonal patterns
- **Customer Behavior**: Order volumes, AOV, retention indicators
- **Product Performance**: Category analysis, inventory insights
- **Geographic Analysis**: State-level performance with interactive maps
- **Operational Metrics**: Fulfillment rates, delivery performance
- **Customer Experience**: Satisfaction scores, delivery time analysis

### 🏗️ Modular Architecture
- **Reusable Functions**: Well-documented business metric calculations
- **Clean Data Pipeline**: Automated data loading and preprocessing
- **Consistent Visualizations**: Professional charts with business-oriented styling
- **Quality Assurance**: Built-in data quality checks and validation

## Quick Start

### 1. Installation

```bash
# Clone or download the project files
# Navigate to the project directory
cd lesson7_files

# Install required packages
pip install -r requirements.txt
```

### 2. Data Setup

Ensure your data files are in the `ecommerce_data/` directory:
- `orders_dataset.csv`
- `order_items_dataset.csv` 
- `products_dataset.csv`
- `customers_dataset.csv`
- `order_reviews_dataset.csv`
- `order_payments_dataset.csv` (optional)

### 3. Configure Analysis

Open `EDA_Refactored.ipynb` and modify the configuration section:

```python
# Analysis Configuration
ANALYSIS_YEAR = 2023          # Primary year for analysis
COMPARISON_YEAR = 2022        # Comparison year for growth metrics
DATA_PATH = 'ecommerce_data'  # Path to data files

# Optional: Filter by specific periods
ANALYSIS_MONTHS = [1, 2, 3]   # Q1 only, or None for full year
ANALYSIS_QUARTERS = [1, 2]    # H1 only, or None for full year
```

### 4. Run Analysis

Execute the notebook cells sequentially to generate:
- Executive summary dashboard
- Detailed business metrics
- Interactive visualizations
- Strategic insights and recommendations

## Usage Examples

### Example 1: Annual Performance Review
```python
# Configure for full year analysis
ANALYSIS_YEAR = 2023
COMPARISON_YEAR = 2022
ANALYSIS_MONTHS = None  # Full year
```

### Example 2: Quarterly Deep Dive
```python
# Configure for Q1 analysis only
ANALYSIS_YEAR = 2023
COMPARISON_YEAR = 2022
ANALYSIS_QUARTERS = [1]  # Q1 only
```

### Example 3: Custom Date Range
```python
# Configure for specific months
ANALYSIS_YEAR = 2023
COMPARISON_YEAR = 2022
ANALYSIS_MONTHS = [11, 12]  # Holiday season
```

## Key Business Metrics

The framework calculates comprehensive business metrics organized into categories:

### Revenue Metrics
- **Total Revenue**: Sum of delivered order values
- **Revenue Growth**: Year-over-year percentage change
- **Monthly Trends**: Month-over-month growth rates
- **Seasonal Patterns**: Revenue distribution across periods

### Customer Metrics
- **Order Volume**: Total number of orders
- **Average Order Value (AOV)**: Mean order value per transaction
- **Customer Satisfaction**: Average review scores
- **Delivery Performance**: Average delivery times and satisfaction by speed

### Product Metrics
- **Category Performance**: Revenue and order volume by product category
- **Product Mix Analysis**: Category contribution to total revenue
- **Inventory Insights**: Best and worst performing categories

### Geographic Metrics
- **State-Level Performance**: Revenue distribution across states
- **Market Concentration**: Geographic diversification analysis
- **Growth Opportunities**: Underperforming regions with potential

### Operational Metrics
- **Order Fulfillment**: Delivery rates and status distribution
- **Logistics Performance**: Delivery time trends and benchmarks
- **Process Efficiency**: Order processing and fulfillment metrics

## Code Modules

### business_metrics.py
Contains all business metric calculation functions with comprehensive documentation:

```python
from business_metrics import calculate_revenue_metrics, generate_business_summary

# Calculate revenue metrics for any period
revenue_metrics = calculate_revenue_metrics(
    sales_data, 
    current_period='year',
    current_period=2023,
    comparison_period=2022
)
```

### data_loader.py
Handles data loading, cleaning, and preprocessing:

```python
from data_loader import load_and_prepare_data

# Load and prepare all datasets
sales_data, all_datasets = load_and_prepare_data(
    data_path='ecommerce_data',
    target_year=2023,
    comparison_year=2022
)
```

## Visualization Features

- **Professional Styling**: Consistent color schemes and formatting
- **Interactive Maps**: Geographic performance with Plotly
- **Executive Dashboard**: KPI summary with key metrics
- **Trend Analysis**: Time series visualizations for all metrics
- **Comparative Analysis**: Side-by-side period comparisons

## Data Quality Assurance

The framework includes comprehensive data quality checks:
- Missing value analysis
- Duplicate detection
- Data type validation
- Date range verification
- Business logic validation

## Customization Options

### Adding New Metrics
1. Add calculation function to `business_metrics.py`
2. Include in notebook analysis sections
3. Update visualization components as needed

### Modifying Time Periods
1. Adjust configuration parameters in notebook
2. Use `create_configurable_date_filter()` for custom ranges
3. Modify comparison logic in metric functions

### Extending Visualizations
1. Add new chart types using consistent styling
2. Include in dashboard or dedicated sections
3. Ensure mobile-responsive design

## Best Practices

### Code Organization
- Keep business logic in `business_metrics.py`
- Use `data_loader.py` for data preprocessing
- Maintain notebook for analysis flow and visualization

### Performance Optimization
- Filter data early in the pipeline
- Use vectorized operations with pandas
- Cache intermediate results for large datasets

### Documentation Standards
- Include docstrings for all functions
- Comment complex business logic
- Maintain this README with updates

## Troubleshooting

### Common Issues

**ModuleNotFoundError**: Ensure all packages from `requirements.txt` are installed
```bash
pip install -r requirements.txt
```

**Data Loading Errors**: Verify file paths and CSV structure
```python
# Check data directory
import os
print(os.listdir('ecommerce_data'))
```

**Memory Issues with Large Datasets**: Use data filtering early
```python
# Filter dates before detailed analysis
sales_data = create_configurable_date_filter(
    sales_data, 
    start_year=2023,
    end_year=2023
)
```

**Visualization Problems**: Ensure Plotly is properly installed for interactive maps
```bash
pip install plotly>=5.10.0
```

## Contributing

To extend or modify this framework:

1. **Add New Metrics**: Create functions in `business_metrics.py`
2. **Enhance Visualizations**: Use consistent styling and color schemes
3. **Improve Data Processing**: Optimize `data_loader.py` functions
4. **Update Documentation**: Maintain comprehensive docstrings and README

## Support

For questions or issues:
1. Check the troubleshooting section above
2. Review function docstrings for detailed parameter information
3. Examine the original EDA.ipynb for reference implementations
4. Test with smaller data samples to isolate issues

## License

This project is designed for educational and business analysis purposes. Ensure compliance with your organization's data usage policies.

---

**Framework Version**: 1.0  
**Last Updated**: 2025  
**Python Version**: 3.8+  
**Dependencies**: See requirements.txt