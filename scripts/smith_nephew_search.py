import requests
import pandas as pd

BASE_URL = "https://api.fda.gov/device/event.json"

print("=" * 80)
print("SMITH & NEPHEW - ALL DEVICES - LAST 5 YEARS")
print("=" * 80)
print()

# Try different search variations
searches = [
    'device.manufacturer_d_name:"SMITH"',
    'device.manufacturer_d_name:"SMITH & NEPHEW"',
    'device.manufacturer_d_name:"SMITH AND NEPHEW"'
]

all_records = []

for search_query in searches:
    print(f"Trying: {search_query}")
    
    params = {
        'search': search_query,
        'limit': 100,
        'skip': 0
    }
    
    page = 0
    while page < 100:
        params['skip'] = page * 100
        
        try:
            response = requests.get(BASE_URL, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                
                if not results:
                    break
                
                all_records.extend(results)
                page += 1
                print(f"  Page {page}: {len(results)} records (total: {len(all_records)})")
                
                if len(results) < 100:
                    break
            else:
                print(f"  Error: {response.status_code}")
                break
                
        except Exception as e:
            print(f"  Error: {str(e)}")
            break
    
    if all_records:
        print(f"  ✓ Found {len(all_records)} records with this query")
        break
    else:
        print(f"  No results")
        print()

if not all_records:
    print("No records found. Trying device list approach...")
    
    # Try specific devices
    devices = [
        "Birmingham Hip",
        "BHR",
        "R3",
        "OXINIUM",
        "LEGION",
        "JOURNEY"
    ]
    
    for device in devices:
        print(f"Trying device: {device}")
        params = {
            'search': f'device.brand_name:"{device}"',
            'limit': 100
        }
        
        try:
            response = requests.get(BASE_URL, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                print(f"  Found: {len(results)} records")
                all_records.extend(results)
        except Exception as e:
            print(f"  Error: {e}")

print()
print(f"TOTAL RECORDS: {len(all_records)}")

if not all_records:
    print("No data found. Checking API status...")
    test_response = requests.get(BASE_URL + "?search=report_number:*&limit=1")
    print(f"API Status: {test_response.status_code}")
