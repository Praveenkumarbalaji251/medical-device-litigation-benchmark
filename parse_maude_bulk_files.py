#!/usr/bin/env python3
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
