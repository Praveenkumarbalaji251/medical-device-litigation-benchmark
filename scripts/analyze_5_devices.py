import requests
import json
from datetime import datetime

BASE_URL = "https://api.fda.gov/device/event.json"

# 5 devices for analysis
DEVICES = [
    {
        "name": "Philips DreamStation",
        "brand": "DreamStation",
        "case_filed": "2021-07-01",
        "analysis_start": "2021-01",
        "analysis_end": "2021-06"
    },
    {
        "name": "Bard PowerPort",
        "brand": "PowerPort",
        "case_filed": "2022-08-01",
        "analysis_start": "2021-08",
        "analysis_end": "2022-07"
    },
    {
        "name": "Bard Composix Kugel",
        "brand": "Composix",
        "case_filed": "2006-03-01",
        "analysis_start": "2005-09",
        "analysis_end": "2006-02"
    },
    {
        "name": "Smith & Nephew BHR",
        "brand": "Birmingham Hip",
        "case_filed": "2017-04-01",
        "analysis_start": "2016-10",
        "analysis_end": "2017-03"
    },
    {
        "name": "Zimmer NexGen Knee",
        "brand": "NexGen",
        "case_filed": "2010-06-01",
        "analysis_start": "2009-12",
        "analysis_end": "2010-05"
    }
]

def get_all_monthly_data(brand_name):
    """Get all monthly data for a device"""
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
            
            # Group by month
            monthly = {}
            for item in results:
                date_str = item['time']
                year_month = date_str[:4] + '-' + date_str[4:6]
                if year_month not in monthly:
                    monthly[year_month] = 0
                monthly[year_month] += item['count']
            
            return monthly
        else:
            print(f"  API Error: {response.status_code}")
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
        else:
            return []
    except Exception as e:
        return []

def analyze_device(device):
    """Analyze single device"""
    print("=" * 80)
    print(f"ANALYZING: {device['name']}")
    print("=" * 80)
    print(f"Brand: {device['brand']}")
    print(f"Case Filed: {device['case_filed']}")
    print(f"Analysis Period: {device['analysis_start']} to {device['analysis_end']}")
    print()
    
    # Get monthly data
    print("Fetching monthly MDR data...")
    monthly = get_all_monthly_data(device['brand'])
    
    if not monthly:
        print("No data found")
        return None
    
    # Get event types
    print("Fetching event types...")
    event_types = get_event_types(device['brand'])
    
    # Calculate totals
    total_all_time = sum(monthly.values())
    
    # Get 6-month analysis period
    from datetime import datetime
    from dateutil.relativedelta import relativedelta
    
    analysis_months = []
    start_date = datetime.strptime(device['analysis_start'], "%Y-%m")
    end_date = datetime.strptime(device['analysis_end'], "%Y-%m")
    
    current = start_date
    while current <= end_date:
        month_str = current.strftime("%Y-%m")
        analysis_months.append(month_str)
        current = current + relativedelta(months=1)
    
    # Get counts for analysis period
    analysis_counts = []
    for month in analysis_months:
        count = monthly.get(month, 0)
        analysis_counts.append({
            'month': month,
            'count': count
        })
    
    total_6month = sum(m['count'] for m in analysis_counts)
    
    # Calculate spike (use first non-zero month as baseline)
    first_month = 0
    for m in analysis_counts:
        if m['count'] > 0:
            first_month = m['count']
            break
    
    last_month = analysis_counts[-1]['count'] if analysis_counts else 0
    multiplier = last_month / first_month if first_month > 0 else 0
    
    # Event type stats
    total_events = sum(e['count'] for e in event_types)
    deaths = next((e['count'] for e in event_types if e['term'] == 'Death'), 0)
    injuries = next((e['count'] for e in event_types if e['term'] == 'Injury'), 0)
    malfunctions = next((e['count'] for e in event_types if e['term'] == 'Malfunction'), 0)
    
    # Print results
    print()
    print("RESULTS:")
    print("-" * 60)
    print(f"Total reports (all time): {total_all_time:,}")
    print(f"6-month period total: {total_6month:,}")
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
    
    # Determine pattern
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
        'total_all_time': total_all_time,
        'total_6month': total_6month,
        'first_month': first_month,
        'last_month': last_month,
        'multiplier': multiplier,
        'pattern': pattern,
        'deaths': deaths,
        'injuries': injuries,
        'malfunctions': malfunctions,
        'monthly_counts': analysis_counts,
        'event_types': event_types
    }

def main():
    """Analyze all 5 devices"""
    print("\n")
    print("=" * 80)
    print("5 DEVICE MDR ANALYSIS")
    print("Analyzing 6 months before litigation filing")
    print("=" * 80)
    print("\n")
    
    results = []
    
    for device in DEVICES:
        result = analyze_device(device)
        if result:
            results.append(result)
        print("\n")
    
    # Save results
    output_file = 'five_device_analysis.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()
    
    for r in results:
        print(f"{r['device']:30s}: {r['multiplier']:5.1f}x - {r['pattern']}")
    
    print()
    print(f"✓ Detailed results saved to: {output_file}")
    print()

if __name__ == "__main__":
    main()
