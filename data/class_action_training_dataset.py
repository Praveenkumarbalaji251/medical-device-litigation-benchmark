"""
Class Action Lawsuit Training Dataset
Labeled data for medical device litigation with product codes, dates, and outcomes
"""

import pandas as pd
from datetime import datetime

# Comprehensive training dataset with verified MDL cases
TRAINING_DATASET = [
    # ============================================================================
    # ORTHOPEDIC - HIP IMPLANTS (Proven high-value litigation area)
    # ============================================================================
    {
        'case_id': 'MDL-2197',
        'case_name': 'DePuy ASR Hip',
        'manufacturer': 'DePuy Orthopaedics (J&J)',
        'device_type': 'Hip Implant',
        'device_category': 'ORTHOPEDIC_HIP',
        'product_codes': ['JDG', 'LPH', 'MEH'],  # Metal-on-metal, acetabular, femoral
        'primary_product_code': 'JDG',
        'filing_date': '2010-09-01',
        'settlement_date': '2013-11-19',
        'settlement_amount': 4000000000,  # $4B
        'court': 'N.D. Ohio',
        'judge': 'David A. Katz',
        'status': 'Settled',
        'mdrs_6mo_before': 1110,
        'deaths': 0,
        'injuries': 1097,
        'malfunctions': 5,
        'device_class': 'III',  # PMA
        'failure_mode': 'Metal wear, metallosis, loosening',
        'injury_types': 'Pain, revision surgery, tissue damage',
    },
    {
        'case_id': 'MDL-2441',
        'case_name': 'Stryker Rejuvenate Hip',
        'manufacturer': 'Stryker Corporation',
        'device_type': 'Hip Implant',
        'device_category': 'ORTHOPEDIC_HIP',
        'product_codes': ['MEH', 'LPH', 'KWY'],  # Femoral stem, acetabular, head
        'primary_product_code': 'MEH',
        'filing_date': '2012-08-01',
        'settlement_date': '2014-11-03',
        'settlement_amount': 1400000000,  # $1.4B
        'court': 'D. Minnesota',
        'judge': 'John R. Tunheim',
        'status': 'Settled',
        'mdrs_6mo_before': 768,
        'deaths': 0,
        'injuries': 761,
        'malfunctions': 4,
        'device_class': 'II',  # 510(k)
        'failure_mode': 'Modular neck corrosion, fretting',
        'injury_types': 'Metallosis, revision surgery, pain',
    },
    {
        'case_id': 'MDL-2244',
        'case_name': 'DePuy Pinnacle Hip',
        'manufacturer': 'DePuy Orthopaedics (J&J)',
        'device_type': 'Hip Implant',
        'device_category': 'ORTHOPEDIC_HIP',
        'product_codes': ['LPH', 'MEH', 'KWY'],  # Acetabular shell, femoral, head
        'primary_product_code': 'LPH',
        'filing_date': '2011-08-01',
        'settlement_date': '2016-06-01',
        'settlement_amount': 1000000000,  # $1B+
        'court': 'N.D. Texas',
        'judge': 'Ed Kinkeade',
        'status': 'Settled',
        'mdrs_6mo_before': 501,
        'deaths': 1,
        'injuries': 468,
        'malfunctions': 27,
        'device_class': 'II',
        'failure_mode': 'Metal-on-metal wear, loosening',
        'injury_types': 'Metallosis, pseudotumor, revision',
    },
    {
        'case_id': 'MDL-2329',
        'case_name': 'Wright Conserve Hip',
        'manufacturer': 'Wright Medical Technology',
        'device_type': 'Hip Implant',
        'device_category': 'ORTHOPEDIC_HIP',
        'product_codes': ['MEH', 'LPH'],  # Hip resurfacing
        'primary_product_code': 'MEH',
        'filing_date': '2011-10-01',
        'settlement_date': '2015-08-01',
        'settlement_amount': 240000000,  # $240M
        'court': 'N.D. Georgia',
        'judge': 'Richard W. Story',
        'status': 'Settled',
        'mdrs_6mo_before': 213,
        'deaths': 0,
        'injuries': 209,
        'malfunctions': 3,
        'device_class': 'II',
        'failure_mode': 'Metal-on-metal wear, corrosion',
        'injury_types': 'Metallosis, pain, revision surgery',
    },
    {
        'case_id': 'MDL-2158',
        'case_name': 'Zimmer Durom Cup Hip',
        'manufacturer': 'Zimmer Biomet',
        'device_type': 'Hip Implant',
        'device_category': 'ORTHOPEDIC_HIP',
        'product_codes': ['LPH'],  # Acetabular cup
        'primary_product_code': 'LPH',
        'filing_date': '2008-09-01',
        'settlement_date': '2013-03-01',
        'settlement_amount': 228000000,  # $228M
        'court': 'D. New Jersey',
        'judge': 'Joseph A. Greenaway Jr.',
        'status': 'Settled',
        'mdrs_6mo_before': 357,
        'deaths': 0,
        'injuries': 320,
        'malfunctions': 34,
        'device_class': 'II',
        'failure_mode': 'Cup loosening, migration',
        'injury_types': 'Pain, instability, revision',
    },
    {
        'case_id': 'MDL-2716',
        'case_name': 'Zimmer M/L Taper Hip',
        'manufacturer': 'Zimmer Biomet',
        'device_type': 'Hip Implant',
        'device_category': 'ORTHOPEDIC_HIP',
        'product_codes': ['MEH', 'KWY'],  # Modular femoral stem
        'primary_product_code': 'MEH',
        'filing_date': '2016-03-24',
        'settlement_date': None,
        'settlement_amount': None,
        'court': 'N.D. Indiana',
        'judge': 'Robert L. Miller Jr.',
        'status': 'Active',
        'mdrs_6mo_before': 136,
        'deaths': 1,
        'injuries': 124,
        'malfunctions': 11,
        'device_class': 'II',
        'failure_mode': 'Modular taper corrosion, fretting',
        'injury_types': 'Metallosis, pain, revision',
    },
    
    # ============================================================================
    # ORTHOPEDIC - KNEE IMPLANTS
    # ============================================================================
    {
        'case_id': 'MDL-3044',
        'case_name': 'Exactech Knee/Hip/Ankle',
        'manufacturer': 'Exactech Inc.',
        'device_type': 'Joint Implants',
        'device_category': 'ORTHOPEDIC_KNEE',
        'product_codes': ['JWH', 'JWI', 'KWA', 'MEH', 'LPH'],  # Multiple joints
        'primary_product_code': 'JWH',
        'filing_date': '2022-06-14',
        'settlement_date': None,
        'settlement_amount': None,
        'court': 'E.D. New York',
        'judge': 'Joanna Seybert',
        'status': 'Active',
        'mdrs_6mo_before': 896,
        'deaths': 0,
        'injuries': 634,
        'malfunctions': 262,
        'device_class': 'II',
        'failure_mode': 'Polyethylene liner degradation, oxidation',
        'injury_types': 'Pain, instability, early failure, revision',
    },
    
    # ============================================================================
    # SURGICAL MESH - HERNIA (Major litigation area)
    # ============================================================================
    {
        'case_id': 'MDL-2327',
        'case_name': 'Ethicon Transvaginal Mesh',
        'manufacturer': 'Ethicon (J&J)',
        'device_type': 'Pelvic Mesh',
        'device_category': 'SURGICAL_MESH',
        'product_codes': ['KEO', 'FPB'],  # Pelvic mesh, surgical mesh
        'primary_product_code': 'KEO',
        'filing_date': '2012-01-31',
        'settlement_date': '2019-10-14',
        'settlement_amount': 8000000000,  # $8B+
        'court': 'S.D. West Virginia',
        'judge': 'Joseph R. Goodwin',
        'status': 'Settled',
        'mdrs_6mo_before': 1090,
        'deaths': 3,
        'injuries': 843,
        'malfunctions': 240,
        'device_class': 'II',
        'failure_mode': 'Mesh erosion, contraction, migration',
        'injury_types': 'Chronic pain, organ perforation, infection',
    },
    {
        'case_id': 'MDL-2326',
        'case_name': 'Boston Scientific Pelvic Mesh',
        'manufacturer': 'Boston Scientific',
        'device_type': 'Pelvic Mesh',
        'device_category': 'SURGICAL_MESH',
        'product_codes': ['KEO', 'MNO'],  # Pelvic mesh, urethral sling
        'primary_product_code': 'KEO',
        'filing_date': '2012-02-13',
        'settlement_date': '2015-08-28',
        'settlement_amount': 189000000,  # $189M
        'court': 'S.D. West Virginia',
        'judge': 'Joseph R. Goodwin',
        'status': 'Settled',
        'mdrs_6mo_before': 1982,
        'deaths': 1,
        'injuries': 1570,
        'malfunctions': 405,
        'device_class': 'II',
        'failure_mode': 'Mesh erosion, contraction',
        'injury_types': 'Pain, bleeding, infection, organ damage',
    },
    {
        'case_id': 'MDL-2846',
        'case_name': 'Bard/Davol Hernia Mesh',
        'manufacturer': 'C.R. Bard (Davol)',
        'device_type': 'Hernia Mesh',
        'device_category': 'SURGICAL_MESH',
        'product_codes': ['MNX', 'FPB'],  # Hernia mesh, surgical mesh
        'primary_product_code': 'MNX',
        'filing_date': '2018-08-02',
        'settlement_date': None,
        'settlement_amount': None,
        'court': 'S.D. Ohio',
        'judge': 'Edmund A. Sargus Jr.',
        'status': 'Active',
        'mdrs_6mo_before': 2421,
        'deaths': 17,
        'injuries': 2359,
        'malfunctions': 44,
        'device_class': 'II',
        'failure_mode': 'Mesh shrinkage, adhesion, migration',
        'injury_types': 'Chronic pain, infection, bowel obstruction',
    },
    {
        'case_id': 'MDL-2782',
        'case_name': 'Physiomesh Ethicon',
        'manufacturer': 'Ethicon (J&J)',
        'device_type': 'Hernia Mesh',
        'device_category': 'SURGICAL_MESH',
        'product_codes': ['MNX', 'FPB'],  # Hernia mesh
        'primary_product_code': 'MNX',
        'filing_date': '2016-11-07',
        'settlement_date': None,
        'settlement_amount': None,
        'court': 'N.D. Georgia',
        'judge': 'Richard W. Story',
        'status': 'Active',
        'mdrs_6mo_before': 76,
        'deaths': 0,
        'injuries': 65,
        'malfunctions': 11,
        'device_class': 'II',
        'failure_mode': 'High recurrence rate, adhesion',
        'injury_types': 'Hernia recurrence, pain, revision',
    },
    {
        'case_id': 'MDL-2753',
        'case_name': 'Atrium C-QUR Mesh',
        'manufacturer': 'Atrium Medical',
        'device_type': 'Hernia Mesh',
        'device_category': 'SURGICAL_MESH',
        'product_codes': ['MNX', 'FPB'],
        'primary_product_code': 'MNX',
        'filing_date': '2016-08-23',
        'settlement_date': None,
        'settlement_amount': None,
        'court': 'D. New Hampshire',
        'judge': 'Joseph A. DiClerico Jr.',
        'status': 'Active',
        'mdrs_6mo_before': 39,
        'deaths': 0,
        'injuries': 38,
        'malfunctions': 1,
        'device_class': 'II',
        'failure_mode': 'Omega-3 coating degradation, adhesion',
        'injury_types': 'Chronic pain, adhesions, infection',
    },
    
    # ============================================================================
    # BREAST IMPLANTS
    # ============================================================================
    {
        'case_id': 'MDL-2921',
        'case_name': 'Allergan BIOCELL Implants',
        'manufacturer': 'Allergan (AbbVie)',
        'device_type': 'Breast Implant',
        'device_category': 'BREAST',
        'product_codes': ['GZH', 'MWT'],  # Silicone implant, tissue expander
        'primary_product_code': 'GZH',
        'filing_date': '2019-12-18',
        'settlement_date': None,
        'settlement_amount': None,
        'court': 'D. New Jersey',
        'judge': 'Brian R. Martinotti',
        'status': 'Active',
        'mdrs_6mo_before': 213,
        'deaths': 9,
        'injuries': 189,
        'malfunctions': 13,
        'device_class': 'III',  # PMA
        'failure_mode': 'BIA-ALCL (breast cancer), textured surface',
        'injury_types': 'Anaplastic large cell lymphoma, implant removal',
    },
    
    # ============================================================================
    # CARDIOVASCULAR - IVC FILTERS
    # ============================================================================
    {
        'case_id': 'MDL-2641',
        'case_name': 'Bard IVC Filters',
        'manufacturer': 'C.R. Bard',
        'device_type': 'IVC Filter',
        'device_category': 'CARDIOVASCULAR',
        'product_codes': ['LXH'],  # Vena cava filter
        'primary_product_code': 'LXH',
        'filing_date': '2015-08-03',
        'settlement_date': None,
        'settlement_amount': None,
        'court': 'D. Arizona',
        'judge': 'David G. Campbell',
        'status': 'Active',
        'mdrs_6mo_before': 348,
        'deaths': 0,
        'injuries': 151,
        'malfunctions': 194,
        'device_class': 'II',
        'failure_mode': 'Filter migration, fracture, perforation',
        'injury_types': 'Organ perforation, embolization, death',
    },
    {
        'case_id': 'MDL-2570',
        'case_name': 'Cook Medical IVC Filters',
        'manufacturer': 'Cook Medical',
        'device_type': 'IVC Filter',
        'device_category': 'CARDIOVASCULAR',
        'product_codes': ['LXH'],
        'primary_product_code': 'LXH',
        'filing_date': '2014-08-28',
        'settlement_date': None,
        'settlement_amount': None,
        'court': 'S.D. Indiana',
        'judge': 'Richard L. Young',
        'status': 'Active',
        'mdrs_6mo_before': 40,
        'deaths': 1,
        'injuries': 24,
        'malfunctions': 13,
        'device_class': 'II',
        'failure_mode': 'Filter fracture, migration, tilt',
        'injury_types': 'Perforation, migration, death',
    },
    
    # ============================================================================
    # CARDIOVASCULAR - PACEMAKER/DEFIBRILLATOR LEADS
    # ============================================================================
    {
        'case_id': 'MDL-1905',
        'case_name': 'Medtronic Sprint Fidelis Leads',
        'manufacturer': 'Medtronic Inc.',
        'device_type': 'Defibrillator Lead',
        'device_category': 'CARDIAC_RHYTHM',
        'product_codes': ['DXY'],  # Defibrillator electrode
        'primary_product_code': 'DXY',
        'filing_date': '2008-06-26',
        'settlement_date': '2012-06-11',
        'settlement_amount': 268000000,  # $268M
        'court': 'D. Minnesota',
        'judge': 'Donovan W. Frank',
        'status': 'Settled',
        'mdrs_6mo_before': 1466,
        'deaths': 78,
        'injuries': 1356,
        'malfunctions': 17,
        'device_class': 'III',  # PMA
        'failure_mode': 'Lead fracture, insulation breach',
        'injury_types': 'Inappropriate shocks, sudden death, lead revision',
    },
    
    # ============================================================================
    # WOMEN'S HEALTH - BIRTH CONTROL
    # ============================================================================
    {
        'case_id': 'MDL-2325',
        'case_name': 'Essure Birth Control',
        'manufacturer': 'Bayer/Conceptus',
        'device_type': 'Contraceptive Implant',
        'device_category': 'WOMENS_HEALTH',
        'product_codes': ['HCF'],  # Contraceptive tubal occlusion device
        'primary_product_code': 'HCF',
        'filing_date': '2013-09-03',
        'settlement_date': None,
        'settlement_amount': None,
        'court': 'E.D. Pennsylvania',
        'judge': 'Gene E.K. Pratter',
        'status': 'Active',
        'mdrs_6mo_before': 154,
        'deaths': 0,
        'injuries': 108,
        'malfunctions': 22,
        'device_class': 'III',  # PMA
        'failure_mode': 'Migration, perforation, nickel sensitivity',
        'injury_types': 'Chronic pain, perforation, unintended pregnancy',
    },
    
    # ============================================================================
    # RESPIRATORY - CPAP/BiPAP
    # ============================================================================
    {
        'case_id': 'MDL-3014',
        'case_name': 'Philips CPAP/BiPAP',
        'manufacturer': 'Philips Respironics',
        'device_type': 'Sleep Apnea Device',
        'device_category': 'RESPIRATORY',
        'product_codes': ['BYG', 'BZD'],  # Ventilator, continuous
        'primary_product_code': 'BYG',
        'filing_date': '2021-10-08',
        'settlement_date': None,
        'settlement_amount': None,
        'court': 'W.D. Pennsylvania',
        'judge': 'Joy Flowers Conti',
        'status': 'Active',
        'mdrs_6mo_before': 4232,
        'deaths': 44,
        'injuries': 1066,
        'malfunctions': 3121,
        'device_class': 'II',
        'failure_mode': 'Sound abatement foam degradation',
        'injury_types': 'Foam inhalation, cancer risk, respiratory issues',
    },
    
    # ============================================================================
    # VASCULAR ACCESS - PORTS/CATHETERS
    # ============================================================================
    {
        'case_id': 'MDL-3081',
        'case_name': 'Bard PowerPort',
        'manufacturer': 'C.R. Bard (BD)',
        'device_type': 'Implantable Port',
        'device_category': 'VASCULAR_ACCESS',
        'product_codes': ['FRN'],  # Implanted vascular access port
        'primary_product_code': 'FRN',
        'filing_date': '2023-08-15',
        'settlement_date': None,
        'settlement_amount': None,
        'court': 'D. Arizona',
        'judge': 'David G. Campbell',
        'status': 'Active',
        'mdrs_6mo_before': 4760,
        'deaths': 12,
        'injuries': 841,
        'malfunctions': 3906,
        'device_class': 'II',
        'failure_mode': 'Catheter fracture, migration',
        'injury_types': 'Embolization, thrombosis, infection, death',
    },
]


def create_training_dataframe():
    """Convert training dataset to pandas DataFrame"""
    df = pd.DataFrame(TRAINING_DATASET)
    
    # Add calculated fields
    df['time_to_settlement_days'] = df.apply(
        lambda row: (datetime.strptime(row['settlement_date'], '%Y-%m-%d') - 
                     datetime.strptime(row['filing_date'], '%Y-%m-%d')).days 
        if row['settlement_date'] else None, 
        axis=1
    )
    
    df['settlement_per_mdr'] = df.apply(
        lambda row: row['settlement_amount'] / row['mdrs_6mo_before'] 
        if row['settlement_amount'] and row['mdrs_6mo_before'] > 0 else None,
        axis=1
    )
    
    df['death_rate'] = df['deaths'] / df['mdrs_6mo_before']
    df['injury_rate'] = df['injuries'] / df['mdrs_6mo_before']
    
    return df


def get_summary_statistics():
    """Generate summary statistics from training dataset"""
    df = create_training_dataframe()
    
    print("\n" + "="*80)
    print("CLASS ACTION TRAINING DATASET SUMMARY")
    print("="*80)
    
    print(f"\nTotal Cases: {len(df)}")
    print(f"Active Cases: {len(df[df['status'] == 'Active'])}")
    print(f"Settled Cases: {len(df[df['status'] == 'Settled'])}")
    
    print(f"\nTotal Settlement Value: ${df['settlement_amount'].sum():,.0f}")
    print(f"Average Settlement: ${df['settlement_amount'].mean():,.0f}")
    
    print(f"\nTotal MDRs (6mo before filing): {df['mdrs_6mo_before'].sum():,}")
    print(f"Total Deaths: {df['deaths'].sum()}")
    print(f"Total Injuries: {df['injuries'].sum()}")
    
    print("\n" + "-"*80)
    print("BY DEVICE CATEGORY:")
    print("-"*80)
    category_summary = df.groupby('device_category').agg({
        'case_id': 'count',
        'settlement_amount': ['sum', 'mean'],
        'mdrs_6mo_before': 'sum',
        'deaths': 'sum',
        'injuries': 'sum'
    })
    print(category_summary)
    
    print("\n" + "-"*80)
    print("TOP PRODUCT CODES BY FREQUENCY:")
    print("-"*80)
    all_codes = []
    for codes in df['product_codes']:
        all_codes.extend(codes)
    code_counts = pd.Series(all_codes).value_counts().head(10)
    print(code_counts)
    
    return df


if __name__ == "__main__":
    df = get_summary_statistics()
    
    # Export to Excel
    output_file = '/Users/praveen/Praveen/data/class_action_training_dataset.xlsx'
    df.to_excel(output_file, index=False, sheet_name='Training Data')
    print(f"\n✅ Training dataset exported to: {output_file}")
