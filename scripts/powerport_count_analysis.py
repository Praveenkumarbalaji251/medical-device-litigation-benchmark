import requests
import json

BASE_URL = "https://api.fda.gov/device/event.json"

print("=" * 80)
print("BARD POWERPORT - MDR ANALYSIS")
print("Case Filed: August 2022")
print("=" * 80)
print()

# Get count by date using aggregation (avoids 500 errors)
print("Getting monthly counts for Aug 2021 - July 2022...")
print()

params = {
    'search': 'device.brand_name:"PowerPort"',
    'count': 'date_received'
}

try:
    response = requests.get(BASE_URL, params=params, timeout=30)
    
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])
        
        # Filter to Aug 2021 - July 2022
        target_months = []
        for item in results:
            date_str = item['time']  # Format: YYYY-MM-DD
            if '2021-08' <= date_str <= '2022-07':
                target_months.append(item)
        
        # Group by month
        monthly = {}
        for item in target_months:
            month = item['time'][:7]  # YYYY-MM
            if month not in monthly:
                monthly[month] = 0
            monthly[month] += item['count']
        
        # Print monthly breakdown
        print("MONTHLY BREAKDOWN (1 year before litigation):")
        print("-" * 60)
        
        months_ordered = [
            '2021-08', '2021-09', '2021-10', '2021-11', '2021-12',
            '2022-01', '2022-02', '2022-03', '2022-04', '2022-05', '2022-06', '2022-07'
        ]
        
        total = 0
        for month in months_ordered:
            count = monthly.get(month, 0)
            total += count
            print(f"{month}: {count:4d} reports")
        
        print("-" * 60)
        print(f"TOTAL:  {total:4d} reports")
        print()
        
        # Calculate trend
        first_count = monthly.get('2021-08', 0)
        last_count = monthly.get('2022-07', 0)
        
        if first_count > 0:
            multiplier = last_count / first_count
            print(f"Aug 2021: {first_count} reports")
            print(f"Jul 2022: {last_count} reports (month before filing)")
            print(f"Increase: {multiplier:.1f}x")
        
    else:
        print(f"Error: {response.status_code}")
        
except Exception as e:
    print(f"Error: {str(e)}")

# Get event type breakdown
print()
print("=" * 80)
print("EVENT TYPE BREAKDOWN")
print("=" * 80)

params = {
    'search': 'device.brand_name:"PowerPort"',
    'count': 'event_type.exact'
}

try:
    response = requests.get(BASE_URL, params=params, timeout=30)
    
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])
        
        total = sum(item['count'] for item in results)
        
        print(f"\nTotal PowerPort reports: {total}")
        print("\nBreakdown:")
        print("-" * 40)
        
        for item in results:
            event_type = item['term']
            count = item['count']
            percentage = (count / total * 100) if total > 0 else 0
            print(f"{event_type:20s}: {count:6d} ({percentage:5.1f}%)")
    
except Exception as e:
    print(f"Error: {str(e)}")
