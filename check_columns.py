import pandas as pd

print("Loading CSV...")
df = pd.read_csv(r'C:\Users\G1020065\Documents\Coding\AUM_and_Flows\FLOWS Previous Month.csv', skiprows=3)
print("\nColumn names:")
for col in df.columns:
    print(f"  - {col}")
print(f"\nTotal columns: {len(df.columns)}")
print(f"Total rows: {len(df)}")