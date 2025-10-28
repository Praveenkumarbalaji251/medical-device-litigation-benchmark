#!/usr/bin/env python3
"""
Script to collect recent medical device cases from CourtListener.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from data_collection.courtlistener_collector import collect_recent_medical_device_cases

def main():
    """Main function to collect cases."""
    print("🔍 Medical Device Case Collector")
    print("=" * 40)
    
    # You can get a free API token from https://www.courtlistener.com/api/
    api_token = input("Enter CourtListener API token (or press Enter to skip): ").strip()
    if not api_token:
        api_token = None
        print("⚠️  No API token - using public rate limits")
    
    months_back = input("How many months back to search? (default: 2): ").strip()
    try:
        months_back = int(months_back) if months_back else 2
    except ValueError:
        months_back = 2
    
    print(f"🔍 Searching for medical device cases from last {months_back} months...")
    
    try:
        output_file = collect_recent_medical_device_cases(
            api_token=api_token,
            months_back=months_back
        )
        
        print(f"\n✅ Success! Cases saved to: {output_file}")
        print("\n📋 Next steps:")
        print("1. Review the collected cases")
        print("2. Run analysis on settlement patterns")
        print("3. Create benchmark metrics")
        
    except Exception as e:
        print(f"❌ Error collecting cases: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())