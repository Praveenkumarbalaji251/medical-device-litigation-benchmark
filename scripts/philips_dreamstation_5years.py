import requests
import pandas as pd
from datetime import datetime
import time

BASE_URL = "https://api.fda.gov/device/event.json"

print("=" * 80)
print("PHILIPS DREAMSTATION - 5 YEAR DATA EXTRACTION")
print("Case Filed: July 1, 2021")
print("Fetching all MDR data from 2020-2025")
print("=" * 80)
print()

# Fetch DreamStation data
params = {
    'search': 'device.brand_name:"DreamStation"',
    'limit': 100,
    'skip': 0
}

all_records = []
page = 0

print("Fetching data from FDA API...")
while page < 200:  # Safety limit
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
            print(f"  Page {page}: {len(results)} records (total: {len(all_records):,})")
            
            if len(results) < 100:
                break
                
            time.sleep(0.2)  # Rate limiting
        else:
            print(f"  API Error: {response.status_code}")
            break
            
    except Exception as e:
        print(f"  Error: {str(e)}")
        break

print()
print(f"Total records fetched: {len(all_records):,}")
print()

if not all_records:
    print("No data retrieved. Exiting.")
    exit()

# Process records
print("Processing records...")

def clean_text(text):
    """Remove illegal Excel characters"""
    if not text:
        return text
    import re
    text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F-\x9F]', '', str(text))
    return text

rows = []
for record in all_records:
    row = {
        'device_name': 'Philips DreamStation',
        'report_number': record.get('report_number', ''),
        'date_received': record.get('date_received', ''),
        'date_of_event': record.get('date_of_event', ''),
        'event_type': ', '.join(record.get('event_type', [])),
        'report_source_code': record.get('report_source_code', ''),
        'manufacturer_name': '',
        'brand_name': '',
        'generic_name': '',
        'model_number': '',
        'product_code': '',
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
        row['product_code'] = device.get('openfda', {}).get('device_class', [''])[0] if device.get('openfda') else ''
        
        problems = device.get('device_event_key', [])
        row['device_problem'] = '; '.join(problems[:5]) if problems else ''
    
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
            
            if text_content:
                if 'Event' in text_type or 'Problem' in text_type:
                    row['event_description'] = clean_text(text_content[:2000])
                elif 'Manufacturer' in text_type:
                    row['manufacturer_narrative'] = clean_text(text_content[:2000])
    
    rows.append(row)

# Create DataFrame
df = pd.DataFrame(rows)

# Parse dates
df['date_received'] = pd.to_datetime(df['date_received'], format='%Y%m%d', errors='coerce')
df['date_of_event'] = pd.to_datetime(df['date_of_event'], format='%Y%m%d', errors='coerce')

# Filter to 2020-2025
df_filtered = df[df['date_received'] >= '2020-01-01'].copy()

print(f"Records from 2020-2025: {len(df_filtered):,}")
print()

# Add analysis columns
df_filtered['year'] = df_filtered['date_received'].dt.year
df_filtered['month'] = df_filtered['date_received'].dt.month
df_filtered['year_month'] = df_filtered['date_received'].dt.strftime('%Y-%m')

# Sort by date
df_filtered = df_filtered.sort_values('date_received')

# Save to Excel
output_file = 'philips_dreamstation_5years.xlsx'

print("Creating Excel file...")
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    # All reports
    df_filtered.to_excel(writer, sheet_name='All Reports', index=False)
    
    # Monthly summary
    monthly = df_filtered.groupby('year_month').agg({
        'report_number': 'count',
        'event_type': lambda x: ', '.join(x.value_counts().head(2).index.tolist())
    }).reset_index()
    monthly.columns = ['Year-Month', 'Report Count', 'Top Event Types']
    monthly.to_excel(writer, sheet_name='Monthly Summary', index=False)
    
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
    
    # Device problems
    problems_list = []
    for idx, row in df_filtered.iterrows():
        if pd.notna(row['device_problem']) and row['device_problem']:
            for problem in row['device_problem'].split(';'):
                problem = problem.strip()
                if problem:
                    problems_list.append(problem)
    
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
print("  2. Monthly Summary - Monthly report counts")
print("  3. Event Types - Breakdown by event type")
print("  4. Yearly Summary - Yearly totals")
print("  5. Top Problems - Most common device problems")
print()

# Summary stats
deaths = df_filtered[df_filtered['event_type'].str.contains('Death', na=False)]
injuries = df_filtered[df_filtered['event_type'].str.contains('Injury', na=False)]
malfunctions = df_filtered[df_filtered['event_type'].str.contains('Malfunction', na=False)]

print(f"Total records (2020-2025): {len(df_filtered):,}")
print(f"Deaths: {len(deaths):,}")
print(f"Injuries: {len(injuries):,}")
print(f"Malfunctions: {len(malfunctions):,}")
print(f"Date range: {df_filtered['date_received'].min()} to {df_filtered['date_received'].max()}")
print()

# Case filing info
case_date = pd.to_datetime('2021-07-01')
recall_date = pd.to_datetime('2021-06-14')

before_filing = df_filtered[df_filtered['date_received'] < case_date]
after_filing = df_filtered[df_filtered['date_received'] >= case_date]

print("=" * 80)
print("LITIGATION TIMELINE")
print("=" * 80)
print(f"Recall Date: June 14, 2021")
print(f"Case Filed: July 1, 2021")
print()
print(f"Reports BEFORE filing: {len(before_filing):,}")
print(f"Reports AFTER filing: {len(after_filing):,}")
print()

# 6 month before
six_months_before = df_filtered[(df_filtered['date_received'] >= case_date - pd.DateOffset(months=6)) & 
                                (df_filtered['date_received'] < case_date)]
print(f"6 months BEFORE filing: {len(six_months_before):,} reports")

# Month by month before filing (Jan-Jun 2021)
print()
print("MONTH-BY-MONTH BEFORE FILING:")
print("-" * 60)
for month in range(1, 7):
    month_df = df_filtered[(df_filtered['date_received'].dt.year == 2021) & 
                           (df_filtered['date_received'].dt.month == month)]
    month_name = pd.to_datetime(f'2021-{month:02d}-01').strftime('%B')
    print(f"{month_name:12s}: {len(month_df):4d} reports")

print()
print("=" * 80)
