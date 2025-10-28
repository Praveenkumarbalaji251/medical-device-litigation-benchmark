import requests

BASE_URL = "https://api.fda.gov/device/event.json"

print("=" * 80)
print("BARD POWERPORT - 1 YEAR BEFORE LITIGATION")
print("Case Filed: August 2022")
print("=" * 80)
print()

params = {
    'search': 'device.brand_name:"PowerPort"',
    'count': 'date_received',
    'limit': 1000
}

response = requests.get(BASE_URL, params=params, timeout=30)
data = response.json()
results = data.get('results', [])

# Group by YYYY-MM
monthly = {}
for item in results:
    date_str = item['time']  # Format: YYYYMMDD
    year_month = date_str[:4] + '-' + date_str[4:6]
    if year_month not in monthly:
        monthly[year_month] = 0
    monthly[year_month] += item['count']

# Print Aug 2021 - July 2022
months = [
    '2021-08', '2021-09', '2021-10', '2021-11', '2021-12',
    '2022-01', '2022-02', '2022-03', '2022-04', '2022-05', '2022-06', '2022-07'
]

print("MONTHLY MDR COUNT (1 year before Aug 2022 filing):")
print("-" * 60)

total = 0
for month in months:
    count = monthly.get(month, 0)
    total += count
    print(f"{month}: {count:4d} reports")

print("-" * 60)
print(f"TOTAL:  {total:4d} reports in 1 year before filing")
print()

# Calculate spike
first = monthly.get('2021-08', 1)
last = monthly.get('2022-07', 1)
multiplier = last / first if first > 0 else 0

print(f"Aug 2021 (baseline): {first} reports")
print(f"Jul 2022 (filing month): {last} reports")
print(f"Multiplier: {multiplier:.1f}x")
print()

# Show pattern
print("=" * 80)
print("FULL TIMELINE (2018-2025)")
print("=" * 80)
print()

for year in ['2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025']:
    year_total = sum(count for ym, count in monthly.items() if ym.startswith(year))
    print(f"{year}: {year_total:5d} reports")

print()
print("NOTE: Litigation filed August 2022")
print("Big spike in Nov 2022 (313 reports) - 3 months after filing")
