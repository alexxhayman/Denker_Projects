# Cash Flow Dashboard

An interactive dashboard for analyzing cash flow data from "FLOWS Previous Month.csv".

## Features

### 📊 Overview Tab
- **Key Metrics**: Total Inflows, Outflows, Net Cash Flow, and Transaction Count
- **Pie Chart**: Visual distribution of inflows vs outflows
- **Transaction Types**: Bar chart showing top transaction types by value
- **Daily Trend**: Line chart tracking daily cash flow patterns
- **Fund Analysis**: Top 10 funds by total flow

### 📈 Top Inflows Tab
- Top 50 largest inflow transactions with detailed information
- Visual bar chart of top 20 inflows
- Transaction type breakdown for inflows
- Pie chart showing inflow distribution by type

### 📉 Top Outflows Tab
- Top 50 largest outflow transactions with detailed information
- Visual bar chart of top 20 outflows
- Transaction type breakdown for outflows
- Pie chart showing outflow distribution by type

### 🔍 Details Tab
- Interactive filters for Fund, Flow Type, and Transaction Type
- Detailed transaction table (top 100 by value)
- Summary statistics (Total, Average, Median)

### Sidebar Information
- Report period and date range
- Quick stats: Unique clients, funds, and agents
- Client type breakdown with values

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Dashboard

Run the following command in your terminal:

```bash
streamlit run cash_flow_dashboard.py
```

The dashboard will open automatically in your default web browser at `http://localhost:8501`

## Data Requirements

The dashboard expects a CSV file named "FLOWS Previous Month.csv" in the same directory with the following columns:
- Product_Owner_Name
- Client_Type
- Fund_Family
- Fund_Name
- Entity_Name
- Transaction_type
- Processing_Date
- Price_Date
- Units
- Value
- Agent_Name
- And other related columns

## Data Cleaning

The dashboard automatically:
- Removes the first 3 header rows
- Cleans numeric values (removes commas, handles negative values)
- Converts dates to proper format
- Categorizes transactions as Inflows (positive) or Outflows (negative)

## Key Insights Provided

1. **Total Financial Position**: See overall inflows, outflows, and net position
2. **Transaction Patterns**: Understand which transaction types drive the most value
3. **Daily Trends**: Track how cash flows change over time
4. **Top Performers**: Identify largest individual transactions
5. **Fund Performance**: Compare performance across different funds
6. **Agent Analysis**: See which agents handle the most volume

## Notes

- All monetary values are displayed in Rands (R)
- Negative values indicate outflows (redemptions, fees, etc.)
- Positive values indicate inflows (purchases, investments, etc.)
- The dashboard uses caching for better performance
