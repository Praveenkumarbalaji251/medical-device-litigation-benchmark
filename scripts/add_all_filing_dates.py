import json

# Load current data
with open('frontend/data/benchmark_cases_data_v48.json', 'r') as f:
    data = json.load(f)

# Filing dates for the 18 expansion cases (17 with MDL + 1 Paradigm)
expansion_filing_dates = {
    '2974': '2018-10',
    '2996': '2020-01',
    '2775': '2017-04',  # Already has this
    '2666': '2015-12',
    '3032': '2021-03',
    '2928': '2019-10',
    '2787': '2017-03',
    '2868': '2018-07',
    '2768': '2016-11',
    '2903': '2018-12',
    '3070': '2021-12',
    '2428': '2013-02',
    '2904': '2018-12',
    '2995': '2020-01',
    '2881': '2018-05',
    '2749': '2016-06',
    '2965': '2019-11',
    '2848': '2017-11',
}

print("=" * 80)
print("ADDING FILING DATES TO EXPANSION CASES")
print("=" * 80)

updated_count = 0

for case in data['cases']:
    mdl = str(case.get('mdl_number', ''))
    
    # Check if this case needs a filing date
    if mdl in expansion_filing_dates:
        # Only update if filing_date is missing or empty
        if not case.get('filing_date'):
            case['filing_date'] = expansion_filing_dates[mdl]
            name = case.get('name', case.get('case_name', 'Unknown'))
            print(f"✓ Added filing date for MDL {mdl}: {name} - {expansion_filing_dates[mdl]}")
            updated_count += 1
        else:
            print(f"  Skipped MDL {mdl}: Already has filing date {case['filing_date']}")

print(f"\n✓ Updated {updated_count} cases with filing dates")

# Save updated JSON
with open('frontend/data/benchmark_cases_data_v48.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"\n✅ SUCCESS: Saved to frontend/data/benchmark_cases_data_v48.json")

# Verify all cases now
cases_with_dates = sum(1 for c in data['cases'] if c.get('filing_date'))
cases_without_dates = len(data['cases']) - cases_with_dates

print(f"\nFinal Status:")
print(f"  Cases with filing dates: {cases_with_dates}/48")
print(f"  Cases without filing dates: {cases_without_dates}/48")
