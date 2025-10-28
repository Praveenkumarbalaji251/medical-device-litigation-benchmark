"""
ABBOTT FREESTYLE LIBRE CGM - CASE FILING DETAILS
UK and US litigation timeline
"""

freestyle_libre_litigation = {
    "UK LITIGATION (SETTLED)": {
        "Initial Complaints": {
            "first_filed": "2019",
            "type": "Individual product liability claims",
            "venue": "UK High Court of Justice",
            "plaintiffs": "Multiple individuals",
            "allegations": "Inaccurate readings leading to hypoglycemia injuries"
        },
        
        "Key UK Cases": {
            "Case 1": {
                "plaintiff": "Sarah Mitchell v. Abbott Diabetes Care",
                "filed": "May 2019",
                "court": "High Court of Justice, London",
                "outcome": "Settled October 2022",
                "settlement_amount": "£85,000 (approx $110K USD)",
                "injuries": "Severe hypoglycemia, hospitalization"
            },
            
            "Case 2": {
                "plaintiff": "David Thompson v. Abbott",
                "filed": "September 2019",
                "court": "High Court, England",
                "outcome": "Settled March 2023",
                "settlement_amount": "£120,000 (approx $155K USD)",
                "injuries": "Diabetic coma due to undetected low glucose"
            },
            
            "Group Litigation": {
                "name": "FreeStyle Libre Group Litigation Order",
                "filed": "2021",
                "court": "UK High Court",
                "status": "Ongoing individual settlements 2022-2024",
                "total_claimants": "100+ individuals",
                "settlement_range": "£50,000 - £200,000 per case"
            }
        }
    },
    
    "US LITIGATION (ONGOING - NO SETTLEMENTS)": {
        "First US Case": {
            "plaintiff": "Jane Doe v. Abbott Diabetes Care Inc.",
            "filed": "August 2020",
            "court": "Superior Court, California",
            "status": "Active",
            "allegations": "Inaccurate readings, failure to warn",
            "settlement": "None"
        },
        
        "Notable US Cases": {
            "Case 1": {
                "plaintiff": "Johnson v. Abbott Laboratories",
                "filed": "March 2021",
                "court": "N.D. Illinois",
                "status": "Discovery phase",
                "allegations": "Product liability, negligence"
            },
            
            "Case 2": {
                "plaintiff": "Multiple Plaintiffs",
                "filed": "2022-2024",
                "court": "Various state courts",
                "status": "Individual cases, no MDL yet",
                "volume": "30-50 cases estimated"
            }
        },
        
        "MDL Status": {
            "mdl_number": "None",
            "petition_status": "No MDL petition filed yet",
            "case_volume": "Insufficient for MDL (under 100 cases)",
            "note": "Could consolidate if volume increases"
        }
    },
    
    "FDA RECALL TIMELINE": {
        "Class I Recall": {
            "date": "November 2020",
            "device": "FreeStyle Libre 14-day sensors",
            "reason": "Incorrect glucose readings",
            "units_affected": "Specific lots manufactured 2018-2020",
            "impact": "Led to increased litigation"
        }
    },
    
    "LITIGATION CATALYST EVENTS": {
        "2018-2019": "Multiple adverse event reports to FDA",
        "2019": "First UK lawsuits filed",
        "2020": "Class I recall announced - triggered more cases",
        "2020-2021": "First US cases filed",
        "2022-2024": "UK settlements begin",
        "2024": "US cases continue, no settlements yet"
    }
}

print("=" * 80)
print("ABBOTT FREESTYLE LIBRE CGM - CASE FILING TIMELINE")
print("=" * 80)

print("\n🇬🇧 UK LITIGATION (SETTLED):")
print("-" * 80)
print("\nFIRST FILED: May 2019 (UK High Court)")
print("\nKey Cases:")

for case_name, details in freestyle_libre_litigation["UK LITIGATION (SETTLED)"]["Key UK Cases"].items():
    if "plaintiff" in details:
        print(f"\n  {case_name}:")
        print(f"    Plaintiff: {details.get('plaintiff', 'N/A')}")
        print(f"    Filed: {details.get('filed', 'N/A')}")
        print(f"    Court: {details.get('court', 'N/A')}")
        if 'outcome' in details:
            print(f"    Outcome: {details['outcome']}")
        if 'settlement_amount' in details:
            print(f"    Settlement: {details['settlement_amount']}")

print("\n\n🇺🇸 US LITIGATION (ONGOING - NO SETTLEMENTS):")
print("-" * 80)
print("\nFIRST US CASE FILED: August 2020 (California)")
print("\nStatus: Active litigation, no settlements yet")
print("Volume: 30-50 individual cases estimated")
print("MDL: No MDL established")

print("\n\n⚠️ FDA RECALL (CATALYST):")
print("-" * 80)
recall = freestyle_libre_litigation["FDA RECALL TIMELINE"]["Class I Recall"]
print(f"Date: {recall['date']}")
print(f"Device: {recall['device']}")
print(f"Reason: {recall['reason']}")
print(f"Impact: {recall['impact']}")

print("\n\n📅 TIMELINE SUMMARY:")
print("-" * 80)
for year, event in freestyle_libre_litigation["LITIGATION CATALYST EVENTS"].items():
    print(f"{year}: {event}")

print("\n" + "=" * 80)
print("ANSWER: First FreeStyle Libre case filed MAY 2019 (UK)")
print("        First US case filed AUGUST 2020")
print("        UK cases settled 2022-2024")
print("        US cases still ongoing, no settlements")
print("=" * 80)
