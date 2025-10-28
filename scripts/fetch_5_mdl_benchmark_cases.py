#!/usr/bin/env python3
"""
Fetch MAUDE data for 5 Major MDL Benchmark Cases
6-month window BEFORE each MDL filing date
"""

import requests
import pandas as pd
import time
import re
from datetime import datetime
import os

def clean_text(text):
    """Remove illegal characters for Excel"""
    if pd.isna(text) or text is None:
        return ""
    text = str(text)
    text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F-\x9F]', '', text)
    return text

def fetch_maude_data(search_query, start_date, end_date, case_name):
    """Fetch MAUDE data for a specific device and date range"""
    
    print("\n" + "="*80)
    print(f"FETCHING: {case_name}")
    print("="*80)
    print(f"Search Query: {search_query}")
    print(f"Date Range: {start_date} to {end_date}")
    print("="*80)
    
    # Convert dates to FDA format (YYYYMMDD)
    start_fda = start_date.replace('-', '')
    end_fda = end_date.replace('-', '')
    
    # Build search query with date range
    date_query = f"+AND+date_received:%5B{start_fda}+TO+{end_fda}%5D"
    full_query = search_query + date_query
    
    all_records = []
    seen_report_numbers = set()
    
    skip = 0
    limit = 100
    page = 1
    
    while True:
        print(f"Page {page} (skip={skip})...", end=" ")
        
        # Build URL directly to avoid double-encoding
        url = f"https://api.fda.gov/device/event.json?search={full_query}&limit={limit}&skip={skip}"
        
        try:
            response = requests.get(url)
            
            if response.status_code != 200:
                print(f"Status {response.status_code}")
                break
            
            data = response.json()
            
            if 'results' not in data or len(data['results']) == 0:
                print("No more results")
                break
            
            batch_size = len(data['results'])
            new_records = 0
            
            for record in data['results']:
                try:
                    report_number = record.get('report_number', '')
                    
                    if report_number in seen_report_numbers:
                        continue
                    
                    seen_report_numbers.add(report_number)
                    
                    # Extract device info
                    device_info = record.get('device', [{}])[0] if record.get('device') else {}
                    
                    # Extract event info
                    mdr_text = record.get('mdr_text', [{}])
                    event_description = ""
                    manufacturer_narrative = ""
                    
                    for text_entry in mdr_text:
                        text_type = text_entry.get('text_type_code', '')
                        if 'Description' in text_type or 'Problem' in text_type:
                            event_description = clean_text(text_entry.get('text', ''))
                        elif 'Manufacturer' in text_type or 'Narrative' in text_type:
                            manufacturer_narrative = clean_text(text_entry.get('text', ''))
                    
                    parsed_record = {
                        'report_number': report_number,
                        'date_received': record.get('date_received', ''),
                        'date_of_event': record.get('date_of_event', ''),
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
                        'device_operator': device_info.get('device_operator', ''),
                        'manufacturer_g1_name': device_info.get('manufacturer_g1_name', '')
                    }
                    
                    all_records.append(parsed_record)
                    new_records += 1
                    
                except Exception as e:
                    continue
            
            print(f"Got {batch_size} records, {new_records} new unique")
            
            if batch_size < limit:
                break
            
            skip += limit
            page += 1
            time.sleep(0.5)
            
            if page > 300:
                print("Safety limit reached (300 pages)")
                break
                
        except Exception as e:
            print(f"Error: {e}")
            break
    
    print(f"\n✓ Total unique records: {len(all_records)}")
    return all_records

# Define the 5 benchmark cases
cases = [
    {
        'name': 'Philips CPAP',
        'mdl': '3014',
        'mdl_date': '2021-10-08',
        'start_date': '2021-04-08',
        'end_date': '2021-10-08',
        'court': 'W.D. Pennsylvania',
        'search_queries': [
            'device.manufacturer_d_name:"PHILIPS"+AND+device.generic_name:"ventilator"',
            'device.brand_name:"DREAMSTATION"',
            'device.brand_name:"TRILOGY"',
            'device.brand_name:"BIPAP"'
        ]
    },
    {
        'name': 'Bard PowerPort',
        'mdl': '3081',
        'mdl_date': '2023-08-15',
        'start_date': '2023-02-15',
        'end_date': '2023-08-15',
        'court': 'D. Arizona',
        'search_queries': [
            'device.brand_name:"POWERPORT"',
            'device.brand_name:"POWER+PORT"',
            'device.manufacturer_d_name:"BARD"+AND+device.generic_name:"catheter"'
        ]
    },
    {
        'name': 'Hernia Mesh (Bard/Davol)',
        'mdl': '2846',
        'mdl_date': '2018-08-02',
        'start_date': '2018-02-02',
        'end_date': '2018-08-02',
        'court': 'S.D. Ohio',
        'search_queries': [
            'device.manufacturer_d_name:"DAVOL"+AND+device.generic_name:"mesh"',
            'device.manufacturer_d_name:"BARD"+AND+device.generic_name:"mesh"',
            'device.brand_name:"VENTRALEX"',
            'device.brand_name:"COMPOSIX"'
        ]
    },
    {
        'name': 'Exactech Joint Implants',
        'mdl': '3044',
        'mdl_date': '2022-06-14',
        'start_date': '2021-12-14',
        'end_date': '2022-06-14',
        'court': 'E.D. New York',
        'search_queries': [
            'device.manufacturer_d_name:"EXACTECH"',
            'device.brand_name:"OPTETRAK"',
            'device.brand_name:"NOVATION"'
        ]
    },
    {
        'name': 'Allergan BIOCELL',
        'mdl': '2921',
        'mdl_date': '2019-12-18',
        'start_date': '2019-06-18',
        'end_date': '2019-12-18',
        'court': 'D. New Jersey',
        'search_queries': [
            'device.brand_name:"BIOCELL"',
            'device.brand_name:"NATRELLE"+AND+device.manufacturer_d_name:"ALLERGAN"'
        ]
    }
]

# Create output directory
output_dir = '/Users/praveen/Praveen/benchmark_cases'
os.makedirs(output_dir, exist_ok=True)

print("="*80)
print("5 MAJOR MDL BENCHMARK CASES - MAUDE DATA EXTRACTION")
print("6-Month Window BEFORE MDL Filing Date")
print("="*80)

# Fetch data for each case
all_case_data = {}

for case in cases:
    print(f"\n{'#'*80}")
    print(f"CASE: {case['name']}")
    print(f"MDL No. {case['mdl']}")
    print(f"Court: {case['court']}")
    print(f"MDL Filed: {case['mdl_date']}")
    print(f"MAUDE Window: {case['start_date']} to {case['end_date']}")
    print(f"{'#'*80}")
    
    all_records = []
    seen_reports = set()
    
    # Try each search query for this case
    for search_query in case['search_queries']:
        records = fetch_maude_data(
            search_query,
            case['start_date'],
            case['end_date'],
            f"{case['name']} - {search_query}"
        )
        
        # Deduplicate across search queries
        for record in records:
            if record['report_number'] not in seen_reports:
                seen_reports.add(record['report_number'])
                all_records.append(record)
        
        time.sleep(1)
    
    all_case_data[case['name']] = {
        'records': all_records,
        'metadata': case
    }
    
    print(f"\n{'='*80}")
    print(f"TOTAL UNIQUE RECORDS FOR {case['name']}: {len(all_records)}")
    print(f"{'='*80}")

# Save all data
print("\n" + "="*80)
print("SAVING DATA TO EXCEL")
print("="*80)

for case_name, case_data in all_case_data.items():
    records = case_data['records']
    metadata = case_data['metadata']
    
    if len(records) == 0:
        print(f"\n⚠️  {case_name}: No records found")
        continue
    
    df = pd.DataFrame(records)
    
    # Convert dates
    df['date_received'] = pd.to_datetime(df['date_received'], format='%Y%m%d', errors='coerce')
    df['date_of_event'] = pd.to_datetime(df['date_of_event'], format='%Y%m%d', errors='coerce')
    df = df.sort_values('date_received')
    
    # Create filename
    filename = f"{case_name.replace(' ', '_').replace('/', '_').lower()}_mdl_{metadata['mdl']}.xlsx"
    filepath = os.path.join(output_dir, filename)
    
    # Monthly breakdown
    df['year_month'] = df['date_received'].dt.to_period('M')
    monthly_summary = df.groupby('year_month').size().reset_index()
    monthly_summary.columns = ['Month', 'Count']
    monthly_summary['Date'] = monthly_summary['Month'].dt.to_timestamp()
    
    # Event type summary
    event_summary = df['event_type'].value_counts().reset_index()
    event_summary.columns = ['Event Type', 'Count']
    
    # Brand summary
    brand_summary = df['brand_name'].value_counts().reset_index()
    brand_summary.columns = ['Brand Name', 'Count']
    
    # Save to Excel
    with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
        # All reports
        df.to_excel(writer, sheet_name='All Reports', index=False)
        
        # Monthly summary
        monthly_summary.to_excel(writer, sheet_name='Monthly Summary', index=False)
        
        # Event types
        event_summary.to_excel(writer, sheet_name='Event Types', index=False)
        
        # Brand names
        brand_summary.to_excel(writer, sheet_name='Brand Names', index=False)
        
        # Metadata
        meta_df = pd.DataFrame([{
            'Case Name': case_name,
            'MDL Number': metadata['mdl'],
            'MDL Filing Date': metadata['mdl_date'],
            'Court': metadata['court'],
            'MAUDE Start Date': metadata['start_date'],
            'MAUDE End Date': metadata['end_date'],
            'Total Records': len(df),
            'Date Range': f"{df['date_received'].min()} to {df['date_received'].max()}"
        }])
        meta_df.to_excel(writer, sheet_name='Case Metadata', index=False)
    
    print(f"\n✓ {case_name}")
    print(f"  File: {filename}")
    print(f"  Records: {len(df)}")
    print(f"  Date Range: {df['date_received'].min()} to {df['date_received'].max()}")
    print(f"  Monthly Average: {len(df)/6:.1f} reports/month")

# Create master summary
print("\n" + "="*80)
print("CREATING MASTER SUMMARY")
print("="*80)

summary_data = []
for case_name, case_data in all_case_data.items():
    records = case_data['records']
    metadata = case_data['metadata']
    
    if len(records) > 0:
        df = pd.DataFrame(records)
        df['date_received'] = pd.to_datetime(df['date_received'], format='%Y%m%d', errors='coerce')
        
        summary_data.append({
            'Case Name': case_name,
            'MDL Number': metadata['mdl'],
            'MDL Filing Date': metadata['mdl_date'],
            'Court': metadata['court'],
            'MAUDE Window': f"{metadata['start_date']} to {metadata['end_date']}",
            'Total Reports': len(df),
            'Avg Reports/Month': len(df)/6,
            'First Report': df['date_received'].min(),
            'Last Report': df['date_received'].max()
        })

summary_df = pd.DataFrame(summary_data)
summary_filepath = os.path.join(output_dir, 'benchmark_cases_summary.xlsx')

with pd.ExcelWriter(summary_filepath, engine='openpyxl') as writer:
    summary_df.to_excel(writer, sheet_name='Summary', index=False)

print(f"✓ Master summary saved: benchmark_cases_summary.xlsx")

print("\n" + "="*80)
print("BENCHMARK CASES SUMMARY")
print("="*80)
print(f"\n{'Case':<30} {'MDL':<8} {'Reports':<10} {'Avg/Month':<12}")
print("-"*80)
for _, row in summary_df.iterrows():
    print(f"{row['Case Name']:<30} {row['MDL Number']:<8} {row['Total Reports']:<10} {row['Avg Reports/Month']:<12.1f}")

print("\n" + "="*80)
print("EXTRACTION COMPLETE")
print("="*80)
print(f"Location: {output_dir}")
print(f"Files created: {len(all_case_data) + 1}")
print("="*80)
