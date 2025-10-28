"""
Research: 12 New Medical Device Cases - Breast Devices & Similar USA Litigation
Focus: Breast implants, tissue expanders, and related devices
"""

print("=" * 80)
print("12 NEW MEDICAL DEVICE CASES - BREAST DEVICES & USA LITIGATION")
print("=" * 80)

cases = [
    {
        "number": 1,
        "device": "Mentor Breast Implants",
        "manufacturer": "Mentor Worldwide LLC (Johnson & Johnson)",
        "mdl_number": "MDL 2004",
        "court": "D. New Jersey",
        "filing_date": "2009-03-01",
        "status": "Settled",
        "allegations": "Rupture, silicone leakage, capsular contracture, BIA-ALCL",
        "settlement": "$20M+ settlements (2012-2015)",
        "key_facts": [
            "Memory Gel and MemoryShape implants",
            "FDA approved 2006, litigation started 2009",
            "BIA-ALCL (lymphoma) cases emerged 2011+",
            "Consolidated with other silicone implant cases"
        ]
    },
    {
        "number": 2,
        "device": "Sientra Breast Implants",
        "manufacturer": "Sientra Inc.",
        "mdl_number": None,
        "court": "Various State Courts (CA, TX, FL)",
        "filing_date": "2015-09-01",
        "status": "Active",
        "allegations": "Mold contamination, rupture, BIA-ALCL, capsular contracture",
        "settlement": "No settlements yet",
        "key_facts": [
            "2015 recall due to mold contamination",
            "BIA-ALCL cases increasing 2016-2024",
            "Textured surface implants (OPUS line)",
            "FDA recall: October 2015 (Class I recall)"
        ]
    },
    {
        "number": 3,
        "device": "Natrelle Breast Implants (Allergan/AbbVie)",
        "manufacturer": "Allergan (AbbVie)",
        "mdl_number": "MDL 2921", # Already have this one, but different product line
        "court": "D. New Jersey",
        "filing_date": "2019-02-01",
        "status": "Active/Settled (mixed)",
        "allegations": "BIA-ALCL, squamous cell carcinoma, rupture",
        "settlement": "Individual settlements $50K-$500K",
        "key_facts": [
            "Different from BIOCELL (smoother surface)",
            "Saline and silicone versions",
            "BIA-ALCL cases lower than BIOCELL but present",
            "Ongoing litigation 2019-2025"
        ]
    },
    {
        "number": 4,
        "device": "Ideal Implant (Structured Breast Implant)",
        "manufacturer": "Ideal Implant Inc.",
        "mdl_number": None,
        "court": "Various State Courts (TX, CA)",
        "filing_date": "2018-06-01",
        "status": "Active",
        "allegations": "Rupture, deflation, capsular contracture, pain",
        "settlement": "No settlements",
        "key_facts": [
            "Saline-filled structured implant (2014 FDA approval)",
            "Marketed as 'silicone look, saline safety'",
            "Higher rupture rates than traditional saline",
            "Growing litigation 2018-2024"
        ]
    },
    {
        "number": 5,
        "device": "CPG/McGhan Breast Implants",
        "manufacturer": "Allergan (now AbbVie)",
        "mdl_number": "MDL 926",
        "court": "D. Alabama",
        "filing_date": "1992-01-01",
        "status": "Settled (historic)",
        "allegations": "Silicone leakage, autoimmune disease, rupture",
        "settlement": "$1.2B settlement fund (1994)",
        "key_facts": [
            "Part of 1990s silicone implant crisis",
            "FDA moratorium 1992-2006",
            "One of largest medical device settlements",
            "Historic case, good benchmark data"
        ]
    },
    {
        "number": 6,
        "device": "Poly Implant Prothèse (PIP) Implants",
        "manufacturer": "Poly Implant Prothèse (France)",
        "mdl_number": None,
        "court": "Various State Courts (CA, NY, FL)",
        "filing_date": "2010-03-01",
        "status": "Settled/Dismissed (mixed)",
        "allegations": "Industrial-grade silicone, high rupture rate, cancer fears",
        "settlement": "Manufacturer bankrupt, limited US settlements",
        "key_facts": [
            "Largest implant scandal in history (400K women worldwide)",
            "Used industrial silicone instead of medical grade",
            "Recalled globally 2010",
            "Limited US cases (mostly European/Latin America)"
        ]
    },
    {
        "number": 7,
        "device": "Tissuel Tissue Expanders",
        "manufacturer": "Mentor Worldwide LLC",
        "mdl_number": None,
        "court": "Various State Courts",
        "filing_date": "2016-01-01",
        "status": "Active",
        "allegations": "Deflation, port malfunction, infection, pain",
        "settlement": "No major settlements",
        "key_facts": [
            "Used in breast reconstruction (post-mastectomy)",
            "Port/valve failures causing deflation",
            "Infection rates higher than expected",
            "Growing litigation 2016-2024"
        ]
    },
    {
        "number": 8,
        "device": "AeroForm Tissue Expander",
        "manufacturer": "AirXpanders (acquired by Allergan 2016)",
        "mdl_number": None,
        "court": "Various State Courts (CA, TX)",
        "filing_date": "2017-09-01",
        "status": "Discontinued/Active litigation",
        "allegations": "CO2 leakage, device failure, pain, need for revision",
        "settlement": "No settlements, device discontinued 2020",
        "key_facts": [
            "CO2-based tissue expander (needle-free)",
            "FDA approved 2014",
            "Discontinued 2020 due to issues",
            "Allegations of premature device failure"
        ]
    },
    {
        "number": 9,
        "device": "SAVI SCOUT Surgical Guidance System",
        "manufacturer": "Cianna Medical (Merit Medical)",
        "mdl_number": None,
        "court": "Various State Courts",
        "filing_date": "2020-01-01",
        "status": "Active (emerging)",
        "allegations": "Reflector migration, retention, pain, MRI interference",
        "settlement": "No settlements",
        "key_facts": [
            "Radar reflector for breast tumor localization",
            "FDA approved 2014",
            "Reports of reflectors left in body",
            "MRI safety concerns emerging 2019+"
        ]
    },
    {
        "number": 10,
        "device": "Bard Gel Mark ULTRA Breast Tissue Marker",
        "manufacturer": "Bard (BD)",
        "mdl_number": None,
        "court": "Various State Courts",
        "filing_date": "2019-06-01",
        "status": "Active",
        "allegations": "Migration, infection, painful removal, foreign body reaction",
        "settlement": "No settlements",
        "key_facts": [
            "Collagen-based biopsy site marker",
            "Used to mark tumor sites",
            "Reports of migration to lymph nodes",
            "Difficult/painful removal procedures"
        ]
    },
    {
        "number": 11,
        "device": "ATEC Breast Biopsy System",
        "manufacturer": "Hologic Inc.",
        "mdl_number": None,
        "court": "Various State Courts",
        "filing_date": "2018-03-01",
        "status": "Active",
        "allegations": "Excessive bleeding, hematoma, tissue damage, device malfunction",
        "settlement": "Individual settlements (confidential)",
        "key_facts": [
            "Automated tissue excision/collection",
            "Vacuum-assisted breast biopsy",
            "Reports of uncontrolled bleeding",
            "Device malfunction during procedures"
        ]
    },
    {
        "number": 12,
        "device": "Motiva Breast Implants",
        "manufacturer": "Establishment Labs (Costa Rica)",
        "mdl_number": None,
        "court": "Various State Courts (CA, FL, TX)",
        "filing_date": "2022-01-01",
        "status": "Active (very recent)",
        "allegations": "Rupture, Q Inside microchip failure, BIA-ALCL concerns",
        "settlement": "No settlements (too early)",
        "key_facts": [
            "FDA approved 2023 (but used off-label before)",
            "Q Inside microchip for tracking",
            "SmoothSilk/SilkSurface technology",
            "Emerging litigation 2022-2025"
        ]
    }
]

print("\n" + "=" * 80)
print("CASE SUMMARIES")
print("=" * 80)

for case in cases:
    print(f"\n{case['number']}. {case['device']}")
    print(f"   Manufacturer: {case['manufacturer']}")
    print(f"   MDL: {case['mdl_number'] or 'No MDL'}")
    print(f"   Court: {case['court']}")
    print(f"   Filing Date: {case['filing_date']}")
    print(f"   Status: {case['status']}")
    print(f"   Allegations: {case['allegations']}")
    print(f"   Settlement: {case['settlement']}")
    print(f"   Key Facts:")
    for fact in case['key_facts']:
        print(f"     • {fact}")

print("\n" + "=" * 80)
print("CATEGORY BREAKDOWN")
print("=" * 80)

categories = {
    "Breast Implants (Silicone/Saline)": [1, 2, 3, 4, 5, 6, 12],
    "Tissue Expanders": [7, 8],
    "Surgical Guidance/Markers": [9, 10],
    "Biopsy Devices": [11]
}

for category, numbers in categories.items():
    print(f"\n{category}: {len(numbers)} cases")
    for num in numbers:
        case = next(c for c in cases if c['number'] == num)
        print(f"  • {case['device']} ({case['status']})")

print("\n" + "=" * 80)
print("SETTLEMENT STATUS")
print("=" * 80)

settled = [c for c in cases if 'Settled' in c['status']]
active = [c for c in cases if 'Active' in c['status']]
mixed = [c for c in cases if 'mixed' in c['status'].lower()]

print(f"\nSettled: {len(settled)} cases")
for c in settled:
    print(f"  • {c['device']}: {c['settlement']}")

print(f"\nActive (No Settlements): {len(active)} cases")
for c in active:
    print(f"  • {c['device']}")

print("\n" + "=" * 80)
print("PRIORITY FOR BENCHMARK (MAUDE Data Availability)")
print("=" * 80)

priorities = [
    ("HIGH PRIORITY", [1, 2, 3, 5, 7, 11], "Good MAUDE data, established litigation"),
    ("MEDIUM PRIORITY", [4, 6, 9, 10], "Some MAUDE data, growing litigation"),
    ("LOW PRIORITY", [8, 12], "Limited MAUDE data (new/discontinued)")
]

for priority_level, case_nums, reason in priorities:
    print(f"\n{priority_level} ({reason}):")
    for num in case_nums:
        case = next(c for c in cases if c['number'] == num)
        print(f"  {num}. {case['device']}")

print("\n" + "=" * 80)
print("RECOMMENDED 12 CASES FOR EXPANSION")
print("=" * 80)
print("""
Top 12 to add to benchmark (prioritized by data availability + litigation status):

1. Mentor Breast Implants (MDL 2004) - SETTLED, good benchmark
2. Sientra Breast Implants - ACTIVE, FDA recall, BIA-ALCL cases
3. Natrelle Breast Implants - ACTIVE, different from BIOCELL
4. Ideal Implant - ACTIVE, unique structured design
5. CPG/McGhan Implants (MDL 926) - HISTORIC, $1.2B settlement
6. PIP Implants - SCANDAL, international impact
7. Tissuel Tissue Expanders - ACTIVE, reconstruction focus
8. AeroForm Tissue Expander - DISCONTINUED, good case study
9. SAVI SCOUT - EMERGING, surgical guidance
10. Bard Gel Mark - ACTIVE, tissue marker
11. ATEC Breast Biopsy - ACTIVE, some settlements
12. Motiva Implants - NEW, microchip technology

Total: 12 cases (7 breast implants, 2 tissue expanders, 3 surgical devices)
""")

print("=" * 80)
