"""
Fetch MAUDE Data for 21 Additional Cases - CORRECTLY FIXED VERSION
Using the EXACT working pattern from fetch_10_expansion_cases_FIXED.py
Key: device.FIELD:"VALUE+WITH+SPACES"
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
        
        # Filter out None values from patient_problems
        patient_problems = [p for p in patient_problems if p is not None]
        
        processed.append({
            'mdr_report_key': record.get('mdr_report_key'),
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
    
    print(f"  Processed {len(processed)} records successfully")
    
    if len(processed) == 0:
        print("  WARNING: No records processed!")
        return pd.DataFrame()
    
    df = pd.DataFrame(processed)
    print(f"  DataFrame created: {len(df)} rows, {len(df.columns)} columns")
    return df

# ============================================================================
# CASE 1: Paragard IUD (MDL 2974)
# ============================================================================
def fetch_paragard_iud():
    print("\n" + "="*80)
    print("CASE 1: Paragard IUD (MDL 2974)")
    print("="*80)
    
    start_date = "20180601"
    end_date = "20251027"
    
    all_records = []
    
    # Search 1: Brand name
    records = fetch_maude_data('device.brand_name:"Paragard"', start_date, end_date)
    all_records.extend(records)
    
    # Search 2: Generic name
    records = fetch_maude_data('device.generic_name:"intrauterine"', start_date, end_date)
    all_records.extend(records)
    
    # Search 3: Manufacturer
    records = fetch_maude_data('device.manufacturer_d_name:"Teva"', start_date, end_date)
    all_records.extend(records)
    
    print(f"\n  Total raw records fetched: {len(all_records)}")
    
    df = process_records(all_records)
    
    if len(df) > 0:
        df = df.drop_duplicates(subset=['mdr_report_key'])
        print(f"  After deduplication: {len(df)} unique MDRs")
    
    print(f"\n✓ Total unique MDRs: {len(df)}")
    return df, "paragard_iud_mdl_2974.xlsx"

# ============================================================================
# CASE 2: Zimmer Persona Knee (MDL 2996)
# ============================================================================
def fetch_zimmer_persona():
    print("\n" + "="*80)
    print("CASE 2: Zimmer Persona Knee (MDL 2996)")
    print("="*80)
    
    start_date = "20190101"
    end_date = "20251027"
    
    all_records = []
    
    records = fetch_maude_data('device.brand_name:"Persona"', start_date, end_date)
    all_records.extend(records)
    
    records = fetch_maude_data('device.manufacturer_d_name:"Zimmer+Biomet"+AND+device.generic_name:"knee"', start_date, end_date)
    all_records.extend(records)
    
    print(f"\n  Total raw records fetched: {len(all_records)}")
    df = process_records(all_records)
    
    if len(df) > 0:
        df = df.drop_duplicates(subset=['mdr_report_key'])
        print(f"  After deduplication: {len(df)} unique MDRs")
    
    print(f"\n✓ Total unique MDRs: {len(df)}")
    return df, "zimmer_persona_knee_mdl_2996.xlsx"

# ============================================================================
# CASE 3: Smith & Nephew Birmingham Hip (MDL 2775)
# ============================================================================
def fetch_birmingham_hip():
    print("\n" + "="*80)
    print("CASE 3: Smith & Nephew Birmingham Hip (MDL 2775)")
    print("="*80)
    
    start_date = "20160801"
    end_date = "20251027"
    
    all_records = []
    
    records = fetch_maude_data('device.brand_name:"Birmingham"', start_date, end_date)
    all_records.extend(records)
    
    records = fetch_maude_data('device.manufacturer_d_name:"Smith+Nephew"+AND+device.generic_name:"hip"', start_date, end_date)
    all_records.extend(records)
    
    records = fetch_maude_data('device.brand_name:"BHR"', start_date, end_date)
    all_records.extend(records)
    
    print(f"\n  Total raw records fetched: {len(all_records)}")
    df = process_records(all_records)
    
    if len(df) > 0:
        df = df.drop_duplicates(subset=['mdr_report_key'])
        print(f"  After deduplication: {len(df)} unique MDRs")
    
    print(f"\n✓ Total unique MDRs: {len(df)}")
    return df, "smith_nephew_birmingham_hip_mdl_2775.xlsx"

# ============================================================================
# CASE 4: 3M Bair Hugger (MDL 2666)
# ============================================================================
def fetch_bair_hugger():
    print("\n" + "="*80)
    print("CASE 4: 3M Bair Hugger (MDL 2666)")
    print("="*80)
    
    start_date = "20141101"
    end_date = "20251027"
    
    all_records = []
    
    records = fetch_maude_data('device.brand_name:"Bair+Hugger"', start_date, end_date)
    all_records.extend(records)
    
    records = fetch_maude_data('device.manufacturer_d_name:"3M"+AND+device.generic_name:"warming"', start_date, end_date)
    all_records.extend(records)
    
    print(f"\n  Total raw records fetched: {len(all_records)}")
    df = process_records(all_records)
    
    if len(df) > 0:
        df = df.drop_duplicates(subset=['mdr_report_key'])
        print(f"  After deduplication: {len(df)} unique MDRs")
    
    print(f"\n✓ Total unique MDRs: {len(df)}")
    return df, "3m_bair_hugger_mdl_2666.xlsx"

# ============================================================================
# CASE 5: Medtronic MiniMed Insulin Pump (MDL 3032)
# ============================================================================
def fetch_minimed_pump():
    print("\n" + "="*80)
    print("CASE 5: Medtronic MiniMed Insulin Pump (MDL 3032)")
    print("="*80)
    
    start_date = "20200301"
    end_date = "20251027"
    
    all_records = []
    
    records = fetch_maude_data('device.brand_name:"MiniMed"', start_date, end_date)
    all_records.extend(records)
    
    records = fetch_maude_data('device.manufacturer_d_name:"Medtronic"+AND+device.generic_name:"insulin+pump"', start_date, end_date)
    all_records.extend(records)
    
    print(f"\n  Total raw records fetched: {len(all_records)}")
    df = process_records(all_records)
    
    if len(df) > 0:
        df = df.drop_duplicates(subset=['mdr_report_key'])
        print(f"  After deduplication: {len(df)} unique MDRs")
    
    print(f"\n✓ Total unique MDRs: {len(df)}")
    return df, "medtronic_minimed_pump_mdl_3032.xlsx"

# ============================================================================
# CASE 6: Arthrex Hip Fixation (MDL 2928)
# ============================================================================
def fetch_arthrex_hip():
    print("\n" + "="*80)
    print("CASE 6: Arthrex Hip Fixation (MDL 2928)")
    print("="*80)
    
    start_date = "20180201"
    end_date = "20251027"
    
    all_records = []
    
    records = fetch_maude_data('device.manufacturer_d_name:"Arthrex"+AND+device.generic_name:"hip"', start_date, end_date)
    all_records.extend(records)
    
    records = fetch_maude_data('device.brand_name:"FiberTak"', start_date, end_date)
    all_records.extend(records)
    
    print(f"\n  Total raw records fetched: {len(all_records)}")
    df = process_records(all_records)
    
    if len(df) > 0:
        df = df.drop_duplicates(subset=['mdr_report_key'])
        print(f"  After deduplication: {len(df)} unique MDRs")
    
    print(f"\n✓ Total unique MDRs: {len(df)}")
    return df, "arthrex_hip_fixation_mdl_2928.xlsx"

# ============================================================================
# CASE 7: Olympus Duodenoscope (MDL 2787)
# ============================================================================
def fetch_olympus_duodenoscope():
    print("\n" + "="*80)
    print("CASE 7: Olympus Duodenoscope (MDL 2787)")
    print("="*80)
    
    start_date = "20161001"
    end_date = "20251027"
    
    all_records = []
    
    records = fetch_maude_data('device.manufacturer_d_name:"Olympus"+AND+device.generic_name:"duodenoscope"', start_date, end_date)
    all_records.extend(records)
    
    records = fetch_maude_data('device.brand_name:"TJF"', start_date, end_date)
    all_records.extend(records)
    
    print(f"\n  Total raw records fetched: {len(all_records)}")
    df = process_records(all_records)
    
    if len(df) > 0:
        df = df.drop_duplicates(subset=['mdr_report_key'])
        print(f"  After deduplication: {len(df)} unique MDRs")
    
    print(f"\n✓ Total unique MDRs: {len(df)}")
    return df, "olympus_duodenoscope_mdl_2787.xlsx"

# ============================================================================
# CASE 8: Abbott HeartMate II LVAD (MDL 2868)
# ============================================================================
def fetch_heartmate_lvad():
    print("\n" + "="*80)
    print("CASE 8: Abbott HeartMate II LVAD (MDL 2868)")
    print("="*80)
    
    start_date = "20171001"
    end_date = "20251027"
    
    all_records = []
    
    records = fetch_maude_data('device.brand_name:"HeartMate"', start_date, end_date)
    all_records.extend(records)
    
    records = fetch_maude_data('device.manufacturer_d_name:"Abbott"+AND+device.generic_name:"ventricular+assist"', start_date, end_date)
    all_records.extend(records)
    
    print(f"\n  Total raw records fetched: {len(all_records)}")
    df = process_records(all_records)
    
    if len(df) > 0:
        df = df.drop_duplicates(subset=['mdr_report_key'])
        print(f"  After deduplication: {len(df)} unique MDRs")
    
    print(f"\n✓ Total unique MDRs: {len(df)}")
    return df, "abbott_heartmate_lvad_mdl_2868.xlsx"

# ============================================================================
# CASE 9: Stryker LFIT V40 (MDL 2768)
# ============================================================================
def fetch_stryker_lfit():
    print("\n" + "="*80)
    print("CASE 9: Stryker LFIT V40 Femoral Head (MDL 2768)")
    print("="*80)
    
    start_date = "20160701"
    end_date = "20251027"
    
    all_records = []
    
    records = fetch_maude_data('device.brand_name:"LFIT"', start_date, end_date)
    all_records.extend(records)
    
    records = fetch_maude_data('device.manufacturer_d_name:"Stryker"+AND+device.generic_name:"femoral"', start_date, end_date)
    all_records.extend(records)
    
    print(f"\n  Total raw records fetched: {len(all_records)}")
    df = process_records(all_records)
    
    if len(df) > 0:
        df = df.drop_duplicates(subset=['mdr_report_key'])
        print(f"  After deduplication: {len(df)} unique MDRs")
    
    print(f"\n✓ Total unique MDRs: {len(df)}")
    return df, "stryker_lfit_v40_mdl_2768.xlsx"

# ============================================================================
# CASE 10: Medtronic Synchromed II (MDL 2903)
# ============================================================================
def fetch_synchromed_pump():
    print("\n" + "="*80)
    print("CASE 10: Medtronic Synchromed II Pain Pump (MDL 2903)")
    print("="*80)
    
    start_date = "20171201"
    end_date = "20251027"
    
    all_records = []
    
    records = fetch_maude_data('device.brand_name:"SynchroMed"', start_date, end_date)
    all_records.extend(records)
    
    records = fetch_maude_data('device.manufacturer_d_name:"Medtronic"+AND+device.generic_name:"infusion"', start_date, end_date)
    all_records.extend(records)
    
    print(f"\n  Total raw records fetched: {len(all_records)}")
    df = process_records(all_records)
    
    if len(df) > 0:
        df = df.drop_duplicates(subset=['mdr_report_key'])
        print(f"  After deduplication: {len(df)} unique MDRs")
    
    print(f"\n✓ Total unique MDRs: {len(df)}")
    return df, "medtronic_synchromed_ii_mdl_2903.xlsx"

# ============================================================================
# CASE 11: Teleflex EZ-IO (MDL 3070)
# ============================================================================
def fetch_teleflex_ezio():
    print("\n" + "="*80)
    print("CASE 11: Teleflex EZ-IO Device (MDL 3070)")
    print("="*80)
    
    start_date = "20201201"
    end_date = "20251027"
    
    all_records = []
    
    records = fetch_maude_data('device.brand_name:"EZ-IO"', start_date, end_date)
    all_records.extend(records)
    
    records = fetch_maude_data('device.manufacturer_d_name:"Teleflex"', start_date, end_date)
    all_records.extend(records)
    
    print(f"\n  Total raw records fetched: {len(all_records)}")
    df = process_records(all_records)
    
    if len(df) > 0:
        df = df.drop_duplicates(subset=['mdr_report_key'])
        print(f"  After deduplication: {len(df)} unique MDRs")
    
    print(f"\n✓ Total unique MDRs: {len(df)}")
    return df, "teleflex_ezio_mdl_3070.xlsx"

# ============================================================================
# CASE 12: Fresenius GranuFlo (MDL 2428)
# ============================================================================
def fetch_fresenius_granuflo():
    print("\n" + "="*80)
    print("CASE 12: Fresenius GranuFlo/NaturaLyte (MDL 2428)")
    print("="*80)
    
    start_date = "20120601"
    end_date = "20251027"
    
    all_records = []
    
    records = fetch_maude_data('device.brand_name:"GranuFlo"', start_date, end_date)
    all_records.extend(records)
    
    records = fetch_maude_data('device.brand_name:"NaturaLyte"', start_date, end_date)
    all_records.extend(records)
    
    records = fetch_maude_data('device.manufacturer_d_name:"Fresenius"+AND+device.generic_name:"dialysis"', start_date, end_date)
    all_records.extend(records)
    
    print(f"\n  Total raw records fetched: {len(all_records)}")
    df = process_records(all_records)
    
    if len(df) > 0:
        df = df.drop_duplicates(subset=['mdr_report_key'])
        print(f"  After deduplication: {len(df)} unique MDRs")
    
    print(f"\n✓ Total unique MDRs: {len(df)}")
    return df, "fresenius_granuflo_mdl_2428.xlsx"

# ============================================================================
# CASE 13: Boston Scientific Lotus Valve (MDL 2904)
# ============================================================================
def fetch_lotus_valve():
    print("\n" + "="*80)
    print("CASE 13: Boston Scientific Lotus Edge Valve (MDL 2904)")
    print("="*80)
    
    start_date = "20171201"
    end_date = "20251027"
    
    all_records = []
    
    records = fetch_maude_data('device.brand_name:"Lotus"', start_date, end_date)
    all_records.extend(records)
    
    records = fetch_maude_data('device.manufacturer_d_name:"Boston+Scientific"+AND+device.generic_name:"valve"', start_date, end_date)
    all_records.extend(records)
    
    print(f"\n  Total raw records fetched: {len(all_records)}")
    df = process_records(all_records)
    
    if len(df) > 0:
        df = df.drop_duplicates(subset=['mdr_report_key'])
        print(f"  After deduplication: {len(df)} unique MDRs")
    
    print(f"\n✓ Total unique MDRs: {len(df)}")
    return df, "boston_scientific_lotus_valve_mdl_2904.xlsx"

# ============================================================================
# CASE 14: Conformis iTotal Knee (MDL 2995)
# ============================================================================
def fetch_conformis_knee():
    print("\n" + "="*80)
    print("CASE 14: Conformis iTotal Knee (MDL 2995)")
    print("="*80)
    
    start_date = "20190101"
    end_date = "20251027"
    
    all_records = []
    
    records = fetch_maude_data('device.brand_name:"iTotal"', start_date, end_date)
    all_records.extend(records)
    
    records = fetch_maude_data('device.manufacturer_d_name:"Conformis"', start_date, end_date)
    all_records.extend(records)
    
    print(f"\n  Total raw records fetched: {len(all_records)}")
    df = process_records(all_records)
    
    if len(df) > 0:
        df = df.drop_duplicates(subset=['mdr_report_key'])
        print(f"  After deduplication: {len(df)} unique MDRs")
    
    print(f"\n✓ Total unique MDRs: {len(df)}")
    return df, "conformis_itotal_knee_mdl_2995.xlsx"

# ============================================================================
# CASE 15: Medtronic Bone Screw (MDL 2881)
# ============================================================================
def fetch_medtronic_bone_screw():
    print("\n" + "="*80)
    print("CASE 15: Medtronic Bone Screw (MDL 2881)")
    print("="*80)
    
    start_date = "20171101"
    end_date = "20251027"
    
    all_records = []
    
    records = fetch_maude_data('device.brand_name:"Sextant"', start_date, end_date)
    all_records.extend(records)
    
    records = fetch_maude_data('device.brand_name:"CD+Horizon"', start_date, end_date)
    all_records.extend(records)
    
    records = fetch_maude_data('device.manufacturer_d_name:"Medtronic"+AND+device.generic_name:"pedicle+screw"', start_date, end_date)
    all_records.extend(records)
    
    print(f"\n  Total raw records fetched: {len(all_records)}")
    df = process_records(all_records)
    
    if len(df) > 0:
        df = df.drop_duplicates(subset=['mdr_report_key'])
        print(f"  After deduplication: {len(df)} unique MDRs")
    
    print(f"\n✓ Total unique MDRs: {len(df)}")
    return df, "medtronic_bone_screw_mdl_2881.xlsx"

# ============================================================================
# CASE 16: Wright Profemur Hip (MDL 2749)
# ============================================================================
def fetch_wright_profemur():
    print("\n" + "="*80)
    print("CASE 16: Wright Profemur Hip (MDL 2749)")
    print("="*80)
    
    start_date = "20160501"
    end_date = "20251027"
    
    all_records = []
    
    records = fetch_maude_data('device.brand_name:"Profemur"', start_date, end_date)
    all_records.extend(records)
    
    records = fetch_maude_data('device.manufacturer_d_name:"Wright"+AND+device.generic_name:"hip"', start_date, end_date)
    all_records.extend(records)
    
    print(f"\n  Total raw records fetched: {len(all_records)}")
    df = process_records(all_records)
    
    if len(df) > 0:
        df = df.drop_duplicates(subset=['mdr_report_key'])
        print(f"  After deduplication: {len(df)} unique MDRs")
    
    print(f"\n✓ Total unique MDRs: {len(df)}")
    return df, "wright_profemur_hip_mdl_2749.xlsx"

# ============================================================================
# CASE 17: Stryker Trident/Accolade TMZF (MDL 2965)
# ============================================================================
def fetch_stryker_tmzf():
    print("\n" + "="*80)
    print("CASE 17: Stryker Trident/Accolade TMZF Hip (MDL 2965)")
    print("="*80)
    
    start_date = "20181001"
    end_date = "20251027"
    
    all_records = []
    
    records = fetch_maude_data('device.brand_name:"Accolade"', start_date, end_date)
    all_records.extend(records)
    
    records = fetch_maude_data('device.brand_name:"Trident"', start_date, end_date)
    all_records.extend(records)
    
    records = fetch_maude_data('device.manufacturer_d_name:"Stryker"+AND+device.generic_name:"hip"', start_date, end_date)
    all_records.extend(records)
    
    print(f"\n  Total raw records fetched: {len(all_records)}")
    df = process_records(all_records)
    
    if len(df) > 0:
        df = df.drop_duplicates(subset=['mdr_report_key'])
        print(f"  After deduplication: {len(df)} unique MDRs")
    
    print(f"\n✓ Total unique MDRs: {len(df)}")
    return df, "stryker_tmzf_hip_mdl_2965.xlsx"

# ============================================================================
# CASE 18: NuVasive XLIF (MDL 2848)
# ============================================================================
def fetch_nuvasive_xlif():
    print("\n" + "="*80)
    print("CASE 18: NuVasive XLIF Implant (MDL 2848)")
    print("="*80)
    
    start_date = "20170801"
    end_date = "20251027"
    
    all_records = []
    
    records = fetch_maude_data('device.brand_name:"XLIF"', start_date, end_date)
    all_records.extend(records)
    
    records = fetch_maude_data('device.manufacturer_d_name:"NuVasive"', start_date, end_date)
    all_records.extend(records)
    
    print(f"\n  Total raw records fetched: {len(all_records)}")
    df = process_records(all_records)
    
    if len(df) > 0:
        df = df.drop_duplicates(subset=['mdr_report_key'])
        print(f"  After deduplication: {len(df)} unique MDRs")
    
    print(f"\n✓ Total unique MDRs: {len(df)}")
    return df, "nuvasive_xlif_mdl_2848.xlsx"

# ============================================================================
# CASE 19: Medtronic Paradigm Insulin Pump
# ============================================================================
def fetch_paradigm_pump():
    print("\n" + "="*80)
    print("CASE 19: Medtronic Paradigm Insulin Pump")
    print("="*80)
    
    start_date = "20180601"
    end_date = "20251027"
    
    all_records = []
    
    records = fetch_maude_data('device.brand_name:"Paradigm"', start_date, end_date)
    all_records.extend(records)
    
    records = fetch_maude_data('device.manufacturer_d_name:"Medtronic"+AND+device.generic_name:"insulin"', start_date, end_date)
    all_records.extend(records)
    
    print(f"\n  Total raw records fetched: {len(all_records)}")
    df = process_records(all_records)
    
    if len(df) > 0:
        df = df.drop_duplicates(subset=['mdr_report_key'])
        print(f"  After deduplication: {len(df)} unique MDRs")
    
    print(f"\n✓ Total unique MDRs: {len(df)}")
    return df, "medtronic_paradigm_pump.xlsx"

# ============================================================================
# CASE 20: Bard Denali IVC Filter
# ============================================================================
def fetch_bard_denali():
    print("\n" + "="*80)
    print("CASE 20: Bard Denali IVC Filter")
    print("="*80)
    
    start_date = "20141101"
    end_date = "20251027"
    
    all_records = []
    
    records = fetch_maude_data('device.brand_name:"Denali"', start_date, end_date)
    all_records.extend(records)
    
    records = fetch_maude_data('device.manufacturer_d_name:"Bard"+AND+device.generic_name:"filter"', start_date, end_date)
    all_records.extend(records)
    
    print(f"\n  Total raw records fetched: {len(all_records)}")
    df = process_records(all_records)
    
    if len(df) > 0:
        df = df.drop_duplicates(subset=['mdr_report_key'])
        print(f"  After deduplication: {len(df)} unique MDRs")
    
    print(f"\n✓ Total unique MDRs: {len(df)}")
    return df, "bard_denali_ivc_filter.xlsx"

# ============================================================================
# CASE 21: Boehringer Pradaxa (MDL 2385)
# ============================================================================
def fetch_pradaxa():
    print("\n" + "="*80)
    print("CASE 21: Boehringer Ingelheim Pradaxa (MDL 2385)")
    print("="*80)
    
    start_date = "20120201"
    end_date = "20251027"
    
    all_records = []
    
    records = fetch_maude_data('device.brand_name:"Pradaxa"', start_date, end_date)
    all_records.extend(records)
    
    records = fetch_maude_data('device.generic_name:"dabigatran"', start_date, end_date)
    all_records.extend(records)
    
    print(f"\n  Total raw records fetched: {len(all_records)}")
    df = process_records(all_records)
    
    if len(df) > 0:
        df = df.drop_duplicates(subset=['mdr_report_key'])
        print(f"  After deduplication: {len(df)} unique MDRs")
    
    print(f"\n✓ Total unique MDRs: {len(df)}")
    return df, "boehringer_pradaxa_mdl_2385.xlsx"

# ============================================================================
# MAIN EXECUTION
# ============================================================================
if __name__ == "__main__":
    print("="*80)
    print(" FETCHING MAUDE DATA FOR 21 ADDITIONAL MDL CASES")
    print(" Expansion to 50-Case Benchmark Dataset")
    print(" Using CORRECT FDA API Syntax: device.FIELD:\"VALUE\"")
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
        df, filename = func()
        
        if len(df) > 0:
            filepath = f'benchmark_cases_expansion_21/{filename}'
            df.to_excel(filepath, index=False)
            print(f"  ✓ Saved to: {filepath}")
        
        count = len(df)
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
        print(f"{status} {result['case']:.<60} {result['records']:>6,} MDRs")
    
    print("="*80)
    print(f"Total Records Fetched: {total_records:,}")
    print(f"Total Cases: 21")
    print(f"Cases with Data: {sum(1 for r in results if r['records'] > 0)}")
    print(f"Time Elapsed: {elapsed_time/60:.1f} minutes")
    print(f"Combined Benchmark: 29 existing + 21 new = 50 cases")
    print("="*80)
    
    # Save summary
    with open('/tmp/fetch_21_summary.txt', 'w') as f:
        f.write("21 Additional Cases MAUDE Fetch Summary\n")
        f.write("="*80 + "\n\n")
        for result in results:
            status = "✓" if result['records'] > 0 else "✗"
            f.write(f"{status} {result['case']}: {result['records']:,} MDRs\n")
        f.write(f"\nTotal: {total_records:,} MDRs\n")
        f.write(f"Time: {elapsed_time/60:.1f} minutes\n")
    
    print("\n✓ Summary saved to /tmp/fetch_21_summary.txt")
