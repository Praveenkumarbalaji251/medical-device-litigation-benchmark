"""
Fetch MAUDE Data for 10 Additional MDL Cases (2010+) - FIXED VERSION
Extracts FDA adverse event reports for 6-month period before MDL filing
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
            print(f"    → Exception: {e}")
            break
    
    return all_records


def process_records(records):
    """Process MAUDE records into structured data"""
    processed = []
    
    print(f"  Processing {len(records)} raw records...")
    
    for record in records:
        try:
            # Extract key fields
            mdr_report_key = record.get('mdr_report_key', 'UNKNOWN')
            date_received = record.get('date_received', '')
            
            # Event type
            event_type = record.get('event_type', 'Unknown')
            
            # Device info
            device = record.get('device', [{}])[0] if record.get('device') else {}
            brand_name = device.get('brand_name', '')
            generic_name = device.get('generic_name', '')
            manufacturer_d_name = device.get('manufacturer_d_name', '')
            
            # Patient info (patient is a list like device)
            patient = record.get('patient', [{}])[0] if record.get('patient') else {}
            patient_problems = patient.get('patient_problems', []) if patient else []
            
            processed.append({
                'mdr_report_key': mdr_report_key,
                'date_received': date_received,
                'event_type': event_type,
                'brand_name': brand_name,
                'generic_name': generic_name,
                'manufacturer': manufacturer_d_name,
                'patient_problems': ', '.join(patient_problems) if patient_problems else ''
            })
        except Exception as e:
            print(f"    Warning: Error processing record: {e}")
            continue
    
    print(f"  Processed {len(processed)} records successfully")
    
    if len(processed) == 0:
        print("  WARNING: No records processed!")
        return pd.DataFrame()
    
    df = pd.DataFrame(processed)
    print(f"  DataFrame created: {len(df)} rows, {len(df.columns)} columns")
    return df


# ==============================================================================
# CASE 1: 3M Combat Arms Earplugs (MDL 2885)
# ==============================================================================
def fetch_3m_earplugs():
    print("\n" + "="*80)
    print("CASE 1: 3M Combat Arms Earplugs (MDL 2885)")
    print("="*80)
    
    # 6-month window: Oct 2018 - Apr 2019
    start_date = "20181001"
    end_date = "20190401"
    
    all_records = []
    
    # Search 1: Brand name
    records = fetch_maude_data('device.brand_name:"Combat+Arms"', start_date, end_date)
    all_records.extend(records)
    
    # Search 2: Generic name
    records = fetch_maude_data('device.generic_name:"earplug"', start_date, end_date)
    all_records.extend(records)
    
    # Search 3: Manufacturer
    records = fetch_maude_data('device.manufacturer_d_name:"3M"', start_date, end_date)
    all_records.extend(records)
    
    print(f"\n  Total raw records fetched: {len(all_records)}")
    
    # Process and deduplicate
    df = process_records(all_records)
    
    if len(df) > 0:
        df = df.drop_duplicates(subset=['mdr_report_key'])
        print(f"  After deduplication: {len(df)} unique MDRs")
    
    print(f"\n✓ Total unique MDRs: {len(df)}")
    return df, "3m_combat_arms_earplugs_mdl_2885.xlsx"


# ==============================================================================
# CASE 2: Medtronic Sprint Quattro Leads (MDL 2187)
# ==============================================================================
def fetch_medtronic_sprint_quattro():
    print("\n" + "="*80)
    print("CASE 2: Medtronic Sprint Quattro Leads (MDL 2187)")
    print("="*80)
    
    # 6-month window: Aug 2009 - Feb 2010
    start_date = "20090824"
    end_date = "20100224"
    
    all_records = []
    
    # Search 1: Sprint Quattro
    records = fetch_maude_data('device.brand_name:"Sprint+Quattro"', start_date, end_date)
    all_records.extend(records)
    
    # Search 2: Quattro
    records = fetch_maude_data('device.brand_name:"Quattro"', start_date, end_date)
    all_records.extend(records)
    
    # Search 3: Medtronic + cardiac lead
    records = fetch_maude_data('device.manufacturer_d_name:"Medtronic"+AND+device.generic_name:"lead"', start_date, end_date)
    all_records.extend(records)
    
    print(f"\n  Total raw records fetched: {len(all_records)}")
    
    df = process_records(all_records)
    
    if len(df) > 0:
        df = df.drop_duplicates(subset=['mdr_report_key'])
        print(f"  After deduplication: {len(df)} unique MDRs")
    
    print(f"\n✓ Total unique MDRs: {len(df)}")
    return df, "medtronic_sprint_quattro_leads_mdl_2187.xlsx"


# ==============================================================================
# CASE 3: Medtronic Infuse Bone Graft (MDL 2431)
# ==============================================================================
def fetch_medtronic_infuse():
    print("\n" + "="*80)
    print("CASE 3: Medtronic Infuse Bone Graft (MDL 2431)")
    print("="*80)
    
    # 6-month window: Aug 2011 - Feb 2012
    start_date = "20110822"
    end_date = "20120222"
    
    all_records = []
    
    # Search 1: Infuse
    records = fetch_maude_data('device.brand_name:"Infuse"', start_date, end_date)
    all_records.extend(records)
    
    # Search 2: BMP (Bone Morphogenetic Protein)
    records = fetch_maude_data('device.generic_name:"bone+morphogenetic+protein"', start_date, end_date)
    all_records.extend(records)
    
    # Search 3: Medtronic + bone graft
    records = fetch_maude_data('device.manufacturer_d_name:"Medtronic"+AND+device.generic_name:"bone+graft"', start_date, end_date)
    all_records.extend(records)
    
    print(f"\n  Total raw records fetched: {len(all_records)}")
    
    df = process_records(all_records)
    
    if len(df) > 0:
        df = df.drop_duplicates(subset=['mdr_report_key'])
        print(f"  After deduplication: {len(df)} unique MDRs")
    
    print(f"\n✓ Total unique MDRs: {len(df)}")
    return df, "medtronic_infuse_bone_graft_mdl_2431.xlsx"


# ==============================================================================
# CASE 4: Biomet M2a Magnum Hip (MDL 2652)
# ==============================================================================
def fetch_biomet_m2a():
    print("\n" + "="*80)
    print("CASE 4: Biomet M2a Magnum Hip (MDL 2652)")
    print("="*80)
    
    # 6-month window: Jun 2012 - Dec 2012
    start_date = "20120617"
    end_date = "20121217"
    
    all_records = []
    
    # Search 1: M2a Magnum
    records = fetch_maude_data('device.brand_name:"M2a+Magnum"', start_date, end_date)
    all_records.extend(records)
    
    # Search 2: M2a
    records = fetch_maude_data('device.brand_name:"M2a"', start_date, end_date)
    all_records.extend(records)
    
    # Search 3: Biomet + hip
    records = fetch_maude_data('device.manufacturer_d_name:"Biomet"+AND+device.generic_name:"hip"', start_date, end_date)
    all_records.extend(records)
    
    print(f"\n  Total raw records fetched: {len(all_records)}")
    
    df = process_records(all_records)
    
    if len(df) > 0:
        df = df.drop_duplicates(subset=['mdr_report_key'])
        print(f"  After deduplication: {len(df)} unique MDRs")
    
    print(f"\n✓ Total unique MDRs: {len(df)}")
    return df, "biomet_m2a_magnum_hip_mdl_2652.xlsx"


# ==============================================================================
# CASE 5: Power Morcellator (MDL 2586)
# ==============================================================================
def fetch_power_morcellator():
    print("\n" + "="*80)
    print("CASE 5: Power Morcellator (MDL 2586)")
    print("="*80)
    
    # 6-month window: Apr 2014 - Oct 2014
    start_date = "20140406"
    end_date = "20141006"
    
    all_records = []
    
    # Search 1: Morcellator
    records = fetch_maude_data('device.generic_name:"morcellator"', start_date, end_date)
    all_records.extend(records)
    
    # Search 2: Brand names
    records = fetch_maude_data('device.brand_name:"morcellator"', start_date, end_date)
    all_records.extend(records)
    
    # Search 3: Laparoscopic power morcellator
    records = fetch_maude_data('device.generic_name:"laparoscopic"', start_date, end_date)
    all_records.extend(records)
    
    print(f"\n  Total raw records fetched: {len(all_records)}")
    
    df = process_records(all_records)
    
    if len(df) > 0:
        df = df.drop_duplicates(subset=['mdr_report_key'])
        print(f"  After deduplication: {len(df)} unique MDRs")
    
    print(f"\n✓ Total unique MDRs: {len(df)}")
    return df, "power_morcellator_mdl_2586.xlsx"


# ==============================================================================
# CASE 6: Nevro Spinal Cord Stimulator (MDL 2876)
# ==============================================================================
def fetch_nevro_scs():
    print("\n" + "="*80)
    print("CASE 6: Nevro Spinal Cord Stimulator (MDL 2876)")
    print("="*80)
    
    # 6-month window: Aug 2018 - Feb 2019
    start_date = "20180806"
    end_date = "20190206"
    
    all_records = []
    
    # Search 1: Nevro
    records = fetch_maude_data('device.manufacturer_d_name:"Nevro"', start_date, end_date)
    all_records.extend(records)
    
    # Search 2: HF10
    records = fetch_maude_data('device.brand_name:"HF10"', start_date, end_date)
    all_records.extend(records)
    
    # Search 3: Senza
    records = fetch_maude_data('device.brand_name:"Senza"', start_date, end_date)
    all_records.extend(records)
    
    print(f"\n  Total raw records fetched: {len(all_records)}")
    
    df = process_records(all_records)
    
    if len(df) > 0:
        df = df.drop_duplicates(subset=['mdr_report_key'])
        print(f"  After deduplication: {len(df)} unique MDRs")
    
    print(f"\n✓ Total unique MDRs: {len(df)}")
    return df, "nevro_spinal_cord_stimulator_mdl_2876.xlsx"


# ==============================================================================
# CASE 7: da Vinci Surgical Robot (MDL 2920)
# ==============================================================================
def fetch_davinci_robot():
    print("\n" + "="*80)
    print("CASE 7: da Vinci Surgical Robot (MDL 2920)")
    print("="*80)
    
    # 6-month window: Feb 2013 - Aug 2013
    start_date = "20130209"
    end_date = "20130809"
    
    all_records = []
    
    # Search 1: da Vinci
    records = fetch_maude_data('device.brand_name:"da+Vinci"', start_date, end_date)
    all_records.extend(records)
    
    # Search 2: Intuitive Surgical
    records = fetch_maude_data('device.manufacturer_d_name:"Intuitive+Surgical"', start_date, end_date)
    all_records.extend(records)
    
    # Search 3: robotic surgical
    records = fetch_maude_data('device.generic_name:"robotic"', start_date, end_date)
    all_records.extend(records)
    
    print(f"\n  Total raw records fetched: {len(all_records)}")
    
    df = process_records(all_records)
    
    if len(df) > 0:
        df = df.drop_duplicates(subset=['mdr_report_key'])
        print(f"  After deduplication: {len(df)} unique MDRs")
    
    print(f"\n✓ Total unique MDRs: {len(df)}")
    return df, "davinci_surgical_robot_mdl_2920.xlsx"


# ==============================================================================
# CASE 8: Cook Zenith Aortic Graft (MDL 2846)
# ==============================================================================
def fetch_cook_zenith():
    print("\n" + "="*80)
    print("CASE 8: Cook Zenith Aortic Graft (MDL 2846)")
    print("="*80)
    
    # 6-month window: May 2015 - Nov 2015
    start_date = "20150505"
    end_date = "20151105"
    
    all_records = []
    
    # Search 1: Zenith
    records = fetch_maude_data('device.brand_name:"Zenith"', start_date, end_date)
    all_records.extend(records)
    
    # Search 2: Cook + aortic
    records = fetch_maude_data('device.manufacturer_d_name:"Cook"+AND+device.generic_name:"aortic"', start_date, end_date)
    all_records.extend(records)
    
    # Search 3: Cook + graft
    records = fetch_maude_data('device.manufacturer_d_name:"Cook"+AND+device.generic_name:"graft"', start_date, end_date)
    all_records.extend(records)
    
    print(f"\n  Total raw records fetched: {len(all_records)}")
    
    df = process_records(all_records)
    
    if len(df) > 0:
        df = df.drop_duplicates(subset=['mdr_report_key'])
        print(f"  After deduplication: {len(df)} unique MDRs")
    
    print(f"\n✓ Total unique MDRs: {len(df)}")
    return df, "cook_zenith_aortic_graft_mdl_2846.xlsx"


# ==============================================================================
# CASE 9: STAAR Visian ICL (No MDL, but major class action)
# ==============================================================================
def fetch_staar_icl():
    print("\n" + "="*80)
    print("CASE 9: STAAR Visian ICL")
    print("="*80)
    
    # 6-month window: Dec 2013 - Jun 2014
    start_date = "20131218"
    end_date = "20140618"
    
    all_records = []
    
    # Search 1: Visian
    records = fetch_maude_data('device.brand_name:"Visian"', start_date, end_date)
    all_records.extend(records)
    
    # Search 2: STAAR
    records = fetch_maude_data('device.manufacturer_d_name:"STAAR"', start_date, end_date)
    all_records.extend(records)
    
    # Search 3: ICL
    records = fetch_maude_data('device.brand_name:"ICL"', start_date, end_date)
    all_records.extend(records)
    
    print(f"\n  Total raw records fetched: {len(all_records)}")
    
    df = process_records(all_records)
    
    if len(df) > 0:
        df = df.drop_duplicates(subset=['mdr_report_key'])
        print(f"  After deduplication: {len(df)} unique MDRs")
    
    print(f"\n✓ Total unique MDRs: {len(df)}")
    return df, "staar_visian_icl.xlsx"


# ==============================================================================
# CASE 10: Medtronic Pain Pump (MDL 2662)
# ==============================================================================
def fetch_medtronic_pain_pump():
    print("\n" + "="*80)
    print("CASE 10: Medtronic Pain Pump (MDL 2662)")
    print("="*80)
    
    # 6-month window: Jul 2009 - Jan 2010
    start_date = "20090715"
    end_date = "20100115"
    
    all_records = []
    
    # Search 1: SynchroMed
    records = fetch_maude_data('device.brand_name:"SynchroMed"', start_date, end_date)
    all_records.extend(records)
    
    # Search 2: Medtronic + infusion pump
    records = fetch_maude_data('device.manufacturer_d_name:"Medtronic"+AND+device.generic_name:"infusion+pump"', start_date, end_date)
    all_records.extend(records)
    
    # Search 3: Pain pump
    records = fetch_maude_data('device.generic_name:"pump"', start_date, end_date)
    all_records.extend(records)
    
    print(f"\n  Total raw records fetched: {len(all_records)}")
    
    df = process_records(all_records)
    
    if len(df) > 0:
        df = df.drop_duplicates(subset=['mdr_report_key'])
        print(f"  After deduplication: {len(df)} unique MDRs")
    
    print(f"\n✓ Total unique MDRs: {len(df)}")
    return df, "medtronic_pain_pump_mdl_2662.xlsx"


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================
def main():
    print("\n" + "="*80)
    print(" FDA MAUDE DATA FETCH - 10 EXPANSION CASES (2010+)")
    print("="*80)
    
    # Create output directory
    output_dir = "benchmark_cases_expansion"
    os.makedirs(output_dir, exist_ok=True)
    print(f"\nOutput directory: {output_dir}/")
    
    # List of fetch functions
    fetch_functions = [
        fetch_3m_earplugs,
        fetch_medtronic_sprint_quattro,
        fetch_medtronic_infuse,
        fetch_biomet_m2a,
        fetch_power_morcellator,
        fetch_nevro_scs,
        fetch_davinci_robot,
        fetch_cook_zenith,
        fetch_staar_icl,
        fetch_medtronic_pain_pump
    ]
    
    # Fetch and save each case
    results = []
    for fetch_func in fetch_functions:
        try:
            df, filename = fetch_func()
            
            if len(df) > 0:
                filepath = os.path.join(output_dir, filename)
                df.to_excel(filepath, index=False)
                print(f"✓ Saved: {filepath}")
                print(f"  Rows: {len(df)}, Columns: {len(df.columns)}")
                
                results.append({
                    'case': filename.replace('.xlsx', ''),
                    'mdrs': len(df),
                    'file': filepath
                })
            else:
                print(f"✗ No data for {filename}")
                results.append({
                    'case': filename.replace('.xlsx', ''),
                    'mdrs': 0,
                    'file': 'NOT CREATED (no data)'
                })
                
        except Exception as e:
            print(f"✗ Error: {e}")
            results.append({
                'case': fetch_func.__name__,
                'mdrs': 0,
                'file': f'ERROR: {e}'
            })
        
        time.sleep(1)
    
    # Summary
    print("\n" + "="*80)
    print(" FETCH SUMMARY")
    print("="*80)
    
    total_mdrs = 0
    for result in results:
        print(f"{result['case']:50s} {result['mdrs']:6d} MDRs")
        total_mdrs += result['mdrs']
    
    print(f"\n{'TOTAL':50s} {total_mdrs:6d} MDRs")
    print("="*80)


if __name__ == "__main__":
    main()
