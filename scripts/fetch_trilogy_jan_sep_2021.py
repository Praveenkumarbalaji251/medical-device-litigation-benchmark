#!/usr/bin/env python3
"""
Extract Respironics Trilogy MDRs from MAUDE
Date Range: January 2021 to September 2021
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
print("RESPIRONICS TRILOGY - MDR EXTRACTION")
print("Date Range: January 2021 to September 2021")
print("="*80)

base_url = "https://api.fda.gov/device/event.json"

# Search for Respironics Trilogy
# Try multiple search strategies
search_terms = [
    'device.brand_name:"TRILOGY"',
    'device.brand_name:"Trilogy"',
    'device.manufacturer_d_name:"RESPIRONICS"'
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
                    
                    # Get date received
                    date_received_str = record.get('date_received', '')
                    
                    # Only process records from Jan 2021 to Sep 2021
                    if date_received_str:
                        try:
                            date_received = pd.to_datetime(date_received_str, format='%Y%m%d')
                            
                            # Filter for Jan-Sep 2021
                            if not (pd.to_datetime('2021-01-01') <= date_received <= pd.to_datetime('2021-09-30')):
                                continue
                        except:
                            continue
                    else:
                        continue
                    
                    seen_report_numbers.add(report_number)
                    
                    # Extract device info
                    device_info = record.get('device', [{}])[0] if record.get('device') else {}
                    
                    # Check if it's actually Trilogy device
                    brand_name = device_info.get('brand_name', '')
                    if 'trilogy' not in str(brand_name).lower() and search_idx < 2:
                        continue
                    
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
                        'date_received': date_received_str,
                        'event_type': ', '.join(record.get('event_type', [])) if record.get('event_type') else '',
                        'report_source_code': record.get('report_source_code', ''),
                        'brand_name': clean_text(device_info.get('brand_name', '')),
                        'generic_name': clean_text(device_info.get('generic_name', '')),
                        'manufacturer_d_name': clean_text(device_info.get('manufacturer_d_name', '')),
                        'model_number': clean_text(device_info.get('model_number', '')),
                        'catalog_number': clean_text(device_info.get('catalog_number', '')),
                        'device_class': device_info.get('device_class', ''),
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
            
            print(f"New unique Trilogy records in date range: {new_records}")
            
            if batch_size < limit:
                print("Reached last page")
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
print(f"TOTAL UNIQUE TRILOGY RECORDS (Jan-Sep 2021): {len(all_records)}")
print("="*80)

if len(all_records) > 0:
    df = pd.DataFrame(all_records)
    
    # Convert dates
    df['date_received'] = pd.to_datetime(df['date_received'], format='%Y%m%d', errors='coerce')
    df = df.sort_values('date_received')
    
    print(f"\nDate range: {df['date_received'].min()} to {df['date_received'].max()}")
    print(f"Total records: {len(df)}")
    
    # Monthly breakdown
    df['year_month'] = df['date_received'].dt.to_period('M')
    monthly = df.groupby('year_month').size()
    
    print("\n" + "="*80)
    print("MONTHLY BREAKDOWN (Jan-Sep 2021)")
    print("="*80)
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep']
    for i in range(1, 10):
        period = pd.Period(f'2021-{i:02d}', freq='M')
        count = monthly.get(period, 0)
        print(f"{month_names[i-1]} 2021: {count} reports")
    
    # Brand names
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
    
    with pd.ExcelWriter('/Users/praveen/Praveen/respironics_trilogy_jan_sep_2021.xlsx', 
                        engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='All Reports', index=False)
        
        # Monthly summary
        monthly_df = monthly.reset_index()
        monthly_df.columns = ['Month', 'Count']
        monthly_df['Date'] = monthly_df['Month'].dt.to_timestamp()
        monthly_df.to_excel(writer, sheet_name='Monthly Summary', index=False)
        
        # Event types
        event_summary = df['event_type'].value_counts().reset_index()
        event_summary.columns = ['Event Type', 'Count']
        event_summary.to_excel(writer, sheet_name='Event Types', index=False)
    
    print("Excel saved: respironics_trilogy_jan_sep_2021.xlsx")
    print(f"Location: /Users/praveen/Praveen/")
    print("\n" + "="*80)
    print("EXTRACTION COMPLETE")
    print("="*80)
else:
    print("\nNo Trilogy records found in Jan-Sep 2021 date range!")
