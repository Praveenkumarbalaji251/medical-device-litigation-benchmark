#!/usr/bin/env python3
"""
Fetch ALL Paragard IUD MDR Reports from FDA MAUDE Database
Pull complete detailed records, not just counts
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
    # Remove control characters that Excel doesn't like
    text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F-\x9F]', '', text)
    return text

print("="*80)
print("FETCHING ALL PARAGARD IUD MDR REPORTS FROM FDA MAUDE")
print("="*80)

base_url = "https://api.fda.gov/device/event.json"

# Search terms for Paragard
search_query = 'device.brand_name:"Paragard"'

all_records = []
skip = 0
limit = 100  # FDA API max per request

print(f"\nSearch query: {search_query}")
print("Fetching data in batches of 100...")

# Fetch all pages
page = 1
while True:
    print(f"\nFetching page {page} (skip={skip})...")
    
    params = {
        'search': search_query,
        'limit': limit,
        'skip': skip
    }
    
    try:
        response = requests.get(base_url, params=params)
        
        if response.status_code != 200:
            print(f"Error: Status code {response.status_code}")
            if response.status_code == 404:
                print("No more results found")
            break
        
        data = response.json()
        
        if 'results' not in data or len(data['results']) == 0:
            print("No more results")
            break
        
        batch_size = len(data['results'])
        print(f"Retrieved {batch_size} records")
        
        # Parse each record
        for record in data['results']:
            try:
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
                    'report_number': record.get('report_number', ''),
                    'date_received': record.get('date_received', ''),
                    'event_type': ', '.join(record.get('event_type', [])) if record.get('event_type') else '',
                    'report_source_code': record.get('report_source_code', ''),
                    'device_date_of_manufacturer': device_info.get('device_date_of_manufacturer', ''),
                    'brand_name': clean_text(device_info.get('brand_name', '')),
                    'generic_name': clean_text(device_info.get('generic_name', '')),
                    'manufacturer_d_name': clean_text(device_info.get('manufacturer_d_name', '')),
                    'device_class': device_info.get('device_class', ''),
                    'device_operator': device_info.get('device_operator', ''),
                    'patient_sequence_number': patient_info.get('sequence_number_outcome', ''),
                    'patient_sequence_treatment': patient_info.get('sequence_number_treatment', ''),
                    'event_description': event_description[:32000],  # Excel cell limit
                    'manufacturer_narrative': manufacturer_narrative[:32000],
                    'adverse_event_flag': record.get('adverse_event_flag', ''),
                    'product_problem_flag': record.get('product_problem_flag', ''),
                    'date_of_event': record.get('date_of_event', ''),
                    'reprocessed_and_reused_flag': record.get('reprocessed_and_reused_flag', ''),
                    'removal_correction_number': record.get('removal_correction_number', '')
                }
                
                all_records.append(parsed_record)
                
            except Exception as e:
                print(f"Error parsing record: {e}")
                continue
        
        # Check if we got less than limit (last page)
        if batch_size < limit:
            print("Reached last page")
            break
        
        skip += limit
        page += 1
        
        # Rate limiting
        time.sleep(0.5)
        
        # Safety limit
        if page > 1000:
            print("Reached safety limit of 1000 pages")
            break
            
    except Exception as e:
        print(f"Error fetching data: {e}")
        break

print("\n" + "="*80)
print(f"TOTAL RECORDS FETCHED: {len(all_records)}")
print("="*80)

if len(all_records) == 0:
    print("No records found!")
else:
    # Create DataFrame
    df = pd.DataFrame(all_records)
    
    # Convert date_received to proper date format
    df['date_received'] = pd.to_datetime(df['date_received'], format='%Y%m%d', errors='coerce')
    
    # Sort by date
    df = df.sort_values('date_received')
    
    print(f"\nDate range: {df['date_received'].min()} to {df['date_received'].max()}")
    print(f"Total records: {len(df)}")
    
    # Show breakdown by year
    df['year'] = df['date_received'].dt.year
    yearly_counts = df['year'].value_counts().sort_index()
    
    print("\n" + "="*80)
    print("YEARLY BREAKDOWN")
    print("="*80)
    for year, count in yearly_counts.items():
        print(f"{year}: {count} reports")
    
    # Event type breakdown
    print("\n" + "="*80)
    print("EVENT TYPE BREAKDOWN")
    print("="*80)
    event_types = df['event_type'].value_counts().head(10)
    for event, count in event_types.items():
        print(f"{event}: {count}")
    
    # MDL filing date
    mdl_date = pd.to_datetime('2020-12-16')
    df['period'] = df['date_received'].apply(lambda x: 'Before MDL' if x < mdl_date else 'After MDL')
    
    before_count = len(df[df['period'] == 'Before MDL'])
    after_count = len(df[df['period'] == 'After MDL'])
    
    print("\n" + "="*80)
    print("BEFORE vs AFTER MDL (December 16, 2020)")
    print("="*80)
    print(f"Before MDL: {before_count} reports")
    print(f"After MDL: {after_count} reports")
    
    # Monthly aggregation
    df['year_month'] = df['date_received'].dt.to_period('M')
    monthly_summary = df.groupby('year_month').size().reset_index(name='count')
    monthly_summary['date'] = monthly_summary['year_month'].dt.to_timestamp()
    
    # Save to Excel
    print("\n" + "="*80)
    print("SAVING TO EXCEL")
    print("="*80)
    
    with pd.ExcelWriter('paragard_all_mdr_reports.xlsx', engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='All Reports', index=False)
        monthly_summary.to_excel(writer, sheet_name='Monthly Summary', index=False)
        yearly_counts.reset_index().to_excel(writer, sheet_name='Yearly Summary', index=False)
        
        # Event type summary
        event_summary = df['event_type'].value_counts().reset_index()
        event_summary.columns = ['Event Type', 'Count']
        event_summary.to_excel(writer, sheet_name='Event Types', index=False)
        
        # Before/After summary
        period_summary = df.groupby('period').size().reset_index(name='count')
        period_summary.to_excel(writer, sheet_name='Before After MDL', index=False)
    
    print("Excel file saved: paragard_all_mdr_reports.xlsx")
    print(f"Sheets: All Reports, Monthly Summary, Yearly Summary, Event Types, Before After MDL")
    
    # Show sample of event descriptions
    print("\n" + "="*80)
    print("SAMPLE EVENT DESCRIPTIONS (first 5)")
    print("="*80)
    for idx, row in df.head(5).iterrows():
        print(f"\nReport {row['report_number']} ({row['date_received'].strftime('%Y-%m-%d')}):")
        desc = row['event_description'][:200]
        print(f"  {desc}...")
    
    print("\n" + "="*80)
    print("COMPLETE - All Paragard MDR reports saved to Excel")
    print("="*80)
