import pandas as pd

# Test data loading and cleaning
try:
    # Read the CSV, skipping the first 3 lines
    df = pd.read_csv('/home/user/Denker_Projects/FLOWS Previous Month.csv', skiprows=3)

    print(f"✓ Data loaded successfully")
    print(f"  Total rows: {len(df):,}")
    print(f"  Total columns: {len(df.columns)}")
    print(f"\n✓ Column names:")
    for col in df.columns:
        print(f"  - {col}")

    # Clean the Value column
    df['Value'] = df['Value'].astype(str).str.replace(',', '').str.replace(' ', '')
    df['Value'] = pd.to_numeric(df['Value'], errors='coerce')

    print(f"\n✓ Value column cleaned")
    print(f"  Min value: R {df['Value'].min():,.2f}")
    print(f"  Max value: R {df['Value'].max():,.2f}")
    print(f"  Total sum: R {df['Value'].sum():,.2f}")

    # Create flow type
    df['Flow_Type'] = df['Value'].apply(lambda x: 'Outflow' if x < 0 else 'Inflow')

    inflows = df[df['Flow_Type'] == 'Inflow']['Value'].sum()
    outflows = df[df['Flow_Type'] == 'Outflow']['Value'].sum()

    print(f"\n✓ Flow analysis:")
    print(f"  Total Inflows: R {inflows:,.2f}")
    print(f"  Total Outflows: R {outflows:,.2f}")
    print(f"  Net Flow: R {(inflows + outflows):,.2f}")

    # Convert dates
    df['Processing_Date'] = pd.to_datetime(df['Processing_Date'], errors='coerce')
    print(f"\n✓ Date conversion successful")
    print(f"  Date range: {df['Processing_Date'].min()} to {df['Processing_Date'].max()}")

    # Top 5 inflows
    print(f"\n✓ Top 5 Inflows:")
    top_inflows = df[df['Flow_Type'] == 'Inflow'].nlargest(5, 'Value')
    for idx, row in top_inflows.iterrows():
        print(f"  - R {row['Value']:,.2f} | {row['Entity_Name']} | {row['Transaction_type']}")

    # Top 5 outflows
    print(f"\n✓ Top 5 Outflows:")
    top_outflows = df[df['Flow_Type'] == 'Outflow'].nsmallest(5, 'Value')
    for idx, row in top_outflows.iterrows():
        print(f"  - R {row['Value']:,.2f} | {row['Entity_Name']} | {row['Transaction_type']}")

    print(f"\n✅ All tests passed! Dashboard should work correctly.")

except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
