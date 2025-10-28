#!/usr/bin/env python3
"""
Analyze the downloaded Allergan CSV/Excel files
Verify unique MDR count and compare with FDA data
"""

import pandas as pd
import os

print("="*80)
print("ANALYZING DOWNLOADED ALLERGAN FILES")
print("="*80)

# File paths
files = [
    '/Users/praveen/Downloads/allergan 1.csv',
    '/Users/praveen/Downloads/Allergan.csv',
    '/Users/praveen/Downloads/allergan2.csv'
]

all_data = []
file_counts = {}

for file_path in files:
    try:
        # Try reading as Excel first (these are .xlsx files with .csv extension)
        df = pd.read_excel(file_path)
        print(f"\n✓ Loaded {os.path.basename(file_path)}: {len(df)} rows")
        file_counts[os.path.basename(file_path)] = len(df)
        all_data.append(df)
    except Exception as e:
        print(f"\n✗ Error loading {os.path.basename(file_path)}: {e}")

if len(all_data) > 0:
    # Combine all dataframes
    combined_df = pd.concat(all_data, ignore_index=True)
    
    print("\n" + "="*80)
    print("COMBINED DATA SUMMARY")
    print("="*80)
    print(f"Total rows (with duplicates): {len(combined_df)}")
    
    # Check for Report Number column
    if 'Report Number' in combined_df.columns:
        # Count unique MDRs
        unique_mdrs = combined_df['Report Number'].nunique()
        total_mdrs = len(combined_df)
        duplicates = total_mdrs - unique_mdrs
        
        print(f"Unique MDR Reports: {unique_mdrs}")
        print(f"Duplicate entries: {duplicates}")
        
        # Remove duplicates
        combined_unique = combined_df.drop_duplicates(subset=['Report Number'])
        print(f"\nAfter removing duplicates: {len(combined_unique)} unique records")
        
        # Show columns
        print("\n" + "="*80)
        print("AVAILABLE COLUMNS")
        print("="*80)
        for i, col in enumerate(combined_unique.columns, 1):
            print(f"{i}. {col}")
        
        # Date analysis
        if 'Date Received' in combined_unique.columns:
            combined_unique['Date Received'] = pd.to_datetime(combined_unique['Date Received'], errors='coerce')
            
            print("\n" + "="*80)
            print("DATE RANGE")
            print("="*80)
            print(f"Earliest: {combined_unique['Date Received'].min()}")
            print(f"Latest: {combined_unique['Date Received'].max()}")
            
            # MDL filing date
            mdl_date = pd.to_datetime('2019-12-18')
            combined_unique['Period'] = combined_unique['Date Received'].apply(
                lambda x: 'Before MDL' if x < mdl_date else 'After MDL'
            )
            
            period_counts = combined_unique['Period'].value_counts()
            print("\n" + "="*80)
            print("BEFORE vs AFTER MDL (December 18, 2019)")
            print("="*80)
            for period, count in period_counts.items():
                print(f"{period}: {count} reports")
        
        # Brand analysis
        if 'Brand Name' in combined_unique.columns:
            print("\n" + "="*80)
            print("TOP 10 BRAND NAMES")
            print("="*80)
            brand_counts = combined_unique['Brand Name'].value_counts().head(10)
            for brand, count in brand_counts.items():
                print(f"{brand}: {count}")
        
        # Save combined unique file
        output_file = '/Users/praveen/Praveen/allergan_downloaded_unique.xlsx'
        combined_unique.to_excel(output_file, index=False)
        print("\n" + "="*80)
        print(f"SAVED: {output_file}")
        print(f"Contains {len(combined_unique)} unique MDR records")
        print("="*80)
        
        # Compare with FDA data
        print("\n" + "="*80)
        print("COMPARISON WITH FDA MAUDE DATA")
        print("="*80)
        print(f"Downloaded files: {len(combined_unique)} unique MDRs")
        print(f"FDA MAUDE query: 1,945 total MDRs (BIOCELL + NATRELLE)")
        print(f"Difference: {1945 - len(combined_unique)} records")
        print("\nNote: Downloaded data may be filtered subset or different date range")
        print("="*80)
        
    else:
        print("\nError: 'Report Number' column not found")
        print("Available columns:", list(combined_df.columns))
else:
    print("\nNo data loaded!")
