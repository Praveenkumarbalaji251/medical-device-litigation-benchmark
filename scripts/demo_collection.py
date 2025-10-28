#!/usr/bin/env python3
"""
Demo script to test CourtListener case collection.
"""

import sys
import os
from pathlib import Path
import pandas as pd

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from data_collection.courtlistener_collector import CourtListenerCollector

def demo_collection():
    """Demo the case collection functionality."""
    print("🏛️  Medical Device Case Collection Demo")
    print("=" * 50)
    
    # Initialize collector (no API token for demo - will use public limits)
    collector = CourtListenerCollector()
    
    print("🔍 Searching for recent medical device cases...")
    print("   (Using public API limits - no token required)")
    
    try:
        # Search for cases from last 30 days (smaller sample for demo)
        from datetime import datetime, timedelta
        
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        
        print(f"📅 Date range: {start_date} to {end_date}")
        
        # Test with just a few key medical device terms for demo
        test_terms = ["Philips CPAP", "hernia mesh", "medical device"]
        
        all_cases = []
        for term in test_terms:
            print(f"🔍 Searching for: {term}")
            cases = collector._search_by_term(term, start_date, end_date)
            all_cases.extend(cases)
            print(f"   Found {len(cases)} cases")
            
        # Remove duplicates
        unique_cases = {case['id']: case for case in all_cases}.values()
        unique_cases = list(unique_cases)
        
        print(f"\n📊 Total unique cases found: {len(unique_cases)}")
        
        if unique_cases:
            # Convert to DataFrame for analysis
            df = collector.export_to_dataframe(unique_cases)
            
            print("\n📋 Sample cases found:")
            print("-" * 80)
            for i, case in enumerate(unique_cases[:3]):  # Show first 3 cases
                print(f"{i+1}. {case.get('case_name', 'Unknown Case')}")
                print(f"   Court: {case.get('court', {}).get('full_name', 'Unknown')}")
                print(f"   Filed: {case.get('date_filed', 'Unknown')}")
                print(f"   Docket: {case.get('docket_number', 'Unknown')}")
                print()
            
            # Save demo results
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            csv_file = f"data/raw/demo_cases_{timestamp}.csv"
            df.to_csv(csv_file, index=False)
            
            print(f"💾 Demo results saved to: {csv_file}")
            
            # Show some statistics
            print(f"\n📈 Quick Statistics:")
            print(f"   Total cases: {len(df)}")
            print(f"   Date range: {df['date_filed'].min()} to {df['date_filed'].max()}")
            print(f"   Unique courts: {df['court'].nunique()}")
            
            return csv_file
        else:
            print("ℹ️  No cases found in the recent period.")
            print("   This is normal - try expanding the date range or different search terms.")
            return None
            
    except Exception as e:
        print(f"❌ Error during collection: {e}")
        print("ℹ️  This might be due to rate limiting or network issues.")
        print("   For full collection, consider getting a free CourtListener API token.")
        return None

if __name__ == "__main__":
    demo_collection()