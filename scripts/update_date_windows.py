import pandas as pd
import json
from pathlib import Path
from datetime import datetime

# Load the current JSON
with open('frontend/data/benchmark_cases_data_v48.json', 'r') as f:
    data = json.load(f)

# Map of Excel files to MDL numbers
expansion_files = {
    '2974': 'paragard_iud_mdl_2974.xlsx',
    '2996': 'zimmer_persona_knee_mdl_2996.xlsx',
    '2775': 'smith_nephew_birmingham_hip_mdl_2775.xlsx',
    '2666': '3m_bair_hugger_mdl_2666.xlsx',
    '3032': 'medtronic_minimed_pump_mdl_3032.xlsx',
    '2928': 'arthrex_hip_fixation_mdl_2928.xlsx',
    '2787': 'olympus_duodenoscope_mdl_2787.xlsx',
    '2868': 'abbott_heartmate_lvad_mdl_2868.xlsx',
    '2768': 'stryker_lfit_v40_mdl_2768.xlsx',
    '2903': 'medtronic_synchromed_ii_mdl_2903.xlsx',
    '3070': 'teleflex_ezio_mdl_3070.xlsx',
    '2428': 'fresenius_granuflo_mdl_2428.xlsx',
    '2904': 'boston_scientific_lotus_valve_mdl_2904.xlsx',
    '2995': 'conformis_itotal_knee_mdl_2995.xlsx',
    '2881': 'medtronic_bone_screw_mdl_2881.xlsx',
    '2749': 'wright_profemur_hip_mdl_2749.xlsx',
    '2965': 'stryker_tmzf_hip_mdl_2965.xlsx',
    '2848': 'nuvasive_xlif_mdl_2848.xlsx',
    'paradigm': 'medtronic_paradigm_pump.xlsx',
}

print("Extracting date windows from Excel files...")
date_windows = {}

for mdl, filename in expansion_files.items():
    filepath = f'benchmark_cases_expansion_21/{filename}'
    try:
        df = pd.read_excel(filepath)
        
        # Get date range from date_received column
        if 'date_received' in df.columns:
            df['date_received'] = pd.to_datetime(df['date_received'], errors='coerce')
            min_date = df['date_received'].min()
            max_date = df['date_received'].max()
            
            if pd.notna(min_date) and pd.notna(max_date):
                date_window = f"{min_date.strftime('%b %Y')} to {max_date.strftime('%b %Y')}"
                date_windows[mdl] = date_window
                print(f"✓ MDL {mdl}: {date_window} ({len(df)} MDRs)")
            else:
                print(f"✗ MDL {mdl}: No valid dates found")
        else:
            print(f"✗ MDL {mdl}: No date_received column")
            
    except Exception as e:
        print(f"✗ MDL {mdl}: Error - {str(e)}")

print(f"\n✓ Extracted {len(date_windows)} date windows")

# Update the JSON with date windows
print("\nUpdating JSON with date windows...")
updated_count = 0

for case in data['cases']:
    mdl = str(case.get('mdl_number', ''))
    
    # Handle the Paradigm Pump case (no MDL number)
    if case.get('device_name') == 'Medtronic Paradigm Pump' and 'paradigm' in date_windows:
        case['data_window'] = date_windows['paradigm']
        updated_count += 1
        print(f"✓ Updated: {case['device_name']} - {date_windows['paradigm']}")
    elif mdl in date_windows:
        case['data_window'] = date_windows[mdl]
        updated_count += 1
        print(f"✓ Updated: {case['device_name']} (MDL {mdl}) - {date_windows[mdl]}")

print(f"\n✓ Updated {updated_count} cases with date windows")

# Save updated JSON
with open('frontend/data/benchmark_cases_data_v48.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"\n✅ SUCCESS: Updated JSON saved to frontend/data/benchmark_cases_data_v48.json")
print(f"Total cases: {len(data['cases'])}")
print(f"Cases with date windows: {sum(1 for c in data['cases'] if c.get('data_window') != 'N/A to N/A')}")
