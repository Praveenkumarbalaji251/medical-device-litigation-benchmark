#!/usr/bin/env python3
"""
Alternative Methods to Get Real MAUDE Data
Complete guide to accessing FDA medical device adverse event data
"""

def show_all_data_access_methods():
    """Show all methods to access MAUDE data with pros/cons."""
    
    print("🔍 ALL METHODS TO GET REAL MAUDE DATA")
    print("=" * 60)
    
    methods = {
        "METHOD 1: FDA MAUDE Web Interface (EASIEST)": {
            "url": "https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfmaude/search.cfm",
            "access": "FREE - No registration required",
            "how_to": [
                "1. Go to the URL above",
                "2. Select 'Device Problem' or 'Device Name'",
                "3. Enter: 'DreamStation' or 'Philips CPAP'",
                "4. Set date range: 01/01/2020 to 06/30/2021",
                "5. Click 'Search'",
                "6. Export results to Excel/CSV",
                "7. Repeat for each device"
            ],
            "pros": [
                "✅ Most reliable - always works",
                "✅ No coding required",
                "✅ Can see full report details",
                "✅ Export directly to Excel",
                "✅ Free and instant access"
            ],
            "cons": [
                "❌ Manual process for each device",
                "❌ Time-consuming for 50 devices",
                "❌ Limited to 500 results per search",
                "❌ Need to aggregate manually"
            ],
            "best_for": "Quick checks, verifying specific devices, small datasets"
        },
        
        "METHOD 2: FDA MAUDE Bulk Download Files": {
            "url": "https://www.fda.gov/medical-devices/medical-device-reporting-mdr-how-report-medical-device-problems/manufacturer-and-user-facility-device-experience-database-maude",
            "direct_download": "https://www.fda.gov/medical-devices/mandatory-reporting-requirements-manufacturers-importers-and-device-user-facilities/manufacturer-and-user-facility-device-experience-database-maude",
            "access": "FREE - Direct download",
            "file_format": "ZIP files with ASCII text files (pipe-delimited)",
            "how_to": [
                "1. Go to FDA MAUDE download page",
                "2. Download quarterly files (e.g., 'device2020q1.zip')",
                "3. Download: mdrfoiThru2020.zip, mdrfoi2021.zip, etc.",
                "4. Unzip files (they contain .txt files)",
                "5. Files: device.txt, patient.txt, foitext.txt",
                "6. Use Python/Pandas to parse pipe-delimited format",
                "7. Filter by manufacturer/device name"
            ],
            "file_types": {
                "device.txt": "Device information",
                "patient.txt": "Patient outcomes (deaths, injuries)",
                "foitext.txt": "Event descriptions and narratives",
                "mdrfoi.txt": "Master file linking all data"
            },
            "pros": [
                "✅ Complete dataset - ALL reports",
                "✅ Historical data back to 1991",
                "✅ Can process locally without API limits",
                "✅ Includes full event narratives",
                "✅ Updated quarterly"
            ],
            "cons": [
                "❌ Large files (100MB+ per quarter)",
                "❌ Complex pipe-delimited format",
                "❌ Requires coding to parse",
                "❌ Need to merge multiple files"
            ],
            "best_for": "Complete historical analysis, all 50 devices, deep analysis",
            "example_code": """
# Python code to process MAUDE bulk files
import pandas as pd

# Read pipe-delimited file
df = pd.read_csv('mdrfoi.txt', sep='|', encoding='latin1', low_memory=False)

# Filter for Philips devices
philips = df[df['BRAND_NAME'].str.contains('DreamStation', na=False)]

# Get date range
philips_2020_2021 = philips[
    (philips['DATE_RECEIVED'] >= '20200101') & 
    (philips['DATE_RECEIVED'] <= '20210630')
]

# Count by month
monthly = philips_2020_2021.groupby('DATE_RECEIVED').size()
print(monthly)
            """
        },
        
        "METHOD 3: OpenFDA API (When Working)": {
            "url": "https://open.fda.gov/apis/device/event/",
            "api_endpoint": "https://api.fda.gov/device/event.json",
            "access": "FREE - No API key required (but recommended)",
            "rate_limits": "240 requests/minute without key, 1000/minute with key",
            "how_to": [
                "1. Read API documentation at open.fda.gov",
                "2. Optional: Get free API key at https://open.fda.gov/apis/authentication/",
                "3. Build query URL with search parameters",
                "4. Use Python requests or curl",
                "5. Handle pagination (max 1000 results per page)",
                "6. Parse JSON responses"
            ],
            "example_queries": {
                "basic_search": "https://api.fda.gov/device/event.json?search=device.brand_name:DreamStation&limit=100",
                "date_range": "https://api.fda.gov/device/event.json?search=device.brand_name:DreamStation+AND+date_received:[20200101+TO+20210630]&limit=1000",
                "count_by_month": "https://api.fda.gov/device/event.json?search=device.brand_name:DreamStation&count=date_received"
            },
            "pros": [
                "✅ Programmatic access - automate everything",
                "✅ JSON format - easy to parse",
                "✅ Real-time data",
                "✅ Flexible queries",
                "✅ Can aggregate with count parameter"
            ],
            "cons": [
                "❌ Sometimes has server issues (HTTP 500)",
                "❌ Rate limits require throttling",
                "❌ Pagination for large datasets",
                "❌ Complex query syntax"
            ],
            "status": "⚠️  Currently experiencing HTTP 500 errors (temporary)",
            "best_for": "Automated monitoring, real-time alerts, API integration"
        },
        
        "METHOD 4: FOIA Request to FDA": {
            "url": "https://www.fda.gov/regulatory-information/freedom-information",
            "access": "FREE (small fees for large requests)",
            "how_to": [
                "1. Submit FOIA request at FDA.gov",
                "2. Request: 'All MDR reports for Philips DreamStation 2020-2021'",
                "3. Provide specific date ranges and device details",
                "4. Wait 20-60 days for response",
                "5. Receive data in requested format"
            ],
            "pros": [
                "✅ Can get specific custom datasets",
                "✅ Official government response",
                "✅ Can request redacted patient info"
            ],
            "cons": [
                "❌ Slow (20-60 day turnaround)",
                "❌ May have fees for large requests",
                "❌ Not suitable for 50 devices"
            ],
            "best_for": "Legal cases requiring certified data, audit trails"
        },
        
        "METHOD 5: Commercial Medical Device Databases": {
            "providers": [
                {
                    "name": "ECRI Institute",
                    "url": "https://www.ecri.org/",
                    "cost": "$2,000-10,000/year",
                    "features": "Curated device data, adverse event analysis, expert reviews"
                },
                {
                    "name": "MD+DI (Medical Device + Diagnostic Industry)",
                    "url": "https://www.mddionline.com/",
                    "cost": "$500-3,000/year",
                    "features": "Industry news, regulatory tracking, device databases"
                },
                {
                    "name": "GlobalData Healthcare",
                    "url": "https://www.globaldata.com/",
                    "cost": "$5,000-20,000/year",
                    "features": "Medical device market intelligence, FDA tracking"
                },
                {
                    "name": "Definitive Healthcare",
                    "url": "https://www.definitivehc.com/",
                    "cost": "$3,000-15,000/year",
                    "features": "Healthcare provider data, device adoption tracking"
                }
            ],
            "pros": [
                "✅ Cleaned and structured data",
                "✅ Expert analysis included",
                "✅ Customer support",
                "✅ Additional context (market data, recalls)"
            ],
            "cons": [
                "❌ Expensive",
                "❌ May not have raw MDR data",
                "❌ Subscription required"
            ],
            "best_for": "Large law firms, ongoing monitoring, competitive intelligence"
        },
        
        "METHOD 6: Academic/Research Databases": {
            "sources": [
                {
                    "name": "PubMed Device Studies",
                    "url": "https://pubmed.ncbi.nlm.nih.gov/",
                    "access": "FREE",
                    "description": "Academic papers analyzing device safety"
                },
                {
                    "name": "FDA Device Classification Database",
                    "url": "https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfPCD/classification.cfm",
                    "access": "FREE",
                    "description": "Device classifications and regulatory history"
                },
                {
                    "name": "FDA 510(k) Premarket Database",
                    "url": "https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/pmn.cfm",
                    "access": "FREE",
                    "description": "Device clearances and submissions"
                }
            ],
            "best_for": "Understanding device background, regulatory history"
        },
        
        "METHOD 7: Web Scraping FDA Site": {
            "approach": "Automated scraping of FDA MAUDE web interface",
            "tools_needed": ["Python", "Selenium or BeautifulSoup", "Pandas"],
            "how_to": [
                "1. Use Selenium to automate web browser",
                "2. Fill in search forms programmatically",
                "3. Extract data from result pages",
                "4. Handle pagination",
                "5. Export to CSV/database"
            ],
            "pros": [
                "✅ Automates manual search process",
                "✅ No API limits",
                "✅ Can get data when API is down"
            ],
            "cons": [
                "❌ Technically complex",
                "❌ May violate terms of service",
                "❌ Fragile (breaks if site changes)",
                "❌ Slower than API"
            ],
            "legal_note": "⚠️  Check FDA terms of service before scraping",
            "best_for": "When API is down and bulk files too complex"
        }
    }
    
    # Print detailed breakdown
    for method_name, details in methods.items():
        print(f"\n{'='*60}")
        print(f"📊 {method_name}")
        print(f"{'='*60}")
        
        if 'url' in details:
            print(f"🔗 URL: {details['url']}")
        
        if 'access' in details:
            print(f"💰 Access: {details['access']}")
        
        if 'how_to' in details:
            print(f"\n📋 HOW TO USE:")
            for step in details['how_to']:
                print(f"  {step}")
        
        if 'pros' in details:
            print(f"\n✅ PROS:")
            for pro in details['pros']:
                print(f"  {pro}")
        
        if 'cons' in details:
            print(f"\n❌ CONS:")
            for con in details['cons']:
                print(f"  {con}")
        
        if 'best_for' in details:
            print(f"\n🎯 BEST FOR: {details['best_for']}")
        
        if 'example_code' in details:
            print(f"\n💻 EXAMPLE CODE:")
            print(details['example_code'])
    
    # Recommendation
    print(f"\n{'='*60}")
    print("🎯 RECOMMENDED APPROACH FOR YOUR 50 DEVICES")
    print(f"{'='*60}")
    
    recommendations = """
BEST STRATEGY: Combination Approach

PHASE 1: Quick Assessment (This Week)
  Method: FDA MAUDE Web Interface (Method 1)
  Action: Manually search top 10 priority devices
  Time: 2-3 hours
  Goal: Identify which devices show warning signs
  
PHASE 2: Complete Data Collection (Next Week)  
  Method: FDA Bulk Download Files (Method 2)
  Action: Download all quarterly files 2020-2025
  Process: Use Python script to parse all 50 devices at once
  Time: 1 day setup, then automated
  Goal: Complete historical dataset for all devices
  
PHASE 3: Ongoing Monitoring (Monthly)
  Method: OpenFDA API (Method 3) - when it recovers
  Action: Automate monthly queries for all 50 devices
  Alert: Email notification when reports spike 10x
  Goal: Real-time litigation prediction

BACKUP: If you need data TODAY
  Method: FDA Web Interface exports
  Export each device's results to Excel
  Combine manually in your master template
  Takes longer but works 100% of the time
    """
    
    print(recommendations)
    
    # Provide specific next steps
    print(f"\n{'='*60}")
    print("🚀 IMMEDIATE ACTION PLAN")
    print(f"{'='*60}")
    
    print("""
RIGHT NOW (Next 30 minutes):
  1. Go to: https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfmaude/search.cfm
  2. Search "DreamStation" from 2020-2021
  3. Export to Excel - verify you get data
  4. This confirms the manual method works

TODAY (Next 2 hours):
  5. Search your top 10 priority devices manually
  6. Look for the 30x increase pattern
  7. Mark devices with 4+ indicators as HIGH RISK
  
THIS WEEK:
  8. Download FDA bulk files (Method 2)
  9. Run Python parser script I'll create for you
  10. Generate complete dataset for all 50 devices
  
NEXT WEEK:
  11. Apply 5-indicator model to all devices
  12. Rank devices by litigation probability
  13. Identify next "Philips CPAP" opportunity
    """)
    
    return methods

def create_bulk_file_parser():
    """Create script to parse FDA bulk download files."""
    
    parser_code = '''#!/usr/bin/env python3
"""
FDA MAUDE Bulk File Parser
Processes downloaded FDA MAUDE quarterly files for all 50 devices
"""

import pandas as pd
import glob
from pathlib import Path

# Your 50 devices
DEVICE_SEARCH_TERMS = {
    "Philips CPAP": ["DreamStation", "Philips", "Respironics"],
    "Ethicon Mesh": ["Physiomesh", "Ethicon"],
    "DePuy Hip": ["ASR", "DePuy", "Pinnacle"],
    # ... add all 50 devices
}

def parse_maude_bulk_files(file_pattern="mdrfoi*.txt"):
    """Parse downloaded MAUDE files."""
    
    files = glob.glob(file_pattern)
    print(f"Found {len(files)} MAUDE files")
    
    all_data = []
    
    for file in files:
        print(f"Processing: {file}")
        df = pd.read_csv(file, sep='|', encoding='latin1', 
                        low_memory=False, on_bad_lines='skip')
        all_data.append(df)
    
    # Combine all files
    combined = pd.concat(all_data, ignore_index=True)
    
    # Filter for your devices
    results = {}
    for device_name, search_terms in DEVICE_SEARCH_TERMS.items():
        mask = False
        for term in search_terms:
            mask |= combined['BRAND_NAME'].str.contains(term, na=False, case=False)
        
        device_data = combined[mask]
        results[device_name] = device_data
        print(f"{device_name}: {len(device_data)} reports")
    
    return results

if __name__ == "__main__":
    results = parse_maude_bulk_files()
    
    # Save each device to separate file
    for device, data in results.items():
        filename = f"{device.replace(' ', '_')}_maude_data.csv"
        data.to_csv(filename, index=False)
        print(f"Saved: {filename}")
'''
    
    with open("parse_maude_bulk_files.py", "w") as f:
        f.write(parser_code)
    
    print(f"\n💾 Created: parse_maude_bulk_files.py")
    print("This script will process FDA bulk files for all 50 devices at once")

if __name__ == "__main__":
    methods = show_all_data_access_methods()
    create_bulk_file_parser()
    
    print(f"\n✅ COMPLETE GUIDE GENERATED!")
    print("You now have 7 different ways to get MAUDE data.")
    print("Use Method 1 (web interface) for quick checks today.")
    print("Use Method 2 (bulk files) for complete analysis this week.")