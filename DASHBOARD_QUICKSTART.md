# 🚀 Dashboard Quick Start Guide

## Launch the Dashboard

```bash
# Navigate to project directory
cd lesson7_files

# Install dependencies (if not already done)
pip install -r requirements.txt

# Launch the Streamlit dashboard
streamlit run app.py
```

The dashboard will automatically open in your browser at `http://localhost:8501`

## Dashboard Overview

### 📊 **Layout Structure**
```
┌─────────────────────────────────────────────────────┐
│ Header: E-commerce Business Dashboard    [Filters]  │
├─────────────────────────────────────────────────────┤
│ KPI Cards: Revenue | Monthly | AOV | Orders        │
├─────────────────────────────────────────────────────┤
│ Charts Grid:                                        │
│ ┌─────────────────┬─────────────────┐               │
│ │ Revenue Trend   │ Top Categories  │               │
│ └─────────────────┴─────────────────┘               │
│ ┌─────────────────┬─────────────────┐               │
│ │ Revenue by State│ Satisfaction    │               │
│ └─────────────────┴─────────────────┘               │
├─────────────────────────────────────────────────────┤
│ Bottom Cards: Delivery Time | Review Score         │
└─────────────────────────────────────────────────────┘
```

### 🎛️ **Controls**
- **Analysis Year**: Primary year for current metrics (defaults to 2023)
- **Comparison Year**: Previous year for trend calculations (defaults to 2022)
- **Filter by Months**: Select specific months or "All Months" for full year analysis

### 📈 **Key Features**
- **Real-time Filtering**: All charts update when you change years or months
- **Trend Indicators**: Green ↑ for positive, Red ↓ for negative trends
- **Professional Styling**: Clean business-oriented design with integrated chart titles
- **Interactive Charts**: Hover for detailed information
- **Smart Defaults**: Automatically selects 2023 vs 2022 comparison

## Troubleshooting

**Dashboard won't start?**
```bash
pip install streamlit plotly pandas numpy
```

**No data showing?**
- Verify `ecommerce_data/` folder contains all CSV files
- Check that data has multiple years available

**Charts not loading?**
- Refresh the browser page
- Check browser console for errors