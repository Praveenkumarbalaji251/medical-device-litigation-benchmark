"""
Export All MDR Report Numbers from Benchmark Cases to Consolidated Excel
This creates a master reference file with all MDR numbers organized by case and month
"""

import pandas as pd
import json
from datetime import datetime
import os

print("="*80)
print("EXPORTING ALL MDR NUMBERS TO MASTER EXCEL FILE")
print("="*80)

# Load the processed JSON data
json_path = '/Users/praveen/Praveen/frontend/data/benchmark_cases_data.json'
output_excel = '/Users/praveen/Praveen/MDR_MASTER_REFERENCE.xlsx'

print(f"\n📂 Reading data from: {json_path}")

with open(json_path, 'r') as f:
    data = json.load(f)

print(f"📊 Found {data['total_cases']} cases to process")
print(f"   - Active: {data['active_cases']}")
print(f"   - Settled: {data['settled_cases']}")

# Create Excel writer
with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
    
    # Sheet 1: Master Summary
    summary_data = []
    total_mdrs = 0
    
    for case in data['cases']:
        case_total = case['totals']['total']
        total_mdrs += case_total
        
        summary_data.append({
            'Case Name': case['case_name'],
            'MDL Number': case['mdl_number'],
            'Status': case.get('status', 'Active'),
            'Filing Date': case['filing_date'],
            'Court': case['court'],
            'Settlement': case.get('settlement', 'N/A'),
            'Total MDRs': case_total,
            'Deaths': case['totals']['death'],
            'Injuries': case['totals']['injury'],
            'Malfunctions': case['totals']['malfunction'],
            'Date Range': f"{case['date_range']['start']} to {case['date_range']['end']}"
        })
    
    summary_df = pd.DataFrame(summary_data)
    summary_df.to_excel(writer, sheet_name='Master Summary', index=False)
    print(f"\n✅ Sheet 1: Master Summary ({len(summary_data)} cases)")
    
    # Sheet 2: All MDR Numbers by Case
    all_mdrs_data = []
    
    for case in data['cases']:
        for month_data in case['monthly_data']:
            mdr_numbers = month_data.get('mdr_numbers', [])
            
            for mdr in mdr_numbers:
                all_mdrs_data.append({
                    'MDR Report Number': mdr,
                    'Case Name': case['case_name'],
                    'MDL Number': case['mdl_number'],
                    'Status': case.get('status', 'Active'),
                    'Month': month_data['month'],
                    'Date': month_data['date'],
                    'Settlement': case.get('settlement', 'N/A')
                })
    
    all_mdrs_df = pd.DataFrame(all_mdrs_data)
    all_mdrs_df.to_excel(writer, sheet_name='All MDR Numbers', index=False)
    print(f"✅ Sheet 2: All MDR Numbers ({len(all_mdrs_data)} reports)")
    
    # Sheet 3-12: Individual case sheets with MDRs by month
    for idx, case in enumerate(data['cases'], 1):
        case_mdrs = []
        
        for month_data in case['monthly_data']:
            mdr_numbers = month_data.get('mdr_numbers', [])
            
            case_mdrs.append({
                'Month': month_data['month'],
                'Date': month_data['date'],
                'Total Events': month_data['total'],
                'Deaths': month_data['death'],
                'Injuries': month_data['injury'],
                'Malfunctions': month_data['malfunction'],
                'Other': month_data['other'],
                'MDR Count': len(mdr_numbers),
                'MDR Report Numbers': ', '.join(mdr_numbers) if mdr_numbers else 'None'
            })
        
        case_df = pd.DataFrame(case_mdrs)
        
        # Clean sheet name (Excel has 31 char limit and no special chars)
        clean_name = case['case_name'].replace('/', '-').replace('\\', '-').replace('(', '').replace(')', '')
        sheet_name = f"{idx}. {clean_name[:25]}"
        case_df.to_excel(writer, sheet_name=sheet_name, index=False)
        print(f"✅ Sheet {idx+2}: {case['case_name']} ({case['totals']['total']} MDRs)")
    
    # Sheet: MDR Numbers by Status (Active vs Settled)
    active_mdrs = []
    settled_mdrs = []
    
    for case in data['cases']:
        status = case.get('status', 'Active')
        for month_data in case['monthly_data']:
            for mdr in month_data.get('mdr_numbers', []):
                mdr_entry = {
                    'MDR Number': mdr,
                    'Case': case['case_name'],
                    'MDL': case['mdl_number'],
                    'Month': month_data['month']
                }
                
                if status == 'Settled':
                    mdr_entry['Settlement'] = case.get('settlement', 'N/A')
                    settled_mdrs.append(mdr_entry)
                else:
                    active_mdrs.append(mdr_entry)
    
    if active_mdrs:
        active_df = pd.DataFrame(active_mdrs)
        active_df.to_excel(writer, sheet_name='Active Cases - MDRs', index=False)
        print(f"✅ Sheet: Active Cases MDRs ({len(active_mdrs)} reports)")
    
    if settled_mdrs:
        settled_df = pd.DataFrame(settled_mdrs)
        settled_df.to_excel(writer, sheet_name='Settled Cases - MDRs', index=False)
        print(f"✅ Sheet: Settled Cases MDRs ({len(settled_mdrs)} reports)")
    
    # Sheet: Monthly Statistics Across All Cases
    monthly_stats = []
    
    # Collect all unique months
    all_months = set()
    for case in data['cases']:
        for month_data in case['monthly_data']:
            all_months.add(month_data['month'])
    
    for month in sorted(all_months):
        month_mdrs = []
        month_deaths = 0
        month_injuries = 0
        month_malfunctions = 0
        
        for case in data['cases']:
            for month_data in case['monthly_data']:
                if month_data['month'] == month:
                    month_mdrs.extend(month_data.get('mdr_numbers', []))
                    month_deaths += month_data['death']
                    month_injuries += month_data['injury']
                    month_malfunctions += month_data['malfunction']
        
        monthly_stats.append({
            'Month': month,
            'Total MDRs': len(month_mdrs),
            'Deaths': month_deaths,
            'Injuries': month_injuries,
            'Malfunctions': month_malfunctions,
            'Cases Active': sum(1 for case in data['cases'] 
                               if any(m['month'] == month for m in case['monthly_data']))
        })
    
    monthly_df = pd.DataFrame(monthly_stats)
    monthly_df.to_excel(writer, sheet_name='Monthly Cross-Case Stats', index=False)
    print(f"✅ Sheet: Monthly Cross-Case Statistics ({len(monthly_stats)} months)")

print("\n" + "="*80)
print("EXPORT COMPLETE!")
print("="*80)
print(f"\n📊 Total Statistics:")
print(f"   Total MDR Reports: {total_mdrs:,}")
print(f"   Total Cases: {data['total_cases']}")
print(f"   Active Cases: {data['active_cases']}")
print(f"   Settled Cases: {data['settled_cases']}")
print(f"\n💾 Output file: {output_excel}")
print(f"📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Print file size
file_size = os.path.getsize(output_excel)
file_size_mb = file_size / (1024 * 1024)
print(f"📦 File size: {file_size_mb:.2f} MB")

print("\n" + "="*80)
print("EXCEL STRUCTURE:")
print("="*80)
print("""
Sheet 1:  Master Summary - Overview of all 10 cases
Sheet 2:  All MDR Numbers - Complete list of all MDR report numbers
Sheet 3-12: Individual case sheets with monthly MDR breakdowns
Sheet 13: Active Cases - MDRs (all active case MDR numbers)
Sheet 14: Settled Cases - MDRs (all settled case MDR numbers with settlements)
Sheet 15: Monthly Cross-Case Stats (aggregate monthly data across all cases)
""")

print("✅ Ready for litigation analysis and case benchmarking!")
print("="*80)
