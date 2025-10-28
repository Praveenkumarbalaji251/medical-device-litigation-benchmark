#!/usr/bin/env python3
"""
Fetch ALL Allergan BIOCELL Textured Breast Implant MDR Reports
MDL No. 2921 - Filed December 18, 2019 (JPML Transfer Order)
"""

import requests
import pandas as pd
import time
import re
from datetime import datetime

def clean_text(text):
    """Remove illegal characters for Excel"""
    if pd.isna(text) or text is None:
        return ""
    text = str(text)
    text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F-\x9F]', '', text)
    return text

print("="*80)
print("FETCHING ALLERGAN BIOCELL BREAST IMPLANT MDR REPORTS")
print("MDL No. 2921 - Transfer Order: December 18, 2019")
print("="*80)

base_url = "https://api.fda.gov/device/event.json"

# Multiple search terms for Allergan BIOCELL
search_terms = [
    'device.brand_name:"BIOCELL"',
    'device.brand_name:"Allergan" AND device.generic_name:"breast implant"',
    'device.manufacturer_d_name:"Allergan" AND device.generic_name:"implant, breast, silicone"'
]

all_records = []
seen_report_numbers = set()

for search_idx, search_query in enumerate(search_terms):
    print(f"\n{'='*80}")
    print(f"SEARCH {search_idx + 1}/{len(search_terms)}: {search_query}")
    print("="*80)
    
    skip = 0
    limit = 100
    page = 1
    
    while True:
        print(f"Fetching page {page} (skip={skip})...")
        
        params = {
            'search': search_query,
            'limit': limit,
            'skip': skip
        }
        
        try:
            response = requests.get(base_url, params=params)
            
            if response.status_code != 200:
                print(f"Error: Status code {response.status_code}")
                break
            
            data = response.json()
            
            if 'results' not in data or len(data['results']) == 0:
                print("No more results")
                break
            
            batch_size = len(data['results'])
            print(f"Retrieved {batch_size} records")
            
            new_records = 0
            for record in data['results']:
                try:
                    report_number = record.get('report_number', '')
                    
                    # Skip duplicates
                    if report_number in seen_report_numbers:
                        continue
                    
                    seen_report_numbers.add(report_number)
                    
                    # Extract device info
                    device_info = record.get('device', [{}])[0] if record.get('device') else {}
                    
                    # Extract patient info
                    patient_info = record.get('patient', [{}])[0] if record.get('patient') else {}
                    
                    # Extract event info
                    mdr_text = record.get('mdr_text', [{}])
                    event_description = ""
                    manufacturer_narrative = ""
                    
                    for text_entry in mdr_text:
                        if text_entry.get('text_type_code') == 'Description of Event or Problem':
                            event_description = clean_text(text_entry.get('text', ''))
                        elif text_entry.get('text_type_code') == 'Manufacturer Narrative':
                            manufacturer_narrative = clean_text(text_entry.get('text', ''))
                    
                    parsed_record = {
                        'report_number': report_number,
                        'date_received': record.get('date_received', ''),
                        'event_type': ', '.join(record.get('event_type', [])) if record.get('event_type') else '',
                        'report_source_code': record.get('report_source_code', ''),
                        'device_date_of_manufacturer': device_info.get('device_date_of_manufacturer', ''),
                        'brand_name': clean_text(device_info.get('brand_name', '')),
                        'generic_name': clean_text(device_info.get('generic_name', '')),
                        'manufacturer_d_name': clean_text(device_info.get('manufacturer_d_name', '')),
                        'model_number': clean_text(device_info.get('model_number', '')),
                        'catalog_number': clean_text(device_info.get('catalog_number', '')),
                        'device_class': device_info.get('device_class', ''),
                        'device_operator': device_info.get('device_operator', ''),
                        'patient_sequence_number': patient_info.get('sequence_number_outcome', ''),
                        'patient_sequence_treatment': patient_info.get('sequence_number_treatment', ''),
                        'event_description': event_description[:32000],
                        'manufacturer_narrative': manufacturer_narrative[:32000],
                        'adverse_event_flag': record.get('adverse_event_flag', ''),
                        'product_problem_flag': record.get('product_problem_flag', ''),
                        'date_of_event': record.get('date_of_event', ''),
                        'search_term': search_query
                    }
                    
                    all_records.append(parsed_record)
                    new_records += 1
                    
                except Exception as e:
                    print(f"Error parsing record: {e}")
                    continue
            
            print(f"New unique records: {new_records}")
            
            if batch_size < limit:
                print("Reached last page for this search")
                break
            
            skip += limit
            page += 1
            time.sleep(0.5)
            
            if page > 200:
                print("Safety limit reached")
                break
                
        except Exception as e:
            print(f"Error fetching data: {e}")
            break

print("\n" + "="*80)
print(f"TOTAL UNIQUE RECORDS FETCHED: {len(all_records)}")
print("="*80)

if len(all_records) == 0:
    print("No records found! Trying alternative search...")
    
    # Try simpler search
    search_query = 'device.generic_name:"breast implant"'
    print(f"\nAlternative search: {search_query}")
    
    params = {
        'search': search_query,
        'limit': 100
    }
    
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        print(f"Found {len(data.get('results', []))} breast implant records")
        print("Note: You may need to filter for Allergan/BIOCELL specifically")
else:
    # Create DataFrame
    df = pd.DataFrame(all_records)
    
    # Convert dates
    df['date_received'] = pd.to_datetime(df['date_received'], format='%Y%m%d', errors='coerce')
    df = df.sort_values('date_received')
    
    print(f"\nDate range: {df['date_received'].min()} to {df['date_received'].max()}")
    print(f"Total records: {len(df)}")
    
    # MDL filing date
    mdl_date = pd.to_datetime('2019-12-18')
    df['period'] = df['date_received'].apply(lambda x: 'Before MDL' if x < mdl_date else 'After MDL')
    
    before_count = len(df[df['period'] == 'Before MDL'])
    after_count = len(df[df['period'] == 'After MDL'])
    
    # Yearly breakdown
    df['year'] = df['date_received'].dt.year
    yearly_counts = df['year'].value_counts().sort_index()
    
    print("\n" + "="*80)
    print("YEARLY BREAKDOWN")
    print("="*80)
    for year, count in yearly_counts.items():
        if pd.notna(year):
            print(f"{int(year)}: {count} reports")
    
    print("\n" + "="*80)
    print("BEFORE vs AFTER MDL (December 18, 2019)")
    print("="*80)
    print(f"Before MDL: {before_count} reports")
    print(f"After MDL: {after_count} reports")
    
    if before_count > 0:
        ratio = after_count / before_count
        print(f"Ratio (After/Before): {ratio:.2f}x")
    
    # 6-month windows
    six_months_before = mdl_date - pd.DateOffset(months=6)
    six_months_after = mdl_date + pd.DateOffset(months=6)
    
    critical_before = df[(df['date_received'] >= six_months_before) & (df['date_received'] < mdl_date)]
    critical_after = df[(df['date_received'] >= mdl_date) & (df['date_received'] <= six_months_after)]
    
    print("\n" + "="*80)
    print("6-MONTH WINDOWS")
    print("="*80)
    print(f"6 months BEFORE MDL (Jun-Dec 2019): {len(critical_before)} reports")
    print(f"6 months AFTER MDL (Dec 2019-Jun 2020): {len(critical_after)} reports")
    
    # Monthly aggregation
    df['year_month'] = df['date_received'].dt.to_period('M')
    monthly_summary = df.groupby('year_month').size().reset_index(name='count')
    monthly_summary['date'] = monthly_summary['year_month'].dt.to_timestamp()
    
    # Event types
    print("\n" + "="*80)
    print("TOP EVENT TYPES")
    print("="*80)
    event_types = df['event_type'].value_counts().head(10)
    for event, count in event_types.items():
        print(f"{event}: {count}")
    
    # Brand names found
    print("\n" + "="*80)
    print("BRAND NAMES FOUND")
    print("="*80)
    brands = df['brand_name'].value_counts().head(10)
    for brand, count in brands.items():
        if brand:
            print(f"{brand}: {count}")
    
    # Save to Excel
    print("\n" + "="*80)
    print("SAVING TO EXCEL")
    print("="*80)
    
    with pd.ExcelWriter('allergan_biocell_all_mdr_reports.xlsx', engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='All Reports', index=False)
        monthly_summary.to_excel(writer, sheet_name='Monthly Summary', index=False)
        yearly_counts.reset_index().rename(columns={'index': 'Year', 'year': 'Count'}).to_excel(writer, sheet_name='Yearly Summary', index=False)
        
        event_summary = df['event_type'].value_counts().reset_index()
        event_summary.columns = ['Event Type', 'Count']
        event_summary.to_excel(writer, sheet_name='Event Types', index=False)
        
        period_summary = df.groupby('period').size().reset_index(name='count')
        period_summary.to_excel(writer, sheet_name='Before After MDL', index=False)
        
        # Brand breakdown
        brand_summary = df['brand_name'].value_counts().reset_index()
        brand_summary.columns = ['Brand Name', 'Count']
        brand_summary.to_excel(writer, sheet_name='Brand Names', index=False)
    
    print("Excel file saved: allergan_biocell_all_mdr_reports.xlsx")
    
    # Show sample descriptions
    print("\n" + "="*80)
    print("SAMPLE EVENT DESCRIPTIONS (first 3)")
    print("="*80)
    for idx, row in df.head(3).iterrows():
        print(f"\nReport {row['report_number']} ({row['date_received'].strftime('%Y-%m-%d') if pd.notna(row['date_received']) else 'N/A'}):")
        print(f"Brand: {row['brand_name']}")
        desc = row['event_description'][:300] if row['event_description'] else "No description"
        print(f"Description: {desc}...")
    
    print("\n" + "="*80)
    print("COMPLETE - All Allergan BIOCELL MDR reports saved")
    print("="*80)
