#!/usr/bin/env python3
"""
Create Excel-style analysis for Philips CPAP MAUDE-Litigation correlation
"""

import pandas as pd
from datetime import datetime
import json

def create_philips_cpap_analysis():
    """Create comprehensive Philips CPAP case analysis for Excel export."""
    
    # PHILIPS CPAP CASE DATA
    philips_cpap_data = {
        "Device Information": {
            "Device Name": "Philips DreamStation CPAP",
            "Manufacturer": "Philips Healthcare", 
            "Device Type": "Sleep Therapy Equipment",
            "FDA Product Code": "BZD", 
            "Models Affected": "DreamStation Auto CPAP, DreamStation Go, BiPAP Auto, SystemOne REMstar",
            "Estimated Devices in Market": "3-4 million worldwide"
        },
        
        "Litigation Timeline": {
            "FDA Recall Date": "2021-06-14",
            "First Lawsuit Filed": "2021-07-01", 
            "MDL Established": "2021-12-16",
            "MDL Number": "3014",
            "MDL Court": "W.D. Pennsylvania", 
            "MDL Judge": "Joy Flowers Conti",
            "Current Plaintiff Count": "700,000+",
            "Estimated Settlement": "$5-15 billion"
        },
        
        "Key Issue": {
            "Primary Problem": "Foam degradation releasing toxic particles",
            "Health Risks": "Cancer, respiratory damage, toxic exposure",
            "Affected Population": "Sleep apnea patients using devices 2009-2021",
            "Severity": "Life-threatening complications reported"
        },
        
        "MAUDE Analysis Periods": {
            "Baseline Period": "2019-01-01 to 2020-12-31",
            "Pre-Litigation Warning": "2021-01-01 to 2021-06-14", 
            "Post-Recall Period": "2021-06-15 to 2022-12-31",
            "Analysis Focus": "6 months before first lawsuit (Jan-June 2021)"
        }
    }
    
    # CREATE MAUDE DATA TRACKING TEMPLATE
    maude_tracking_template = {
        "Month": [
            "2020-01", "2020-02", "2020-03", "2020-04", "2020-05", "2020-06",
            "2020-07", "2020-08", "2020-09", "2020-10", "2020-11", "2020-12", 
            "2021-01", "2021-02", "2021-03", "2021-04", "2021-05", "2021-06"
        ],
        "Total_MAUDE_Reports": [0] * 18,  # To be filled with actual MAUDE data
        "Serious_Injury_Reports": [0] * 18,
        "Death_Reports": [0] * 18,
        "Malfunction_Reports": [0] * 18,
        "Key_Complaint_Keywords": [""] * 18,  # "foam degradation", "black particles", etc.
        "Reporter_Type_Patient": [0] * 18,
        "Reporter_Type_Healthcare": [0] * 18, 
        "Reporter_Type_Manufacturer": [0] * 18,
        "FDA_Actions": [""] * 18,  # Any FDA warnings, letters, etc.
        "Litigation_Prediction_Score": [0] * 18  # 1-10 scale based on report patterns
    }
    
    # EXPECTED MAUDE PATTERN (Hypothetical based on known litigation pattern)
    expected_pattern = {
        "Month": [
            "2020-01", "2020-02", "2020-03", "2020-04", "2020-05", "2020-06",
            "2020-07", "2020-08", "2020-09", "2020-10", "2020-11", "2020-12",
            "2021-01", "2021-02", "2021-03", "2021-04", "2021-05", "2021-06"
        ],
        "Expected_Total_Reports": [
            150, 140, 160, 145, 155, 170,  # 2020 baseline
            165, 180, 175, 190, 200, 220,  # 2020 slight increase
            350, 450, 650, 850, 1200, 1800  # 2021 explosion before recall
        ],
        "Litigation_Risk_Level": [
            "Low", "Low", "Low", "Low", "Low", "Low",
            "Low", "Low", "Low", "Low", "Medium", "Medium", 
            "High", "High", "Critical", "Critical", "Imminent", "Litigation Filed"
        ]
    }
    
    return philips_cpap_data, maude_tracking_template, expected_pattern

def create_excel_analysis():
    """Create Excel-ready analysis files."""
    
    print("📊 CREATING PHILIPS CPAP MAUDE-LITIGATION ANALYSIS")
    print("=" * 55)
    
    # Get the data
    case_data, maude_template, expected_pattern = create_philips_cpap_analysis()
    
    # Create DataFrames for Excel export
    
    # 1. Case Information Sheet
    case_info_df = pd.DataFrame([
        ["Device Name", case_data["Device Information"]["Device Name"]],
        ["Manufacturer", case_data["Device Information"]["Manufacturer"]],
        ["Device Type", case_data["Device Information"]["Device Type"]],
        ["Models Affected", case_data["Device Information"]["Models Affected"]],
        ["Devices in Market", case_data["Device Information"]["Estimated Devices in Market"]],
        ["", ""],  # Blank row
        ["FDA Recall Date", case_data["Litigation Timeline"]["FDA Recall Date"]],
        ["First Lawsuit Filed", case_data["Litigation Timeline"]["First Lawsuit Filed"]],
        ["MDL Established", case_data["Litigation Timeline"]["MDL Established"]],
        ["MDL Number", case_data["Litigation Timeline"]["MDL Number"]],
        ["MDL Court", case_data["Litigation Timeline"]["MDL Court"]],
        ["Current Plaintiffs", case_data["Litigation Timeline"]["Current Plaintiff Count"]],
        ["Estimated Settlement", case_data["Litigation Timeline"]["Estimated Settlement"]],
        ["", ""],  # Blank row
        ["Primary Problem", case_data["Key Issue"]["Primary Problem"]],
        ["Health Risks", case_data["Key Issue"]["Health Risks"]],
        ["Affected Population", case_data["Key Issue"]["Affected Population"]]
    ], columns=["Field", "Value"])
    
    # 2. MAUDE Tracking Template
    maude_df = pd.DataFrame(maude_template)
    
    # 3. Expected Pattern Analysis  
    pattern_df = pd.DataFrame(expected_pattern)
    
    # 4. Analysis Instructions
    instructions_df = pd.DataFrame([
        ["MAUDE SEARCH INSTRUCTIONS", ""],
        ["", ""],
        ["1. Go to FDA MAUDE Database", "https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfmaude/search.cfm"],
        ["2. Search Terms", "Philips DreamStation, Philips CPAP, DreamStation CPAP"],
        ["3. Date Range", "January 1, 2020 to June 30, 2021"],
        ["4. Extract Data", "Total reports per month, injury types, complaint text"],
        ["5. Fill Template", "Complete the MAUDE_Tracking sheet with actual numbers"],
        ["", ""],
        ["KEY METRICS TO TRACK", ""],
        ["Total Reports", "Overall adverse event volume"],
        ["Serious Injuries", "Reports with significant harm"],
        ["Deaths", "Fatality reports"],
        ["Malfunctions", "Device failure reports"],
        ["Keywords", "foam, degradation, particles, cancer, respiratory"],
        ["Reporter Types", "Patient vs Healthcare vs Manufacturer breakdown"],
        ["", ""],
        ["PREDICTION INDICATORS", ""],
        ["300%+ increase in reports", "High litigation probability"],
        ["Shift to serious injuries", "Higher case values expected"], 
        ["Patient reports dominate", "Class action likely"],
        ["FDA actions increase", "Recall/litigation imminent"]
    ], columns=["Instruction", "Details"])
    
    # Save to Excel with multiple sheets
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    excel_file = f"data/raw/Philips_CPAP_MAUDE_Analysis_{timestamp}.xlsx"
    
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        case_info_df.to_excel(writer, sheet_name='Case_Information', index=False)
        maude_df.to_excel(writer, sheet_name='MAUDE_Tracking', index=False)
        pattern_df.to_excel(writer, sheet_name='Expected_Pattern', index=False)
        instructions_df.to_excel(writer, sheet_name='Instructions', index=False)
    
    # Also save as CSV for easy access
    csv_file = f"data/raw/Philips_CPAP_Case_Data_{timestamp}.csv"
    case_info_df.to_csv(csv_file, index=False)
    
    print(f"\n✅ FILES CREATED:")
    print(f"📊 Excel Analysis: {excel_file}")
    print(f"📋 CSV Summary: {csv_file}")
    
    print(f"\n📋 EXCEL SHEETS CREATED:")
    print(f"1. Case_Information - Device and litigation details")
    print(f"2. MAUDE_Tracking - Template to fill with MAUDE data")
    print(f"3. Expected_Pattern - Predicted report patterns")
    print(f"4. Instructions - How to search MAUDE database")
    
    print(f"\n🎯 NEXT STEPS:")
    print(f"1. Open the Excel file")
    print(f"2. Go to FDA MAUDE database")
    print(f"3. Search for 'Philips DreamStation' reports 2020-2021")
    print(f"4. Fill in the MAUDE_Tracking sheet with actual numbers")
    print(f"5. Compare with Expected_Pattern to validate prediction model")
    
    print(f"\n🔍 WHAT TO LOOK FOR:")
    print(f"• Report volume spike 6 months before litigation (Jan-June 2021)")
    print(f"• Keywords: 'foam degradation', 'black particles', 'cancer'")
    print(f"• Shift from manufacturer reports to patient reports")
    print(f"• Increase in serious injury vs. malfunction reports")
    
    return excel_file

if __name__ == "__main__":
    excel_file = create_excel_analysis()
    
    print(f"\n🚀 PHILIPS CPAP ANALYSIS TEMPLATE READY!")
    print(f"Use this as the model for all 50 devices in your benchmark.")