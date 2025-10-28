import requests
import pandas as pd
from datetime import datetime
import time

# Abbott FreeStyle Libre CGM case details
case_info = {
    "device_name": "Abbott FreeStyle Libre CGM",
    "mdl_number": None,  # No US MDL yet
    "filing_date": "2019-05",  # First UK case May 2019
    "court": "UK High Court (UK), Various State Courts (US)",
    "status": "Settled (UK), Active (US)",
    "settlement": "Individual settlements UK: £50K-£200K",
    "allegations": "Inaccurate glucose readings, missed hypoglycemia, adhesive failures"
}

print("=" * 80)
print(f"FETCHING MAUDE DATA: {case_info['device_name']}")
print("=" * 80)

# FDA OpenFDA API endpoint
base_url = "https://api.fda.gov/device/event.json"

# Search query for FreeStyle Libre
# Try multiple variations to capture all devices
queries = [
    'device.brand_name:"FreeStyle+Libre"',
    'device.brand_name:"Freestyle+Libre"',
    'device.brand_name:"Free+Style+Libre"'
]

all_records = []
total_fetched = 0

for query in queries:
    print(f"\nSearching with query: {query}")
    
    skip = 0
    limit = 100
    max_results = 10000  # FDA API limit
    
    while skip < max_results:
        try:
            # Build the request URL
            search_query = f"search={query}&limit={limit}&skip={skip}"
            url = f"{base_url}?{search_query}"
            
            print(f"  Fetching records {skip} to {skip + limit}...")
            
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'results' in data and len(data['results']) > 0:
                    records = data['results']
                    all_records.extend(records)
                    total_fetched += len(records)
                    print(f"  ✓ Retrieved {len(records)} records (Total: {total_fetched})")
                    
                    # If we got fewer records than the limit, we've reached the end
                    if len(records) < limit:
                        print(f"  ✓ Reached end of results for this query")
                        break
                    
                    skip += limit
                    time.sleep(0.5)  # Rate limiting
                else:
                    print(f"  ✓ No more results for this query")
                    break
                    
            elif response.status_code == 404:
                print(f"  ✓ No results found for this query")
                break
            else:
                print(f"  ✗ Error: HTTP {response.status_code}")
                break
                
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            break
    
    time.sleep(1)  # Pause between queries

print(f"\n{'=' * 80}")
print(f"TOTAL RECORDS FETCHED: {len(all_records)}")
print(f"{'=' * 80}")

if len(all_records) == 0:
    print("\n⚠️ No records found. This might mean:")
    print("  1. Brand name spelling is different in MAUDE database")
    print("  2. Device is registered under Abbott or different manufacturer name")
    print("  3. Device name variations not captured")
    exit(0)

# Process the records
print(f"\nProcessing {len(all_records)} records...")

processed_data = []

for record in all_records:
    try:
        # Extract basic info
        mdr_report_key = record.get('mdr_report_key', '')
        report_number = record.get('report_number', '')
        
        # Date received (stored as YYYYMMDD integer)
        date_received = record.get('date_received', '')
        
        # Event type
        event_type = record.get('event_type', '')
        
        # Get device info
        device_info = record.get('device', [{}])[0] if record.get('device') else {}
        manufacturer_name = device_info.get('manufacturer_d_name', '')
        brand_name = device_info.get('brand_name', '')
        generic_name = device_info.get('generic_name', '')
        device_class = device_info.get('device_class', '')
        
        # Get patient info
        patient = record.get('patient', [{}])[0] if record.get('patient') else {}
        
        # Patient problems (multiple possible)
        patient_problems = patient.get('patient_problems', []) if patient else []
        if isinstance(patient_problems, list):
            patient_problems = [p for p in patient_problems if p is not None]
            patient_problems = ', '.join(patient_problems) if patient_problems else ''
        
        # Event description
        event_description = record.get('mdr_text', [{}])[0].get('text', '') if record.get('mdr_text') else ''
        
        # Adverse event flag
        adverse_event_flag = record.get('adverse_event_flag', '')
        
        # Report source
        report_source = record.get('report_source_code', '')
        
        processed_data.append({
            'mdr_report_key': mdr_report_key,
            'report_number': report_number,
            'date_received': date_received,
            'event_type': event_type,
            'manufacturer_name': manufacturer_name,
            'brand_name': brand_name,
            'generic_name': generic_name,
            'device_class': device_class,
            'event_description': patient_problems,
            'adverse_event_flag': adverse_event_flag,
            'report_source': report_source
        })
        
    except Exception as e:
        print(f"Error processing record: {str(e)}")
        continue

# Create DataFrame
df = pd.DataFrame(processed_data)

print(f"\n✓ Processed {len(df)} records into DataFrame")

# Remove duplicates
df = df.drop_duplicates(subset=['mdr_report_key'])
print(f"✓ After removing duplicates: {len(df)} unique records")

# Save to Excel
output_file = 'benchmark_cases_expansion_21/abbott_freestyle_libre_cgm.xlsx'
df.to_excel(output_file, index=False)

print(f"\n{'=' * 80}")
print(f"✅ SUCCESS!")
print(f"{'=' * 80}")
print(f"File saved: {output_file}")
print(f"Total MDRs: {len(df):,}")

# Print summary statistics
if len(df) > 0:
    print(f"\n📊 SUMMARY STATISTICS:")
    print(f"  Date range: {df['date_received'].min()} to {df['date_received'].max()}")
    print(f"  Event types: {df['event_type'].value_counts().to_dict()}")
    print(f"  Unique manufacturers: {df['manufacturer_name'].nunique()}")
    print(f"  Most common brand names: {df['brand_name'].value_counts().head(3).to_dict()}")

print(f"\n{'=' * 80}")
