"""
Fetch MAUDE Data for 21 Additional Cases - FIXED VERSION
Using the proven working pattern from fetch_10_expansion_cases_FIXED.py
"""

import requests
import pandas as pd
from datetime import datetime
import time
import os

# Create output directory
os.makedirs('benchmark_cases_expansion_21', exist_ok=True)

# FDA API Base URL
BASE_URL = "https://api.fda.gov/device/event.json"

def fetch_maude_data(search_query, start_date, end_date, limit=100):
    """Fetch MAUDE reports from FDA OpenFDA API - PROVEN WORKING VERSION"""
    all_records = []
    skip = 0
    
    # Format dates for API (YYYYMMDD)
    date_filter = f"date_received:[{start_date}+TO+{end_date}]"
    
    print(f"  Searching: {search_query}")
    
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
                print(f"    → Fetched {len(data['results'])} records (total: {len(all_records)})")
                
                # Check if we've gotten all results
                if len(data['results']) < limit:
                    break
                
                skip += limit
                time.sleep(0.5)  # Rate limiting
                
            elif response.status_code == 404:
                print(f"    → No records found")
                break
            else:
                print(f"    → Error {response.status_code}")
                break
                
        except Exception as e:
            print(f"    → Exception: {str(e)[:100]}")
            break
    
    return all_records

def process_records(records):
    """
    Process FDA records - FIXED VERSION
    patient field is a LIST like device, not a dict!
    """
    processed = []
    
    for record in records:
        # Extract device info
        device = record.get('device', [{}])[0] if record.get('device') else {}
        
        # CRITICAL: patient is a LIST like device
        patient = record.get('patient', [{}])[0] if record.get('patient') else {}
        patient_problems = patient.get('patient_problems', []) if isinstance(patient, dict) else []
        
        processed.append({
            'report_number': record.get('report_number'),
            'date_received': record.get('date_received'),
            'event_type': record.get('event_type'),
            'manufacturer_name': device.get('manufacturer_d_name', ''),
            'brand_name': device.get('brand_name', ''),
            'generic_name': device.get('generic_name', ''),
            'device_class': device.get('device_class', ''),
            'event_description': ', '.join(patient_problems) if patient_problems else '',
            'adverse_event_flag': record.get('adverse_event_flag', ''),
            'report_source': record.get('report_source_code', '')
        })
    
    return processed

# ============================================================================
# FETCH FUNCTIONS FOR 21 CASES
# ============================================================================

def fetch_case(case_num, case_name, queries, start_date, end_date, filename):
    """Generic fetch function for all cases"""
    print("\n" + "="*80)
    print(f"CASE {case_num}: {case_name}")
    print("="*80)
    
    all_records = []
    for query in queries:
        records = fetch_maude_data(query, start_date, end_date)
        all_records.extend(records)
    
    if all_records:
        # Remove duplicates
        unique_records = {r['report_number']: r for r in all_records}.values()
        df = pd.DataFrame(process_records(list(unique_records)))
        filepath = f'benchmark_cases_expansion_21/{filename}'
        df.to_excel(filepath, index=False)
        print(f"\n✓ Saved {len(df)} unique records to {filepath}")
        return len(df)
    else:
        print("\n✗ No records found")
        return 0

# Define all 21 cases
cases = [
    {
        'num': 1,
        'name': 'Paragard IUD (MDL 2974)',
        'queries': ['brand_name:paragard', 'generic_name:intrauterine'],
        'start': '20180601',
        'end': '20251027',
        'filename': 'paragard_iud_mdl_2974.xlsx'
    },
    {
        'num': 2,
        'name': 'Zimmer Persona Knee (MDL 2996)',
        'queries': ['brand_name:persona', 'manufacturer_d_name:zimmer+AND+generic_name:knee'],
        'start': '20190101',
        'end': '20251027',
        'filename': 'zimmer_persona_knee_mdl_2996.xlsx'
    },
    {
        'num': 3,
        'name': 'Smith & Nephew Birmingham Hip (MDL 2775)',
        'queries': ['brand_name:birmingham', 'manufacturer_d_name:smith+AND+generic_name:hip'],
        'start': '20160801',
        'end': '20251027',
        'filename': 'smith_nephew_birmingham_hip_mdl_2775.xlsx'
    },
    {
        'num': 4,
        'name': '3M Bair Hugger (MDL 2666)',
        'queries': ['brand_name:bair', 'generic_name:warming'],
        'start': '20141101',
        'end': '20251027',
        'filename': '3m_bair_hugger_mdl_2666.xlsx'
    },
    {
        'num': 5,
        'name': 'Medtronic MiniMed Insulin Pump (MDL 3032)',
        'queries': ['brand_name:minimed', 'manufacturer_d_name:medtronic+AND+generic_name:pump'],
        'start': '20200301',
        'end': '20251027',
        'filename': 'medtronic_minimed_pump_mdl_3032.xlsx'
    },
    {
        'num': 6,
        'name': 'Arthrex Hip Fixation (MDL 2928)',
        'queries': ['manufacturer_d_name:arthrex+AND+generic_name:hip', 'brand_name:fibertak'],
        'start': '20180201',
        'end': '20251027',
        'filename': 'arthrex_hip_fixation_mdl_2928.xlsx'
    },
    {
        'num': 7,
        'name': 'Olympus Duodenoscope (MDL 2787)',
        'queries': ['manufacturer_d_name:olympus+AND+generic_name:duodenoscope', 'brand_name:tjf'],
        'start': '20161001',
        'end': '20251027',
        'filename': 'olympus_duodenoscope_mdl_2787.xlsx'
    },
    {
        'num': 8,
        'name': 'Abbott HeartMate II LVAD (MDL 2868)',
        'queries': ['brand_name:heartmate', 'manufacturer_d_name:abbott+AND+generic_name:lvad'],
        'start': '20171001',
        'end': '20251027',
        'filename': 'abbott_heartmate_lvad_mdl_2868.xlsx'
    },
    {
        'num': 9,
        'name': 'Stryker LFIT V40 Femoral Head (MDL 2768)',
        'queries': ['brand_name:lfit', 'manufacturer_d_name:stryker+AND+generic_name:femoral'],
        'start': '20160701',
        'end': '20251027',
        'filename': 'stryker_lfit_v40_mdl_2768.xlsx'
    },
    {
        'num': 10,
        'name': 'Medtronic Synchromed II Pain Pump (MDL 2903)',
        'queries': ['brand_name:synchromed', 'manufacturer_d_name:medtronic+AND+generic_name:infusion'],
        'start': '20171201',
        'end': '20251027',
        'filename': 'medtronic_synchromed_ii_mdl_2903.xlsx'
    },
    {
        'num': 11,
        'name': 'Teleflex EZ-IO Device (MDL 3070)',
        'queries': ['brand_name:ezio', 'manufacturer_d_name:teleflex'],
        'start': '20201201',
        'end': '20251027',
        'filename': 'teleflex_ezio_mdl_3070.xlsx'
    },
    {
        'num': 12,
        'name': 'Fresenius GranuFlo (MDL 2428)',
        'queries': ['brand_name:granuflo', 'brand_name:naturalyte'],
        'start': '20120601',
        'end': '20251027',
        'filename': 'fresenius_granuflo_mdl_2428.xlsx'
    },
    {
        'num': 13,
        'name': 'Boston Scientific Lotus Valve (MDL 2904)',
        'queries': ['brand_name:lotus', 'manufacturer_d_name:boston+AND+generic_name:valve'],
        'start': '20171201',
        'end': '20251027',
        'filename': 'boston_scientific_lotus_valve_mdl_2904.xlsx'
    },
    {
        'num': 14,
        'name': 'Conformis iTotal Knee (MDL 2995)',
        'queries': ['brand_name:itotal', 'manufacturer_d_name:conformis'],
        'start': '20190101',
        'end': '20251027',
        'filename': 'conformis_itotal_knee_mdl_2995.xlsx'
    },
    {
        'num': 15,
        'name': 'Medtronic Bone Screw (MDL 2881)',
        'queries': ['brand_name:sextant', 'brand_name:horizon+AND+manufacturer_d_name:medtronic'],
        'start': '20171101',
        'end': '20251027',
        'filename': 'medtronic_bone_screw_mdl_2881.xlsx'
    },
    {
        'num': 16,
        'name': 'Wright Profemur Hip (MDL 2749)',
        'queries': ['brand_name:profemur', 'manufacturer_d_name:wright+AND+generic_name:hip'],
        'start': '20160501',
        'end': '20251027',
        'filename': 'wright_profemur_hip_mdl_2749.xlsx'
    },
    {
        'num': 17,
        'name': 'Stryker Trident/Accolade TMZF (MDL 2965)',
        'queries': ['brand_name:trident', 'brand_name:accolade+AND+manufacturer_d_name:stryker'],
        'start': '20181001',
        'end': '20251027',
        'filename': 'stryker_tmzf_hip_mdl_2965.xlsx'
    },
    {
        'num': 18,
        'name': 'NuVasive XLIF (MDL 2848)',
        'queries': ['brand_name:xlif', 'manufacturer_d_name:nuvasive'],
        'start': '20170801',
        'end': '20251027',
        'filename': 'nuvasive_xlif_mdl_2848.xlsx'
    },
    {
        'num': 19,
        'name': 'Medtronic Paradigm Insulin Pump',
        'queries': ['brand_name:paradigm', 'manufacturer_d_name:medtronic+AND+generic_name:insulin'],
        'start': '20180601',
        'end': '20251027',
        'filename': 'medtronic_paradigm_pump.xlsx'
    },
    {
        'num': 20,
        'name': 'Bard Denali IVC Filter',
        'queries': ['brand_name:denali', 'manufacturer_d_name:bard+AND+generic_name:filter'],
        'start': '20141101',
        'end': '20251027',
        'filename': 'bard_denali_ivc_filter.xlsx'
    },
    {
        'num': 21,
        'name': 'Boehringer Pradaxa (MDL 2385)',
        'queries': ['brand_name:pradaxa', 'generic_name:dabigatran'],
        'start': '20120201',
        'end': '20251027',
        'filename': 'boehringer_pradaxa_mdl_2385.xlsx'
    }
]

# ============================================================================
# MAIN EXECUTION
# ============================================================================
if __name__ == "__main__":
    print("="*80)
    print(" FETCHING MAUDE DATA FOR 21 ADDITIONAL MDL CASES")
    print(" Expansion to 50-Case Benchmark Dataset")
    print("="*80)
    
    start_time = time.time()
    total_records = 0
    results = []
    
    for case in cases:
        print(f"\n[{case['num']}/21] Processing: {case['name']}")
        count = fetch_case(
            case['num'],
            case['name'],
            case['queries'],
            case['start'],
            case['end'],
            case['filename']
        )
        total_records += count
        results.append({'case': case['name'], 'records': count})
        time.sleep(1)  # Rate limiting between cases
    
    elapsed_time = time.time() - start_time
    
    # Summary
    print("\n" + "="*80)
    print(" FETCH COMPLETE - SUMMARY")
    print("="*80)
    
    for result in results:
        status = "✓" if result['records'] > 0 else "✗"
        print(f"{status} {result['case']:.<60} {result['records']:>6,} MDRs")
    
    print("="*80)
    print(f"Total Records Fetched: {total_records:,}")
    print(f"Total Cases: 21")
    print(f"Time Elapsed: {elapsed_time/60:.1f} minutes")
    print(f"Combined Benchmark: 29 + 21 = 50 cases")
    print("="*80)
    
    # Save summary
    with open('/tmp/fetch_21_summary.txt', 'w') as f:
        f.write("21 Additional Cases MAUDE Fetch Summary\n")
        f.write("="*80 + "\n\n")
        for result in results:
            f.write(f"{result['case']}: {result['records']:,} MDRs\n")
        f.write(f"\nTotal: {total_records:,} MDRs\n")
        f.write(f"Time: {elapsed_time/60:.1f} minutes\n")
    
    print("\n✓ Summary saved to /tmp/fetch_21_summary.txt")
