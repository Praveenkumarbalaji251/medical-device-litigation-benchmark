import json
import pandas as pd
from datetime import datetime

print("=" * 80)
print("INTEGRATING 2 MASS TORT CASES INTO 51-CASE BENCHMARK")
print("=" * 80)

# Load the current 49-case benchmark
print("\nLoading current benchmark...")
with open('frontend/data/benchmark_cases_data_v49.json', 'r') as f:
    data = json.load(f)

print(f"✓ Loaded {len(data['cases'])} existing cases")

# Load Sientra data
print("\nLoading Sientra Breast Implants data...")
sientra_df = pd.read_excel('benchmark_cases_expansion_mass_tort/sientra_breast_implants.xlsx')
print(f"✓ Loaded {len(sientra_df):,} MDR records")

# Get date range
sientra_df['date_received'] = sientra_df['date_received'].astype(str)
valid_dates = sientra_df[sientra_df['date_received'].str.len() == 8]['date_received']
if len(valid_dates) > 0:
    dates = pd.to_datetime(valid_dates, format='%Y%m%d', errors='coerce').dropna()
    sientra_date_window = f"{dates.min().strftime('%Y-%m-%d')} to {dates.max().strftime('%Y-%m-%d')}"
else:
    sientra_date_window = "Date range unavailable"

# Count events
sientra_events = sientra_df['event_type'].value_counts().to_dict()
sientra_injuries = sientra_events.get('Injury', 0)
sientra_malfunctions = sientra_events.get('Malfunction', 0)
sientra_deaths = sientra_events.get('Death', 0)

print(f"  Injuries: {sientra_injuries:,}")
print(f"  Malfunctions: {sientra_malfunctions:,}")
print(f"  Deaths: {sientra_deaths:,}")

# Create Sientra case entry
sientra_case = {
    "name": "Sientra Breast Implants",
    "mdl_number": None,
    "litigation_type": "State Court Mass Tort",
    "court": "Various State Courts (CA, TX, FL)",
    "filing_date": "2015-09-01",
    "status": "Active",
    "allegations": "Mold contamination, rupture, BIA-ALCL, capsular contracture",
    "settlement": "No settlements yet",
    "data_window": sientra_date_window,
    "total_mdrs": len(sientra_df),
    "injuries": sientra_injuries,
    "malfunctions": sientra_malfunctions,
    "deaths": sientra_deaths,
    "device_name": "Sientra Breast Implants (OPUS)",
    "notes": "Class I FDA recall Oct 2015 (mold contamination). BIA-ALCL cases ongoing. State court mass tort."
}

print(f"\n✓ Created Sientra case entry")

# Load ATEC data
print("\nLoading ATEC Breast Biopsy data...")
atec_df = pd.read_excel('benchmark_cases_expansion_mass_tort/atec_breast_biopsy.xlsx')
print(f"✓ Loaded {len(atec_df):,} MDR records")

# Get date range
atec_df['date_received'] = atec_df['date_received'].astype(str)
valid_dates = atec_df[atec_df['date_received'].str.len() == 8]['date_received']
if len(valid_dates) > 0:
    dates = pd.to_datetime(valid_dates, format='%Y%m%d', errors='coerce').dropna()
    atec_date_window = f"{dates.min().strftime('%Y-%m-%d')} to {dates.max().strftime('%Y-%m-%d')}"
else:
    atec_date_window = "Date range unavailable"

# Count events
atec_events = atec_df['event_type'].value_counts().to_dict()
atec_injuries = atec_events.get('Injury', 0)
atec_malfunctions = atec_events.get('Malfunction', 0)
atec_deaths = atec_events.get('Death', 0)

print(f"  Injuries: {atec_injuries:,}")
print(f"  Malfunctions: {atec_malfunctions:,}")
print(f"  Deaths: {atec_deaths:,}")

# Create ATEC case entry
atec_case = {
    "name": "ATEC Breast Biopsy System",
    "mdl_number": None,
    "litigation_type": "Multi-Jurisdiction Mass Tort",
    "court": "Various State and Federal Courts",
    "filing_date": "2018-03-01",
    "status": "Active",
    "allegations": "Excessive bleeding, hematoma, tissue damage, device malfunction",
    "settlement": "Individual settlements (confidential)",
    "data_window": atec_date_window,
    "total_mdrs": len(atec_df),
    "injuries": atec_injuries,
    "malfunctions": atec_malfunctions,
    "deaths": atec_deaths,
    "device_name": "ATEC Breast Biopsy System (Hologic)",
    "notes": "Multi-jurisdiction mass tort. Hologic settling individually to avoid MDL. Vacuum-assisted biopsy device."
}

print(f"\n✓ Created ATEC case entry")

# Add both cases to the benchmark
data['cases'].append(sientra_case)
data['cases'].append(atec_case)

print(f"\n✓ Added 2 cases to benchmark (now {len(data['cases'])} cases)")

# Update metadata
data['total_cases'] = len(data['cases'])
data['last_updated'] = datetime.now().strftime('%Y-%m-%d')

# Calculate new totals
total_mdrs = sum(case.get('total_mdrs', 0) for case in data['cases'])
total_injuries = sum(case.get('injuries', 0) for case in data['cases'])
total_deaths = sum(case.get('deaths', 0) for case in data['cases'])
total_malfunctions = sum(case.get('malfunctions', 0) for case in data['cases'])

print(f"\n📈 NEW BENCHMARK TOTALS:")
print(f"  Total Cases: {len(data['cases'])}")
print(f"  Total MDRs: {total_mdrs:,}")
print(f"  Total Injuries: {total_injuries:,}")
print(f"  Total Deaths: {total_deaths:,}")
print(f"  Total Malfunctions: {total_malfunctions:,}")

# Calculate status breakdown
status_counts = {}
for case in data['cases']:
    status = case.get('status', 'Unknown')
    status_counts[status] = status_counts.get(status, 0) + 1

print(f"\n📊 STATUS BREAKDOWN:")
for status, count in sorted(status_counts.items()):
    print(f"  {status}: {count}")

# Save to new file
output_file = 'frontend/data/benchmark_cases_data_v51.json'
with open(output_file, 'w') as f:
    json.dump(data, f, indent=2)

print(f"\n✅ SUCCESS!")
print(f"✓ Saved to: {output_file}")
print(f"✓ File size: {len(json.dumps(data)) / 1024 / 1024:.2f} MB")

print(f"\n{'=' * 80}")
print("NEXT STEPS:")
print("1. Update frontend/index.html to load benchmark_cases_data_v51.json")
print("2. Update title to '51 Cases | 351K+ MDRs'")
print("3. Update badge to '51 CASES'")
print("4. Add 'Sientra' and 'ATEC' to NEW badge array")
print("5. Push to GitHub for auto-deploy to Render")
print("=" * 80)
