"""
Fetch MAUDE Data for 10 Additional MDL Benchmark Cases
This script extracts FDA adverse event reports for the 6-month period before MDL filing
"""

import requests
import pandas as pd
import time
from datetime import datetime, timedelta
import os

# FDA API base URL
BASE_URL = "https://api.fda.gov/device/event.json"

def fetch_maude_data(search_query, start_date, end_date, limit=100):
    """Fetch MAUDE reports from FDA OpenFDA API"""
    all_records = []
    skip = 0
    
    # Format dates for API (YYYYMMDD)
    date_filter = f"date_received:[{start_date}+TO+{end_date}]"
    
    print(f"  Searching: {search_query}")
    print(f"  Date range: {start_date} to {end_date}")
    
    while True:
        # Build query with URL encoding
        full_query = f"{search_query}+AND+{date_filter}"
        url = f"{BASE_URL}?search={full_query}&limit={limit}&skip={skip}"
        
        try:
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'results' not in data or len(data['results']) == 0:
                    break
                
                all_records.extend(data['results'])
                print(f"    Fetched {len(data['results'])} records (total: {len(all_records)})")
                
                # Check if we've gotten all results
                if len(data['results']) < limit:
                    break
                
                skip += limit
                time.sleep(0.5)  # Rate limiting
                
            elif response.status_code == 404:
                print(f"    No results found")
                break
            else:
                print(f"    Error: HTTP {response.status_code}")
                break
                
        except Exception as e:
            print(f"    Error: {e}")
            break
    
    return all_records

def process_records(records):
    """Process raw FDA records into structured DataFrame"""
    processed = []
    
    for record in records:
        try:
            # Extract device info
            device = record.get('device', [{}])[0] if record.get('device') else {}
            
            processed.append({
                'report_number': record.get('report_number', ''),
                'date_received': record.get('date_received', ''),
                'date_of_event': record.get('date_of_event', ''),
                'event_type': record.get('event_type', ''),
                'report_source_code': record.get('report_source_code', ''),
                'brand_name': device.get('brand_name', ''),
                'generic_name': device.get('generic_name', ''),
                'manufacturer_d_name': device.get('manufacturer_d_name', ''),
                'model_number': device.get('model_number', ''),
                'catalog_number': device.get('catalog_number', ''),
                'device_class': device.get('device_class', ''),
                'event_description': '; '.join(record.get('mdr_text', [{}])[0].get('text', '').split('\n')[:3]) if record.get('mdr_text') else '',
                'manufacturer_narrative': device.get('device_event_key', ''),
                'adverse_event_flag': record.get('adverse_event_flag', ''),
                'product_problem_flag': record.get('product_problem_flag', ''),
                'device_operator': device.get('device_operator', ''),
                'manufacturer_g1_name': device.get('manufacturer_g1_name', '')
            })
        except Exception as e:
            print(f"    Warning: Error processing record: {e}")
            continue
    
    return pd.DataFrame(processed)

# Define the 10 additional cases
cases = [
    {
        'name': 'IVC Filters (C.R. Bard)',
        'filename': 'bard_ivc_filters_mdl_2641.xlsx',
        'mdl': '2641',
        'filing_date': '2015-08-03',
        'court': 'D. Arizona',
        'status': 'Active',
        'searches': [
            'device.brand_name:"Recovery"',
            'device.brand_name:"G2"',
            'manufacturer_d_name:"BARD"+AND+device.generic_name:"filter"'
        ]
    },
    {
        'name': 'Cook Medical IVC Filters',
        'filename': 'cook_ivc_filters_mdl_2570.xlsx',
        'mdl': '2570',
        'filing_date': '2014-08-28',
        'court': 'S.D. Indiana',
        'status': 'Active',
        'searches': [
            'device.brand_name:"Celect"',
            'device.brand_name:"Gunther+Tulip"',
            'manufacturer_d_name:"COOK"+AND+device.generic_name:"filter"'
        ]
    },
    {
        'name': 'Zimmer M/L Taper Hip',
        'filename': 'zimmer_ml_taper_hip_mdl_2716.xlsx',
        'mdl': '2716',
        'filing_date': '2016-03-24',
        'court': 'N.D. Indiana',
        'status': 'Active',
        'searches': [
            'device.brand_name:"M/L+Taper"',
            'device.brand_name:"Versys"',
            'manufacturer_d_name:"ZIMMER"+AND+device.generic_name:"hip"'
        ]
    },
    {
        'name': 'DePuy Pinnacle Hip',
        'filename': 'depuy_pinnacle_hip_mdl_2244.xlsx',
        'mdl': '2244',
        'filing_date': '2011-03-31',
        'court': 'N.D. Texas',
        'status': 'Settled',
        'settlement': '$1+ billion (2013-2016)',
        'searches': [
            'device.brand_name:"Pinnacle"',
            'device.brand_name:"Ultamet"',
            'manufacturer_d_name:"DEPUY"+AND+device.generic_name:"hip"'
        ]
    },
    {
        'name': 'Wright Conserve Hip',
        'filename': 'wright_conserve_hip_mdl_2329.xlsx',
        'mdl': '2329',
        'filing_date': '2012-05-04',
        'court': 'N.D. Georgia',
        'status': 'Settled',
        'settlement': '$240 million (2015)',
        'searches': [
            'device.brand_name:"Conserve"',
            'manufacturer_d_name:"WRIGHT"+AND+device.generic_name:"hip"'
        ]
    },
    {
        'name': 'Mirena IUD (Bayer)',
        'filename': 'mirena_iud_mdl_2434.xlsx',
        'mdl': '2434',
        'filing_date': '2013-04-04',
        'court': 'S.D. New York',
        'status': 'Settled',
        'settlement': 'Undisclosed (2018)',
        'searches': [
            'device.brand_name:"Mirena"',
            'manufacturer_d_name:"BAYER"+AND+device.generic_name:"intrauterine"'
        ]
    },
    {
        'name': 'Essure Birth Control',
        'filename': 'essure_birth_control_mdl_2325.xlsx',
        'mdl': '2325',
        'filing_date': '2013-09-03',
        'court': 'E.D. Pennsylvania',
        'status': 'Active',
        'searches': [
            'device.brand_name:"Essure"',
            'manufacturer_d_name:"BAYER"+AND+device.generic_name:"contraceptive"',
            'manufacturer_d_name:"CONCEPTUS"'
        ]
    },
    {
        'name': 'Physiomesh (Ethicon)',
        'filename': 'physiomesh_ethicon_mdl_2782.xlsx',
        'mdl': '2782',
        'filing_date': '2016-11-07',
        'court': 'N.D. Georgia',
        'status': 'Active',
        'searches': [
            'device.brand_name:"Physiomesh"',
            'manufacturer_d_name:"ETHICON"+AND+device.generic_name:"mesh"'
        ]
    },
    {
        'name': 'Atrium C-QUR Mesh',
        'filename': 'atrium_cqur_mesh_mdl_2753.xlsx',
        'mdl': '2753',
        'filing_date': '2016-08-23',
        'court': 'D. New Hampshire',
        'status': 'Active',
        'searches': [
            'device.brand_name:"C-QUR"',
            'device.brand_name:"CQUR"',
            'manufacturer_d_name:"ATRIUM"+AND+device.generic_name:"mesh"'
        ]
    },
    {
        'name': 'Medtronic Sprint Fidelis',
        'filename': 'medtronic_sprint_fidelis_mdl_1905.xlsx',
        'mdl': '1905',
        'filing_date': '2008-06-26',
        'court': 'D. Minnesota',
        'status': 'Settled',
        'settlement': '$268 million (2010-2012)',
        'searches': [
            'device.brand_name:"Sprint+Fidelis"',
            'device.brand_name:"Fidelis"',
            'manufacturer_d_name:"MEDTRONIC"+AND+device.generic_name:"lead"'
        ]
    }
]

# Create output directory
output_dir = '/Users/praveen/Praveen/benchmark_cases_additional'
os.makedirs(output_dir, exist_ok=True)

print("="*80)
print("FETCHING 10 ADDITIONAL MDL BENCHMARK CASES FROM FDA MAUDE")
print("="*80)
print(f"\nOutput directory: {output_dir}")
print(f"Total cases to fetch: {len(cases)}\n")

all_cases_summary = []

for idx, case in enumerate(cases, 1):
    print(f"\n{'='*80}")
    print(f"CASE {idx}/10: {case['name']}")
    print(f"{'='*80}")
    print(f"MDL: {case['mdl']} | Court: {case['court']} | Status: {case['status']}")
    if case.get('settlement'):
        print(f"Settlement: {case['settlement']}")
    
    # Calculate 6-month window
    filing_date = datetime.strptime(case['filing_date'], '%Y-%m-%d')
    start_date = filing_date - timedelta(days=183)
    
    start_str = start_date.strftime('%Y%m%d')
    end_str = filing_date.strftime('%Y%m%d')
    
    print(f"Date window: {start_date.strftime('%Y-%m-%d')} to {filing_date.strftime('%Y-%m-%d')}")
    
    # Fetch data from multiple search strategies
    all_records = []
    seen_report_numbers = set()
    
    for search_idx, search_query in enumerate(case['searches'], 1):
        print(f"\n  Search {search_idx}/{len(case['searches'])}:")
        records = fetch_maude_data(search_query, start_str, end_str)
        
        # Deduplicate
        new_records = []
        for record in records:
            report_num = record.get('report_number', '')
            if report_num and report_num not in seen_report_numbers:
                new_records.append(record)
                seen_report_numbers.add(report_num)
        
        all_records.extend(new_records)
        print(f"    New unique records: {len(new_records)}")
    
    print(f"\n  Total unique records: {len(all_records)}")
    
    if len(all_records) == 0:
        print(f"  ⚠️  No records found for {case['name']}")
        continue
    
    # Process into DataFrame
    df = process_records(all_records)
    
    # Convert date_received to datetime
    df['date_received'] = pd.to_datetime(df['date_received'], format='%Y%m%d', errors='coerce')
    
    # Create Excel file with multiple sheets
    output_path = os.path.join(output_dir, case['filename'])
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # Sheet 1: All Reports
        df.to_excel(writer, sheet_name='All Reports', index=False)
        
        # Sheet 2: Monthly Summary
        df['year_month'] = df['date_received'].dt.to_period('M')
        monthly = df.groupby('year_month').size().reset_index(name='count')
        monthly['year_month'] = monthly['year_month'].astype(str)
        monthly.to_excel(writer, sheet_name='Monthly Summary', index=False)
        
        # Sheet 3: Event Types
        event_summary = df['event_type'].value_counts().reset_index()
        event_summary.columns = ['Event Type', 'Count']
        event_summary.to_excel(writer, sheet_name='Event Types', index=False)
        
        # Sheet 4: Brand Names
        brand_summary = df['brand_name'].value_counts().head(20).reset_index()
        brand_summary.columns = ['Brand Name', 'Count']
        brand_summary.to_excel(writer, sheet_name='Brand Names', index=False)
        
        # Sheet 5: Case Metadata
        metadata = pd.DataFrame([{
            'Case Name': case['name'],
            'MDL Number': case['mdl'],
            'Filing Date': case['filing_date'],
            'Court': case['court'],
            'Status': case['status'],
            'Settlement': case.get('settlement', 'N/A'),
            'Data Window Start': start_date.strftime('%Y-%m-%d'),
            'Data Window End': filing_date.strftime('%Y-%m-%d'),
            'Total Records': len(df),
            'Search Queries Used': len(case['searches'])
        }])
        metadata.to_excel(writer, sheet_name='Case Metadata', index=False)
    
    print(f"  ✅ Saved to: {case['filename']}")
    
    # Add to summary
    all_cases_summary.append({
        'Case Name': case['name'],
        'MDL': case['mdl'],
        'Status': case['status'],
        'Settlement': case.get('settlement', 'N/A'),
        'Total MDRs': len(df),
        'Filing Date': case['filing_date'],
        'Court': case['court']
    })

# Create master summary file
print(f"\n{'='*80}")
print("CREATING MASTER SUMMARY")
print(f"{'='*80}")

summary_df = pd.DataFrame(all_cases_summary)
summary_path = os.path.join(output_dir, 'additional_cases_summary.xlsx')
summary_df.to_excel(summary_path, index=False)

print(f"\n✅ Master summary saved to: additional_cases_summary.xlsx")
print(f"\n📊 FINAL STATISTICS:")
print(f"   Cases processed: {len(all_cases_summary)}")
print(f"   Total MDRs: {summary_df['Total MDRs'].sum():,}")
print(f"   Active cases: {len([c for c in cases if c['status'] == 'Active'])}")
print(f"   Settled cases: {len([c for c in cases if c['status'] == 'Settled'])}")

print(f"\n{'='*80}")
print("FETCH COMPLETE!")
print(f"{'='*80}")
print(f"All files saved to: {output_dir}")
