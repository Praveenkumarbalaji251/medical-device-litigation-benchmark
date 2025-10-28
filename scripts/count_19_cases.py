"""
Analyze and integrate 19 successfully fetched cases
"""
import pandas as pd
import os
from datetime import datetime

print("="*80)
print(" ANALYZING 19 SUCCESSFULLY FETCHED CASES")
print("="*80)

directory = 'benchmark_cases_expansion_21'
files = [f for f in os.listdir(directory) if f.endswith('.xlsx')]

results = []
total_mdrs = 0

for filename in sorted(files):
    filepath = os.path.join(directory, filename)
    try:
        df = pd.read_excel(filepath)
        mdrs = len(df)
        total_mdrs += mdrs
        
        case_name = filename.replace('.xlsx', '').replace('_', ' ').title()
        
        results.append({
            'filename': filename,
            'case_name': case_name,
            'mdrs': mdrs
        })
        
        print(f"✓ {case_name:.<60} {mdrs:>6,} MDRs")
    except Exception as e:
        print(f"✗ {filename}: Error - {str(e)}")

print("="*80)
print(f"Total Cases: {len(results)}")
print(f"Total MDRs: {total_mdrs:,}")
print(f"Combined with existing 29 cases: 29 + {len(results)} = {29 + len(results)} cases")
print("="*80)

# Save summary
with open('/tmp/fetch_19_summary.txt', 'w') as f:
    f.write(f"19 Additional Cases Successfully Fetched\n")
    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("="*80 + "\n\n")
    for r in results:
        f.write(f"{r['case_name']}: {r['mdrs']:,} MDRs\n")
    f.write(f"\nTotal: {total_mdrs:,} MDRs across {len(results)} cases\n")

print(f"\n✓ Summary saved to /tmp/fetch_19_summary.txt")
