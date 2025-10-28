"""
GLUCOSE MONITORING DEVICES WITH SETTLEMENTS
Historical settlements and current litigation status
"""

glucose_device_settlements = {
    "SETTLED CASES": {
        "1. Abbott FreeStyle Blood Glucose Meters": {
            "device": "FreeStyle, FreeStyle Lite, FreeStyle Freedom",
            "settlement_year": "2015-2016",
            "settlement_type": "Class action settlement",
            "settlement_amount": "$27 million (estimated)",
            "allegations": "Inaccurate readings, strip defects",
            "court": "Various state courts",
            "status": "Settled and closed",
            "notes": "Blood glucose meters, not CGM"
        },
        
        "2. Roche Accu-Chek Blood Glucose Meters": {
            "device": "Accu-Chek Aviva, Compact Plus, others",
            "settlement_year": "2012-2015",
            "settlement_type": "Class action settlement",
            "settlement_amount": "Undisclosed (small settlements)",
            "allegations": "Inaccurate readings, meter malfunctions",
            "court": "Various state and federal courts",
            "status": "Settled",
            "notes": "Multiple small settlements"
        },
        
        "3. OneTouch Ultra Blood Glucose Meters": {
            "device": "OneTouch Ultra, Ultra2, UltraMini",
            "settlement_year": "2014-2016",
            "settlement_type": "Class action settlement",
            "settlement_amount": "Undisclosed (minimal)",
            "allegations": "Inaccurate readings leading to dosing errors",
            "court": "Federal and state courts",
            "status": "Settled/Dismissed",
            "notes": "Most claims dismissed, small settlements"
        },
        
        "4. Abbott FreeStyle Libre (UK/Europe)": {
            "device": "FreeStyle Libre 1, Libre 2 CGM",
            "settlement_year": "2022-2024",
            "settlement_type": "Individual settlements (UK)",
            "settlement_amount": "Various individual amounts",
            "allegations": "Inaccurate readings, hypoglycemia not detected",
            "court": "UK courts",
            "status": "Settled (UK), Ongoing (US)",
            "notes": "UK has more settlements than US for Libre CGM"
        }
    },
    
    "ONGOING LITIGATION (No Settlements Yet)": {
        "5. Dexcom G6/G7 CGM": {
            "device": "Dexcom G6, G7 continuous glucose monitors",
            "filing_years": "2020-2024",
            "status": "Active litigation",
            "allegations": "Inaccurate readings, sensor failures, skin reactions",
            "settlement_status": "No settlements yet",
            "notes": "Individual state court cases, no MDL"
        },
        
        "6. Abbott FreeStyle Libre (US)": {
            "device": "FreeStyle Libre 1, 2, 3 CGM",
            "filing_years": "2019-2024",
            "status": "Active litigation (US)",
            "allegations": "Inaccurate readings, missed hypoglycemia",
            "settlement_status": "No US settlements yet",
            "notes": "UK settled, US cases ongoing"
        },
        
        "7. Medtronic Guardian CGM Sensors": {
            "device": "Guardian Sensor 3, Guardian Connect",
            "filing_years": "2018-2024",
            "status": "Part of larger pump litigation",
            "allegations": "Inaccurate readings, frequent calibration needs",
            "settlement_status": "No separate settlements (part of pump cases)",
            "notes": "Usually bundled with MiniMed pump litigation"
        }
    },
    
    "RECALL HISTORY (Not Settlements)": {
        "8. Abbott FreeStyle Libre - Class I Recall": {
            "recall_year": "2020",
            "reason": "Incorrect glucose readings",
            "devices_affected": "FreeStyle Libre 14-day sensors",
            "fda_action": "Class I recall (most serious)",
            "settlement": "Recall, not settlement",
            "notes": "Led to increased litigation"
        },
        
        "9. Dexcom G6 - Voluntary Recall": {
            "recall_year": "2021-2022",
            "reason": "Applicator issues, sensor errors",
            "devices_affected": "G6 sensors (specific lots)",
            "fda_action": "Voluntary recall",
            "settlement": "No settlement, just recall",
            "notes": "Product replacement offered"
        }
    }
}

print("=" * 80)
print("GLUCOSE MONITORING DEVICES WITH SETTLEMENTS")
print("=" * 80)

print("\n✅ SETTLED CASES (Historical):")
print("-" * 80)
for name, details in glucose_device_settlements["SETTLED CASES"].items():
    print(f"\n{name}")
    print(f"  Device: {details['device']}")
    print(f"  Settlement Year: {details.get('settlement_year', 'N/A')}")
    print(f"  Amount: {details.get('settlement_amount', 'Undisclosed')}")
    print(f"  Type: {details.get('settlement_type', 'N/A')}")
    print(f"  Status: {details['status']}")
    print(f"  Notes: {details.get('notes', '')}")

print("\n\n⏳ ONGOING LITIGATION (No Settlements Yet):")
print("-" * 80)
for name, details in glucose_device_settlements["ONGOING LITIGATION (No Settlements Yet)"].items():
    print(f"\n{name}")
    print(f"  Device: {details['device']}")
    print(f"  Filing Years: {details.get('filing_years', 'N/A')}")
    print(f"  Status: {details['status']}")
    print(f"  Settlement Status: {details.get('settlement_status', 'None')}")

print("\n\n⚠️ RECALLS (Not Settlements):")
print("-" * 80)
for name, details in glucose_device_settlements["RECALL HISTORY (Not Settlements)"].items():
    print(f"\n{name}")
    print(f"  Year: {details.get('recall_year', 'N/A')}")
    print(f"  Reason: {details.get('reason', 'N/A')}")
    print(f"  FDA Action: {details.get('fda_action', 'N/A')}")

print("\n" + "=" * 80)
print("SUMMARY:")
print("=" * 80)
print("✅ SETTLED: Blood glucose meters (Abbott, Roche, OneTouch) - 2012-2016")
print("✅ SETTLED: Abbott FreeStyle Libre CGM (UK only) - 2022-2024")
print("⏳ ONGOING: Dexcom G6/G7 CGM (US) - No settlements yet")
print("⏳ ONGOING: Abbott FreeStyle Libre CGM (US) - No settlements yet")
print("⏳ ONGOING: Medtronic Guardian CGM - Part of pump litigation")
print("\nNOTE: Most CGM litigation is recent (2020+) and ongoing")
print("Blood glucose meter settlements were smaller, older cases")
print("=" * 80)
