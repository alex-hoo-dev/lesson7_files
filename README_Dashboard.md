# E-commerce Business Dashboard

A professional Streamlit dashboard for visualizing and analyzing e-commerce business performance metrics. This interactive dashboard provides comprehensive insights into revenue trends, customer behavior, product performance, and operational efficiency.

## Features

### 📊 **Interactive Dashboard Layout**
- **Header Section**: Title with year-over-year date range filtering
- **KPI Cards**: Four key performance indicators with trend arrows
- **Analytics Grid**: 2x2 chart layout with professional visualizations
- **Customer Experience**: Bottom row focusing on satisfaction metrics

### 🔍 **Key Performance Indicators**
- **Total Revenue**: Current period revenue with YoY comparison
- **Monthly Growth**: Average month-over-month growth percentage  
- **Average Order Value**: AOV with trend indicators
- **Total Orders**: Order volume with YoY comparison

### 📈 **Advanced Visualizations**
- **Revenue Trend**: Line chart comparing current vs previous year
- **Product Categories**: Top 10 categories with blue gradient bars
- **Geographic Analysis**: US choropleth map showing revenue by state
- **Customer Satisfaction**: Review scores by delivery time buckets

### 🎯 **Customer Experience Metrics**
- **Delivery Performance**: Average delivery time tracking
- **Review Scores**: Customer satisfaction with star ratings

## Quick Start

### 1. Installation

```bash
# Clone or navigate to the project directory
cd lesson7_files

# Install required packages
pip install -r requirements.txt
```

### 2. Data Setup

Ensure your data files are in the `ecommerce_data/` directory:
```
ecommerce_data/
├── orders_dataset.csv
├── order_items_dataset.csv
├── products_dataset.csv
├── customers_dataset.csv
├── order_reviews_dataset.csv
└── order_payments_dataset.csv
```

### 3. Launch Dashboard

```bash
# Start the Streamlit dashboard
streamlit run app.py
```

The dashboard will open automatically in your browser at `http://localhost:8501`

## Dashboard Components

### Header Controls
- **Analysis Year**: Select primary year for analysis
- **Comparison Year**: Choose comparison year for trend calculations

### KPI Cards Row
Four cards displaying key metrics with trend indicators:
- Green arrows (↑) for positive trends
- Red arrows (↓) for negative trends  
- Two decimal places for trend percentages

### Charts Grid (2x2 Layout)

#### Revenue Trend Chart
- **Solid line**: Current period data
- **Dashed line**: Previous period comparison
- **Grid lines**: Enhanced readability
- **Y-axis formatting**: Values as $300K instead of $300,000

#### Top 10 Categories
- **Bar chart**: Horizontal orientation, sorted descending
- **Color scheme**: Blue gradient (light to dark)
- **Value formatting**: $300K, $2M format
- **Labels**: Category names with proper formatting

#### Revenue by State Map
- **Choropleth map**: US states color-coded by revenue
- **Color scale**: Blue gradient from light to dark
- **Interactive**: Hover for detailed state information

#### Satisfaction vs Delivery Time  
- **Bar chart**: Review scores by delivery speed buckets
- **Categories**: 1-3 days, 4-7 days, 8+ days
- **Color coding**: Consistent blue gradient theme

### Bottom Row Cards

#### Average Delivery Time
- **Large display**: Days with one decimal place
- **Clean layout**: Centered text and values

#### Review Score
- **Rating display**: Numerical score with star visualization
- **Stars**: Visual representation of rating level
- **Subtitle**: Clear labeling for context

## Technical Details

### Architecture
- **Frontend**: Streamlit with custom CSS styling
- **Visualizations**: Plotly for interactive charts
- **Data Processing**: Pandas for data manipulation
- **Backend**: Modular Python functions from existing analysis framework

### Performance Optimization
- **Data Caching**: `@st.cache_data` for improved load times
- **Efficient Filtering**: Date range filtering applied before calculations
- **Memory Management**: Optimized data structures and processing

### Styling Features
- **Professional Design**: Clean, business-oriented interface
- **Consistent Branding**: Uniform color scheme and typography
- **Responsive Layout**: Adapts to different screen sizes
- **Custom CSS**: Professional card styling and formatting

## Configuration

### Customization Options

**Color Schemes**: Modify the blue gradient colors in the chart configurations:
```python
color_continuous_scale=['#DBEAFE', '#1D4ED8']  # Light blue to dark blue
```

**Chart Heights**: Adjust visualization heights:
```python
fig.update_layout(height=400)  # Standard chart height
```

**KPI Card Styling**: Customize card appearance in the CSS section:
```css
.kpi-card {
    height: 140px;  /* Uniform card heights */
    /* Additional styling... */
}
```

### Data Requirements
- **Date Columns**: Must include timestamp columns for date filtering
- **Geographic Data**: State abbreviations for map visualization
- **Review Data**: Numerical scores (1-5 scale) for satisfaction metrics

## Troubleshooting

### Common Issues

**Data Loading Errors**
- Verify all CSV files are in `ecommerce_data/` directory
- Check file permissions and formats
- Ensure data contains required columns

**Performance Issues**
- Large datasets may require additional caching
- Consider data sampling for development/testing
- Monitor memory usage with multiple users

**Chart Display Problems**
- Verify Plotly installation: `pip install plotly>=5.10.0`
- Check browser compatibility (modern browsers recommended)
- Clear browser cache if charts don't display properly

**Missing Dependencies**
```bash
# Install missing packages
pip install streamlit plotly pandas numpy
```

### Deployment Options

**Local Development**
```bash
streamlit run app.py
```

**Production Deployment**
- **Streamlit Cloud**: Deploy directly from GitHub repository
- **Docker**: Containerize for consistent deployment
- **Cloud Platforms**: AWS, GCP, Azure with proper configuration

## Usage Examples

### Business Reviews
- **Monthly Business Reviews**: Compare YoY performance across all metrics
- **Category Analysis**: Identify top-performing product categories
- **Geographic Insights**: Understand regional performance patterns
- **Customer Experience**: Monitor satisfaction and delivery performance

### Strategic Planning
- **Trend Analysis**: Use historical comparisons for forecasting
- **Resource Allocation**: Focus on high-performing categories and regions
- **Operational Improvements**: Address delivery time and satisfaction issues
- **Growth Opportunities**: Identify underperforming areas for improvement

## Support and Maintenance

### Updates
- Dashboard automatically reflects data changes
- No restart required for new data (with caching refresh)
- Version control friendly for collaborative development

### Monitoring
- Built-in error handling and user feedback
- Performance monitoring through Streamlit metrics
- Data quality validation in loading functions

---

**Dashboard Version**: 1.0  
**Last Updated**: 2025  
**Framework**: Streamlit + Plotly  
**Dependencies**: See requirements.txt