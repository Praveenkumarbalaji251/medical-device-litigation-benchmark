import pandas as pd
import json
from datetime import datetime

# Load the current JSON
with open('frontend/data/benchmark_cases_data_v48.json', 'r') as f:
    data = json.load(f)

# Load filing dates
with open('all_50_case_filing_dates.json', 'r') as f:
    filing_data = json.load(f)

# Map of Excel files to MDL numbers and device names
expansion_files = {
    '2974': {'file': 'paragard_iud_mdl_2974.xlsx', 'name': 'Paragard IUD'},
    '2996': {'file': 'zimmer_persona_knee_mdl_2996.xlsx', 'name': 'Zimmer Persona Knee System'},
    '2775': {'file': 'smith_nephew_birmingham_hip_mdl_2775.xlsx', 'name': 'Smith & Nephew Birmingham Hip Resurfacing'},
    '2666': {'file': '3m_bair_hugger_mdl_2666.xlsx', 'name': '3M Bair Hugger Warming Blanket'},
    '3032': {'file': 'medtronic_minimed_pump_mdl_3032.xlsx', 'name': 'Medtronic MiniMed Insulin Pump'},
    '2928': {'file': 'arthrex_hip_fixation_mdl_2928.xlsx', 'name': 'Arthrex Hip Fixation System'},
    '2787': {'file': 'olympus_duodenoscope_mdl_2787.xlsx', 'name': 'Olympus TJF-Q180V Duodenoscope'},
    '2868': {'file': 'abbott_heartmate_lvad_mdl_2868.xlsx', 'name': 'Abbott HeartMate II LVAD'},
    '2768': {'file': 'stryker_lfit_v40_mdl_2768.xlsx', 'name': 'Stryker LFIT V40 Femoral Head'},
    '2903': {'file': 'medtronic_synchromed_ii_mdl_2903.xlsx', 'name': 'Medtronic Synchromed II Pain Pump'},
    '3070': {'file': 'teleflex_ezio_mdl_3070.xlsx', 'name': 'Teleflex EZ-IO Intraosseous Device'},
    '2428': {'file': 'fresenius_granuflo_mdl_2428.xlsx', 'name': 'Fresenius GranuFlo/NaturaLyte'},
    '2904': {'file': 'boston_scientific_lotus_valve_mdl_2904.xlsx', 'name': 'Boston Scientific Lotus Edge Valve'},
    '2995': {'file': 'conformis_itotal_knee_mdl_2995.xlsx', 'name': 'Conformis iTotal CR Knee'},
    '2881': {'file': 'medtronic_bone_screw_mdl_2881.xlsx', 'name': 'Medtronic Infuse Bone Graft'},
    '2749': {'file': 'wright_profemur_hip_mdl_2749.xlsx', 'name': 'Wright Medical Profemur Hip System'},
    '2965': {'file': 'stryker_tmzf_hip_mdl_2965.xlsx', 'name': 'Stryker TMZF Modular Hip System'},
    '2848': {'file': 'nuvasive_xlif_mdl_2848.xlsx', 'name': 'NuVasive XLIF Spinal System'},
    'paradigm': {'file': 'medtronic_paradigm_pump.xlsx', 'name': 'Medtronic Paradigm Insulin Pump'},
}

print("=" * 80)
print("EXTRACTING DATE WINDOWS AND FILING DATES")
print("=" * 80)

case_updates = {}

for mdl, info in expansion_files.items():
    filepath = f'benchmark_cases_expansion_21/{info["file"]}'
    try:
        df = pd.read_excel(filepath)
        
        # Convert integer dates (YYYYMMDD) to datetime
        if 'date_received' in df.columns:
            # Convert from YYYYMMDD integer to datetime
            df['date_received'] = pd.to_datetime(df['date_received'], format='%Y%m%d', errors='coerce')
            
            min_date = df['date_received'].min()
            max_date = df['date_received'].max()
            
            if pd.notna(min_date) and pd.notna(max_date):
                date_window = f"{min_date.strftime('%b %Y')} to {max_date.strftime('%b %Y')}"
                
                # Find filing date from JSON
                filing_date = None
                for case_name, case_info in filing_data.items():
                    if case_info.get('mdl_number') == mdl:
                        filing_date = case_info.get('mdl_established', '')
                        break
                
                case_updates[mdl] = {
                    'name': info['name'],
                    'date_window': date_window,
                    'filing_date': filing_date,
                    'mdrs': len(df)
                }
                
                print(f"✓ MDL {mdl}: {info['name']}")
                print(f"  Data Window: {date_window}")
                print(f"  Filing Date: {filing_date or 'Not found'}")
                print(f"  MDRs: {len(df):,}")
                print()
            else:
                print(f"✗ MDL {mdl}: No valid dates found")
        else:
            print(f"✗ MDL {mdl}: No date_received column")
            
    except Exception as e:
        print(f"✗ MDL {mdl}: Error - {str(e)}")

print("=" * 80)
print(f"✓ Extracted {len(case_updates)} case updates")
print("=" * 80)

# Update the JSON
print("\nUpdating JSON...")
updated_count = 0

for case in data['cases']:
    mdl = str(case.get('mdl_number', ''))
    
    # Handle Paradigm Pump (no MDL number)
    if 'Paradigm' in case.get('name', '') and 'paradigm' in case_updates:
        update = case_updates['paradigm']
        case['name'] = update['name']
        case['data_window'] = update['date_window']
        if update['filing_date']:
            case['filing_date'] = update['filing_date']
        updated_count += 1
        print(f"✓ Updated: {update['name']}")
        
    elif mdl in case_updates:
        update = case_updates[mdl]
        case['name'] = update['name']
        case['data_window'] = update['date_window']
        if update['filing_date']:
            case['filing_date'] = update['filing_date']
        updated_count += 1
        print(f"✓ Updated: {update['name']} (MDL {mdl})")

print(f"\n✓ Updated {updated_count} cases")

# Save updated JSON
with open('frontend/data/benchmark_cases_data_v48.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"\n✅ SUCCESS: Updated JSON saved")
print(f"File: frontend/data/benchmark_cases_data_v48.json")
