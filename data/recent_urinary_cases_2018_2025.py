"""
RECENT URINARY DEVICE MASS TORT CASES (2018-2025)
Last 7 years of urinary/bladder/pelvic device litigation
"""

recent_urinary_cases = {
    "1. Ethicon TVT-O/TVT Secur Sling": {
        "mdl_number": "2327",
        "filing_date": "2012-04",
        "status": "Settled 2019",
        "settlement": "$116M+ (2019 global settlement)",
        "notes": "Recent settlements concluded 2018-2019",
        "search_query": 'device.brand_name:"TVT"+OR+device.brand_name:"Secur"'
    },
    
    "2. Boston Scientific Urolift": {
        "mdl_number": "Possible new MDL",
        "filing_date": "2022-2023 (emerging)",
        "status": "Active/Emerging",
        "allegations": "Prostate device - retention, pain, erosion",
        "notes": "Newer cases, check for consolidation",
        "search_query": 'device.brand_name:"UroLift"'
    },
    
    "3. Medtronic InterStim Sacral Nerve Stimulator": {
        "mdl_number": "No MDL yet (individual suits)",
        "filing_date": "2020-2024 (emerging)",
        "status": "Active",
        "allegations": "Battery failures, migrations, lead failures for bladder control",
        "notes": "Increasing cases, potential MDL",
        "search_query": 'device.brand_name:"InterStim"'
    },
    
    "4. Coloplast Titan/Genesis Penile Implants": {
        "mdl_number": "No MDL (state court coordination)",
        "filing_date": "2019-2024",
        "status": "Active",
        "allegations": "Device failures, infections, erosion",
        "notes": "Coordinated in Minnesota state court",
        "search_query": 'device.manufacturer_d_name:"Coloplast"+AND+(device.brand_name:"Titan"+OR+device.brand_name:"Genesis")'
    },
    
    "5. Boston Scientific Greenlight Laser": {
        "mdl_number": "No MDL (individual cases)",
        "filing_date": "2018-2023",
        "status": "Active",
        "allegations": "Prostate treatment - incontinence, strictures",
        "notes": "BPH treatment device",
        "search_query": 'device.brand_name:"GreenLight"'
    },
    
    "6.Axonics Sacral Neuromodulation": {
        "mdl_number": "No MDL yet",
        "filing_date": "2021-2024 (very new)",
        "status": "Emerging",
        "allegations": "Bladder control device - failures, pain",
        "notes": "Competing with InterStim, newer litigation",
        "search_query": 'device.manufacturer_d_name:"Axonics"+AND+device.generic_name:"stimulator"'
    },
    
    "7. AMS/Boston Scientific Male Sling (AdVance/AdVance XP)": {
        "mdl_number": "No official MDL",
        "filing_date": "2015-2023",
        "status": "Active",
        "allegations": "Male urinary incontinence - erosion, pain",
        "notes": "Smaller volume but ongoing",
        "search_query": 'device.brand_name:"AdVance"'
    }
}

print("=" * 80)
print("RECENT URINARY DEVICE MASS TORT CASES (2018-2025)")
print("=" * 80)
print("\nNOTE: Most large pelvic mesh MDLs were filed 2010-2015")
print("Recent cases (2018+) are mostly emerging without formal MDLs yet\n")

for name, info in recent_urinary_cases.items():
    print(f"\n{name}")
    print(f"   MDL: {info.get('mdl_number', 'N/A')}")
    print(f"   Filed: {info.get('filing_date', 'N/A')}")
    print(f"   Status: {info.get('status', 'N/A')}")
    if 'settlement' in info:
        print(f"   Settlement: {info['settlement']}")
    if 'allegations' in info:
        print(f"   Allegations: {info['allegations']}")
    print(f"   Notes: {info.get('notes', 'N/A')}")

print("\n" + "=" * 80)
print("ANALYSIS:")
print("=" * 80)
print("✓ Most major urinary device MDLs were 2010-2015 (mesh crisis)")
print("✓ 2018-2025: Mostly emerging cases without formal MDL consolidation")
print("✓ InterStim (sacral nerve stimulator) has growing case volume")
print("✓ UroLift (prostate treatment) has emerging litigation")
print("✓ Penile implants and male slings have smaller but active cases")
print("\nRECOMMENDATION: Focus on InterStim, UroLift, or recently settled")
print("Ethicon cases (2018-2019 settlements) for 7-year window")
print("=" * 80)
