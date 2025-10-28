#!/usr/bin/env python3
"""
Real MAUDE Data Fetcher for Philips CPAP Device
Based on your working FDA API script
Timeline: January 2020 - June 2021 (pre-litigation period)
"""

import requests
import time
import os
import glob
from datetime import datetime, timedelta
import json
import pandas as pd
from tqdm import tqdm
from pathlib import Path

# Configuration
BASE_URL = "https://api.fda.gov/device/event.json"
PAGE_LIMIT = 1000
MAX_RETRIES = 5
BACKOFF = 1.5
OUT_DIR = "philips_cpap_maude_data"
os.makedirs(OUT_DIR, exist_ok=True)

# Philips CPAP device search terms
DEVICE_SEARCH_TERMS = [
    "DreamStation",
    "Philips+CPAP",
    "Respironics",
    "SystemOne",
    "REMstar"
]

def fetch_device_day_to_jsonl(yyyy_mm_dd, device_term, out_jsonl_path):
    """Fetch all events for a single day AND specific device, append to JSONL."""
    
    # Build search query: date AND device
    search_query = f"date_received:{yyyy_mm_dd}+AND+(device.brand_name:{device_term}+OR+device.manufacturer_d_name:Philips)"
    
    params_total = {"search": search_query, "limit": 1}
    attempt, total = 0, 0
    
    # Get total count first
    while True:
        attempt += 1
        try:
            r = requests.get(BASE_URL, params=params_total, timeout=30,
                           headers={"User-Agent": "philips-cpap-analyzer/1.0"})
            if r.status_code == 200:
                payload = r.json()
                if "error" in payload:
                    error_msg = payload['error'].get('message', 'unknown')
                    if "No matches" in error_msg or "no results" in error_msg.lower():
                        return 0  # No data for this day/device combo
                    print(f"OpenFDA error for {yyyy_mm_dd} ({device_term}): {error_msg}")
                    return 0
                total = payload.get("meta", {}).get("results", {}).get("total", 0)
                break
            elif r.status_code == 404:
                return 0  # No results
            else:
                print(f"HTTP {r.status_code} for {yyyy_mm_dd} ({device_term}) attempt {attempt}")
        except Exception as e:
            print(f"Exception getting total for {yyyy_mm_dd} ({device_term}): {e}")
        
        if attempt >= MAX_RETRIES:
            print(f"Failed total for {yyyy_mm_dd} ({device_term}) after {MAX_RETRIES} attempts")
            return 0
        time.sleep(BACKOFF ** attempt)
    
    if total == 0:
        return 0
    
    # Fetch all pages
    pages = (total + PAGE_LIMIT - 1) // PAGE_LIMIT
    wrote = 0
    
    with open(out_jsonl_path, "a", encoding="utf-8") as f:
        for page_idx in range(pages):
            skip = page_idx * PAGE_LIMIT
            attempt = 0
            
            while True:
                attempt += 1
                params = {
                    "search": search_query,
                    "limit": PAGE_LIMIT,
                    "skip": skip
                }
                
                try:
                    r = requests.get(BASE_URL, params=params, timeout=90,
                                   headers={"User-Agent": "philips-cpap-analyzer/1.0"})
                    
                    if r.status_code == 200:
                        payload = r.json()
                        if "error" in payload:
                            print(f"Error on {yyyy_mm_dd} ({device_term}) p{page_idx+1}: {payload['error'].get('message','unknown')}")
                            break
                        
                        results = payload.get("results", [])
                        if not results:
                            break
                        
                        for rec in results:
                            rec["retrieval_day"] = yyyy_mm_dd
                            rec["search_term"] = device_term
                            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                        
                        wrote += len(results)
                        break
                    
                    else:
                        print(f"HTTP {r.status_code} on {yyyy_mm_dd} ({device_term}) p{page_idx+1}")
                        if attempt >= MAX_RETRIES:
                            break
                        time.sleep(BACKOFF ** attempt)
                
                except Exception as e:
                    print(f"Exception: {e}")
                    if attempt >= MAX_RETRIES:
                        break
                    time.sleep(BACKOFF ** attempt)
            
            time.sleep(0.1)  # Rate limiting
    
    return wrote


def main():
    """Main function to fetch Philips CPAP MAUDE data."""
    
    print("🔍 FETCHING REAL PHILIPS CPAP MAUDE DATA")
    print("=" * 55)
    print(f"Device: Philips DreamStation CPAP")
    print(f"Timeline: January 2020 - June 2021 (pre-litigation)")
    print(f"Output Directory: {OUT_DIR}")
    print()
    
    # Timeline: Jan 2020 - June 2021 (18 months pre-litigation)
    start = datetime(2020, 1, 1)
    end = datetime(2021, 6, 30)
    
    # Generate all days in range
    days = []
    d = start
    while d <= end:
        days.append(d.strftime("%Y%m%d"))  # FDA format: YYYYMMDD
        d += timedelta(days=1)
    
    print(f"📅 Fetching {len(days)} days of data...")
    print(f"🔍 Search terms: {', '.join(DEVICE_SEARCH_TERMS)}")
    print()
    
    total_rows = 0
    device_counts = {term: 0 for term in DEVICE_SEARCH_TERMS}
    
    # Fetch data for each device term
    for device_term in DEVICE_SEARCH_TERMS:
        print(f"\n🔍 Searching for: {device_term}")
        term_rows = 0
        
        for day in tqdm(days, desc=f"{device_term}"):
            day_jsonl = Path(OUT_DIR) / f"maude_{device_term}_{day}.jsonl"
            wrote = fetch_device_day_to_jsonl(day, device_term, str(day_jsonl))
            term_rows += wrote
            total_rows += wrote
            
            if wrote > 0:
                print(f"  {day[:4]}-{day[4:6]}-{day[6:]}: {wrote} reports")
        
        device_counts[device_term] = term_rows
        print(f"✅ Total for {device_term}: {term_rows} reports")
    
    print(f"\n📊 TOTAL ROWS COLLECTED: {total_rows}")
    print(f"\n📊 BREAKDOWN BY SEARCH TERM:")
    for term, count in device_counts.items():
        print(f"  {term}: {count} reports")
    
    # Merge all JSONL files to single CSV
    print(f"\n📝 Merging JSONL files to CSV...")
    csv_out = Path(OUT_DIR) / "philips_cpap_maude_2020_2021.csv"
    
    if csv_out.exists():
        csv_out.unlink()
    
    jsonl_files = sorted(glob.glob(str(Path(OUT_DIR) / "maude_*.jsonl")))
    
    if not jsonl_files:
        print("❌ No JSONL files found!")
        return
    
    print(f"Found {len(jsonl_files)} JSONL files")
    
    header_written = False
    all_data = []
    
    for jf in tqdm(jsonl_files, desc="JSONL→CSV"):
        try:
            with open(jf, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        all_data.append(json.loads(line))
        except Exception as e:
            print(f"Error reading {jf}: {e}")
            continue
    
    if all_data:
        df = pd.json_normalize(all_data)
        df.to_csv(csv_out, index=False)
        print(f"✅ Wrote CSV: {csv_out} ({len(df)} rows)")
        
        # Create analysis summary
        print(f"\n📊 QUICK ANALYSIS:")
        
        # Extract key columns
        if 'date_received' in df.columns:
            df['year_month'] = df['date_received'].astype(str).str[:6]
            monthly = df.groupby('year_month').size()
            print(f"\n📅 MONTHLY REPORT COUNTS:")
            for month, count in monthly.items():
                if len(str(month)) == 6:
                    formatted = f"{month[:4]}-{month[4:]}"
                    print(f"  {formatted}: {count} reports")
        
        # Event types
        if 'event_type' in df.columns:
            print(f"\n⚠️  EVENT TYPES:")
            event_counts = df['event_type'].value_counts()
            for event, count in event_counts.head(10).items():
                print(f"  {event}: {count}")
        
        # Deaths and injuries
        deaths = 0
        injuries = 0
        if 'patient' in df.columns:
            for col in df.columns:
                if 'death' in col.lower():
                    deaths += df[col].notna().sum()
                elif 'injury' in col.lower() or 'serious' in col.lower():
                    injuries += df[col].notna().sum()
        
        print(f"\n💀 Deaths: {deaths}")
        print(f"🏥 Injuries: {injuries}")
        
        # Optional: Create Excel (if dataset not too large)
        if len(df) < 300000:
            print(f"\n📊 Creating Excel file...")
            xlsx_out = Path(OUT_DIR) / "philips_cpap_maude_2020_2021.xlsx"
            try:
                df.to_excel(xlsx_out, index=False, engine='openpyxl')
                print(f"✅ Wrote Excel: {xlsx_out}")
            except Exception as e:
                print(f"⚠️  Excel creation failed (dataset too large or missing openpyxl): {e}")
        
        # Save summary JSON
        summary = {
            "device": "Philips DreamStation CPAP",
            "search_terms": DEVICE_SEARCH_TERMS,
            "date_range": f"{start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}",
            "total_reports": len(df),
            "total_deaths": int(deaths),
            "total_injuries": int(injuries),
            "fetch_timestamp": datetime.now().isoformat(),
            "monthly_counts": monthly.to_dict() if 'year_month' in df.columns else {},
            "device_term_breakdown": device_counts
        }
        
        summary_file = Path(OUT_DIR) / "fetch_summary.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        print(f"✅ Saved summary: {summary_file}")
        
    else:
        print("❌ No data collected!")
    
    print(f"\n🚀 PHILIPS CPAP MAUDE DATA FETCH COMPLETE!")
    print(f"📁 All files saved to: {OUT_DIR}/")


if __name__ == "__main__":
    main()