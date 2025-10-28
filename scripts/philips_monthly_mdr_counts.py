#!/usr/bin/env python3
"""
Get monthly MDR counts for Philips DreamStation Jan-July 2021
The critical 6-month window before litigation
"""

import requests
import json
from datetime import datetime

def get_monthly_count(device_name, year, month):
    """Get MDR count for a specific month."""
    
    # Calculate date range for the month
    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year
    
    # Format dates as YYYYMMDD
    start_date = f"{year}{month:02d}01"
    
    # Last day of month
    from calendar import monthrange
    last_day = monthrange(year, month)[1]
    end_date = f"{year}{month:02d}{last_day}"
    
    url = "https://api.fda.gov/device/event.json"
    
    # Build query
    search_query = f'device.brand_name:{device_name} AND date_received:[{start_date} TO {end_date}]'
    
    params = {
        'search': search_query,
        'limit': 1
    }
    
    month_name = datetime(year, month, 1).strftime('%B')
    print(f"📅 {month_name} {year}: ", end='', flush=True)
    
    try:
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            if 'meta' in data and 'results' in data['meta']:
                total = data['meta']['results']['total']
                print(f"{total:,} reports")
                return total
            else:
                print(f"0 reports")
                return 0
        else:
            print(f"❌ Error {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def get_event_breakdown(device_name, year, month):
    """Get breakdown of event types for a month."""
    
    from calendar import monthrange
    last_day = monthrange(year, month)[1]
    
    start_date = f"{year}{month:02d}01"
    end_date = f"{year}{month:02d}{last_day}"
    
    url = "https://api.fda.gov/device/event.json"
    
    results = {
        'deaths': 0,
        'injuries': 0,
        'malfunctions': 0
    }
    
    # Count deaths
    search_query = f'device.brand_name:{device_name} AND date_received:[{start_date} TO {end_date}] AND event_type:Death'
    response = requests.get(url, params={'search': search_query, 'limit': 1}, timeout=30)
    if response.status_code == 200:
        data = response.json()
        if 'meta' in data and 'results' in data['meta']:
            results['deaths'] = data['meta']['results']['total']
    
    # Count injuries
    search_query = f'device.brand_name:{device_name} AND date_received:[{start_date} TO {end_date}] AND event_type:Injury'
    response = requests.get(url, params={'search': search_query, 'limit': 1}, timeout=30)
    if response.status_code == 200:
        data = response.json()
        if 'meta' in data and 'results' in data['meta']:
            results['injuries'] = data['meta']['results']['total']
    
    # Count malfunctions
    search_query = f'device.brand_name:{device_name} AND date_received:[{start_date} TO {end_date}] AND event_type:Malfunction'
    response = requests.get(url, params={'search': search_query, 'limit': 1}, timeout=30)
    if response.status_code == 200:
        data = response.json()
        if 'meta' in data and 'results' in data['meta']:
            results['malfunctions'] = data['meta']['results']['total']
    
    return results

def main():
    """Get monthly counts for Jan-July 2021."""
    
    print("🔬 PHILIPS DREAMSTATION - MONTHLY MDR COUNTS")
    print("=" * 70)
    print("Critical 6-month window before litigation filing (July 1, 2021)")
    print("=" * 70)
    
    device = "DreamStation"
    year = 2021
    
    monthly_data = []
    
    # Get counts for Jan-July 2021
    print("\n📊 MONTHLY REPORT COUNTS:")
    print("-" * 70)
    
    for month in range(1, 8):  # Jan through July
        count = get_monthly_count(device, year, month)
        
        if count is not None:
            monthly_data.append({
                'month': month,
                'month_name': datetime(year, month, 1).strftime('%B'),
                'count': count
            })
    
    # Calculate escalation
    print("\n" + "=" * 70)
    print("📈 ESCALATION ANALYSIS:")
    print("=" * 70)
    
    if len(monthly_data) >= 2:
        baseline = monthly_data[0]['count']  # First available month
        
        print(f"\nBaseline ({monthly_data[0]['month_name']} 2021): {baseline:,} reports")
        print(f"\nMonth-over-month increase:\n")
        
        for i, data in enumerate(monthly_data):
            if i == 0:
                print(f"  {data['month_name']:10s}: {data['count']:6,} reports (baseline)")
            else:
                increase = ((data['count'] - baseline) / baseline * 100) if baseline > 0 else 0
                increase_from_prev = ((data['count'] - monthly_data[i-1]['count']) / monthly_data[i-1]['count'] * 100) if monthly_data[i-1]['count'] > 0 else 0
                print(f"  {data['month_name']:10s}: {data['count']:6,} reports (+{increase:6.1f}% from baseline, +{increase_from_prev:5.1f}% from prev month)")
        
        # Find June data
        june_data = next((d for d in monthly_data if d['month'] == 6), None)
        
        if june_data:
            june_count = june_data['count']
            total_increase = ((june_count - baseline) / baseline * 100) if baseline > 0 else 0
            
            print(f"\n🎯 PRE-LITIGATION WINDOW SUMMARY:")
            print(f"   Start: {baseline:,} reports ({monthly_data[0]['month_name']})")
            print(f"   Peak (June):   {june_count:,} reports")
            print(f"   Increase: {total_increase:.1f}%")
            
            if total_increase > 300:
                print(f"   ⚠️  WARNING: >300% increase detected!")
                print(f"   🚨 LITIGATION RISK: CRITICAL")
        
        # July (litigation filed)
        july_data = next((d for d in monthly_data if d['month'] == 7), None)
        if july_data:
            july_count = july_data['count']
            print(f"\n📅 July 2021 (Litigation Filed July 1):")
            print(f"   Reports: {july_count:,}")
            print(f"   Increase from baseline: {((july_count - baseline) / baseline * 100):.1f}%")
    
    # Get detailed breakdown for key months
    print("\n" + "=" * 70)
    print("💀 DETAILED BREAKDOWN FOR KEY MONTHS:")
    print("=" * 70)
    
    key_months = [
        (1, 'January 2021 (Baseline)'),
        (6, 'June 2021 (Month before recall)'),
        (7, 'July 2021 (Litigation filed)')
    ]
    
    for month, label in key_months:
        print(f"\n{label}:")
        
        # Find the matching month in monthly_data
        month_info = next((d for d in monthly_data if d['month'] == month), None)
        
        if month_info:
            breakdown = get_event_breakdown(device, year, month)
            total = month_info['count']
            
            print(f"  Total Reports: {total:,}")
            if total > 0:
                print(f"  Deaths:        {breakdown['deaths']:,} ({breakdown['deaths']/total*100:.1f}%)")
                print(f"  Injuries:      {breakdown['injuries']:,} ({breakdown['injuries']/total*100:.1f}%)")
                print(f"  Malfunctions:  {breakdown['malfunctions']:,} ({breakdown['malfunctions']/total*100:.1f}%)")
            else:
                print(f"  No data available")
        else:
            print(f"  No data available for this month")
    
    # Save to JSON
    june_data = next((d for d in monthly_data if d['month'] == 6), None)
    july_data = next((d for d in monthly_data if d['month'] == 7), None)
    
    output = {
        'device': device,
        'analysis_period': 'January - July 2021',
        'litigation_date': '2021-07-01',
        'monthly_counts': monthly_data,
        'summary': {
            'baseline': monthly_data[0]['count'] if monthly_data else 0,
            'peak_june': june_data['count'] if june_data else 0,
            'litigation_month_july': july_data['count'] if july_data else 0,
            'increase_pct': total_increase if june_data else 0
        }
    }
    
    output_file = 'philips_monthly_mdr_jan_july_2021.json'
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    print("\n" + "=" * 70)
    print(f"✅ Data saved to: {output_file}")
    print("=" * 70)

if __name__ == "__main__":
    main()
