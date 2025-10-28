import pandas as pd

print("=" * 80)
print("SMITH & NEPHEW BHR - EXCEL FILE PREVIEW")
print("=" * 80)
print()

# Read the Excel file
file = 'smith_nephew_bhr_5years.xlsx'

# Yearly Summary
print("YEARLY SUMMARY:")
print("-" * 60)
df_yearly = pd.read_excel(file, sheet_name='Yearly Summary')
print(df_yearly.to_string(index=False))
print()

# Monthly Summary (last 12 months)
print("MONTHLY SUMMARY (Last 12 months):")
print("-" * 60)
df_monthly = pd.read_excel(file, sheet_name='Monthly Summary')
print(df_monthly.tail(12).to_string(index=False))
print()

# Event Types
print("EVENT TYPE BREAKDOWN:")
print("-" * 60)
df_events = pd.read_excel(file, sheet_name='Event Types')
print(df_events.to_string(index=False))
print()

# Top Problems
print("TOP 10 DEVICE PROBLEMS:")
print("-" * 60)
df_problems = pd.read_excel(file, sheet_name='Top Problems')
print(df_problems.head(10).to_string(index=False))
print()

# Sample records
print("SAMPLE RECORDS (First 3):")
print("-" * 60)
df_all = pd.read_excel(file, sheet_name='All Reports')
print(f"Total columns: {len(df_all.columns)}")
print(f"Columns: {', '.join(df_all.columns.tolist())}")
print()
print(df_all.head(3)[['report_number', 'date_received', 'event_type', 'brand_name']].to_string(index=False))
print()

print("=" * 80)
print(f"✓ Excel file: {file}")
print(f"✓ Total records: {len(df_all)}")
print(f"✓ Date range: 2020-2025")
print("=" * 80)
