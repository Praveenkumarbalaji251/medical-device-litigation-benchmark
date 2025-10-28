#!/usr/bin/env python3
"""
Process benchmark case data for frontend visualization
Extracts: Case date, Monthly injury/death/malfunction counts, Product codes
"""

import pandas as pd
import json
import os
from datetime import datetime

# Define case metadata for ACTIVE cases
active_cases_metadata = {
    'philips_cpap_mdl_3014.xlsx': {
        'name': 'Philips CPAP/BiPAP',
        'mdl': '3014',
        'filing_date': '2021-10-08',
        'court': 'W.D. Pennsylvania',
        'status': 'Active'
    },
    'bard_powerport_mdl_3081.xlsx': {
        'name': 'Bard PowerPort',
        'mdl': '3081',
        'filing_date': '2023-08-15',
        'court': 'D. Arizona',
        'status': 'Active'
    },
    'hernia_mesh_(bard_davol)_mdl_2846.xlsx': {
        'name': 'Hernia Mesh (Bard/Davol)',
        'mdl': '2846',
        'filing_date': '2018-08-02',
        'court': 'S.D. Ohio',
        'status': 'Active'
    },
    'exactech_joint_implants_mdl_3044.xlsx': {
        'name': 'Exactech Joint Implants',
        'mdl': '3044',
        'filing_date': '2022-06-14',
        'court': 'E.D. New York',
        'status': 'Active'
    },
    'allergan_biocell_mdl_2921.xlsx': {
        'name': 'Allergan BIOCELL',
        'mdl': '2921',
        'filing_date': '2019-12-18',
        'court': 'D. New Jersey',
        'status': 'Active'
    }
}

# Define case metadata for SETTLED cases
settled_cases_metadata = {
    'transvaginal_mesh_(ethicon_j&j)_mdl_2327.xlsx': {
        'name': 'Transvaginal Mesh (Ethicon/J&J)',
        'mdl': '2327',
        'filing_date': '2012-04-12',
        'court': 'S.D. West Virginia',
        'status': 'Settled',
        'settlement': '$8+ billion (2014-2019)'
    },
    'depuy_asr_hip_implant_mdl_2197.xlsx': {
        'name': 'DePuy ASR Hip Implant',
        'mdl': '2197',
        'filing_date': '2010-09-23',
        'court': 'N.D. Ohio',
        'status': 'Settled',
        'settlement': '$4+ billion (2013)'
    },
    'stryker_rejuvenate_hip_implant_mdl_2441.xlsx': {
        'name': 'Stryker Rejuvenate Hip',
        'mdl': '2441',
        'filing_date': '2012-12-20',
        'court': 'D. Minnesota',
        'status': 'Settled',
        'settlement': '$1.4+ billion (2014)'
    },
    'zimmer_durom_cup_hip_implant_mdl_2158.xlsx': {
        'name': 'Zimmer Durom Cup Hip',
        'mdl': '2158',
        'filing_date': '2010-05-12',
        'court': 'D. New Jersey',
        'status': 'Settled',
        'settlement': '$228 million (2013)'
    },
    'boston_scientific_pelvic_mesh_mdl_2326.xlsx': {
        'name': 'Boston Scientific Pelvic Mesh',
        'mdl': '2326',
        'filing_date': '2012-02-17',
        'court': 'S.D. West Virginia',
        'status': 'Settled',
        'settlement': '$189 million (2015)'
    }
}

# Define case metadata for ADDITIONAL ACTIVE cases
additional_active_metadata = {
    'bard_ivc_filters_mdl_2641.xlsx': {
        'name': 'IVC Filters (C.R. Bard)',
        'mdl': '2641',
        'filing_date': '2015-08-03',
        'court': 'D. Arizona',
        'status': 'Active'
    },
    'cook_ivc_filters_mdl_2570.xlsx': {
        'name': 'Cook Medical IVC Filters',
        'mdl': '2570',
        'filing_date': '2014-08-28',
        'court': 'S.D. Indiana',
        'status': 'Active'
    },
    'zimmer_ml_taper_hip_mdl_2716.xlsx': {
        'name': 'Zimmer M/L Taper Hip',
        'mdl': '2716',
        'filing_date': '2016-03-24',
        'court': 'N.D. Indiana',
        'status': 'Active'
    },
    'essure_birth_control_mdl_2325.xlsx': {
        'name': 'Essure Birth Control',
        'mdl': '2325',
        'filing_date': '2013-09-03',
        'court': 'E.D. Pennsylvania',
        'status': 'Active'
    },
    'physiomesh_ethicon_mdl_2782.xlsx': {
        'name': 'Physiomesh (Ethicon)',
        'mdl': '2782',
        'filing_date': '2016-11-07',
        'court': 'N.D. Georgia',
        'status': 'Active'
    },
    'atrium_cqur_mesh_mdl_2753.xlsx': {
        'name': 'Atrium C-QUR Mesh',
        'mdl': '2753',
        'filing_date': '2016-08-23',
        'court': 'D. New Hampshire',
        'status': 'Active'
    }
}

# Define case metadata for ADDITIONAL SETTLED cases
additional_settled_metadata = {
    'depuy_pinnacle_hip_mdl_2244.xlsx': {
        'name': 'DePuy Pinnacle Hip',
        'mdl': '2244',
        'filing_date': '2011-03-31',
        'court': 'N.D. Texas',
        'status': 'Settled',
        'settlement': '$1+ billion (2013-2016)'
    },
    'wright_conserve_hip_mdl_2329.xlsx': {
        'name': 'Wright Conserve Hip',
        'mdl': '2329',
        'filing_date': '2012-05-04',
        'court': 'N.D. Georgia',
        'status': 'Settled',
        'settlement': '$240 million (2015)'
    },
    'medtronic_sprint_fidelis_mdl_1905.xlsx': {
        'name': 'Medtronic Sprint Fidelis',
        'mdl': '1905',
        'filing_date': '2008-06-26',
        'court': 'D. Minnesota',
        'status': 'Settled',
        'settlement': '$268 million (2010-2012)'
    }
}

# Combine all
cases_metadata = {**active_cases_metadata, **settled_cases_metadata, **additional_active_metadata, **additional_settled_metadata}

def categorize_event_type(event_type_str):
    """Categorize event types into Injury, Death, Malfunction"""
    if pd.isna(event_type_str):
        return 'Unknown'
    
    # Remove commas and spaces (handle the "M, a, l, f, u, n, c, t, i, o, n" format)
    event_type_clean = str(event_type_str).replace(',', '').replace(' ', '').lower()
    
    if 'death' in event_type_clean or event_type_clean == 'de':
        return 'Death'
    elif 'injury' in event_type_clean or event_type_clean == 'in':
        return 'Injury'
    elif 'malfunction' in event_type_clean or event_type_clean == 'ma':
        return 'Malfunction'
    else:
        return 'Other'

def process_case_file(filepath, metadata):
    """Process a single case file and extract monthly statistics"""
    
    print(f"\nProcessing: {metadata['name']}")
    
    try:
        # Read the Excel file
        df = pd.read_excel(filepath, sheet_name='All Reports', engine='openpyxl')
        
        # Convert date_received to datetime
        df['date_received'] = pd.to_datetime(df['date_received'], format='%Y%m%d', errors='coerce')
        
        # Categorize events
        df['event_category'] = df['event_type'].apply(categorize_event_type)
        
        # Extract product identifiers (generic names and device class)
        product_info = []
        if 'generic_name' in df.columns:
            top_generics = df['generic_name'].value_counts().head(10)
            for name, count in top_generics.items():
                if pd.notna(name) and name:
                    product_info.append(f"{name} ({count})")
        
        # Get device classes
        device_classes = []
        if 'device_class' in df.columns:
            classes = df['device_class'].value_counts()
            for cls, count in classes.items():
                if pd.notna(cls):
                    device_classes.append(f"Class {cls}: {count}")
        
        # Group by month and event category
        df['year_month'] = df['date_received'].dt.to_period('M')
        
        monthly_stats = df.groupby(['year_month', 'event_category']).size().unstack(fill_value=0)
        
        # Convert to dictionary format for JSON with MoM calculations
        monthly_data = []
        prev_total = None
        prev_death = None
        prev_injury = None
        prev_malfunction = None
        
        for period, row in monthly_stats.iterrows():
            death = int(row.get('Death', 0))
            injury = int(row.get('Injury', 0))
            malfunction = int(row.get('Malfunction', 0))
            other = int(row.get('Other', 0))
            unknown = int(row.get('Unknown', 0))
            total = int(row.sum())
            
            # Get MDR report numbers for this month
            month_mdrs = df[df['year_month'] == period]['report_number'].tolist()
            mdr_numbers = [str(mdr) for mdr in month_mdrs if pd.notna(mdr)]
            
            # Calculate month-over-month changes
            mom_total = None
            mom_death = None
            mom_injury = None
            mom_malfunction = None
            
            if prev_total is not None and prev_total > 0:
                mom_total = ((total - prev_total) / prev_total) * 100
            if prev_death is not None and prev_death > 0:
                mom_death = ((death - prev_death) / prev_death) * 100
            if prev_injury is not None and prev_injury > 0:
                mom_injury = ((injury - prev_injury) / prev_injury) * 100
            if prev_malfunction is not None and prev_malfunction > 0:
                mom_malfunction = ((malfunction - prev_malfunction) / prev_malfunction) * 100
            
            monthly_data.append({
                'month': str(period),
                'date': period.to_timestamp().strftime('%Y-%m-%d'),
                'injury': injury,
                'death': death,
                'malfunction': malfunction,
                'other': other,
                'unknown': unknown,
                'total': total,
                'mdr_numbers': mdr_numbers,
                'mom_total': round(mom_total, 1) if mom_total is not None else None,
                'mom_death': round(mom_death, 1) if mom_death is not None else None,
                'mom_injury': round(mom_injury, 1) if mom_injury is not None else None,
                'mom_malfunction': round(mom_malfunction, 1) if mom_malfunction is not None else None
            })
            
            # Store current values for next iteration
            prev_total = total
            prev_death = death
            prev_injury = injury
            prev_malfunction = malfunction
        
        # Calculate totals
        totals = {
            'injury': int(df[df['event_category'] == 'Injury'].shape[0]),
            'death': int(df[df['event_category'] == 'Death'].shape[0]),
            'malfunction': int(df[df['event_category'] == 'Malfunction'].shape[0]),
            'other': int(df[df['event_category'] == 'Other'].shape[0]),
            'unknown': int(df[df['event_category'] == 'Unknown'].shape[0]),
            'total': len(df)
        }
        
        print(f"  Total records: {totals['total']}")
        print(f"  Deaths: {totals['death']}, Injuries: {totals['injury']}, Malfunctions: {totals['malfunction']}")
        print(f"  Product types: {len(product_info)}")
        
        return {
            'case_name': metadata['name'],
            'mdl_number': metadata['mdl'],
            'filing_date': metadata['filing_date'],
            'court': metadata['court'],
            'status': metadata.get('status', 'Active'),
            'settlement': metadata.get('settlement'),
            'monthly_data': monthly_data,
            'totals': totals,
            'product_info': product_info,
            'device_classes': device_classes,
            'date_range': {
                'start': df['date_received'].min().strftime('%Y-%m-%d') if not df['date_received'].isna().all() else None,
                'end': df['date_received'].max().strftime('%Y-%m-%d') if not df['date_received'].isna().all() else None
            }
        }
        
    except Exception as e:
        print(f"  Error processing file: {e}")
        return None

# Main processing
print("="*80)
print("PROCESSING BENCHMARK CASES FOR FRONTEND")
print("="*80)

active_dir = '/Users/praveen/Praveen/benchmark_cases'
settled_dir = '/Users/praveen/Praveen/benchmark_cases_settled'
additional_dir = '/Users/praveen/Praveen/benchmark_cases_additional'
output_file = '/Users/praveen/Praveen/frontend/data/benchmark_cases_data.json'

# Create output directory
os.makedirs(os.path.dirname(output_file), exist_ok=True)

all_cases_data = []

# Process active cases
print("\n📂 Processing ORIGINAL ACTIVE cases...")
for filename, metadata in active_cases_metadata.items():
    filepath = os.path.join(active_dir, filename)
    
    if os.path.exists(filepath):
        case_data = process_case_file(filepath, metadata)
        if case_data:
            all_cases_data.append(case_data)
    else:
        print(f"\n⚠️  File not found: {filename}")

# Process settled cases
print("\n📂 Processing ORIGINAL SETTLED cases...")
for filename, metadata in settled_cases_metadata.items():
    filepath = os.path.join(settled_dir, filename)
    
    if os.path.exists(filepath):
        case_data = process_case_file(filepath, metadata)
        if case_data:
            all_cases_data.append(case_data)
    else:
        print(f"\n⚠️  File not found: {filename}")

# Process additional active cases
print("\n📂 Processing ADDITIONAL ACTIVE cases...")
for filename, metadata in additional_active_metadata.items():
    filepath = os.path.join(additional_dir, filename)
    
    if os.path.exists(filepath):
        case_data = process_case_file(filepath, metadata)
        if case_data:
            all_cases_data.append(case_data)
    else:
        print(f"\n⚠️  File not found: {filename}")

# Process additional settled cases
print("\n📂 Processing ADDITIONAL SETTLED cases...")
for filename, metadata in additional_settled_metadata.items():
    filepath = os.path.join(additional_dir, filename)
    
    if os.path.exists(filepath):
        case_data = process_case_file(filepath, metadata)
        if case_data:
            all_cases_data.append(case_data)
    else:
        print(f"\n⚠️  File not found: {filename}")

# Save to JSON
active_cases = [c for c in all_cases_data if c.get('status') == 'Active']
settled_cases = [c for c in all_cases_data if c.get('status') == 'Settled']

output_data = {
    'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'total_cases': len(all_cases_data),
    'active_cases': len(active_cases),
    'settled_cases': len(settled_cases),
    'cases': all_cases_data
}

with open(output_file, 'w') as f:
    json.dump(output_data, f, indent=2)

print("\n" + "="*80)
print("PROCESSING COMPLETE")
print("="*80)
print(f"Total cases processed: {len(all_cases_data)}")
print(f"  - Active: {len(active_cases)}")
print(f"  - Settled: {len(settled_cases)}")
print(f"Output file: {output_file}")
print("="*80)

# Print summary
print("\nSUMMARY BY CASE:")
print("-"*100)
print(f"{'Case':<35} {'MDL':<8} {'Status':<10} {'Deaths':<8} {'Injuries':<10} {'Malfunctions':<15}")
print("-"*100)
for case in all_cases_data:
    status = case.get('status', 'Active')
    print(f"{case['case_name']:<35} {case['mdl_number']:<8} {status:<10} {case['totals']['death']:<8} {case['totals']['injury']:<10} {case['totals']['malfunction']:<15}")
print("-"*100)

# Print settlements for settled cases
if settled_cases:
    print("\n💰 SETTLEMENT AMOUNTS:")
    print("-"*80)
    for case in settled_cases:
        if case.get('settlement'):
            print(f"  {case['case_name']:<40} {case['settlement']}")
    print("-"*80)
