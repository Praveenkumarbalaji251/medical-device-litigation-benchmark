"""
Integrate 19 additional cases into the benchmark dataset
Creates: benchmark_cases_data_v48.json (29 existing + 19 new = 48 cases)
"""

import pandas as pd
import json
from datetime import datetime
from collections import Counter
import os

print("="*80)
print(" INTEGRATING 19 NEW CASES INTO BENCHMARK DATASET")
print(" Creating 48-Case Benchmark (29 existing + 19 new)")
print("="*80)

# Load existing 29-case dataset
print("\n1. Loading existing 29-case dataset...")
with open('frontend/data/benchmark_cases_data_v29.json', 'r') as f:
    existing_data = json.load(f)

print(f"   ✓ Loaded {existing_data['total_cases']} existing cases")

# Process 19 new cases
print("\n2. Processing 19 new case files...")

new_cases_data = []
directory = 'benchmark_cases_expansion_21'

# Case metadata mapping
case_metadata = {
    'paragard_iud_mdl_2974.xlsx': {
        'case_name': 'Paragard IUD',
        'mdl_number': '2974',
        'status': 'Active',
        'category': 'Contraceptive Device',
        'manufacturer': 'Teva/CooperSurgical'
    },
    'zimmer_persona_knee_mdl_2996.xlsx': {
        'case_name': 'Zimmer Persona Knee',
        'mdl_number': '2996',
        'status': 'Active',
        'category': 'Orthopedic Implant',
        'manufacturer': 'Zimmer Biomet'
    },
    'smith_nephew_birmingham_hip_mdl_2775.xlsx': {
        'case_name': 'Smith & Nephew Birmingham Hip',
        'mdl_number': '2775',
        'status': 'Active',
        'category': 'Orthopedic Implant',
        'manufacturer': 'Smith & Nephew'
    },
    '3m_bair_hugger_mdl_2666.xlsx': {
        'case_name': '3M Bair Hugger',
        'mdl_number': '2666',
        'status': 'Active',
        'category': 'Surgical Equipment',
        'manufacturer': '3M/Arizant'
    },
    'medtronic_minimed_pump_mdl_3032.xlsx': {
        'case_name': 'Medtronic MiniMed Insulin Pump',
        'mdl_number': '3032',
        'status': 'Active',
        'category': 'Diabetes Device',
        'manufacturer': 'Medtronic'
    },
    'arthrex_hip_fixation_mdl_2928.xlsx': {
        'case_name': 'Arthrex Hip Fixation',
        'mdl_number': '2928',
        'status': 'Active',
        'category': 'Orthopedic Device',
        'manufacturer': 'Arthrex'
    },
    'olympus_duodenoscope_mdl_2787.xlsx': {
        'case_name': 'Olympus Duodenoscope',
        'mdl_number': '2787',
        'status': 'Active',
        'category': 'Endoscopic Device',
        'manufacturer': 'Olympus'
    },
    'abbott_heartmate_lvad_mdl_2868.xlsx': {
        'case_name': 'Abbott HeartMate II LVAD',
        'mdl_number': '2868',
        'status': 'Active',
        'category': 'Cardiac Device',
        'manufacturer': 'Abbott'
    },
    'stryker_lfit_v40_mdl_2768.xlsx': {
        'case_name': 'Stryker LFIT V40 Femoral Head',
        'mdl_number': '2768',
        'status': 'Active',
        'category': 'Orthopedic Implant',
        'manufacturer': 'Stryker'
    },
    'medtronic_synchromed_ii_mdl_2903.xlsx': {
        'case_name': 'Medtronic Synchromed II Pain Pump',
        'mdl_number': '2903',
        'status': 'Active',
        'category': 'Pain Management',
        'manufacturer': 'Medtronic'
    },
    'teleflex_ezio_mdl_3070.xlsx': {
        'case_name': 'Teleflex EZ-IO Device',
        'mdl_number': '3070',
        'status': 'Active',
        'category': 'Emergency Medical Device',
        'manufacturer': 'Teleflex'
    },
    'fresenius_granuflo_mdl_2428.xlsx': {
        'case_name': 'Fresenius GranuFlo/NaturaLyte',
        'mdl_number': '2428',
        'status': 'Settled',
        'category': 'Dialysis Product',
        'manufacturer': 'Fresenius',
        'settlement': 250000000
    },
    'boston_scientific_lotus_valve_mdl_2904.xlsx': {
        'case_name': 'Boston Scientific Lotus Edge Valve',
        'mdl_number': '2904',
        'status': 'Active',
        'category': 'Cardiac Device',
        'manufacturer': 'Boston Scientific'
    },
    'conformis_itotal_knee_mdl_2995.xlsx': {
        'case_name': 'Conformis iTotal Knee',
        'mdl_number': '2995',
        'status': 'Active',
        'category': 'Orthopedic Implant',
        'manufacturer': 'Conformis'
    },
    'medtronic_bone_screw_mdl_2881.xlsx': {
        'case_name': 'Medtronic Bone Screw',
        'mdl_number': '2881',
        'status': 'Active',
        'category': 'Spinal Device',
        'manufacturer': 'Medtronic'
    },
    'wright_profemur_hip_mdl_2749.xlsx': {
        'case_name': 'Wright Profemur Hip',
        'mdl_number': '2749',
        'status': 'Active',
        'category': 'Orthopedic Implant',
        'manufacturer': 'Wright Medical'
    },
    'stryker_tmzf_hip_mdl_2965.xlsx': {
        'case_name': 'Stryker Trident/Accolade TMZF Hip',
        'mdl_number': '2965',
        'status': 'Active',
        'category': 'Orthopedic Implant',
        'manufacturer': 'Stryker'
    },
    'nuvasive_xlif_mdl_2848.xlsx': {
        'case_name': 'NuVasive XLIF Implant',
        'mdl_number': '2848',
        'status': 'Active',
        'category': 'Spinal Device',
        'manufacturer': 'NuVasive'
    },
    'medtronic_paradigm_pump.xlsx': {
        'case_name': 'Medtronic Paradigm Insulin Pump',
        'mdl_number': None,
        'status': 'Active',
        'category': 'Diabetes Device',
        'manufacturer': 'Medtronic'
    }
}

for filename in sorted(case_metadata.keys()):
    filepath = os.path.join(directory, filename)
    
    if not os.path.exists(filepath):
        print(f"   ⚠ Skipping {filename} (not found)")
        continue
    
    print(f"\n   Processing: {filename}")
    
    try:
        df = pd.read_excel(filepath)
        metadata = case_metadata[filename]
        
        # Aggregate by month
        df['date_received'] = pd.to_datetime(df['date_received'], format='%Y%m%d', errors='coerce')
        df['month'] = df['date_received'].dt.to_period('M').astype(str)
        
        monthly_counts = df.groupby('month').size().to_dict()
        
        # Count event types (death, injury, malfunction)
        death_count = df[df['event_type'].str.contains('Death', case=False, na=False)].shape[0]
        injury_count = df[df['event_type'].str.contains('Injury', case=False, na=False)].shape[0]
        malfunction_count = df[df['event_type'].str.contains('Malfunction', case=False, na=False)].shape[0]
        
        # Create monthly data array
        monthly_data = []
        for month, count in sorted(monthly_counts.items()):
            month_df = df[df['month'] == month]
            monthly_data.append({
                'month': month,
                'total': int(count),
                'death': int(month_df[month_df['event_type'].str.contains('Death', case=False, na=False)].shape[0]),
                'injury': int(month_df[month_df['event_type'].str.contains('Injury', case=False, na=False)].shape[0]),
                'malfunction': int(month_df[month_df['event_type'].str.contains('Malfunction', case=False, na=False)].shape[0])
            })
        
        case_data = {
            'case_name': metadata['case_name'],
            'mdl_number': metadata['mdl_number'],
            'status': metadata['status'],
            'category': metadata['category'],
            'manufacturer': metadata['manufacturer'],
            'total_mdrs': len(df),
            'summary': {
                'total_deaths': int(death_count),
                'total_injuries': int(injury_count),
                'total_malfunctions': int(malfunction_count)
            },
            'monthly_data': monthly_data
        }
        
        if 'settlement' in metadata:
            case_data['settlement'] = metadata['settlement']
        
        new_cases_data.append(case_data)
        
        print(f"      ✓ {len(df):,} MDRs | Deaths: {death_count} | Injuries: {injury_count}")
        
    except Exception as e:
        print(f"      ✗ Error: {str(e)}")

print(f"\n   ✓ Successfully processed {len(new_cases_data)} new cases")

# Merge with existing data
print("\n3. Merging datasets...")

all_cases = existing_data['cases'] + new_cases_data

# Calculate new totals
total_cases = len(all_cases)
active_cases = sum(1 for c in all_cases if c.get('status') == 'Active')
settled_cases = sum(1 for c in all_cases if c.get('status') == 'Settled')
total_mdrs_new = sum([c.get('total_mdrs', 0) for c in new_cases_data])

print(f"   ✓ Total cases: {total_cases}")
print(f"   ✓ Active: {active_cases} | Settled: {settled_cases}")
print(f"   ✓ New MDRs added: {total_mdrs_new:,}")

# Create new dataset
new_dataset = {
    'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'total_cases': total_cases,
    'active_cases': active_cases,
    'settled_cases': settled_cases,
    'total_mdrs': total_mdrs_new,  # Only new MDRs in this batch
    'cases': all_cases
}

# Save to file
output_file = 'frontend/data/benchmark_cases_data_v48.json'
print(f"\n4. Saving to {output_file}...")

with open(output_file, 'w') as f:
    json.dump(new_dataset, f, indent=2)

file_size = os.path.getsize(output_file) / 1024 / 1024
print(f"   ✓ Saved {file_size:.2f} MB")

print("\n" + "="*80)
print(" INTEGRATION COMPLETE")
print("="*80)
print(f"✓ Total Cases: {total_cases} (29 existing + {len(new_cases_data)} new)")
print(f"✓ New MDRs: {total_mdrs_new:,}")
print(f"✓ File: {output_file} ({file_size:.2f} MB)")
print(f"✓ Active Cases: {active_cases}")
print(f"✓ Settled Cases: {settled_cases}")
print("="*80)
