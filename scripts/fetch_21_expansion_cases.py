"""
Fetch MAUDE Data for 21 Additional Cases - Expansion to 50-Case Benchmark
Using corrected patient field handling: patient = record.get('patient', [{}])[0]
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import time
import os

# Create output directory
os.makedirs('benchmark_cases_expansion_21', exist_ok=True)

# FDA API Base URL
BASE_URL = "https://api.fda.gov/device/event.json"

def fetch_maude_data(search_queries, start_date, end_date, limit=100):
    """
    Fetch MAUDE data with multiple search queries for better recall
    Fixed: patient field is a LIST like device, not a dict
    Fixed: Remove quotes from search terms for FDA API
    """
    all_records = []
    seen_report_numbers = set()
    
    for query in search_queries:
        skip = 0
        total_fetched = 0
        
        print(f"  Query: {query}")
        
        while True:
            # Build URL with proper encoding (no params dict to avoid double encoding)
            date_filter = f"date_received:[{start_date}+TO+{end_date}]"
            full_query = f"{query}+AND+{date_filter}"
            url = f"{BASE_URL}?search={full_query}&limit={limit}&skip={skip}"
            
            try:
                response = requests.get(url, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    results = data.get('results', [])
                    
                    if not results:
                        break
                    
                    # Process records with correct patient field handling
                    new_records = process_records(results, seen_report_numbers)
                    all_records.extend(new_records)
                    total_fetched += len(results)
                    
                    print(f"    Fetched {len(results)} records (skip={skip}, new={len(new_records)})")
                    
                    # Check if we've reached the end
                    total_available = data.get('meta', {}).get('results', {}).get('total', 0)
                    if skip + limit >= total_available or len(results) < limit:
                        break
                    
                    skip += limit
                    time.sleep(0.5)  # Rate limiting
                    
                elif response.status_code == 404:
                    print(f"    No results found")
                    break
                else:
                    print(f"    Error {response.status_code}: {response.text[:200]}")
                    break
                    
            except Exception as e:
                print(f"    Exception: {str(e)}")
                break
        
        print(f"  Total from this query: {total_fetched} records")
    
    return all_records

def process_records(results, seen_report_numbers):
    """
    Process FDA records into structured format
    FIXED: patient field is a LIST (like device), not a dict!
    """
    processed = []
    
    for record in results:
        report_number = record.get('report_number')
        
        # Skip duplicates
        if report_number in seen_report_numbers:
            continue
        
        seen_report_numbers.add(report_number)
        
        # Extract device info
        device = record.get('device', [{}])[0]
        
        # CRITICAL FIX: patient is a LIST like device, not a dict
        patient = record.get('patient', [{}])[0]  # Get first element from list
        patient_problems = patient.get('patient_problems', []) if isinstance(patient, dict) else []
        
        processed.append({
            'report_number': report_number,
            'date_received': record.get('date_received'),
            'event_type': record.get('event_type'),
            'manufacturer_name': device.get('manufacturer_d_name', ''),
            'brand_name': device.get('brand_name', ''),
            'generic_name': device.get('generic_name', ''),
            'device_class': device.get('device_class', ''),
            'product_code': device.get('openfda', {}).get('device_class', ''),
            'event_description': ', '.join(patient_problems) if patient_problems else '',
            'adverse_event_flag': record.get('adverse_event_flag', ''),
            'report_source': record.get('report_source_code', '')
        })
    
    return processed

# ============================================================================
# CASE 1: Paragard IUD (MDL 2974)
# ============================================================================
def fetch_paragard_iud():
    print("\n" + "="*80)
    print("CASE 1: Paragard IUD (MDL 2974)")
    print("="*80)
    
    # Filing: Dec 2018, search 6 months before
    start_date = "20180601"
    end_date = "20251027"
    
    queries = [
        'brand_name:paragard',
        'generic_name:intrauterine',
        'manufacturer_d_name:teva'
    ]
    
    records = fetch_maude_data(queries, start_date, end_date)
    
    if records:
        df = pd.DataFrame(records)
        filename = 'benchmark_cases_expansion_21/paragard_iud_mdl_2974.xlsx'
        df.to_excel(filename, index=False)
        print(f"\n✓ Saved {len(df)} records to {filename}")
        return len(df)
    else:
        print("\n✗ No records found")
        return 0

# ============================================================================
# CASE 2: Zimmer Persona Knee (MDL 2996)
# ============================================================================
def fetch_zimmer_persona():
    print("\n" + "="*80)
    print("CASE 2: Zimmer Persona Knee (MDL 2996)")
    print("="*80)
    
    start_date = "20190101"
    end_date = "20251027"
    
    queries = [
        'brand_name:"persona"',
        'manufacturer_d_name:"zimmer biomet" AND generic_name:"knee"',
        'brand_name:"persona knee" OR brand_name:"persona cr"'
    ]
    
    records = fetch_maude_data(queries, start_date, end_date)
    
    if records:
        df = pd.DataFrame(records)
        filename = 'benchmark_cases_expansion_21/zimmer_persona_knee_mdl_2996.xlsx'
        df.to_excel(filename, index=False)
        print(f"\n✓ Saved {len(df)} records to {filename}")
        return len(df)
    else:
        print("\n✗ No records found")
        return 0

# ============================================================================
# CASE 3: Smith & Nephew Birmingham Hip (MDL 2775)
# ============================================================================
def fetch_birmingham_hip():
    print("\n" + "="*80)
    print("CASE 3: Smith & Nephew Birmingham Hip (MDL 2775)")
    print("="*80)
    
    start_date = "20160801"
    end_date = "20251027"
    
    queries = [
        'brand_name:"birmingham hip"',
        'manufacturer_d_name:"smith nephew" AND generic_name:"hip"',
        'brand_name:"bhr" OR generic_name:"hip resurfacing"'
    ]
    
    records = fetch_maude_data(queries, start_date, end_date)
    
    if records:
        df = pd.DataFrame(records)
        filename = 'benchmark_cases_expansion_21/smith_nephew_birmingham_hip_mdl_2775.xlsx'
        df.to_excel(filename, index=False)
        print(f"\n✓ Saved {len(df)} records to {filename}")
        return len(df)
    else:
        print("\n✗ No records found")
        return 0

# ============================================================================
# CASE 4: 3M Bair Hugger (MDL 2666)
# ============================================================================
def fetch_bair_hugger():
    print("\n" + "="*80)
    print("CASE 4: 3M Bair Hugger Warming Blanket (MDL 2666)")
    print("="*80)
    
    start_date = "20141101"
    end_date = "20251027"
    
    queries = [
        'brand_name:"bair hugger"',
        'manufacturer_d_name:"3m" AND generic_name:"warming"',
        'generic_name:"patient warming system" OR generic_name:"forced air"'
    ]
    
    records = fetch_maude_data(queries, start_date, end_date)
    
    if records:
        df = pd.DataFrame(records)
        filename = 'benchmark_cases_expansion_21/3m_bair_hugger_mdl_2666.xlsx'
        df.to_excel(filename, index=False)
        print(f"\n✓ Saved {len(df)} records to {filename}")
        return len(df)
    else:
        print("\n✗ No records found")
        return 0

# ============================================================================
# CASE 5: Medtronic MiniMed Insulin Pump (MDL 3032)
# ============================================================================
def fetch_minimed_pump():
    print("\n" + "="*80)
    print("CASE 5: Medtronic MiniMed Insulin Pump (MDL 3032)")
    print("="*80)
    
    start_date = "20200301"
    end_date = "20251027"
    
    queries = [
        'brand_name:"minimed"',
        'manufacturer_d_name:"medtronic" AND generic_name:"insulin pump"',
        'brand_name:"minimed 600" OR brand_name:"minimed 670g"'
    ]
    
    records = fetch_maude_data(queries, start_date, end_date)
    
    if records:
        df = pd.DataFrame(records)
        filename = 'benchmark_cases_expansion_21/medtronic_minimed_pump_mdl_3032.xlsx'
        df.to_excel(filename, index=False)
        print(f"\n✓ Saved {len(df)} records to {filename}")
        return len(df)
    else:
        print("\n✗ No records found")
        return 0

# ============================================================================
# CASE 6: Arthrex Hip Fixation (MDL 2928)
# ============================================================================
def fetch_arthrex_hip():
    print("\n" + "="*80)
    print("CASE 6: Arthrex Hip Fixation (MDL 2928)")
    print("="*80)
    
    start_date = "20180201"
    end_date = "20251027"
    
    queries = [
        'manufacturer_d_name:"arthrex" AND generic_name:"hip"',
        'brand_name:"fibertak"',
        'manufacturer_d_name:"arthrex" AND generic_name:"anchor"'
    ]
    
    records = fetch_maude_data(queries, start_date, end_date)
    
    if records:
        df = pd.DataFrame(records)
        filename = 'benchmark_cases_expansion_21/arthrex_hip_fixation_mdl_2928.xlsx'
        df.to_excel(filename, index=False)
        print(f"\n✓ Saved {len(df)} records to {filename}")
        return len(df)
    else:
        print("\n✗ No records found")
        return 0

# ============================================================================
# CASE 7: Olympus Duodenoscope (MDL 2787)
# ============================================================================
def fetch_olympus_duodenoscope():
    print("\n" + "="*80)
    print("CASE 7: Olympus Duodenoscope (MDL 2787)")
    print("="*80)
    
    start_date = "20161001"
    end_date = "20251027"
    
    queries = [
        'manufacturer_d_name:"olympus" AND generic_name:"duodenoscope"',
        'brand_name:"tjf" AND manufacturer_d_name:"olympus"',
        'generic_name:"endoscope ercp" OR generic_name:"duodenoscope"'
    ]
    
    records = fetch_maude_data(queries, start_date, end_date)
    
    if records:
        df = pd.DataFrame(records)
        filename = 'benchmark_cases_expansion_21/olympus_duodenoscope_mdl_2787.xlsx'
        df.to_excel(filename, index=False)
        print(f"\n✓ Saved {len(df)} records to {filename}")
        return len(df)
    else:
        print("\n✗ No records found")
        return 0

# ============================================================================
# CASE 8: Abbott HeartMate II LVAD (MDL 2868)
# ============================================================================
def fetch_heartmate_lvad():
    print("\n" + "="*80)
    print("CASE 8: Abbott HeartMate II LVAD (MDL 2868)")
    print("="*80)
    
    start_date = "20171001"
    end_date = "20251027"
    
    queries = [
        'brand_name:"heartmate ii" OR brand_name:"heartmate 2"',
        'manufacturer_d_name:"abbott" AND generic_name:"lvad"',
        'generic_name:"ventricular assist" AND manufacturer_d_name:"abbott"'
    ]
    
    records = fetch_maude_data(queries, start_date, end_date)
    
    if records:
        df = pd.DataFrame(records)
        filename = 'benchmark_cases_expansion_21/abbott_heartmate_lvad_mdl_2868.xlsx'
        df.to_excel(filename, index=False)
        print(f"\n✓ Saved {len(df)} records to {filename}")
        return len(df)
    else:
        print("\n✗ No records found")
        return 0

# ============================================================================
# CASE 9: Stryker LFIT V40 Femoral Head (MDL 2768)
# ============================================================================
def fetch_stryker_lfit():
    print("\n" + "="*80)
    print("CASE 9: Stryker LFIT V40 Femoral Head (MDL 2768)")
    print("="*80)
    
    start_date = "20160701"
    end_date = "20251027"
    
    queries = [
        'brand_name:"lfit" OR brand_name:"l fit"',
        'manufacturer_d_name:"stryker" AND generic_name:"femoral head"',
        'brand_name:"v40" AND manufacturer_d_name:"stryker"'
    ]
    
    records = fetch_maude_data(queries, start_date, end_date)
    
    if records:
        df = pd.DataFrame(records)
        filename = 'benchmark_cases_expansion_21/stryker_lfit_v40_mdl_2768.xlsx'
        df.to_excel(filename, index=False)
        print(f"\n✓ Saved {len(df)} records to {filename}")
        return len(df)
    else:
        print("\n✗ No records found")
        return 0

# ============================================================================
# CASE 10: Medtronic Synchromed II Pain Pump (MDL 2903)
# ============================================================================
def fetch_synchromed_pump():
    print("\n" + "="*80)
    print("CASE 10: Medtronic Synchromed II Pain Pump (MDL 2903)")
    print("="*80)
    
    start_date = "20171201"
    end_date = "20251027"
    
    queries = [
        'brand_name:"synchromed"',
        'manufacturer_d_name:"medtronic" AND generic_name:"infusion pump"',
        'brand_name:"synchromed ii" OR brand_name:"synchromed 2"'
    ]
    
    records = fetch_maude_data(queries, start_date, end_date)
    
    if records:
        df = pd.DataFrame(records)
        filename = 'benchmark_cases_expansion_21/medtronic_synchromed_ii_mdl_2903.xlsx'
        df.to_excel(filename, index=False)
        print(f"\n✓ Saved {len(df)} records to {filename}")
        return len(df)
    else:
        print("\n✗ No records found")
        return 0

# ============================================================================
# CASE 11: Teleflex EZ-IO Device (MDL 3070)
# ============================================================================
def fetch_teleflex_ezio():
    print("\n" + "="*80)
    print("CASE 11: Teleflex EZ-IO Device (MDL 3070)")
    print("="*80)
    
    start_date = "20201201"
    end_date = "20251027"
    
    queries = [
        'brand_name:"ez-io" OR brand_name:"ezio"',
        'manufacturer_d_name:"teleflex" AND generic_name:"intraosseous"',
        'generic_name:"io needle" OR generic_name:"bone drill"'
    ]
    
    records = fetch_maude_data(queries, start_date, end_date)
    
    if records:
        df = pd.DataFrame(records)
        filename = 'benchmark_cases_expansion_21/teleflex_ezio_mdl_3070.xlsx'
        df.to_excel(filename, index=False)
        print(f"\n✓ Saved {len(df)} records to {filename}")
        return len(df)
    else:
        print("\n✗ No records found")
        return 0

# ============================================================================
# CASE 12: Fresenius GranuFlo/NaturaLyte (MDL 2428)
# ============================================================================
def fetch_fresenius_granuflo():
    print("\n" + "="*80)
    print("CASE 12: Fresenius GranuFlo/NaturaLyte (MDL 2428)")
    print("="*80)
    
    start_date = "20120601"
    end_date = "20251027"
    
    queries = [
        'brand_name:"granuflo"',
        'brand_name:"naturalyte"',
        'manufacturer_d_name:"fresenius" AND generic_name:"dialysis"'
    ]
    
    records = fetch_maude_data(queries, start_date, end_date)
    
    if records:
        df = pd.DataFrame(records)
        filename = 'benchmark_cases_expansion_21/fresenius_granuflo_mdl_2428.xlsx'
        df.to_excel(filename, index=False)
        print(f"\n✓ Saved {len(df)} records to {filename}")
        return len(df)
    else:
        print("\n✗ No records found")
        return 0

# ============================================================================
# CASE 13: Boston Scientific Lotus Edge Valve (MDL 2904)
# ============================================================================
def fetch_lotus_valve():
    print("\n" + "="*80)
    print("CASE 13: Boston Scientific Lotus Edge Valve (MDL 2904)")
    print("="*80)
    
    start_date = "20171201"
    end_date = "20251027"
    
    queries = [
        'brand_name:"lotus edge" OR brand_name:"lotus valve"',
        'manufacturer_d_name:"boston scientific" AND generic_name:"valve"',
        'brand_name:"lotus" AND generic_name:"transcatheter"'
    ]
    
    records = fetch_maude_data(queries, start_date, end_date)
    
    if records:
        df = pd.DataFrame(records)
        filename = 'benchmark_cases_expansion_21/boston_scientific_lotus_valve_mdl_2904.xlsx'
        df.to_excel(filename, index=False)
        print(f"\n✓ Saved {len(df)} records to {filename}")
        return len(df)
    else:
        print("\n✗ No records found")
        return 0

# ============================================================================
# CASE 14: Conformis iTotal Knee (MDL 2995)
# ============================================================================
def fetch_conformis_knee():
    print("\n" + "="*80)
    print("CASE 14: Conformis iTotal Knee (MDL 2995)")
    print("="*80)
    
    start_date = "20190101"
    end_date = "20251027"
    
    queries = [
        'brand_name:"itotal"',
        'manufacturer_d_name:"conformis"',
        'brand_name:"conformis" AND generic_name:"knee"'
    ]
    
    records = fetch_maude_data(queries, start_date, end_date)
    
    if records:
        df = pd.DataFrame(records)
        filename = 'benchmark_cases_expansion_21/conformis_itotal_knee_mdl_2995.xlsx'
        df.to_excel(filename, index=False)
        print(f"\n✓ Saved {len(df)} records to {filename}")
        return len(df)
    else:
        print("\n✗ No records found")
        return 0

# ============================================================================
# CASE 15: Medtronic Bone Screw (MDL 2881)
# ============================================================================
def fetch_medtronic_bone_screw():
    print("\n" + "="*80)
    print("CASE 15: Medtronic Bone Screw (MDL 2881)")
    print("="*80)
    
    start_date = "20171101"
    end_date = "20251027"
    
    queries = [
        'brand_name:"cd horizon" AND brand_name:"sextant"',
        'manufacturer_d_name:"medtronic" AND generic_name:"pedicle screw"',
        'brand_name:"sextant" OR brand_name:"cd horizon"'
    ]
    
    records = fetch_maude_data(queries, start_date, end_date)
    
    if records:
        df = pd.DataFrame(records)
        filename = 'benchmark_cases_expansion_21/medtronic_bone_screw_mdl_2881.xlsx'
        df.to_excel(filename, index=False)
        print(f"\n✓ Saved {len(df)} records to {filename}")
        return len(df)
    else:
        print("\n✗ No records found")
        return 0

# ============================================================================
# CASE 16: Wright Profemur Hip (MDL 2749)
# ============================================================================
def fetch_wright_profemur():
    print("\n" + "="*80)
    print("CASE 16: Wright Profemur Hip (MDL 2749)")
    print("="*80)
    
    start_date = "20160501"
    end_date = "20251027"
    
    queries = [
        'brand_name:"profemur"',
        'manufacturer_d_name:"wright" AND generic_name:"hip"',
        'brand_name:"profemur modular"'
    ]
    
    records = fetch_maude_data(queries, start_date, end_date)
    
    if records:
        df = pd.DataFrame(records)
        filename = 'benchmark_cases_expansion_21/wright_profemur_hip_mdl_2749.xlsx'
        df.to_excel(filename, index=False)
        print(f"\n✓ Saved {len(df)} records to {filename}")
        return len(df)
    else:
        print("\n✗ No records found")
        return 0

# ============================================================================
# CASE 17: Stryker Trident/Accolade TMZF Hip (MDL 2965)
# ============================================================================
def fetch_stryker_tmzf():
    print("\n" + "="*80)
    print("CASE 17: Stryker Trident/Accolade TMZF Hip (MDL 2965)")
    print("="*80)
    
    start_date = "20181001"
    end_date = "20251027"
    
    queries = [
        'brand_name:"accolade tmzf"',
        'brand_name:"trident" AND manufacturer_d_name:"stryker"',
        'manufacturer_d_name:"stryker" AND generic_name:"hip" AND generic_name:"tmzf"'
    ]
    
    records = fetch_maude_data(queries, start_date, end_date)
    
    if records:
        df = pd.DataFrame(records)
        filename = 'benchmark_cases_expansion_21/stryker_tmzf_hip_mdl_2965.xlsx'
        df.to_excel(filename, index=False)
        print(f"\n✓ Saved {len(df)} records to {filename}")
        return len(df)
    else:
        print("\n✗ No records found")
        return 0

# ============================================================================
# CASE 18: NuVasive XLIF Implant (MDL 2848)
# ============================================================================
def fetch_nuvasive_xlif():
    print("\n" + "="*80)
    print("CASE 18: NuVasive XLIF Implant (MDL 2848)")
    print("="*80)
    
    start_date = "20170801"
    end_date = "20251027"
    
    queries = [
        'brand_name:"xlif"',
        'manufacturer_d_name:"nuvasive"',
        'generic_name:"lateral interbody fusion" OR generic_name:"xlif"'
    ]
    
    records = fetch_maude_data(queries, start_date, end_date)
    
    if records:
        df = pd.DataFrame(records)
        filename = 'benchmark_cases_expansion_21/nuvasive_xlif_mdl_2848.xlsx'
        df.to_excel(filename, index=False)
        print(f"\n✓ Saved {len(df)} records to {filename}")
        return len(df)
    else:
        print("\n✗ No records found")
        return 0

# ============================================================================
# CASE 19: Medtronic Paradigm Insulin Pump
# ============================================================================
def fetch_paradigm_pump():
    print("\n" + "="*80)
    print("CASE 19: Medtronic Paradigm Insulin Pump")
    print("="*80)
    
    start_date = "20180601"
    end_date = "20251027"
    
    queries = [
        'brand_name:"paradigm"',
        'manufacturer_d_name:"medtronic" AND generic_name:"insulin pump"',
        'brand_name:"paradigm revel" OR brand_name:"paradigm veo"'
    ]
    
    records = fetch_maude_data(queries, start_date, end_date)
    
    if records:
        df = pd.DataFrame(records)
        filename = 'benchmark_cases_expansion_21/medtronic_paradigm_pump.xlsx'
        df.to_excel(filename, index=False)
        print(f"\n✓ Saved {len(df)} records to {filename}")
        return len(df)
    else:
        print("\n✗ No records found")
        return 0

# ============================================================================
# CASE 20: Bard Denali IVC Filter
# ============================================================================
def fetch_bard_denali():
    print("\n" + "="*80)
    print("CASE 20: Bard Denali IVC Filter")
    print("="*80)
    
    start_date = "20141101"
    end_date = "20251027"
    
    queries = [
        'brand_name:"denali"',
        'manufacturer_d_name:"bard" AND generic_name:"ivc filter"',
        'brand_name:"denali filter"'
    ]
    
    records = fetch_maude_data(queries, start_date, end_date)
    
    if records:
        df = pd.DataFrame(records)
        filename = 'benchmark_cases_expansion_21/bard_denali_ivc_filter.xlsx'
        df.to_excel(filename, index=False)
        print(f"\n✓ Saved {len(df)} records to {filename}")
        return len(df)
    else:
        print("\n✗ No records found")
        return 0

# ============================================================================
# CASE 21: Boehringer Ingelheim Pradaxa (MDL 2385)
# ============================================================================
def fetch_pradaxa():
    print("\n" + "="*80)
    print("CASE 21: Boehringer Ingelheim Pradaxa (MDL 2385)")
    print("="*80)
    
    start_date = "20120201"
    end_date = "20251027"
    
    queries = [
        'brand_name:"pradaxa"',
        'generic_name:"dabigatran"',
        'manufacturer_d_name:"boehringer"'
    ]
    
    records = fetch_maude_data(queries, start_date, end_date)
    
    if records:
        df = pd.DataFrame(records)
        filename = 'benchmark_cases_expansion_21/boehringer_pradaxa_mdl_2385.xlsx'
        df.to_excel(filename, index=False)
        print(f"\n✓ Saved {len(df)} records to {filename}")
        return len(df)
    else:
        print("\n✗ No records found")
        return 0

# ============================================================================
# MAIN EXECUTION
# ============================================================================
if __name__ == "__main__":
    print("="*80)
    print(" FETCHING MAUDE DATA FOR 21 ADDITIONAL MDL CASES")
    print(" Expansion to 50-Case Benchmark Dataset")
    print("="*80)
    
    start_time = time.time()
    
    # Execute all fetch functions
    fetch_functions = [
        fetch_paragard_iud,
        fetch_zimmer_persona,
        fetch_birmingham_hip,
        fetch_bair_hugger,
        fetch_minimed_pump,
        fetch_arthrex_hip,
        fetch_olympus_duodenoscope,
        fetch_heartmate_lvad,
        fetch_stryker_lfit,
        fetch_synchromed_pump,
        fetch_teleflex_ezio,
        fetch_fresenius_granuflo,
        fetch_lotus_valve,
        fetch_conformis_knee,
        fetch_medtronic_bone_screw,
        fetch_wright_profemur,
        fetch_stryker_tmzf,
        fetch_nuvasive_xlif,
        fetch_paradigm_pump,
        fetch_bard_denali,
        fetch_pradaxa
    ]
    
    total_records = 0
    results = []
    
    for i, func in enumerate(fetch_functions, 1):
        print(f"\n[{i}/21] Executing: {func.__name__}")
        count = func()
        total_records += count
        results.append({
            'case': func.__name__.replace('fetch_', '').replace('_', ' ').title(),
            'records': count
        })
        time.sleep(1)  # Rate limiting between cases
    
    elapsed_time = time.time() - start_time
    
    # Summary
    print("\n" + "="*80)
    print(" FETCH COMPLETE - SUMMARY")
    print("="*80)
    
    for result in results:
        status = "✓" if result['records'] > 0 else "✗"
        print(f"{status} {result['case']:.<50} {result['records']:>6,} MDRs")
    
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
