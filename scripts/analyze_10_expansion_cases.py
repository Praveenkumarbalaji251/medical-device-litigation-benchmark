"""
Analysis of 10 Additional MDL Cases - MAUDE Data Fetch Results
Successfully fetched FDA adverse event reports for benchmark expansion
"""

import pandas as pd
import os
from datetime import datetime

# Load all case files
data_dir = "benchmark_cases_expansion"
case_files = [
    ("3M Combat Arms Earplugs", "MDL 2885", "3m_combat_arms_earplugs_mdl_2885.xlsx"),
    ("Medtronic Sprint Quattro Leads", "MDL 2187", "medtronic_sprint_quattro_leads_mdl_2187.xlsx"),
    ("Medtronic Infuse Bone Graft", "MDL 2431", "medtronic_infuse_bone_graft_mdl_2431.xlsx"),
    ("Biomet M2a Magnum Hip", "MDL 2652", "biomet_m2a_magnum_hip_mdl_2652.xlsx"),
    ("Power Morcellator", "MDL 2586", "power_morcellator_mdl_2586.xlsx"),
    ("Nevro Spinal Cord Stimulator", "MDL 2876", "nevro_spinal_cord_stimulator_mdl_2876.xlsx"),
    ("da Vinci Surgical Robot", "MDL 2920", "davinci_surgical_robot_mdl_2920.xlsx"),
    ("Cook Zenith Aortic Graft", "MDL 2846", "cook_zenith_aortic_graft_mdl_2846.xlsx"),
    ("STAAR Visian ICL", "No MDL", "staar_visian_icl.xlsx"),
    ("Medtronic Pain Pump", "MDL 2662", "medtronic_pain_pump_mdl_2662.xlsx"),
]

print("\n" + "="*80)
print(" MAUDE DATA FETCH - 10 EXPANSION CASES ANALYSIS")
print("="*80)

# Collect data for each case
all_cases = []
total_mdrs = 0

for case_name, mdl_num, filename in case_files:
    filepath = os.path.join(data_dir, filename)
    
    if os.path.exists(filepath):
        df = pd.read_excel(filepath)
        
        # Basic stats
        num_mdrs = len(df)
        total_mdrs += num_mdrs
        
        # Event type breakdown
        event_counts = df['event_type'].value_counts() if 'event_type' in df.columns else {}
        
        # Manufacturer breakdown
        manufacturers = df['manufacturer'].value_counts().head(3) if 'manufacturer' in df.columns else {}
        
        # Date range
        dates = pd.to_datetime(df['date_received'], format='%Y%m%d', errors='coerce')
        date_range = f"{dates.min().strftime('%Y-%m-%d')} to {dates.max().strftime('%Y-%m-%d')}" if len(dates) > 0 else "N/A"
        
        all_cases.append({
            'case_name': case_name,
            'mdl_number': mdl_num,
            'total_mdrs': num_mdrs,
            'date_range': date_range,
            'top_manufacturer': manufacturers.index[0] if len(manufacturers) > 0 else "N/A",
            'event_types': len(event_counts),
            'file': filename
        })
        
        print(f"\n{case_name} ({mdl_num})")
        print(f"  MDRs: {num_mdrs:,}")
        print(f"  Date Range: {date_range}")
        print(f"  Event Types: {len(event_counts)}")
        if len(manufacturers) > 0:
            print(f"  Top Manufacturers:")
            for mfr, count in manufacturers.head(3).items():
                print(f"    - {mfr}: {count} reports")
    else:
        print(f"\n{case_name} ({mdl_num})")
        print(f"  FILE NOT FOUND: {filename}")

# Summary table
print("\n" + "="*80)
print(" SUMMARY")
print("="*80)

summary_df = pd.DataFrame(all_cases)
print(summary_df[['case_name', 'mdl_number', 'total_mdrs']].to_string(index=False))

print(f"\n{'TOTAL MDRs FETCHED:':40s} {total_mdrs:,}")
print(f"{'Cases Successfully Fetched:':40s} {len(all_cases)}/10")

# Device category breakdown
print("\n" + "="*80)
print(" DEVICE CATEGORY BREAKDOWN")
print("="*80)

categories = {
    'Orthopedic Implants': ['Biomet M2a Magnum Hip', 'Medtronic Infuse Bone Graft'],
    'Cardiac Devices': ['Medtronic Sprint Quattro Leads'],
    'Surgical Systems': ['da Vinci Surgical Robot', 'Power Morcellator'],
    'Neurological Devices': ['Nevro Spinal Cord Stimulator', 'Medtronic Pain Pump'],
    'Ophthalmic Implants': ['STAAR Visian ICL'],
    'Vascular Grafts': ['Cook Zenith Aortic Graft'],
    'Hearing Protection': ['3M Combat Arms Earplugs']
}

for category, devices in categories.items():
    category_mdrs = sum([case['total_mdrs'] for case in all_cases if case['case_name'] in devices])
    print(f"{category:30s} {category_mdrs:6,} MDRs ({len(devices)} devices)")

# Top 5 cases by MDR volume
print("\n" + "="*80)
print(" TOP 5 CASES BY MDR VOLUME")
print("="*80)

sorted_cases = sorted(all_cases, key=lambda x: x['total_mdrs'], reverse=True)
for i, case in enumerate(sorted_cases[:5], 1):
    print(f"{i}. {case['case_name']:40s} {case['total_mdrs']:6,} MDRs")

# Save summary
summary_df.to_excel(os.path.join(data_dir, "fetch_summary_analysis.xlsx"), index=False)
print(f"\n✓ Summary saved to: {data_dir}/fetch_summary_analysis.xlsx")

print("\n" + "="*80)
print(" NEXT STEPS")
print("="*80)
print("1. Integrate these 10 cases with existing 19 cases (total: 29 cases)")
print("2. Analyze MDR patterns across all cases")
print("3. Build comprehensive labeled dataset for ML training")
print("4. Update benchmark dashboard with new cases")
print("="*80)
