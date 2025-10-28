import requests
import pandas as pd
from datetime import datetime

BASE_URL = "https://api.fda.gov/device/event.json"

# 3 CATHETER LAWSUITS
CATHETER_CASES = [
    {
        "name": "Bard PowerPort",
        "brand": "PowerPort",
        "manufacturer": "Bard",
        "case_filed": "2022-08-01",
        "analysis_start": "2021-08",
        "analysis_end": "2022-07",
        "description": "Implantable port catheter - infections, fractures, migration"
    },
    {
        "name": "Cook IVC Filter",
        "brand": "Celect",
        "manufacturer": "Cook",
        "case_filed": "2014-08-01",
        "analysis_start": "2013-08",
        "analysis_end": "2014-07",
        "description": "Inferior vena cava filter - fractures, migration, perforation"
    },
    {
        "name": "Bard IVC Filter",
        "brand": "G2",
        "manufacturer": "Bard",
        "case_filed": "2015-04-01",
        "analysis_start": "2014-10",
        "analysis_end": "2015-03",
        "description": "IVC filter - fractures, migration, organ perforation"
    }
]

def get_monthly_data(brand_name):
    """Get all monthly MDR data for a device"""
    params = {
        'search': f'device.brand_name:"{brand_name}"',
        'count': 'date_received',
        'limit': 1000
    }
    
    try:
        response = requests.get(BASE_URL, params=params, timeout=30)
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            
            monthly = {}
            for item in results:
                date_str = item['time']
                year_month = date_str[:4] + '-' + date_str[4:6]
                if year_month not in monthly:
                    monthly[year_month] = 0
                monthly[year_month] += item['count']
            
            return monthly
        else:
            return {}
    except Exception as e:
        print(f"  Error: {str(e)}")
        return {}

def get_event_types(brand_name):
    """Get event type breakdown"""
    params = {
        'search': f'device.brand_name:"{brand_name}"',
        'count': 'event_type.exact'
    }
    
    try:
        response = requests.get(BASE_URL, params=params, timeout=30)
        if response.status_code == 200:
            data = response.json()
            return data.get('results', [])
        return []
    except:
        return []

def analyze_catheter(device):
    """Analyze single catheter device"""
    print("=" * 80)
    print(f"ANALYZING: {device['name']}")
    print("=" * 80)
    print(f"Brand: {device['brand']}")
    print(f"Manufacturer: {device['manufacturer']}")
    print(f"Case Filed: {device['case_filed']}")
    print(f"Description: {device['description']}")
    print(f"Analysis Period: {device['analysis_start']} to {device['analysis_end']}")
    print()
    
    # Get data
    print("Fetching MDR data...")
    monthly = get_monthly_data(device['brand'])
    
    if not monthly:
        print("No data found")
        print()
        return None
    
    event_types = get_event_types(device['brand'])
    
    # Calculate totals
    total_all = sum(monthly.values())
    
    # Get 6-month period
    from dateutil.relativedelta import relativedelta
    start_date = datetime.strptime(device['analysis_start'], "%Y-%m")
    end_date = datetime.strptime(device['analysis_end'], "%Y-%m")
    
    analysis_months = []
    current = start_date
    while current <= end_date:
        analysis_months.append(current.strftime("%Y-%m"))
        current = current + relativedelta(months=1)
    
    # Get counts
    analysis_counts = []
    for month in analysis_months:
        count = monthly.get(month, 0)
        analysis_counts.append({'month': month, 'count': count})
    
    total_6month = sum(m['count'] for m in analysis_counts)
    
    # Calculate pattern
    first_month = 0
    for m in analysis_counts:
        if m['count'] > 0:
            first_month = m['count']
            break
    
    last_month = analysis_counts[-1]['count'] if analysis_counts else 0
    multiplier = last_month / first_month if first_month > 0 else 0
    
    # Event stats
    total_events = sum(e['count'] for e in event_types)
    deaths = next((e['count'] for e in event_types if e['term'] == 'Death'), 0)
    injuries = next((e['count'] for e in event_types if e['term'] == 'Injury'), 0)
    malfunctions = next((e['count'] for e in event_types if e['term'] == 'Malfunction'), 0)
    
    # Print results
    print("RESULTS:")
    print("-" * 60)
    print(f"Total reports (all time): {total_all:,}")
    print(f"6-month period: {total_6month:,}")
    print()
    print("Monthly breakdown:")
    for m in analysis_counts:
        print(f"  {m['month']}: {m['count']:5d} reports")
    print()
    print(f"First month: {first_month:5d}")
    print(f"Last month:  {last_month:5d}")
    print(f"Multiplier:  {multiplier:5.1f}x")
    print()
    print("Event Types:")
    print(f"  Deaths:       {deaths:6d} ({deaths/total_events*100 if total_events else 0:5.1f}%)")
    print(f"  Injuries:     {injuries:6d} ({injuries/total_events*100 if total_events else 0:5.1f}%)")
    print(f"  Malfunctions: {malfunctions:6d} ({malfunctions/total_events*100 if total_events else 0:5.1f}%)")
    print()
    
    # Pattern
    if multiplier > 10:
        pattern = "EXPLOSIVE"
    elif multiplier > 4:
        pattern = "STRONG SPIKE"
    elif multiplier > 2:
        pattern = "MODERATE SPIKE"
    elif multiplier < 1:
        pattern = "REVERSE/FLAT"
    else:
        pattern = "MINIMAL CHANGE"
    
    print(f"PATTERN: {pattern}")
    print()
    
    return {
        'device': device['name'],
        'brand': device['brand'],
        'case_filed': device['case_filed'],
        'total_all_time': total_all,
        'total_6month': total_6month,
        'first_month': first_month,
        'last_month': last_month,
        'multiplier': multiplier,
        'pattern': pattern,
        'deaths': deaths,
        'injuries': injuries,
        'malfunctions': malfunctions,
        'monthly_counts': analysis_counts
    }

def main():
    print("\n")
    print("=" * 80)
    print("3 CATHETER LAWSUIT PATTERN ANALYSIS")
    print("Analyzing 6 months before litigation filing")
    print("=" * 80)
    print("\n")
    
    results = []
    
    for device in CATHETER_CASES:
        result = analyze_catheter(device)
        if result:
            results.append(result)
        print()
    
    # Summary
    print("=" * 80)
    print("SUMMARY - CATHETER LITIGATION PATTERNS")
    print("=" * 80)
    print()
    
    for r in results:
        print(f"{r['device']:30s}: {r['multiplier']:5.1f}x - {r['pattern']}")
        print(f"  Total reports: {r['total_all_time']:,}")
        print(f"  Deaths: {r['deaths']}, Injuries: {r['injuries']}")
        print()
    
    # Save
    import json
    with open('catheter_lawsuit_patterns.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("✓ Data saved to: catheter_lawsuit_patterns.json")
    print()

if __name__ == "__main__":
    main()
