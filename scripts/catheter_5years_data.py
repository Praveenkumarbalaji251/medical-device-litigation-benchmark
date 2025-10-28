import requests
import pandas as pd
from datetime import datetime
import time

BASE_URL = "https://api.fda.gov/device/event.json"

# 3 Catheter devices - get last 5 years (2020-2025)
DEVICES = [
    {"name": "Bard PowerPort", "brand": "PowerPort"},
    {"name": "Cook Celect IVC Filter", "brand": "Celect"},
    {"name": "Bard G2 IVC Filter", "brand": "G2"}
]

def fetch_all_records(brand_name):
    """Fetch all records for a device"""
    print(f"\nFetching data for {brand_name}...")
    
    params = {
        'search': f'device.brand_name:"{brand_name}"',
        'limit': 100,
        'skip': 0
    }
    
    all_records = []
    page = 0
    
    while page < 100:  # Safety limit
        params['skip'] = page * 100
        
        try:
            response = requests.get(BASE_URL, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                
                if not results:
                    break
                
                all_records.extend(results)
                page += 1
                print(f"  Page {page}: {len(results)} records (total: {len(all_records)})")
                
                if len(results) < 100:
                    break
                    
                time.sleep(0.2)  # Rate limiting
            else:
                print(f"  API Error: {response.status_code}")
                break
                
        except Exception as e:
            print(f"  Error: {str(e)}")
            break
    
    return all_records

def clean_text(text):
    """Remove illegal Excel characters"""
    if not text:
        return text
    # Remove control characters except newline, tab
    import re
    text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F-\x9F]', '', str(text))
    return text

def process_records(records, device_name):
    """Process records into DataFrame"""
    rows = []
    
    for record in records:
        row = {
            'device_name': device_name,
            'report_number': record.get('report_number', ''),
            'date_received': record.get('date_received', ''),
            'date_of_event': record.get('date_of_event', ''),
            'event_type': ', '.join(record.get('event_type', [])),
            'report_source_code': record.get('report_source_code', ''),
            'manufacturer_name': '',
            'brand_name': '',
            'generic_name': '',
            'model_number': '',
            'product_code': '',
            'device_problem': '',
            'patient_age': '',
            'patient_sex': '',
            'event_description': '',
            'manufacturer_narrative': ''
        }
        
        # Device info
        devices = record.get('device', [])
        if devices:
            device = devices[0]
            row['manufacturer_name'] = device.get('manufacturer_d_name', '')
            row['brand_name'] = device.get('brand_name', '')
            row['generic_name'] = device.get('generic_name', '')
            row['model_number'] = device.get('model_number', '')
            row['product_code'] = device.get('openfda', {}).get('device_class', [''])[0] if device.get('openfda') else ''
            
            problems = device.get('device_event_key', [])
            row['device_problem'] = '; '.join(problems[:5]) if problems else ''
        
        # Patient info
        patient = record.get('patient', [])
        if patient:
            p = patient[0]
            row['patient_age'] = str(p.get('patient_age', ''))
            row['patient_sex'] = p.get('patient_sex', '')
        
        # MDR text - get descriptions
        mdr_text = record.get('mdr_text', [])
        if mdr_text:
            for text_item in mdr_text:
                text_type = text_item.get('text_type_code', '')
                text_content = text_item.get('text', '')
                
                if text_content:
                    if 'Event' in text_type or 'Problem' in text_type:
                        row['event_description'] = clean_text(text_content[:2000])
                    elif 'Manufacturer' in text_type:
                        row['manufacturer_narrative'] = clean_text(text_content[:2000])
        
        rows.append(row)
    
    return pd.DataFrame(rows)

def main():
    print("=" * 80)
    print("3 CATHETER DEVICES - 5 YEAR DATA EXTRACTION")
    print("Fetching all MDR data from 2020-2025")
    print("=" * 80)
    
    all_dataframes = []
    
    for device in DEVICES:
        print(f"\n{'=' * 80}")
        print(f"DEVICE: {device['name']}")
        print('=' * 80)
        
        # Fetch records
        records = fetch_all_records(device['brand'])
        
        if not records:
            print(f"No records found for {device['name']}")
            continue
        
        print(f"Total records fetched: {len(records)}")
        
        # Process to DataFrame
        print("Processing records...")
        df = process_records(records, device['name'])
        
        # Parse dates
        df['date_received'] = pd.to_datetime(df['date_received'], format='%Y%m%d', errors='coerce')
        df['date_of_event'] = pd.to_datetime(df['date_of_event'], format='%Y%m%d', errors='coerce')
        
        # Filter to 2020-2025
        df_filtered = df[df['date_received'] >= '2020-01-01'].copy()
        print(f"Records from 2020-2025: {len(df_filtered)}")
        
        # Add analysis columns
        df_filtered['year'] = df_filtered['date_received'].dt.year
        df_filtered['month'] = df_filtered['date_received'].dt.month
        df_filtered['year_month'] = df_filtered['date_received'].dt.strftime('%Y-%m')
        
        all_dataframes.append(df_filtered)
    
    # Combine all devices
    print("\n" + "=" * 80)
    print("CREATING COMBINED EXCEL FILE")
    print("=" * 80)
    
    combined_df = pd.concat(all_dataframes, ignore_index=True)
    combined_df = combined_df.sort_values(['device_name', 'date_received'])
    
    print(f"\nTotal records (all 3 devices, 2020-2025): {len(combined_df)}")
    print()
    
    # Save to Excel with multiple sheets
    output_file = 'catheter_devices_5years.xlsx'
    
    print("Creating Excel file...")
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # All data combined
        combined_df.to_excel(writer, sheet_name='All Devices Combined', index=False)
        
        # Separate sheet per device
        for device in DEVICES:
            device_df = combined_df[combined_df['device_name'] == device['name']]
            sheet_name = device['name'][:31]  # Excel limit
            device_df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        # Monthly summary by device
        monthly_summary = combined_df.groupby(['device_name', 'year_month']).agg({
            'report_number': 'count',
            'event_type': lambda x: ', '.join(x.value_counts().index[:2])
        }).reset_index()
        monthly_summary.columns = ['Device', 'Year-Month', 'Report Count', 'Top Event Types']
        monthly_summary.to_excel(writer, sheet_name='Monthly Summary', index=False)
        
        # Event type breakdown by device
        event_summary = combined_df.groupby(['device_name', 'event_type']).size().reset_index(name='Count')
        event_summary = event_summary.sort_values(['device_name', 'Count'], ascending=[True, False])
        event_summary.to_excel(writer, sheet_name='Event Types', index=False)
        
        # Yearly summary
        yearly_summary = combined_df.groupby(['device_name', 'year']).size().reset_index(name='Report Count')
        yearly_pivot = yearly_summary.pivot(index='device_name', columns='year', values='Report Count').fillna(0)
        yearly_pivot.to_excel(writer, sheet_name='Yearly Summary')
        
        # Device problems
        problems_list = []
        for idx, row in combined_df.iterrows():
            if pd.notna(row['device_problem']) and row['device_problem']:
                for problem in row['device_problem'].split(';'):
                    problem = problem.strip()
                    if problem:
                        problems_list.append({
                            'device_name': row['device_name'],
                            'problem': problem
                        })
        
        if problems_list:
            problems_df = pd.DataFrame(problems_list)
            problem_summary = problems_df.groupby(['device_name', 'problem']).size().reset_index(name='Count')
            problem_summary = problem_summary.sort_values(['device_name', 'Count'], ascending=[True, False])
            top_problems = problem_summary.groupby('device_name').head(20)
            top_problems.to_excel(writer, sheet_name='Top Problems', index=False)
    
    print()
    print("=" * 80)
    print("COMPLETE")
    print("=" * 80)
    print(f"✓ File saved: {output_file}")
    print()
    print("Sheets included:")
    print("  1. All Devices Combined - All records together")
    print("  2. Bard PowerPort - PowerPort data only")
    print("  3. Cook Celect IVC Filter - Celect data only")
    print("  4. Bard G2 IVC Filter - G2 data only")
    print("  5. Monthly Summary - Monthly counts by device")
    print("  6. Event Types - Event breakdown by device")
    print("  7. Yearly Summary - Yearly comparison table")
    print("  8. Top Problems - Most common problems per device")
    print()
    
    # Summary stats
    print("SUMMARY BY DEVICE (2020-2025):")
    print("-" * 60)
    for device in DEVICES:
        device_data = combined_df[combined_df['device_name'] == device['name']]
        deaths = device_data[device_data['event_type'].str.contains('Death', na=False)]
        injuries = device_data[device_data['event_type'].str.contains('Injury', na=False)]
        
        print(f"\n{device['name']}:")
        print(f"  Total reports: {len(device_data):,}")
        print(f"  Deaths: {len(deaths):,}")
        print(f"  Injuries: {len(injuries):,}")
        print(f"  Date range: {device_data['date_received'].min()} to {device_data['date_received'].max()}")
    
    print()

if __name__ == "__main__":
    main()
