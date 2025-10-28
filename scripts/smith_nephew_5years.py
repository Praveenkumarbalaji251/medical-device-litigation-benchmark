import requests
import pandas as pd
from datetime import datetime

BASE_URL = "https://api.fda.gov/device/event.json"

print("=" * 80)
print("SMITH & NEPHEW BIRMINGHAM HIP - LAST 5 YEARS DATA")
print("Fetching all MDR data from 2020-2025")
print("=" * 80)
print()

# Get all data for Birmingham Hip
params = {
    'search': 'device.brand_name:"Birmingham Hip"',
    'limit': 100,
    'skip': 0
}

all_records = []
page = 0

print("Fetching data from FDA API...")
while True:
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

# Process records into DataFrame
print("Processing records...")

rows = []
for record in all_records:
    # Extract key fields
    row = {
        'report_number': record.get('report_number', ''),
        'date_received': record.get('date_received', ''),
        'date_of_event': record.get('date_of_event', ''),
        'event_type': ', '.join(record.get('event_type', [])),
        'report_source_code': record.get('report_source_code', ''),
        'manufacturer_name': '',
        'brand_name': '',
        'generic_name': '',
        'device_problem': '',
        'patient_age': '',
        'patient_sex': '',
        'event_description': '',
        'manufacturer_narrative': ''
    }
    
    # Device info (can be multiple devices per report)
    devices = record.get('device', [])
    if devices:
        device = devices[0]  # Take first device
        row['manufacturer_name'] = device.get('manufacturer_d_name', '')
        row['brand_name'] = device.get('brand_name', '')
        row['generic_name'] = device.get('generic_name', '')
        
        # Device problems
        problems = device.get('device_event_key', [])
        row['device_problem'] = '; '.join(problems) if problems else ''
    
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
            if text_item.get('text_type_code') == 'Description of Event or Problem':
                row['event_description'] = text_item.get('text', '')
            elif text_item.get('text_type_code') == 'Manufacturer Narrative':
                row['manufacturer_narrative'] = text_item.get('text', '')
    
    rows.append(row)

# Create DataFrame
df = pd.DataFrame(rows)

# Filter to last 5 years (2020-2025)
df['date_received'] = pd.to_datetime(df['date_received'], format='%Y%m%d', errors='coerce')
df['date_of_event'] = pd.to_datetime(df['date_of_event'], format='%Y%m%d', errors='coerce')

# Filter 2020 onwards
df_filtered = df[df['date_received'] >= '2020-01-01'].copy()

print(f"Records from 2020-2025: {len(df_filtered)}")
print()

# Add year and month columns for analysis
df_filtered['year'] = df_filtered['date_received'].dt.year
df_filtered['month'] = df_filtered['date_received'].dt.month
df_filtered['year_month'] = df_filtered['date_received'].dt.strftime('%Y-%m')

# Sort by date
df_filtered = df_filtered.sort_values('date_received')

# Save to Excel
output_file = 'smith_nephew_bhr_5years.xlsx'

print("Saving to Excel...")
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    # Main data sheet
    df_filtered.to_excel(writer, sheet_name='All Reports', index=False)
    
    # Monthly summary
    monthly = df_filtered.groupby('year_month').agg({
        'report_number': 'count',
        'event_type': lambda x: ', '.join(x.value_counts().index[:3])  # Top 3 event types
    }).reset_index()
    monthly.columns = ['Year-Month', 'Report Count', 'Top Event Types']
    monthly.to_excel(writer, sheet_name='Monthly Summary', index=False)
    
    # Event type breakdown
    event_breakdown = df_filtered['event_type'].value_counts().reset_index()
    event_breakdown.columns = ['Event Type', 'Count']
    event_breakdown.to_excel(writer, sheet_name='Event Types', index=False)
    
    # Yearly summary
    yearly = df_filtered.groupby('year').agg({
        'report_number': 'count'
    }).reset_index()
    yearly.columns = ['Year', 'Report Count']
    yearly.to_excel(writer, sheet_name='Yearly Summary', index=False)
    
    # Device problems
    if df_filtered['device_problem'].notna().any():
        problems = df_filtered['device_problem'].value_counts().head(20).reset_index()
        problems.columns = ['Device Problem', 'Count']
        problems.to_excel(writer, sheet_name='Top Problems', index=False)

print()
print("=" * 80)
print("COMPLETE")
print("=" * 80)
print(f"✓ File saved: {output_file}")
print()
print("Sheets included:")
print("  1. All Reports - Complete data with all fields")
print("  2. Monthly Summary - Monthly report counts")
print("  3. Event Types - Breakdown by event type")
print("  4. Yearly Summary - Yearly totals")
print("  5. Top Problems - Most common device problems")
print()
print(f"Total records: {len(df_filtered)}")
print(f"Date range: {df_filtered['date_received'].min()} to {df_filtered['date_received'].max()}")
print()
