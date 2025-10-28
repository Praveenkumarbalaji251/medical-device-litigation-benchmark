"""
Integrate 10 New Expansion Cases into Dashboard Data
Merges new MAUDE data with existing 19-case benchmark dataset
"""

import pandas as pd
import json
from datetime import datetime
import os

# Load existing dashboard data
with open('frontend/data/benchmark_cases_data.json', 'r') as f:
    existing_data = json.load(f)

print("="*80)
print(" INTEGRATING 10 NEW CASES INTO DASHBOARD")
print("="*80)

# Existing cases summary
print(f"\nExisting Dashboard:")
print(f"  - Total Cases: {existing_data['total_cases']}")
print(f"  - Active Cases: {existing_data['active_cases']}")
print(f"  - Settled Cases: {existing_data['settled_cases']}")

# New cases metadata
new_cases_metadata = [
    {
        "case_name": "3M Combat Arms Earplugs",
        "mdl_number": "2885",
        "filing_date": "2019-04-01",
        "court": "N.D. Florida",
        "judge": "Judge M. Casey Rodgers",
        "status": "Settled",
        "settlement": 6000000000,  # $6B settlement
        "category": "Hearing Protection",
        "plaintiffs": "Over 300,000 military veterans",
        "file": "3m_combat_arms_earplugs_mdl_2885.xlsx"
    },
    {
        "case_name": "Medtronic Sprint Quattro Leads",
        "mdl_number": "2187",
        "filing_date": "2010-02-24",
        "court": "D. Minnesota",
        "judge": "Judge Donovan W. Frank",
        "status": "Active",
        "settlement": None,
        "category": "Cardiac Device",
        "plaintiffs": "Patients with implanted cardiac leads",
        "file": "medtronic_sprint_quattro_leads_mdl_2187.xlsx"
    },
    {
        "case_name": "Medtronic Infuse Bone Graft",
        "mdl_number": "2431",
        "filing_date": "2012-02-22",
        "court": "E.D. Wisconsin",
        "judge": "Judge William C. Griesbach",
        "status": "Dismissed",
        "settlement": None,
        "category": "Spinal Device",
        "plaintiffs": "Patients who received Infuse BMP implants",
        "file": "medtronic_infuse_bone_graft_mdl_2431.xlsx"
    },
    {
        "case_name": "Biomet M2a Magnum Hip",
        "mdl_number": "2652",
        "filing_date": "2012-12-17",
        "court": "N.D. Indiana",
        "judge": "Judge Robert L. Miller Jr.",
        "status": "Settled",
        "settlement": 56000000,  # $56M settlement
        "category": "Orthopedic Implant",
        "plaintiffs": "Patients with metal-on-metal hip implants",
        "file": "biomet_m2a_magnum_hip_mdl_2652.xlsx"
    },
    {
        "case_name": "Power Morcellator",
        "mdl_number": "2586",
        "filing_date": "2014-10-06",
        "court": "D. Kansas",
        "judge": "Judge Julie A. Robinson",
        "status": "Active",
        "settlement": None,
        "category": "Surgical Instrument",
        "plaintiffs": "Women who developed cancer after morcellation",
        "file": "power_morcellator_mdl_2586.xlsx"
    },
    {
        "case_name": "Nevro Spinal Cord Stimulator",
        "mdl_number": "2876",
        "filing_date": "2019-02-06",
        "court": "D. New Jersey",
        "judge": "Judge Freda L. Wolfson",
        "status": "Active",
        "settlement": None,
        "category": "Neurological Device",
        "plaintiffs": "Patients with implanted SCS devices",
        "file": "nevro_spinal_cord_stimulator_mdl_2876.xlsx"
    },
    {
        "case_name": "da Vinci Surgical Robot",
        "mdl_number": "2920",
        "filing_date": "2013-08-09",
        "court": "S.D. West Virginia",
        "judge": "Judge Joseph R. Goodwin",
        "status": "Dismissed",
        "settlement": None,
        "category": "Surgical Robot",
        "plaintiffs": "Patients injured during robotic surgery",
        "file": "davinci_surgical_robot_mdl_2920.xlsx"
    },
    {
        "case_name": "Cook Zenith Aortic Graft",
        "mdl_number": "2846",
        "filing_date": "2015-11-05",
        "court": "S.D. Illinois",
        "judge": "Judge J. Phil Gilbert",
        "status": "Active",
        "settlement": None,
        "category": "Vascular Graft",
        "plaintiffs": "Patients with aortic graft complications",
        "file": "cook_zenith_aortic_graft_mdl_2846.xlsx"
    },
    {
        "case_name": "STAAR Visian ICL",
        "mdl_number": None,
        "filing_date": "2014-06-18",
        "court": "C.D. California",
        "judge": "Judge S. James Otero",
        "status": "Active",
        "settlement": None,
        "category": "Ophthalmic Implant",
        "plaintiffs": "Patients with implantable contact lenses",
        "file": "staar_visian_icl.xlsx"
    },
    {
        "case_name": "Medtronic Pain Pump",
        "mdl_number": "2662",
        "filing_date": "2010-01-15",
        "court": "N.D. California",
        "judge": "Judge Phyllis J. Hamilton",
        "status": "Dismissed",
        "settlement": None,
        "category": "Pain Management",
        "plaintiffs": "Patients with intrathecal pain pump complications",
        "file": "medtronic_pain_pump_mdl_2662.xlsx"
    }
]

# Process each new case
new_cases_data = []
total_new_mdrs = 0

for case_meta in new_cases_metadata:
    filepath = f"benchmark_cases_expansion/{case_meta['file']}"
    
    if os.path.exists(filepath):
        df = pd.read_excel(filepath)
        
        # Convert date_received to datetime
        df['date_received'] = pd.to_datetime(df['date_received'], format='%Y%m%d', errors='coerce')
        df['month'] = df['date_received'].dt.to_period('M')
        
        # Aggregate by month
        monthly_summary = []
        for month_period, group in df.groupby('month'):
            month_str = str(month_period)
            
            # Count event types
            event_counts = group['event_type'].value_counts().to_dict()
            
            monthly_summary.append({
                "month": month_str,
                "date": f"{month_str}-01",
                "injury": event_counts.get('Injury', 0),
                "death": event_counts.get('Death', 0),
                "malfunction": event_counts.get('Malfunction', 0),
                "other": event_counts.get('Other', 0) + event_counts.get('No answer provided', 0),
                "unknown": 0,
                "total": len(group),
                "mdr_numbers": group['mdr_report_key'].tolist()[:100]  # Limit to 100 for performance
            })
        
        # Create case entry
        case_entry = {
            "case_name": case_meta['case_name'],
            "mdl_number": case_meta['mdl_number'],
            "filing_date": case_meta['filing_date'],
            "court": case_meta['court'],
            "judge": case_meta.get('judge', ''),
            "status": case_meta['status'],
            "settlement": case_meta['settlement'],
            "category": case_meta['category'],
            "plaintiffs": case_meta['plaintiffs'],
            "total_mdrs": len(df),
            "monthly_data": sorted(monthly_summary, key=lambda x: x['month']),
            "summary": {
                "total_deaths": df[df['event_type'] == 'Death'].shape[0],
                "total_injuries": df[df['event_type'] == 'Injury'].shape[0],
                "total_malfunctions": df[df['event_type'] == 'Malfunction'].shape[0],
                "date_range": f"{df['date_received'].min().strftime('%Y-%m-%d')} to {df['date_received'].max().strftime('%Y-%m-%d')}",
                "top_manufacturers": df['manufacturer'].value_counts().head(3).to_dict()
            }
        }
        
        new_cases_data.append(case_entry)
        total_new_mdrs += len(df)
        
        print(f"\n✓ Processed: {case_meta['case_name']}")
        print(f"   MDRs: {len(df):,} | Deaths: {case_entry['summary']['total_deaths']} | Injuries: {case_entry['summary']['total_injuries']}")

# Merge with existing data
combined_data = {
    "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "total_cases": existing_data['total_cases'] + len(new_cases_data),
    "active_cases": existing_data['active_cases'] + sum(1 for c in new_cases_data if c['status'] == 'Active'),
    "settled_cases": existing_data['settled_cases'] + sum(1 for c in new_cases_data if c['status'] == 'Settled'),
    "total_mdrs": sum(case.get('total_mdrs', 0) for case in existing_data['cases']) + total_new_mdrs,
    "cases": existing_data['cases'] + new_cases_data
}

# Save integrated data
output_path = 'frontend/data/benchmark_cases_data_v29.json'
with open(output_path, 'w') as f:
    json.dump(combined_data, f, indent=2)

print("\n" + "="*80)
print(" INTEGRATION COMPLETE")
print("="*80)
print(f"\nCombined Dataset:")
print(f"  Total Cases: {combined_data['total_cases']} (was {existing_data['total_cases']}, +{len(new_cases_data)})")
print(f"  Active Cases: {combined_data['active_cases']}")
print(f"  Settled Cases: {combined_data['settled_cases']}")
print(f"  Total MDRs: {combined_data['total_mdrs']:,}")
print(f"\n✓ Saved to: {output_path}")

# Create summary by category
print("\n" + "="*80)
print(" CASES BY CATEGORY")
print("="*80)

categories = {}
for case in combined_data['cases']:
    cat = case.get('category', 'Other')
    if cat not in categories:
        categories[cat] = []
    categories[cat].append(case['case_name'])

for cat, cases in sorted(categories.items()):
    print(f"\n{cat} ({len(cases)} cases):")
    for case_name in cases:
        print(f"  - {case_name}")

print("\n" + "="*80)
print(" NEXT: Update frontend/index.html to use new data file")
print("="*80)
