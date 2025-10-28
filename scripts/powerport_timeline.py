import requests

BASE_URL = "https://api.fda.gov/device/event.json"

print("=" * 80)
print("BARD POWERPORT - WHEN ARE THE REPORTS?")
print("Total: 5,940 reports")
print("=" * 80)
print()

params = {
    'search': 'device.brand_name:"PowerPort"',
    'count': 'date_received',
    'limit': 1000
}

try:
    response = requests.get(BASE_URL, params=params, timeout=30)
    
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])
        
        # Group by year
        by_year = {}
        for item in results:
            year = item['time'][:4]
            if year not in by_year:
                by_year[year] = 0
            by_year[year] += item['count']
        
        print("REPORTS BY YEAR:")
        print("-" * 40)
        for year in sorted(by_year.keys()):
            print(f"{year}: {by_year[year]:5d} reports")
        
        print()
        print("MONTH-BY-MONTH (2021-2023):")
        print("-" * 40)
        
        for item in sorted(results, key=lambda x: x['time']):
            date_str = item['time']
            if '2021' <= date_str <= '2023':
                print(f"{date_str}: {item['count']:4d} reports")
        
except Exception as e:
    print(f"Error: {str(e)}")
