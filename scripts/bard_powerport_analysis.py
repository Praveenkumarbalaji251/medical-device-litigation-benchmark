#!/usr/bin/env python3
"""
Bard PowerPort Catheter - MDR Analysis
Case filed: August 2022
Analyzing 1 year before filing (Aug 2021 - July 2022)
"""

import requests
import json
from datetime import datetime

def get_powerport_mdrs_monthly(start_date, end_date):
    """
    Get monthly MDR counts for Bard PowerPort
    Period: Aug 2021 - July 2022 (1 year before litigation)
    """
    
    base_url = "https://api.fda.gov/device/event.json"
    
    # Monthly breakdown
    months = [
        ("2021-08-01", "2021-08-31", "Aug 2021"),
        ("2021-09-01", "2021-09-30", "Sep 2021"),
        ("2021-10-01", "2021-10-31", "Oct 2021"),
        ("2021-11-01", "2021-11-30", "Nov 2021"),
        ("2021-12-01", "2021-12-31", "Dec 2021"),
        ("2022-01-01", "2022-01-31", "Jan 2022"),
        ("2022-02-01", "2022-02-28", "Feb 2022"),
        ("2022-03-01", "2022-03-31", "Mar 2022"),
        ("2022-04-01", "2022-04-30", "Apr 2022"),
        ("2022-05-01", "2022-05-31", "May 2022"),
        ("2022-06-01", "2022-06-30", "Jun 2022"),
        ("2022-07-01", "2022-07-31", "Jul 2022")
    ]
    
    print("=" * 80)
    print("BARD POWERPORT CATHETER - MDR ANALYSIS")
    print("=" * 80)
    print(f"Case Filed: August 2022")
    print(f"Analysis Period: Aug 2021 - July 2022 (1 year before)")
    print(f"Device: PowerPort Implantable Port Catheter System")
    print("=" * 80)
    print()
    
    results = []
    
    for start, end, label in months:
        # Search for PowerPort
        search_query = f'device.brand_name:"PowerPort" AND date_received:[{start}+TO+{end}]'
        
        params = {
            'search': search_query,
            'limit': 1
        }
        
        try:
            response = requests.get(base_url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                total = data.get('meta', {}).get('results', {}).get('total', 0)
                results.append({
                    'month': label,
                    'count': total,
                    'start': start,
                    'end': end
                })
                print(f"{label}: {total} reports")
            else:
                print(f"{label}: API error {response.status_code}")
                results.append({
                    'month': label,
                    'count': 0,
                    'start': start,
                    'end': end,
                    'error': True
                })
        except Exception as e:
            print(f"{label}: Error - {str(e)}")
            results.append({
                'month': label,
                'count': 0,
                'start': start,
                'end': end,
                'error': True
            })
    
    return results

def get_event_type_breakdown():
    """
    Get breakdown by event type for PowerPort
    """
    base_url = "https://api.fda.gov/device/event.json"
    
    print("\n" + "=" * 80)
    print("EVENT TYPE BREAKDOWN (Aug 2021 - July 2022)")
    print("=" * 80)
    
    # Query for the full year
    search_query = 'device.brand_name:"PowerPort" AND date_received:[2021-08-01+TO+2022-07-31]'
    
    # Get event type breakdown
    params = {
        'search': search_query,
        'count': 'event_type.exact'
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            
            total = sum(item['count'] for item in results)
            
            print(f"\nTotal Reports: {total}")
            print("\nBreakdown by Event Type:")
            print("-" * 40)
            
            for item in results:
                event_type = item['term']
                count = item['count']
                percentage = (count / total * 100) if total > 0 else 0
                print(f"{event_type:20s}: {count:6d} ({percentage:5.1f}%)")
            
            return results
        else:
            print(f"API Error: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error: {str(e)}")
        return []

def get_device_problem_breakdown():
    """
    Get top device problems for PowerPort
    """
    base_url = "https://api.fda.gov/device/event.json"
    
    print("\n" + "=" * 80)
    print("TOP 10 DEVICE PROBLEMS (Aug 2021 - July 2022)")
    print("=" * 80)
    
    search_query = 'device.brand_name:"PowerPort" AND date_received:[2021-08-01+TO+2022-07-31]'
    
    params = {
        'search': search_query,
        'count': 'device.device_event_key.exact',
        'limit': 10
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            
            print("\nTop Device Problems:")
            print("-" * 60)
            
            for i, item in enumerate(results[:10], 1):
                problem = item['term']
                count = item['count']
                print(f"{i:2d}. {problem:45s}: {count:5d} reports")
            
            return results
        else:
            print(f"API Error: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error: {str(e)}")
        return []

if __name__ == "__main__":
    print("\nFetching monthly MDR counts...")
    monthly_results = get_powerport_mdrs_monthly("2021-08-01", "2022-07-31")
    
    print("\nFetching event type breakdown...")
    event_types = get_event_type_breakdown()
    
    print("\nFetching device problems...")
    problems = get_device_problem_breakdown()
    
    # Calculate trend
    if monthly_results:
        counts = [r['count'] for r in monthly_results if not r.get('error')]
        if counts:
            first_month = counts[0] if counts[0] > 0 else 1
            last_month = counts[-1]
            multiplier = last_month / first_month
            
            print("\n" + "=" * 80)
            print("TREND ANALYSIS")
            print("=" * 80)
            print(f"First Month (Aug 2021): {first_month} reports")
            print(f"Last Month (Jul 2022):  {last_month} reports")
            print(f"Increase Multiplier:    {multiplier:.1f}x")
            print(f"Case Filed:             August 2022")
            print("=" * 80)
