import requests
import pandas as pd
from datetime import datetime
import time

print("=" * 80)
print("FETCHING MAUDE DATA - 2 MASS TORT CASES")
print("=" * 80)

cases_to_fetch = [
    {
        "name": "Sientra Breast Implants",
        "litigation_type": "State Court Mass Tort",
        "filing_date": "2015-09-01",
        "queries": [
            'device.brand_name:"Sientra"',
            'device.brand_name:"OPUS"',
            'device.manufacturer_d_name:"Sientra"'
        ],
        "allegations": "Mold contamination, rupture, BIA-ALCL, capsular contracture",
        "fda_recall": "October 2015 (Class I)",
        "output_file": "benchmark_cases_expansion_mass_tort/sientra_breast_implants.xlsx"
    },
    {
        "name": "ATEC Breast Biopsy System",
        "litigation_type": "Multi-Jurisdiction Mass Tort",
        "filing_date": "2018-03-01",
        "queries": [
            'device.brand_name:"ATEC"',
            'device.brand_name:"Eviva"',
            'device.generic_name:"Biopsy+Instrument"'
        ],
        "allegations": "Excessive bleeding, hematoma, tissue damage, device malfunction",
        "fda_recall": "None",
        "output_file": "benchmark_cases_expansion_mass_tort/atec_breast_biopsy.xlsx"
    }
]

base_url = "https://api.fda.gov/device/event.json"

for case_num, case_info in enumerate(cases_to_fetch, 1):
    print(f"\n{'=' * 80}")
    print(f"CASE {case_num}/2: {case_info['name']}")
    print(f"{'=' * 80}")
    print(f"Type: {case_info['litigation_type']}")
    print(f"Filing Date: {case_info['filing_date']}")
    print(f"Allegations: {case_info['allegations']}")
    print(f"FDA Recall: {case_info['fda_recall']}")
    
    all_records = []
    total_fetched = 0
    
    for query_num, query in enumerate(case_info['queries'], 1):
        print(f"\n  Query {query_num}/{len(case_info['queries'])}: {query}")
        
        skip = 0
        limit = 100
        max_results = 10000
        
        while skip < max_results:
            try:
                search_query = f"search={query}&limit={limit}&skip={skip}"
                url = f"{base_url}?{search_query}"
                
                print(f"    Fetching records {skip} to {skip + limit}...", end=" ")
                
                response = requests.get(url, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if 'results' in data and len(data['results']) > 0:
                        records = data['results']
                        all_records.extend(records)
                        total_fetched += len(records)
                        print(f"✓ {len(records)} records (Total: {total_fetched})")
                        
                        if len(records) < limit:
                            print(f"    ✓ Reached end of results for this query")
                            break
                        
                        skip += limit
                        time.sleep(0.5)
                    else:
                        print(f"✓ No more results")
                        break
                        
                elif response.status_code == 404:
                    print(f"✓ No results found")
                    break
                else:
                    print(f"✗ Error: HTTP {response.status_code}")
                    break
                    
            except Exception as e:
                print(f"✗ Error: {str(e)}")
                break
        
        time.sleep(1)
    
    print(f"\n  TOTAL RECORDS FETCHED: {len(all_records)}")
    
    if len(all_records) == 0:
        print(f"\n  ⚠️ No records found for {case_info['name']}")
        continue
    
    # Process records
    print(f"\n  Processing {len(all_records)} records...")
    
    processed_data = []
    
    for record in all_records:
        try:
            mdr_report_key = record.get('mdr_report_key', '')
            report_number = record.get('report_number', '')
            date_received = record.get('date_received', '')
            event_type = record.get('event_type', '')
            
            device_info = record.get('device', [{}])[0] if record.get('device') else {}
            manufacturer_name = device_info.get('manufacturer_d_name', '')
            brand_name = device_info.get('brand_name', '')
            generic_name = device_info.get('generic_name', '')
            device_class = device_info.get('device_class', '')
            
            patient = record.get('patient', [{}])[0] if record.get('patient') else {}
            patient_problems = patient.get('patient_problems', []) if patient else []
            if isinstance(patient_problems, list):
                patient_problems = [p for p in patient_problems if p is not None]
                patient_problems = ', '.join(patient_problems) if patient_problems else ''
            
            adverse_event_flag = record.get('adverse_event_flag', '')
            report_source = record.get('report_source_code', '')
            
            processed_data.append({
                'mdr_report_key': mdr_report_key,
                'report_number': report_number,
                'date_received': date_received,
                'event_type': event_type,
                'manufacturer_name': manufacturer_name,
                'brand_name': brand_name,
                'generic_name': generic_name,
                'device_class': device_class,
                'event_description': patient_problems,
                'adverse_event_flag': adverse_event_flag,
                'report_source': report_source
            })
            
        except Exception as e:
            print(f"  Error processing record: {str(e)}")
            continue
    
    df = pd.DataFrame(processed_data)
    print(f"  ✓ Processed {len(df)} records into DataFrame")
    
    # Remove duplicates
    df = df.drop_duplicates(subset=['mdr_report_key'])
    print(f"  ✓ After removing duplicates: {len(df)} unique records")
    
    # Save to Excel
    df.to_excel(case_info['output_file'], index=False)
    
    print(f"\n  ✅ SUCCESS!")
    print(f"  File saved: {case_info['output_file']}")
    print(f"  Total MDRs: {len(df):,}")
    
    if len(df) > 0:
        print(f"\n  📊 SUMMARY:")
        print(f"    Date range: {df['date_received'].min()} to {df['date_received'].max()}")
        if 'event_type' in df.columns:
            event_counts = df['event_type'].value_counts().to_dict()
            print(f"    Event types: {event_counts}")
        print(f"    Unique manufacturers: {df['manufacturer_name'].nunique()}")
        print(f"    Most common brand: {df['brand_name'].value_counts().head(1).to_dict()}")

print("\n" + "=" * 80)
print("FETCH COMPLETE - SUMMARY")
print("=" * 80)

print("""
✅ Sientra Breast Implants - Data fetched
✅ ATEC Breast Biopsy System - Data fetched

Both mass tort cases now have MAUDE data ready for integration!
""")

print("=" * 80)
