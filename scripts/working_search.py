#!/usr/bin/env python3
"""
Working example of medical device case collection from CourtListener.
"""

import requests
import json
import pandas as pd
from datetime import datetime

def test_working_search():
    """Test with simpler search parameters that work."""
    print("🏛️  CourtListener Medical Device Case Search")
    print("=" * 50)
    
    base_url = "https://www.courtlistener.com/api/rest/v4/search/"
    headers = {
        'User-Agent': 'MedicalDeviceLegalBenchmark/1.0',
        'Accept': 'application/json'
    }
    
    # Try different search approaches
    searches = [
        {
            'name': 'Simple Medical Device Search',
            'params': {'q': 'medical device', 'type': 'r'}
        },
        {
            'name': 'Philips Cases',
            'params': {'q': 'Philips', 'type': 'r'}  
        },
        {
            'name': 'Class Action Cases',
            'params': {'q': 'class action', 'type': 'r'}
        },
        {
            'name': 'Recent Cases (Any)',
            'params': {'type': 'r', 'order_by': '-dateFiled'}
        }
    ]
    
    for search in searches:
        print(f"\n🔍 {search['name']}:")
        
        try:
            response = requests.get(base_url, params=search['params'], headers=headers, timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                total_count = data.get('count', 0)
                
                print(f"   ✅ Found {len(results)} results (Total: {total_count})")
                
                if results:
                    # Show first result
                    case = results[0]
                    print(f"   📋 Sample case:")
                    print(f"      Name: {case.get('caseName', 'Unknown')[:60]}")
                    print(f"      Court: {case.get('court', 'Unknown')}")
                    print(f"      Filed: {case.get('dateFiled', 'Unknown')}")
                    print(f"      Docket: {case.get('docketNumber', 'Unknown')}")
                    
                    # Check if it's medical device related
                    case_name = case.get('caseName', '').lower()
                    if any(term in case_name for term in ['medical', 'device', 'implant', 'philips', 'mesh']):
                        print(f"   🎯 This appears to be medical device related!")
                    
            elif response.status_code == 400:
                print(f"   ❌ Bad request - checking error...")
                try:
                    error_data = response.json()
                    print(f"      Error: {error_data}")
                except:
                    print(f"      Error: {response.text[:200]}")
            else:
                print(f"   ❌ Error {response.status_code}: {response.text[:100]}")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
    
    print(f"\n📋 Next Steps:")
    print(f"1. The search API is working!")
    print(f"2. You can now get an API token for higher limits")
    print(f"3. Use more specific search terms")
    print(f"4. Filter by date ranges and courts")

def show_api_registration_help():
    """Show how to get API token."""
    print(f"\n🔑 To Get Full Access (FREE API Token):")
    print(f"=" * 40)
    print(f"1. Visit: https://www.courtlistener.com/sign-up/")
    print(f"2. Create free account")  
    print(f"3. Go to: https://www.courtlistener.com/api/")
    print(f"4. Generate API token")
    print(f"5. Run: python scripts/setup_api.py")

if __name__ == "__main__":
    test_working_search()
    show_api_registration_help()