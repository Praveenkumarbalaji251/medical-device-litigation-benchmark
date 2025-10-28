"""
DIABETES DEVICE CLASS ACTION & MASS TORT CASES
Major litigation involving diabetes management devices
"""

diabetes_device_cases = {
    "INSULIN PUMPS": {
        "1. Medtronic MiniMed Insulin Pumps": {
            "mdl_number": "3032",
            "devices": "MiniMed 600 Series, 630G, 670G",
            "filing_date": "2021-03",
            "court": "C.D. California",
            "status": "Active",
            "allegations": "Battery failures, retractor ring defects, dose errors",
            "recall_history": "Class I recall 2019 (retractor ring)",
            "settlement": "Ongoing",
            "notes": "ALREADY IN YOUR 48 CASES! 50,200 MDRs"
        },
        
        "2. Medtronic Paradigm Insulin Pumps": {
            "mdl_number": "None (individual cases)",
            "devices": "Paradigm Revel, Veo, 722, 523",
            "filing_date": "2015-2020",
            "status": "Various settlements",
            "allegations": "Insulin under-delivery, over-delivery, battery issues",
            "recall_history": "Multiple Class I recalls",
            "settlement": "Individual settlements",
            "notes": "ALREADY IN YOUR 48 CASES! 41,036 MDRs"
        },
        
        "3. Insulet OmniPod Insulin Pumps": {
            "mdl_number": "None yet",
            "devices": "OmniPod, OmniPod DASH",
            "filing_date": "2020-2024",
            "status": "Emerging litigation",
            "allegations": "Pod failures, occlusions, dose errors",
            "recall_history": "Class I recall 2021 (software issue)",
            "settlement": "None yet",
            "notes": "Growing case volume, potential MDL"
        },
        
        "4. Tandem Diabetes Care t:slim Pumps": {
            "mdl_number": "None",
            "devices": "t:slim X2, Basal-IQ, Control-IQ",
            "filing_date": "2019-2024",
            "status": "Individual cases",
            "allegations": "Cartridge leaks, occlusions, software errors",
            "recall_history": "Class II recalls (cartridges)",
            "settlement": "None",
            "notes": "Smaller volume, state court cases"
        }
    },
    
    "CONTINUOUS GLUCOSE MONITORS (CGM)": {
        "5. Dexcom G6/G7 CGM": {
            "mdl_number": "None",
            "devices": "G6, G7 continuous glucose monitors",
            "filing_date": "2020-2024",
            "status": "Individual cases",
            "allegations": "Inaccurate readings, sensor failures, skin reactions",
            "recall_history": "Voluntary recalls (applicator issues)",
            "settlement": "None",
            "notes": "Increasing MAUDE reports"
        },
        
        "6. Abbott FreeStyle Libre CGM": {
            "mdl_number": "None",
            "devices": "Libre 1, 2, 3, Libre 14-day",
            "filing_date": "2019-2024",
            "status": "Individual cases globally",
            "allegations": "Inaccurate readings, hypoglycemia missed, adhesive failures",
            "recall_history": "Class I recall 2020 (incorrect readings)",
            "settlement": "None in US, settlements in UK",
            "notes": "International litigation more active"
        }
    },
    
    "BLOOD GLUCOSE METERS": {
        "7. OneTouch Ultra Blood Glucose Meters": {
            "mdl_number": "None",
            "devices": "OneTouch Ultra, Ultra2, UltraMini",
            "filing_date": "2011-2016",
            "status": "Settled/Dismissed",
            "allegations": "Inaccurate readings leading to improper treatment",
            "recall_history": "Recalls for accuracy issues",
            "settlement": "Class action settled (small amount)",
            "notes": "Older litigation, mostly resolved"
        },
        
        "8. Roche Accu-Chek Blood Glucose Meters": {
            "mdl_number": "None",
            "devices": "Accu-Chek Aviva, Compact Plus",
            "filing_date": "2010-2015",
            "status": "Settled",
            "allegations": "Inaccurate readings, strip defects",
            "recall_history": "Multiple recalls",
            "settlement": "Settled",
            "notes": "Historic case"
        }
    },
    
    "COMBINATION SYSTEMS": {
        "9. Medtronic 670G Hybrid Closed Loop System": {
            "mdl_number": "Part of MDL 3032",
            "devices": "670G with Guardian Sensor 3",
            "filing_date": "2021+",
            "status": "Active (within MiniMed MDL)",
            "allegations": "Auto-mode failures, frequent exits, sensor inaccuracies",
            "recall_history": "Class I recall (retractor ring)",
            "settlement": "Ongoing",
            "notes": "Part of larger MiniMed litigation"
        }
    },
    
    "EMERGING/RECENT (2020-2025)": {
        "10. Insulet OmniPod DASH System": {
            "mdl_number": "None yet",
            "devices": "OmniPod DASH, OmniPod 5",
            "filing_date": "2022-2024",
            "status": "Emerging",
            "allegations": "Pod adhesive failures, occlusions, Bluetooth connectivity issues",
            "recall_history": "2023 recall (software)",
            "settlement": "None",
            "notes": "Most recent litigation trend"
        }
    }
}

print("=" * 80)
print("DIABETES DEVICE CLASS ACTION & MASS TORT CASES")
print("=" * 80)

for category, cases in diabetes_device_cases.items():
    print(f"\n{category}")
    print("-" * 80)
    
    for case_name, details in cases.items():
        print(f"\n{case_name}")
        print(f"  MDL: {details.get('mdl_number', 'N/A')}")
        print(f"  Devices: {details.get('devices', 'N/A')}")
        print(f"  Filed: {details.get('filing_date', 'N/A')}")
        print(f"  Status: {details.get('status', 'N/A')}")
        print(f"  Allegations: {details.get('allegations', 'N/A')}")
        if 'settlement' in details:
            print(f"  Settlement: {details['settlement']}")
        print(f"  Notes: {details.get('notes', 'N/A')}")

print("\n" + "=" * 80)
print("SUMMARY:")
print("=" * 80)
print("✓ Insulin Pumps: Highest litigation volume (Medtronic dominant)")
print("✓ CGM Devices: Emerging litigation, increasing MAUDE reports")
print("✓ Blood Glucose Meters: Mostly historic, settled cases")
print("✓ Already in your 48: Medtronic MiniMed (50K MDRs), Paradigm (41K MDRs)")
print("✓ New candidates: OmniPod, Dexcom, Abbott FreeStyle Libre")
print("=" * 80)
