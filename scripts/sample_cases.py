#!/usr/bin/env python3
"""
Show sample medical device cases from CourtListener without needing API token.
"""

import requests
import json
import pandas as pd
from datetime import datetime, timedelta

def get_recent_medical_device_cases():
    """Get recent medical device cases using public search API."""
    print("🏛️  Recent Medical Device Cases (No API Token Needed)")
    print("=" * 60)
    
    base_url = "https://www.courtlistener.com/api/rest/v4/"
    headers = {
        'User-Agent': 'MedicalDeviceLegalBenchmark/1.0',
        'Accept': 'application/json'
    }
    
    # Calculate date range (last 6 months for better results)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    
    # Search terms for medical devices
    device_terms = [
        "Philips CPAP",
        "hernia mesh", 
        "medical device",
        "pacemaker",
        "hip replacement",
        "IVC filter"
    ]
    
    all_cases = []
    
    for term in device_terms:
        print(f"\n🔍 Searching for: '{term}'")
        
        params = {
            'q': term,
            'type': 'r',  # RECAP documents (federal court cases)
            'filed_after': start_date.strftime('%Y-%m-%d'),
            'order_by': '-dateFiled'
        }
        
        try:
            response = requests.get(
                f"{base_url}search/", 
                params=params, 
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                cases = data.get('results', [])
                all_cases.extend(cases)
                print(f"   Found: {len(cases)} cases")
                
                # Show sample case
                if cases:
                    sample = cases[0]
                    print(f"   📋 Sample: {sample.get('caseName', 'Unknown')[:60]}...")
                    print(f"        Court: {sample.get('court', 'Unknown')}")
                    print(f"        Filed: {sample.get('dateFiled', 'Unknown')}")
                    
            else:
                print(f"   ❌ Error {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Remove duplicates and analyze
    unique_cases = {case['docket_id']: case for case in all_cases if case.get('docket_id')}.values()
    unique_cases = list(unique_cases)
    
    print(f"\n📊 SUMMARY")
    print(f"   Total unique cases found: {len(unique_cases)}")
    
    if unique_cases:
        # Create DataFrame for analysis
        case_data = []
        for case in unique_cases[:10]:  # Show top 10
            case_info = {
                'Case Name': case.get('caseName', 'Unknown')[:50],
                'Court': case.get('court', 'Unknown'),
                'Filed Date': case.get('dateFiled', 'Unknown'),
                'Docket Number': case.get('docketNumber', 'Unknown'),
                'Nature of Suit': case.get('suitNature', 'Unknown')
            }
            case_data.append(case_info)
        
        df = pd.DataFrame(case_data)
        
        print(f"\n📋 TOP 10 RECENT MEDICAL DEVICE CASES:")
        print("=" * 80)
        for i, row in df.iterrows():
            print(f"{i+1:2d}. {row['Case Name']}")
            print(f"    Court: {row['Court']}")
            print(f"    Filed: {row['Filed Date']} | Docket: {row['Docket Number']}")
            print(f"    Nature: {row['Nature of Suit']}")
            print()
        
        # Save results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"data/raw/sample_cases_{timestamp}.csv"
        df.to_csv(output_file, index=False)
        print(f"💾 Results saved to: {output_file}")
        
        return output_file
    else:
        print("   No cases found in recent period")
        return None

if __name__ == "__main__":
    get_recent_medical_device_cases()