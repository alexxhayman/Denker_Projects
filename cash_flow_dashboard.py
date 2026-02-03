import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Cash Flow Dashboard",
    page_icon="💰",
    layout="wide"
)

@st.cache_data
def load_and_clean_data(file_path):
    """Load and clean the CSV data"""
    # Read the CSV, skipping the first 3 lines (filter parameters and empty line)
    df = pd.read_csv(file_path, skiprows=3)

    # Clean the Value column - remove commas and convert to float
    df['Value'] = df['Value'].astype(str).str.replace(',', '').str.replace(' ', '')
    df['Value'] = pd.to_numeric(df['Value'], errors='coerce')

    # Clean the Units column
    df['Units'] = df['Units'].astype(str).str.replace(',', '').str.replace(' ', '')
    df['Units'] = pd.to_numeric(df['Units'], errors='coerce')

    # Convert date columns
    df['Processing_Date'] = pd.to_datetime(df['Processing_Date'], errors='coerce')
    df['Price_Date'] = pd.to_datetime(df['Price_Date'], errors='coerce')

    # Create flow type column
    df['Flow_Type'] = df['Value'].apply(lambda x: 'Outflow' if x < 0 else 'Inflow')

    # Create absolute value column for easier sorting
    df['Abs_Value'] = df['Value'].abs()

    return df

# Load data
try:
    df = load_and_clean_data('/home/user/Denker_Projects/FLOWS Previous Month.csv')

    # Dashboard Title
    st.title("💰 Cash Flow Dashboard - January 2026")
    st.markdown("---")

    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)

    total_inflows = df[df['Flow_Type'] == 'Inflow']['Value'].sum()
    total_outflows = df[df['Flow_Type'] == 'Outflow']['Value'].sum()
    net_flow = total_inflows + total_outflows
    total_transactions = len(df)

    with col1:
        st.metric("Total Inflows", f"R {total_inflows:,.2f}")
    with col2:
        st.metric("Total Outflows", f"R {total_outflows:,.2f}")
    with col3:
        st.metric("Net Cash Flow", f"R {net_flow:,.2f}",
                 delta=f"{(net_flow/total_inflows*100):.1f}%" if total_inflows > 0 else "N/A")
    with col4:
        st.metric("Total Transactions", f"{total_transactions:,}")

    st.markdown("---")

    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Top Inflows", "📉 Top Outflows", "🔍 Details"])

    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            # Inflows vs Outflows Pie Chart
            flow_summary = df.groupby('Flow_Type')['Abs_Value'].sum().reset_index()
            fig_pie = px.pie(
                flow_summary,
                values='Abs_Value',
                names='Flow_Type',
                title='Inflows vs Outflows Distribution',
                color='Flow_Type',
                color_discrete_map={'Inflow': '#2ecc71', 'Outflow': '#e74c3c'}
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)

        with col2:
            # Transaction Type Breakdown
            transaction_summary = df.groupby('Transaction_type')['Value'].agg(['sum', 'count']).reset_index()
            transaction_summary.columns = ['Transaction Type', 'Total Value', 'Count']
            transaction_summary = transaction_summary.sort_values('Total Value', ascending=True).tail(10)

            fig_bar = px.bar(
                transaction_summary,
                x='Total Value',
                y='Transaction Type',
                orientation='h',
                title='Top 10 Transaction Types by Value',
                color='Total Value',
                color_continuous_scale='RdYlGn'
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        # Daily Flow Trend
        daily_flow = df.groupby([df['Processing_Date'].dt.date, 'Flow_Type'])['Value'].sum().reset_index()
        daily_flow.columns = ['Date', 'Flow_Type', 'Value']

        fig_line = px.line(
            daily_flow,
            x='Date',
            y='Value',
            color='Flow_Type',
            title='Daily Cash Flow Trend',
            color_discrete_map={'Inflow': '#2ecc71', 'Outflow': '#e74c3c'}
        )
        fig_line.update_layout(hovermode='x unified')
        st.plotly_chart(fig_line, use_container_width=True)

        # Fund Family Breakdown
        fund_summary = df.groupby('Fund_Family')['Value'].sum().reset_index()
        fund_summary = fund_summary.sort_values('Value', ascending=False).head(10)

        fig_fund = px.bar(
            fund_summary,
            x='Fund_Family',
            y='Value',
            title='Top 10 Funds by Total Flow',
            color='Value',
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig_fund, use_container_width=True)

    with tab2:
        st.subheader("🏆 Top 50 Biggest Inflows")

        top_inflows = df[df['Flow_Type'] == 'Inflow'].nlargest(50, 'Value')[
            ['Processing_Date', 'Client_Name_Selected', 'Entity_Name', 'Fund_Name',
             'Transaction_type', 'Value', 'Units', 'Agent_Name']
        ].copy()

        top_inflows['Processing_Date'] = top_inflows['Processing_Date'].dt.strftime('%Y-%m-%d')
        top_inflows['Value'] = top_inflows['Value'].apply(lambda x: f"R {x:,.2f}")
        top_inflows['Units'] = top_inflows['Units'].apply(lambda x: f"{x:,.4f}" if pd.notna(x) else "")

        st.dataframe(top_inflows, use_container_width=True, hide_index=True)

        # Visualize top 20 inflows
        top_20_inflows = df[df['Flow_Type'] == 'Inflow'].nlargest(20, 'Value')
        fig = px.bar(
            top_20_inflows,
            x='Value',
            y='Entity_Name',
            orientation='h',
            title='Top 20 Largest Inflows',
            color='Value',
            color_continuous_scale='Greens',
            hover_data=['Fund_Name', 'Transaction_type']
        )
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)

        # Transaction type breakdown for inflows
        inflow_by_type = df[df['Flow_Type'] == 'Inflow'].groupby('Transaction_type')['Value'].agg(['sum', 'count']).reset_index()
        inflow_by_type.columns = ['Transaction Type', 'Total Value', 'Count']
        inflow_by_type = inflow_by_type.sort_values('Total Value', ascending=False)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Inflows by Transaction Type")
            st.dataframe(
                inflow_by_type.style.format({
                    'Total Value': 'R {:,.2f}',
                    'Count': '{:,}'
                }),
                use_container_width=True,
                hide_index=True
            )

        with col2:
            fig_inflow_type = px.pie(
                inflow_by_type,
                values='Total Value',
                names='Transaction Type',
                title='Inflow Distribution by Type'
            )
            st.plotly_chart(fig_inflow_type, use_container_width=True)

    with tab3:
        st.subheader("📉 Top 50 Biggest Outflows")

        top_outflows = df[df['Flow_Type'] == 'Outflow'].nsmallest(50, 'Value')[
            ['Processing_Date', 'Client_Name_Selected', 'Entity_Name', 'Fund_Name',
             'Transaction_type', 'Value', 'Units', 'Agent_Name']
        ].copy()

        top_outflows['Processing_Date'] = top_outflows['Processing_Date'].dt.strftime('%Y-%m-%d')
        top_outflows['Value'] = top_outflows['Value'].apply(lambda x: f"R {x:,.2f}")
        top_outflows['Units'] = top_outflows['Units'].apply(lambda x: f"{x:,.4f}" if pd.notna(x) else "")

        st.dataframe(top_outflows, use_container_width=True, hide_index=True)

        # Visualize top 20 outflows
        top_20_outflows = df[df['Flow_Type'] == 'Outflow'].nsmallest(20, 'Value')
        fig = px.bar(
            top_20_outflows,
            x='Value',
            y='Entity_Name',
            orientation='h',
            title='Top 20 Largest Outflows',
            color='Value',
            color_continuous_scale='Reds',
            hover_data=['Fund_Name', 'Transaction_type']
        )
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)

        # Transaction type breakdown for outflows
        outflow_by_type = df[df['Flow_Type'] == 'Outflow'].groupby('Transaction_type')['Value'].agg(['sum', 'count']).reset_index()
        outflow_by_type.columns = ['Transaction Type', 'Total Value', 'Count']
        outflow_by_type = outflow_by_type.sort_values('Total Value', ascending=True)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Outflows by Transaction Type")
            st.dataframe(
                outflow_by_type.style.format({
                    'Total Value': 'R {:,.2f}',
                    'Count': '{:,}'
                }),
                use_container_width=True,
                hide_index=True
            )

        with col2:
            fig_outflow_type = px.pie(
                outflow_by_type,
                values='Total Value',
                names='Transaction Type',
                title='Outflow Distribution by Type'
            )
            st.plotly_chart(fig_outflow_type, use_container_width=True)

    with tab4:
        st.subheader("🔍 Detailed Analysis")

        # Filters
        col1, col2, col3 = st.columns(3)

        with col1:
            fund_filter = st.multiselect(
                "Filter by Fund",
                options=sorted(df['Fund_Name'].unique()),
                default=[]
            )

        with col2:
            flow_filter = st.multiselect(
                "Filter by Flow Type",
                options=['Inflow', 'Outflow'],
                default=['Inflow', 'Outflow']
            )

        with col3:
            transaction_filter = st.multiselect(
                "Filter by Transaction Type",
                options=sorted(df['Transaction_type'].unique()),
                default=[]
            )

        # Apply filters
        filtered_df = df.copy()
        if fund_filter:
            filtered_df = filtered_df[filtered_df['Fund_Name'].isin(fund_filter)]
        if flow_filter:
            filtered_df = filtered_df[filtered_df['Flow_Type'].isin(flow_filter)]
        if transaction_filter:
            filtered_df = filtered_df[filtered_df['Transaction_type'].isin(transaction_filter)]

        st.write(f"Showing {len(filtered_df):,} transactions")

        # Display filtered data
        display_df = filtered_df[
            ['Processing_Date', 'Entity_Name', 'Fund_Name', 'Transaction_type',
             'Value', 'Units', 'Flow_Type', 'Agent_Name', 'Client_Type']
        ].sort_values('Abs_Value', ascending=False).head(100)

        display_df['Processing_Date'] = display_df['Processing_Date'].dt.strftime('%Y-%m-%d')

        st.dataframe(display_df, use_container_width=True, hide_index=True)

        # Summary statistics
        st.subheader("Summary Statistics")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Filtered Total", f"R {filtered_df['Value'].sum():,.2f}")
        with col2:
            st.metric("Average Transaction", f"R {filtered_df['Value'].mean():,.2f}")
        with col3:
            st.metric("Median Transaction", f"R {filtered_df['Value'].median():,.2f}")

    # Sidebar with additional info
    with st.sidebar:
        st.header("📋 Report Information")
        st.write(f"**Period:** January 2026")
        st.write(f"**Total Transactions:** {len(df):,}")
        st.write(f"**Date Range:** {df['Processing_Date'].min().strftime('%Y-%m-%d')} to {df['Processing_Date'].max().strftime('%Y-%m-%d')}")

        st.markdown("---")
        st.subheader("Quick Stats")
        st.write(f"**Unique Clients:** {df['Entity_Name'].nunique():,}")
        st.write(f"**Unique Funds:** {df['Fund_Name'].nunique()}")
        st.write(f"**Unique Agents:** {df['Agent_Name'].nunique():,}")

        st.markdown("---")
        st.subheader("Client Type Breakdown")
        client_type_summary = df.groupby('Client_Type')['Value'].sum().sort_values(ascending=False)
        for client_type, value in client_type_summary.items():
            st.write(f"**{client_type}:** R {value:,.2f}")

except FileNotFoundError:
    st.error("❌ CSV file not found! Please ensure 'FLOWS Previous Month.csv' is in the correct directory.")
except Exception as e:
    st.error(f"❌ An error occurred: {str(e)}")
    st.write("Please check your data file and try again.")
