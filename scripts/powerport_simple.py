#!/usr/bin/env python3
"""
Bard PowerPort - Simple MDR Counter
Using simpler query approach
"""

import requests

def get_powerport_total():
    """Get total PowerPort reports"""
    base_url = "https://api.fda.gov/device/event.json"
    
    # Try simple brand name search
    params = {
        'search': 'device.brand_name:PowerPort',
        'limit': 1
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=30)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            total = data.get('meta', {}).get('results', {}).get('total', 0)
            print(f"Total PowerPort reports: {total}")
            return total
        else:
            print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"Error: {str(e)}")
    
    return 0

def get_powerport_by_year(year):
    """Get PowerPort reports for specific year"""
    base_url = "https://api.fda.gov/device/event.json"
    
    params = {
        'search': f'device.brand_name:PowerPort AND date_received:[{year}0101+TO+{year}1231]',
        'limit': 1
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            total = data.get('meta', {}).get('results', {}).get('total', 0)
            print(f"{year}: {total} reports")
            return total
        else:
            print(f"{year}: Error {response.status_code}")
    except Exception as e:
        print(f"{year}: Error - {str(e)}")
    
    return 0

if __name__ == "__main__":
    print("=" * 60)
    print("BARD POWERPORT MDR ANALYSIS")
    print("=" * 60)
    print()
    
    print("Total reports (all time):")
    total = get_powerport_total()
    print()
    
    print("Yearly breakdown:")
    print("-" * 60)
    for year in [2020, 2021, 2022, 2023, 2024]:
        get_powerport_by_year(year)
    print()
    print("Case filed: August 2022")
