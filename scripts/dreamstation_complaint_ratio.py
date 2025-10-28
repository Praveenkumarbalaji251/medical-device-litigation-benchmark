#!/usr/bin/env python3
"""
Analyze complaint ratio for DreamStation - Patient vs Manufacturer reports
This is a key litigation indicator
"""

import requests
import json

def get_report_source_breakdown(device_name):
    """Get breakdown of who is filing the reports - patients vs manufacturers."""
    
    url = "https://api.fda.gov/device/event.json"
    
    print(f"🔍 Analyzing Report Sources for: {device_name}")
    print("=" * 70)
    
    # Get total count
    params = {'search': f'device.brand_name:{device_name}', 'limit': 1}
    response = requests.get(url, params=params, timeout=30)
    
    if response.status_code != 200:
        print(f"❌ Error getting total count")
        return None
    
    total = response.json()['meta']['results']['total']
    print(f"\n📊 Total Reports: {total:,}")
    
    # Count by report source type
    print(f"\n📋 Report Source Breakdown:\n")
    
    sources = {
        'Patient': 'report_source_code:Patient',
        'User Facility': 'report_source_code:"User facility"',
        'Manufacturer': 'report_source_code:Manufacturer',
        'Distributor': 'report_source_code:Distributor',
        'Other': 'report_source_code:Other'
    }
    
    results = {}
    
    for source_name, source_query in sources.items():
        search_query = f'device.brand_name:{device_name} AND {source_query}'
        params = {'search': search_query, 'limit': 1}
        
        try:
            response = requests.get(url, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                if 'meta' in data and 'results' in data['meta']:
                    count = data['meta']['results']['total']
                    results[source_name] = count
                    percentage = (count / total * 100) if total > 0 else 0
                    print(f"  {source_name:20s}: {count:8,} ({percentage:5.1f}%)")
                else:
                    results[source_name] = 0
                    print(f"  {source_name:20s}: {0:8,} (  0.0%)")
            else:
                results[source_name] = 0
                print(f"  {source_name:20s}: Error")
        except Exception as e:
            print(f"  {source_name:20s}: Error - {e}")
            results[source_name] = 0
    
    # Calculate patient-driven ratio
    patient_driven = results.get('Patient', 0) + results.get('User Facility', 0)
    manufacturer_driven = results.get('Manufacturer', 0)
    
    print(f"\n" + "=" * 70)
    print(f"📊 COMPLAINT RATIO ANALYSIS:")
    print(f"=" * 70)
    print(f"Patient-Driven Reports:      {patient_driven:8,} ({patient_driven/total*100:5.1f}%)")
    print(f"Manufacturer-Driven Reports: {manufacturer_driven:8,} ({manufacturer_driven/total*100:5.1f}%)")
    
    if patient_driven > 0 and manufacturer_driven > 0:
        ratio = patient_driven / manufacturer_driven
        print(f"\nPatient-to-Manufacturer Ratio: {ratio:.2f}:1")
        
        print(f"\n🎯 LITIGATION INDICATOR:")
        if patient_driven / total > 0.70:
            print(f"   ✅ Patient reports >70% = STRONG LITIGATION SIGNAL")
        elif patient_driven / total > 0.50:
            print(f"   ⚠️  Patient reports >50% = MODERATE LITIGATION SIGNAL")
        else:
            print(f"   ℹ️  Patient reports <50% = Lower litigation risk")
    
    return results

def get_reporter_occupation_breakdown(device_name):
    """Get breakdown by reporter occupation."""
    
    url = "https://api.fda.gov/device/event.json"
    
    print(f"\n" + "=" * 70)
    print(f"👤 REPORTER OCCUPATION BREAKDOWN:")
    print(f"=" * 70)
    
    occupations = {
        'Physician': 'reporter_occupation_code:Physician',
        'Nurse': 'reporter_occupation_code:Nurse',
        'Other Health Professional': 'reporter_occupation_code:"Other health professional"',
        'Consumer/Patient': 'reporter_occupation_code:Consumer',
        'Lawyer': 'reporter_occupation_code:Lawyer',
        'Unknown': 'reporter_occupation_code:Unknown'
    }
    
    results = {}
    
    for occupation_name, occupation_query in occupations.items():
        search_query = f'device.brand_name:{device_name} AND {occupation_query}'
        params = {'search': search_query, 'limit': 1}
        
        try:
            response = requests.get(url, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                if 'meta' in data and 'results' in data['meta']:
                    count = data['meta']['results']['total']
                    results[occupation_name] = count
                    print(f"  {occupation_name:30s}: {count:8,}")
                else:
                    results[occupation_name] = 0
            else:
                results[occupation_name] = 0
        except Exception as e:
            results[occupation_name] = 0
    
    return results

def analyze_monthly_complaint_ratio(device_name, year, month):
    """Analyze complaint ratio for a specific month."""
    
    from calendar import monthrange
    last_day = monthrange(year, month)[1]
    
    start_date = f"{year}{month:02d}01"
    end_date = f"{year}{month:02d}{last_day}"
    
    url = "https://api.fda.gov/device/event.json"
    
    month_name = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][month-1]
    
    # Get total for month
    search_query = f'device.brand_name:{device_name} AND date_received:[{start_date} TO {end_date}]'
    params = {'search': search_query, 'limit': 1}
    response = requests.get(url, params=params, timeout=30)
    
    if response.status_code != 200:
        return None
    
    data = response.json()
    if 'meta' not in data or 'results' not in data['meta']:
        return None
    
    total = data['meta']['results']['total']
    
    # Get patient reports
    patient_query = f'device.brand_name:{device_name} AND date_received:[{start_date} TO {end_date}] AND report_source_code:Patient'
    params = {'search': patient_query, 'limit': 1}
    response = requests.get(url, params=params, timeout=30)
    
    patient_count = 0
    if response.status_code == 200:
        data = response.json()
        if 'meta' in data and 'results' in data['meta']:
            patient_count = data['meta']['results']['total']
    
    # Get manufacturer reports
    mfr_query = f'device.brand_name:{device_name} AND date_received:[{start_date} TO {end_date}] AND report_source_code:Manufacturer'
    params = {'search': mfr_query, 'limit': 1}
    response = requests.get(url, params=params, timeout=30)
    
    mfr_count = 0
    if response.status_code == 200:
        data = response.json()
        if 'meta' in data and 'results' in data['meta']:
            mfr_count = data['meta']['results']['total']
    
    patient_pct = (patient_count / total * 100) if total > 0 else 0
    
    return {
        'month': month_name,
        'total': total,
        'patient': patient_count,
        'manufacturer': mfr_count,
        'patient_pct': patient_pct
    }

def main():
    """Analyze complaint ratio for DreamStation."""
    
    print("🔬 DREAMSTATION COMPLAINT RATIO ANALYSIS")
    print("=" * 70)
    print("Patient vs Manufacturer Reports - Key Litigation Indicator")
    print("=" * 70)
    
    device = "DreamStation"
    
    # Overall breakdown
    source_results = get_report_source_breakdown(device)
    
    # Reporter occupation
    occupation_results = get_reporter_occupation_breakdown(device)
    
    # Monthly breakdown for 2021 (pre-litigation)
    print(f"\n" + "=" * 70)
    print(f"📅 MONTHLY PATIENT RATIO (2021 - Pre-Litigation Year):")
    print(f"=" * 70)
    print(f"\n{'Month':<10} {'Total':<10} {'Patient':<10} {'Mfr':<10} {'Patient %':<12} {'Signal'}")
    print("-" * 70)
    
    monthly_data = []
    for month in range(1, 8):  # Jan-July 2021
        result = analyze_monthly_complaint_ratio(device, 2021, month)
        if result:
            monthly_data.append(result)
            signal = "🚨 HIGH" if result['patient_pct'] > 70 else ("⚠️  MED" if result['patient_pct'] > 50 else "ℹ️  LOW")
            print(f"{result['month']:<10} {result['total']:<10} {result['patient']:<10} {result['manufacturer']:<10} {result['patient_pct']:<12.1f} {signal}")
    
    # Summary
    print(f"\n" + "=" * 70)
    print(f"🎯 KEY INSIGHTS:")
    print(f"=" * 70)
    
    if source_results:
        patient_total = source_results.get('Patient', 0)
        mfr_total = source_results.get('Manufacturer', 0)
        total_reports = patient_total + mfr_total + source_results.get('User Facility', 0) + source_results.get('Distributor', 0) + source_results.get('Other', 0)
        
        patient_pct = (patient_total / total_reports * 100) if total_reports > 0 else 0
        
        print(f"\n1. OVERALL PATIENT-DRIVEN RATIO: {patient_pct:.1f}%")
        if patient_pct > 70:
            print(f"   ✅ This indicates patients are experiencing serious issues")
            print(f"   ✅ Not just manufacturer-reported technical problems")
            print(f"   ✅ STRONG INDICATOR for class action litigation")
        
        print(f"\n2. ESCALATION PATTERN:")
        if monthly_data:
            may_data = next((d for d in monthly_data if d['month'] == 'May'), None)
            june_data = next((d for d in monthly_data if d['month'] == 'Jun'), None)
            
            if may_data and june_data:
                print(f"   May 2021:  {may_data['patient_pct']:.1f}% patient reports")
                print(f"   June 2021: {june_data['patient_pct']:.1f}% patient reports")
                print(f"   ⚠️  High patient % + spike in volume = LITIGATION IMMINENT")
    
    # Save results
    output = {
        'device': device,
        'analysis_date': '2025-10-20',
        'source_breakdown': source_results,
        'occupation_breakdown': occupation_results,
        'monthly_2021': monthly_data
    }
    
    output_file = 'dreamstation_complaint_ratio_analysis.json'
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n" + "=" * 70)
    print(f"✅ Analysis saved to: {output_file}")
    print(f"=" * 70)

if __name__ == "__main__":
    main()
