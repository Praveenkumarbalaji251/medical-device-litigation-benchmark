#!/usr/bin/env python3
"""
Quick test of CourtListener API v4 endpoints.
"""

import requests
import json

def test_public_endpoints():
    """Test what we can access without authentication."""
    print("🧪 Testing CourtListener API v4 Public Access")
    print("=" * 50)
    
    base_url = "https://www.courtlistener.com/api/rest/v4/"
    
    # Test basic endpoints that might work without auth
    endpoints_to_test = [
        ("courts", "courts/"),
        ("search", "search/?q=medical+device&type=r&filed_after=2024-01-01"),
        ("dockets", "dockets/?court=dcd&filed_after=2024-01-01")  # DC District Court
    ]
    
    headers = {
        'User-Agent': 'MedicalDeviceLegalBenchmark/1.0',
        'Accept': 'application/json'
    }
    
    for name, endpoint in endpoints_to_test:
        print(f"\n🔍 Testing {name}...")
        url = f"{base_url}{endpoint}"
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if 'results' in data:
                    print(f"   ✅ Success! Found {len(data['results'])} results")
                    if data['results']:
                        print(f"   📋 Sample: {list(data['results'][0].keys())}")
                elif 'count' in data:
                    print(f"   ✅ Success! Total items: {data['count']}")
                else:
                    print(f"   ✅ Success! Response keys: {list(data.keys())}")
                    
            elif response.status_code == 401:
                print(f"   🔐 Authentication required for {name}")
            elif response.status_code == 403:
                print(f"   🚫 Access forbidden for {name}")
            elif response.status_code == 429:
                print(f"   ⏳ Rate limited for {name}")
            else:
                print(f"   ❌ Error {response.status_code}: {response.text[:100]}")
                
        except requests.RequestException as e:
            print(f"   ❌ Request failed: {e}")
    
    print(f"\n📋 Summary:")
    print(f"   - CourtListener API v4 is active")
    print(f"   - Some endpoints may require authentication")
    print(f"   - Get free API token at: https://www.courtlistener.com/api/")

if __name__ == "__main__":
    test_public_endpoints()