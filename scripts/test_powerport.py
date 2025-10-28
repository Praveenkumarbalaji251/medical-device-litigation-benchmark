import requests

BASE_URL = "https://api.fda.gov/device/event.json"

print("Testing FDA API for PowerPort...")
print()

# Try simplest query first
params = {
    'search': 'device.brand_name:"PowerPort"',
    'limit': 1
}

try:
    response = requests.get(BASE_URL, params=params, timeout=30)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        total = data.get('meta', {}).get('results', {}).get('total', 0)
        print(f"Total PowerPort reports: {total}")
    else:
        print(f"Error: {response.status_code}")
        print("FDA API is currently unavailable")
except Exception as e:
    print(f"Error: {str(e)}")
