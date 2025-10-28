#!/usr/bin/env python3
"""
Simple MDR Event Counter - Direct API calls that work
"""

import requests
import json
from datetime import datetime

def count_device_events(device_name):
    """Get total count for a device."""
    
    url = "https://api.fda.gov/device/event.json"
    params = {
        'search': f'device.brand_name:{device_name}',
        'limit': 1
    }
    
    print(f"🔍 Counting events for: {device_name}")
    
    try:
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            total = data['meta']['results']['total']
            print(f"✅ Total Events: {total:,}")
            return total
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def count_deaths(device_name):
    """Count death events."""
    
    url = "https://api.fda.gov/device/event.json"
    params = {
        'search': f'device.brand_name:{device_name} AND event_type:Death',
        'limit': 1
    }
    
    print(f"💀 Counting deaths for: {device_name}")
    
    try:
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            total = data['meta']['results']['total']
            print(f"✅ Deaths: {total:,}")
            return total
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def count_injuries(device_name):
    """Count injury events."""
    
    url = "https://api.fda.gov/device/event.json"
    params = {
        'search': f'device.brand_name:{device_name} AND event_type:Injury',
        'limit': 1
    }
    
    print(f"🤕 Counting injuries for: {device_name}")
    
    try:
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            total = data['meta']['results']['total']
            print(f"✅ Injuries: {total:,}")
            return total
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def count_malfunctions(device_name):
    """Count malfunction events."""
    
    url = "https://api.fda.gov/device/event.json"
    params = {
        'search': f'device.brand_name:{device_name} AND event_type:Malfunction',
        'limit': 1
    }
    
    print(f"⚙️  Counting malfunctions for: {device_name}")
    
    try:
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            total = data['meta']['results']['total']
            print(f"✅ Malfunctions: {total:,}")
            return total
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def get_sample_reports(device_name, limit=5):
    """Get sample reports to see the data."""
    
    url = "https://api.fda.gov/device/event.json"
    params = {
        'search': f'device.brand_name:{device_name}',
        'limit': limit
    }
    
    print(f"\n📄 Sample Reports for: {device_name}")
    
    try:
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            for i, report in enumerate(data['results'], 1):
                print(f"\nReport {i}:")
                print(f"  Date: {report.get('date_received', 'N/A')}")
                print(f"  Event Type: {report.get('event_type', 'N/A')}")
                print(f"  Report Number: {report.get('report_number', 'N/A')}")
                
                if 'patient' in report:
                    for patient in report['patient']:
                        if 'patient_problems' in patient:
                            print(f"  Problems: {patient['patient_problems'][:100]}...")
            
            return data['results']
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    """Test the simple MDR counter."""
    
    print("🔬 SIMPLE MDR EVENT COUNTER")
    print("=" * 60)
    
    device = "DreamStation"
    
    print(f"\n📊 Analyzing: {device}")
    print("=" * 60)
    
    # Get counts
    total = count_device_events(device)
    deaths = count_deaths(device)
    injuries = count_injuries(device)
    malfunctions = count_malfunctions(device)
    
    # Summary
    print(f"\n📊 SUMMARY:")
    print("=" * 60)
    if total:
        print(f"Total Events: {total:,}")
    if deaths:
        print(f"Deaths: {deaths:,} ({deaths/total*100:.1f}%)")
    if injuries:
        print(f"Injuries: {injuries:,} ({injuries/total*100:.1f}%)")
    if malfunctions:
        print(f"Malfunctions: {malfunctions:,} ({malfunctions/total*100:.1f}%)")
    
    # Sample reports
    get_sample_reports(device, 3)
    
    print(f"\n✅ MDR Counter Complete!")

if __name__ == "__main__":
    main()
