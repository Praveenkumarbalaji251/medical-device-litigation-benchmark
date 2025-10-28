"""
URINARY DEVICE MASS TORT CASES - RESEARCH
Major MDL cases involving urinary/bladder devices
"""

urinary_device_cases = {
    "1. Boston Scientific Obtryx/Advantage Sling": {
        "mdl_number": "2326",
        "device": "Transobturator and retropubic sling systems",
        "filing_date": "2012-02",
        "court": "S.D. West Virginia",
        "status": "Settled",
        "allegations": "Erosion, infection, pain, urinary problems",
        "search_query": 'device.brand_name:"Obtryx"+OR+device.brand_name:"Advantage"',
        "settlement": "Individual settlements ongoing"
    },
    
    "2. Coloplast Pelvic Mesh": {
        "mdl_number": "2387",
        "device": "Aris, Axis, Desara mesh systems",
        "filing_date": "2012-08",
        "court": "S.D. West Virginia", 
        "status": "Settled",
        "allegations": "Mesh erosion, pain, organ perforation",
        "search_query": 'device.manufacturer_d_name:"Coloplast"+AND+(device.generic_name:"mesh"+OR+device.generic_name:"sling")',
        "settlement": "$16M+ settlements"
    },
    
    "3. C.R. Bard Pelvic Repair System": {
        "mdl_number": "2187",  # Actually Avaulta mesh
        "device": "Avaulta mesh, Align TO mesh",
        "filing_date": "2010-02",
        "court": "S.D. West Virginia",
        "status": "Settled",
        "allegations": "Mesh erosion, infection, chronic pain",
        "search_query": 'device.brand_name:"Avaulta"+OR+device.brand_name:"Align"',
        "settlement": "$200M+ settlements"
    },
    
    "4. American Medical Systems (AMS) Pelvic Mesh": {
        "mdl_number": "2325",
        "device": "Monarc, Perigee, Apogee mesh",
        "filing_date": "2012-07",
        "court": "S.D. West Virginia",
        "status": "Settled",
        "allegations": "Erosion, pain, sexual dysfunction",
        "search_query": 'device.manufacturer_d_name:"American+Medical+Systems"+AND+device.generic_name:"mesh"',
        "settlement": "$830M+ settlements (largest!)"
    },
    
    "5. Cook Medical Pelvic Mesh": {
        "mdl_number": "2440",
        "device": "Biodesign mesh products",
        "filing_date": "2012-12",
        "court": "S.D. West Virginia",
        "status": "Active",
        "allegations": "Mesh failure, infection, revision surgery",
        "search_query": 'device.manufacturer_d_name:"Cook+Medical"+AND+device.generic_name:"mesh"',
        "settlement": "Ongoing litigation"
    },
    
    "BONUS - Also consider:": {
        "6. Endo/AMS Male Sling": {
            "mdl_number": "2male",
            "device": "AdVance male sling",
            "filing_date": "2015-03",
            "court": "S.D. West Virginia",
            "status": "Active",
            "allegations": "Male urinary incontinence device failures",
            "search_query": 'device.brand_name:"AdVance"+AND+device.generic_name:"sling"'
        },
        
        "7. Caldera Medical InterStim": {
            "device": "Sacral nerve stimulator for bladder control",
            "filing_date": "2018+",
            "allegations": "Battery failures, migrations",
            "search_query": 'device.brand_name:"InterStim"'
        }
    }
}

print("=" * 80)
print("TOP 5 URINARY DEVICE MASS TORT CASES FOR BENCHMARK")
print("=" * 80)

for i, (name, info) in enumerate(list(urinary_device_cases.items())[:5], 1):
    if "BONUS" not in name:
        print(f"\n{i}. {name}")
        print(f"   MDL: {info.get('mdl_number', 'N/A')}")
        print(f"   Filed: {info.get('filing_date', 'N/A')}")
        print(f"   Court: {info.get('court', 'N/A')}")
        print(f"   Status: {info.get('status', 'N/A')}")
        print(f"   Settlement: {info.get('settlement', 'Unknown')}")
        print(f"   Query: {info['search_query']}")

print("\n" + "=" * 80)
print("NOTE: All 5 cases are pelvic/transvaginal mesh related")
print("These were consolidated in S.D. West Virginia (Judge Goodwin)")
print("Total settlements across all 5: $1+ Billion")
print("=" * 80)
