#!/usr/bin/env python3
"""
Analyze Bard Hernia Mesh - Major class action case
Compare pattern to Philips CPAP
"""

import requests
import json
from datetime import datetime
from calendar import monthrange

def analyze_device(device_name, manufacturer=None):
    """Complete analysis of a device's MDR pattern."""
    
    print(f"🔬 ANALYZING: {device_name}")
    print("=" * 70)
    
    url = "https://api.fda.gov/device/event.json"
    
    # Get total count
    if manufacturer:
        search_query = f'(device.brand_name:{device_name} OR device.generic_name:"{manufacturer}")'
    else:
        search_query = f'device.brand_name:{device_name}'
    
    params = {'search': search_query, 'limit': 1}
    
    print(f"🔍 Searching for: {device_name}")
    
    try:
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if 'meta' in data and 'results' in data['meta']:
                total = data['meta']['results']['total']
                print(f"✅ Total MDR Reports: {total:,}\n")
                
                if total == 0:
                    print(f"⚠️  No reports found for '{device_name}'")
                    return None
                
                # Get yearly breakdown
                print(f"📅 YEARLY BREAKDOWN:")
                print("-" * 70)
                
                count_params = {'search': search_query, 'count': 'date_received'}
                response = requests.get(url, params=count_params, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    yearly = {}
                    
                    for item in data['results']:
                        year = item['time'][:4]
                        yearly[year] = yearly.get(year, 0) + item['count']
                    
                    for year in sorted(yearly.keys()):
                        print(f"  {year}: {yearly[year]:,} reports")
                
                # Get event type breakdown
                print(f"\n💀 EVENT TYPE BREAKDOWN:")
                print("-" * 70)
                
                event_types = ['Death', 'Injury', 'Malfunction']
                for event_type in event_types:
                    event_query = f'{search_query} AND event_type:{event_type}'
                    params = {'search': event_query, 'limit': 1}
                    response = requests.get(url, params=params, timeout=30)
                    
                    if response.status_code == 200:
                        data = response.json()
                        if 'meta' in data and 'results' in data['meta']:
                            count = data['meta']['results']['total']
                            pct = (count / total * 100) if total > 0 else 0
                            print(f"  {event_type:15s}: {count:8,} ({pct:5.1f}%)")
                
                # Get report source
                print(f"\n📋 REPORT SOURCE:")
                print("-" * 70)
                
                sources = ['Patient', 'Manufacturer', 'User facility']
                for source in sources:
                    source_query = f'{search_query} AND report_source_code:{source}'
                    params = {'search': source_query, 'limit': 1}
                    response = requests.get(url, params=params, timeout=30)
                    
                    if response.status_code == 200:
                        data = response.json()
                        if 'meta' in data and 'results' in data['meta']:
                            count = data['meta']['results']['total']
                            pct = (count / total * 100) if total > 0 else 0
                            print(f"  {source:15s}: {count:8,} ({pct:5.1f}%)")
                
                return {
                    'device': device_name,
                    'total': total,
                    'yearly': yearly
                }
            else:
                print(f"⚠️  No results found")
                return None
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    """Analyze major hernia mesh case."""
    
    print("🏥 HERNIA MESH CLASS ACTION ANALYSIS")
    print("=" * 70)
    print("Comparing to Philips CPAP pattern")
    print("=" * 70)
    print()
    
    # Try different hernia mesh product names
    devices_to_try = [
        ("Composix", "Bard Composix Hernia Mesh"),
        ("Ventralex", "Bard Ventralex Hernia Patch"),
        ("3DMax", "Bard 3DMax Mesh"),
        ("PerFix", "Bard PerFix Plug"),
        ("Kugel", "Bard Kugel Hernia Patch")
    ]
    
    print("🔍 Searching for Bard Hernia Mesh products...")
    print("=" * 70)
    print()
    
    results = []
    
    for brand_name, full_name in devices_to_try:
        print(f"\n{'='*70}")
        print(f"DEVICE: {full_name}")
        print(f"{'='*70}\n")
        
        result = analyze_device(brand_name)
        
        if result and result['total'] > 0:
            result['full_name'] = full_name
            results.append(result)
        
        print()
    
    # Summary comparison
    if results:
        print("\n" + "=" * 70)
        print("📊 HERNIA MESH SUMMARY:")
        print("=" * 70)
        
        total_mesh_reports = sum(r['total'] for r in results)
        print(f"\nTotal Hernia Mesh Reports Found: {total_mesh_reports:,}")
        
        print(f"\nBreakdown by Product:")
        for r in sorted(results, key=lambda x: x['total'], reverse=True):
            print(f"  {r['full_name']:40s}: {r['total']:8,} reports")
        
        print("\n" + "=" * 70)
        print("🎯 LITIGATION CONTEXT:")
        print("=" * 70)
        print("""
Bard Hernia Mesh Litigation Timeline:
  
  📅 2005-2006: Kugel Patch recalled (ring breakage)
  📅 MDL 2846: Composix Kugel mesh products
  📅 2011: Perfix Plug recalled
  📅 2013-Present: Ongoing litigation for multiple products
  
  💰 Settlements: $184+ million total
  👥 Plaintiffs: Thousands of patients
  
  Key Issues:
  ✅ Mesh migration and shrinkage
  ✅ Adhesions and bowel obstructions  
  ✅ Chronic pain
  ✅ Infection and rejection
  ✅ Need for revision surgery
        """)
        
        # Compare to Philips CPAP
        print("=" * 70)
        print("⚖️  COMPARISON: Hernia Mesh vs Philips CPAP")
        print("=" * 70)
        print(f"""
PHILIPS CPAP:
  Total Reports: 178,755
  Litigation Filed: July 2021
  Settlement: $1.1 billion (2023)
  Pattern: Sudden spike (3→382 reports/month)
  
BARD HERNIA MESH:
  Total Reports: {total_mesh_reports:,}
  Litigation Filed: 2005-2013 (multiple waves)
  Settlement: $184+ million (various)
  Pattern: Long-term chronic issues
        """)
    
    else:
        print("\n⚠️  Could not find hernia mesh data with those brand names")
        print("Let me try a broader search...")
        
        print("\n" + "=" * 70)
        print("TRYING: Generic Hernia Mesh Search")
        print("=" * 70)
        
        # Try generic search
        analyze_device("hernia mesh")

if __name__ == "__main__":
    main()
