"""
Dashboard Data Verification - Check what's displaying
"""
import json

print("="*80)
print(" DASHBOARD DATA VERIFICATION")
print("="*80)

# Load the data
with open('frontend/data/benchmark_cases_data_v29.json', 'r') as f:
    data = json.load(f)

print(f"\n📊 HEADER STATS (Top of Dashboard):")
print(f"   Total Cases: {data['total_cases']}")
print(f"   Total MDRs: {data.get('total_mdrs', 'N/A'):,}" if data.get('total_mdrs') else "   Total MDRs: Calculated from cases")
print(f"   Active Cases: {data['active_cases']}")
print(f"   Settled Cases: {data['settled_cases']}")

# Calculate total MDRs
total_mdrs = sum([
    case.get('totals', {}).get('total', 0) or case.get('total_mdrs', 0) 
    for case in data['cases']
])
total_deaths = sum([
    case.get('totals', {}).get('death', 0) or case.get('summary', {}).get('total_deaths', 0) 
    for case in data['cases']
])
total_injuries = sum([
    case.get('totals', {}).get('injury', 0) or case.get('summary', {}).get('total_injuries', 0) 
    for case in data['cases']
])

print(f"   Calculated Total MDRs: {total_mdrs:,}")
print(f"   Calculated Total Deaths: {total_deaths:,}")
print(f"   Calculated Total Injuries: {total_injuries:,}")

print(f"\n📋 SIDEBAR - ALL 29 CASES:")
print(f"{'#':<3} {'Case Name':<40} {'MDL':<8} {'Status':<10} {'MDRs':>8} {'NEW?':<5}")
print("-" * 80)

new_case_mdls = ['2885', '2187', '2431', '2652', '2586', '2876', '2920', '2846', None, '2662']

for i, case in enumerate(data['cases'], 1):
    mdrs = case.get('totals', {}).get('total', 0) or case.get('total_mdrs', 0)
    mdl = case.get('mdl_number', 'N/A')
    status = case.get('status', 'Unknown')
    is_new = '✅ NEW' if mdl in new_case_mdls else ''
    
    print(f"{i:<3} {case['case_name'][:38]:<40} {str(mdl):<8} {status:<10} {mdrs:>8,} {is_new}")

print("\n" + "="*80)
print(" NEW CASES HIGHLIGHTED (Should have green 'NEW' badge)")
print("="*80)

new_cases = [c for c in data['cases'] if c.get('mdl_number') in new_case_mdls]
print(f"\nFound {len(new_cases)} new cases:")

for case in new_cases:
    mdrs = case.get('total_mdrs', 0)
    deaths = case.get('summary', {}).get('total_deaths', 0)
    settlement = case.get('settlement')
    
    print(f"\n✅ {case['case_name']}")
    print(f"   MDL: {case.get('mdl_number', 'N/A')}")
    print(f"   Status: {case.get('status')}")
    print(f"   MDRs: {mdrs:,}")
    print(f"   Deaths: {deaths}")
    print(f"   Injuries: {case.get('summary', {}).get('total_injuries', 0)}")
    if settlement:
        print(f"   Settlement: ${settlement/1e9:.2f}B")
    print(f"   Category: {case.get('category', 'N/A')}")

print("\n" + "="*80)
print(" DASHBOARD SHOULD SHOW:")
print("="*80)
print("✓ 29 cases in the sidebar (left panel)")
print("✓ 10 cases with green 'NEW' badges")
print("✓ Header showing '29 CASES' badge")
print("✓ Updated KPIs with total MDRs, deaths, injuries")
print("✓ Click on any case to see details in main panel")
print("✓ Monthly charts for each case")
print("="*80)
