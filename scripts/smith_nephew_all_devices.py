import requests
import pandas as pd
from datetime import datetime

BASE_URL = "https://api.fda.gov/device/event.json"

print("=" * 80)
print("SMITH & NEPHEW, INC - ALL DEVICES - LAST 5 YEARS")
print("Fetching all MDR data for manufacturer: SMITH & NEPHEW")
print("=" * 80)
print()

# Search by manufacturer name
params = {
    'search': 'manufacturer_name:"SMITH & NEPHEW"',
    'limit': 100,
    'skip': 0
}

all_records = []
page = 0

print("Fetching data from FDA API...")
while page < 100:  # Safety limit
    params['skip'] = page * 100
    
    try:
        response = requests.get(BASE_URL, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            
            if not results:
                break
            
            all_records.extend(results)
            page += 1
            print(f"  Fetched page {page}: {len(results)} records (total: {len(all_records)})")
            
            if len(results) < 100:
                break
        else:
            print(f"API Error: {response.status_code}")
            break
            
    except Exception as e:
        print(f"Error: {str(e)}")
        break

print()
print(f"Total records fetched: {len(all_records)}")
print()

# Process records
print("Processing records...")

rows = []
for record in all_records:
    row = {
        'report_number': record.get('report_number', ''),
        'date_received': record.get('date_received', ''),
        'date_of_event': record.get('date_of_event', ''),
        'event_type': ', '.join(record.get('event_type', [])),
        'report_source_code': record.get('report_source_code', ''),
        'manufacturer_name': '',
        'brand_name': '',
        'generic_name': '',
        'model_number': '',
        'catalog_number': '',
        'device_problem': '',
        'patient_age': '',
        'patient_sex': '',
        'event_description': '',
        'manufacturer_narrative': ''
    }
    
    # Device info
    devices = record.get('device', [])
    if devices:
        device = devices[0]
        row['manufacturer_name'] = device.get('manufacturer_d_name', '')
        row['brand_name'] = device.get('brand_name', '')
        row['generic_name'] = device.get('generic_name', '')
        row['model_number'] = device.get('model_number', '')
        row['catalog_number'] = device.get('catalog_number', '')
        
        problems = device.get('device_event_key', [])
        row['device_problem'] = '; '.join(problems[:5]) if problems else ''  # Limit to 5 problems
    
    # Patient info
    patient = record.get('patient', [])
    if patient:
        p = patient[0]
        row['patient_age'] = str(p.get('patient_age', ''))
        row['patient_sex'] = p.get('patient_sex', '')
    
    # MDR text
    mdr_text = record.get('mdr_text', [])
    if mdr_text:
        for text_item in mdr_text:
            text_type = text_item.get('text_type_code', '')
            text_content = text_item.get('text', '')
            if text_type and text_content:
                if 'Event' in text_type or 'Problem' in text_type:
                    row['event_description'] = text_content[:1000]  # Limit length
                elif 'Manufacturer' in text_type:
                    row['manufacturer_narrative'] = text_content[:1000]
    
    rows.append(row)

# Create DataFrame
df = pd.DataFrame(rows)

# Parse dates
df['date_received'] = pd.to_datetime(df['date_received'], format='%Y%m%d', errors='coerce')
df['date_of_event'] = pd.to_datetime(df['date_of_event'], format='%Y%m%d', errors='coerce')

# Filter to last 5 years (2020-2025)
df_filtered = df[df['date_received'] >= '2020-01-01'].copy()

print(f"Records from 2020-2025: {len(df_filtered)}")
print()

# Add analysis columns
df_filtered['year'] = df_filtered['date_received'].dt.year
df_filtered['month'] = df_filtered['date_received'].dt.month
df_filtered['year_month'] = df_filtered['date_received'].dt.strftime('%Y-%m')

# Sort by date
df_filtered = df_filtered.sort_values('date_received')

# Save to Excel
output_file = 'smith_nephew_all_devices_5years.xlsx'

print("Creating Excel file with multiple sheets...")
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    # All reports
    df_filtered.to_excel(writer, sheet_name='All Reports', index=False)
    
    # By device/brand
    brand_summary = df_filtered.groupby('brand_name').agg({
        'report_number': 'count',
        'event_type': lambda x: x.value_counts().index[0] if len(x) > 0 else ''
    }).reset_index()
    brand_summary.columns = ['Brand Name', 'Report Count', 'Most Common Event']
    brand_summary = brand_summary.sort_values('Report Count', ascending=False)
    brand_summary.to_excel(writer, sheet_name='By Device', index=False)
    
    # Monthly summary
    monthly = df_filtered.groupby('year_month').agg({
        'report_number': 'count'
    }).reset_index()
    monthly.columns = ['Year-Month', 'Report Count']
    monthly.to_excel(writer, sheet_name='Monthly Trend', index=False)
    
    # Event types
    event_breakdown = df_filtered['event_type'].value_counts().reset_index()
    event_breakdown.columns = ['Event Type', 'Count']
    event_breakdown.to_excel(writer, sheet_name='Event Types', index=False)
    
    # Yearly summary
    yearly = df_filtered.groupby('year').agg({
        'report_number': 'count'
    }).reset_index()
    yearly.columns = ['Year', 'Report Count']
    yearly.to_excel(writer, sheet_name='Yearly Summary', index=False)
    
    # Top problems
    problems_list = []
    for problems in df_filtered['device_problem'].dropna():
        if problems:
            problems_list.extend([p.strip() for p in problems.split(';') if p.strip()])
    
    if problems_list:
        problems_df = pd.Series(problems_list).value_counts().head(30).reset_index()
        problems_df.columns = ['Device Problem', 'Count']
        problems_df.to_excel(writer, sheet_name='Top Problems', index=False)

print()
print("=" * 80)
print("COMPLETE")
print("=" * 80)
print(f"✓ File saved: {output_file}")
print()
print("Sheets included:")
print("  1. All Reports - Complete data (all fields)")
print("  2. By Device - Summary by brand/device")
print("  3. Monthly Trend - Monthly report counts")
print("  4. Event Types - Breakdown by event type")
print("  5. Yearly Summary - Yearly totals")
print("  6. Top Problems - Most common device problems")
print()
print(f"Total records: {len(df_filtered)}")
print(f"Date range: {df_filtered['date_received'].min()} to {df_filtered['date_received'].max()}")
print(f"Unique devices: {df_filtered['brand_name'].nunique()}")
print()

# Show top devices
print("TOP 10 DEVICES BY REPORT COUNT:")
print("-" * 60)
top_devices = df_filtered['brand_name'].value_counts().head(10)
for device, count in top_devices.items():
    print(f"{device:40s}: {count:5d} reports")
print()
