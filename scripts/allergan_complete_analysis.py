#!/usr/bin/env python3
"""
Comprehensive Allergan Breast Implant Analysis
Including BIOCELL and NATRELLE brands
MDL No. 2921 - Filed December 18, 2019
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
print("COMPREHENSIVE ALLERGAN BREAST IMPLANT ANALYSIS")
print("Including BIOCELL + NATRELLE brands")
print("MDL No. 2921 - Filed December 18, 2019")
print("="*80)

base_url = "https://api.fda.gov/device/event.json"

# Search for both BIOCELL and NATRELLE
search_terms = [
    'device.brand_name:"BIOCELL"',
    'device.brand_name:"NATRELLE"',
    'device.brand_name:"Allergan" AND device.generic_name:"breast implant"'
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
                    
                    if report_number in seen_report_numbers:
                        continue
                    
                    seen_report_numbers.add(report_number)
                    
                    device_info = record.get('device', [{}])[0] if record.get('device') else {}
                    patient_info = record.get('patient', [{}])[0] if record.get('patient') else {}
                    
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
            
            print(f"New unique records: {new_records}")
            
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
print(f"TOTAL UNIQUE RECORDS: {len(all_records)}")
print("="*80)

if len(all_records) > 0:
    df = pd.DataFrame(all_records)
    
    # Convert dates
    df['date_received'] = pd.to_datetime(df['date_received'], format='%Y%m%d', errors='coerce')
    df = df.sort_values('date_received')
    
    print(f"\nDate range: {df['date_received'].min()} to {df['date_received'].max()}")
    
    # MDL filing date
    mdl_date = pd.to_datetime('2019-12-18')
    fda_recall_date = pd.to_datetime('2019-07-24')  # FDA requested recall
    
    df['period'] = df['date_received'].apply(lambda x: 'Before MDL' if x < mdl_date else 'After MDL')
    
    # Statistics
    before_count = len(df[df['date_received'] < mdl_date])
    after_count = len(df[df['date_received'] >= mdl_date])
    
    # Brand breakdown
    print("\n" + "="*80)
    print("BRAND BREAKDOWN")
    print("="*80)
    brand_counts = df['brand_name'].value_counts().head(10)
    for brand, count in brand_counts.items():
        if brand:
            print(f"{brand}: {count} reports")
    
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
    print(f"Ratio: {after_count/max(before_count, 1):.2f}x")
    
    # 2019 detailed breakdown
    df_2019 = df[df['year'] == 2019]
    monthly_2019 = df_2019.groupby(df_2019['date_received'].dt.to_period('M')).size()
    
    print("\n" + "="*80)
    print("2019 MONTHLY BREAKDOWN (MDL Filing Year)")
    print("="*80)
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    for i in range(1, 13):
        period = pd.Period(f'2019-{i:02d}', freq='M')
        count = monthly_2019.get(period, 0)
        month_name = month_names[i-1]
        
        marker = ""
        if i == 7:
            marker = " ← FDA RECALL REQUEST (July 24, 2019)"
        elif i == 12:
            marker = " ← MDL FILED (Dec 18, 2019)"
        
        print(f"{month_name} 2019: {count} reports{marker}")
    
    # 6-month windows
    six_months_before = mdl_date - pd.DateOffset(months=6)
    six_months_after = mdl_date + pd.DateOffset(months=6)
    
    critical_before = df[(df['date_received'] >= six_months_before) & (df['date_received'] < mdl_date)]
    critical_after = df[(df['date_received'] >= mdl_date) & (df['date_received'] <= six_months_after)]
    
    print("\n" + "="*80)
    print("6-MONTH WINDOWS")
    print("="*80)
    print(f"BEFORE MDL (Jun-Dec 2019): {len(critical_before)} reports")
    print(f"AFTER MDL (Dec 2019-Jun 2020): {len(critical_after)} reports")
    
    # Calculate averages
    before_avg = len(critical_before) / 6
    after_avg = len(critical_after) / 6
    
    print(f"\nAvg/month BEFORE: {before_avg:.1f}")
    print(f"Avg/month AFTER: {after_avg:.1f}")
    
    # Pattern determination
    if after_count > before_count * 2:
        pattern = "REVERSE (awareness-driven)"
    elif after_count < before_count * 0.5:
        pattern = "DECLINING after filing"
    else:
        pattern = "FLAT/NEUTRAL"
    
    # But check for pre-filing spike
    july_2019_count = len(df[(df['date_received'] >= '2019-07-01') & (df['date_received'] < '2019-08-01')])
    aug_2019_count = len(df[(df['date_received'] >= '2019-08-01') & (df['date_received'] < '2019-09-01')])
    baseline_2019 = len(df[(df['date_received'] >= '2019-01-01') & (df['date_received'] < '2019-06-01')]) / 5
    
    if july_2019_count > baseline_2019 * 3:
        pattern = "PREDICTIVE (pre-filing spike from FDA recall)"
    
    print(f"\nPattern Type: {pattern}")
    print(f"July 2019 spike: {july_2019_count} reports ({july_2019_count/max(baseline_2019, 1):.1f}x baseline)")
    
    # Save to Excel
    print("\n" + "="*80)
    print("SAVING TO EXCEL")
    print("="*80)
    
    with pd.ExcelWriter('allergan_complete_breast_implants.xlsx', engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='All Reports', index=False)
        
        # Monthly summary
        monthly_summary = df.groupby(df['date_received'].dt.to_period('M')).size().reset_index(name='count')
        monthly_summary['date'] = monthly_summary['date_received'].dt.to_timestamp()
        monthly_summary.to_excel(writer, sheet_name='Monthly Summary', index=False)
        
        # 2019 breakdown
        monthly_2019_df = pd.DataFrame({
            'Month': month_names,
            'Count': [monthly_2019.get(pd.Period(f'2019-{i:02d}', freq='M'), 0) for i in range(1, 13)]
        })
        monthly_2019_df.to_excel(writer, sheet_name='2019 Monthly', index=False)
        
        # Brand summary
        brand_summary = df['brand_name'].value_counts().reset_index()
        brand_summary.columns = ['Brand', 'Count']
        brand_summary.to_excel(writer, sheet_name='Brands', index=False)
        
        # Before/After
        period_df = df.groupby('period').size().reset_index(name='count')
        period_df.to_excel(writer, sheet_name='Before After MDL', index=False)
    
    print("Excel saved: allergan_complete_breast_implants.xlsx")
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)
else:
    print("No records found!")
