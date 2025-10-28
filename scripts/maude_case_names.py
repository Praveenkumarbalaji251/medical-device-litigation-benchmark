"""
Medical Device Case Names for MAUDE Database Cross-Reference
Clean list of device names and manufacturers for FDA MAUDE comparison
"""

# MEDICAL DEVICE CASE NAMES FOR MAUDE COMPARISON
MEDICAL_DEVICE_CASES_FOR_MAUDE = {
    
    # Current Major Cases (2020-2025)
    "current_major_litigation": [
        "Philips DreamStation CPAP",
        "Philips BiPAP", 
        "Philips CPAP Foam Degradation",
        "Ethicon Hernia Mesh",
        "Atrium Hernia Mesh",
        "Bard Hernia Mesh", 
        "Boston Scientific Hernia Mesh",
        "Exactech Knee Replacement",
        "Exactech Hip Replacement",
        "Teleflex UroLift",
        "Abbott FreeStyle Libre",
        "Zimmer Biomet Comprehensive Knee",
        "Medtronic MiniMed Insulin Pump"
    ],
    
    # Historic Major Cases (Settled/Resolved)
    "historic_major_cases": [
        "Johnson & Johnson Transvaginal Mesh",
        "Ethicon Transvaginal Mesh",
        "DePuy ASR Hip Replacement",
        "DePuy Pinnacle Hip Replacement", 
        "Bayer Essure Sterilization Device",
        "3M Combat Arms Earplugs",
        "Sulzer Hip Prosthesis",
        "Guidant Pacemaker",
        "Guidant Defibrillator",
        "Medtronic Infuse Bone Graft",
        "Boston Scientific Guidant Defibrillator"
    ],
    
    # Emerging Cases (Watch List)
    "emerging_litigation": [
        "Zimmer Biomet Comprehensive Knee",
        "Abbott FreeStyle Libre CGM", 
        "Medtronic MiniMed 670G",
        "Teleflex UroLift System",
        "da Vinci Surgical Robot",
        "Intuitive Surgical da Vinci"
    ]
}

# EXACT DEVICE MODEL NAMES FOR PRECISE MAUDE SEARCH
EXACT_DEVICE_MODELS = {
    "Philips CPAP Devices": [
        "DreamStation Auto CPAP",
        "DreamStation Go Auto CPAP", 
        "DreamStation BiPAP Auto",
        "DreamStation BiPAP S/T",
        "SystemOne REMstar Auto CPAP",
        "SystemOne BiPAP AutoSV Advanced"
    ],
    
    "DePuy Hip Implants": [
        "ASR XL Acetabular System",
        "ASR Hip Resurfacing System",
        "Pinnacle Acetabular Cup System",
        "Pinnacle Hip Solutions"
    ],
    
    "Hernia Mesh Products": [
        "Ethicon Physiomesh",
        "Ethicon Proceed Mesh", 
        "Atrium C-QUR Mesh",
        "Bard Composix Kugel Mesh",
        "Bard 3DMax Mesh",
        "Boston Scientific ProGrip Mesh"
    ],
    
    "Exactech Orthopedic Implants": [
        "Exactech Optetrak Comprehensive Knee",
        "Exactech Novation Hip System",
        "Exactech Acumatch Hip System"
    ],
    
    "Cardiac Devices": [
        "Guidant PRIZM 2 DR Defibrillator",
        "Guidant Vitality 2 Pacemaker",
        "Boston Scientific COGNIS Defibrillator"
    ]
}

# MANUFACTURER NAMES FOR MAUDE SEARCH
DEVICE_MANUFACTURERS = [
    "Philips Healthcare",
    "Johnson & Johnson", 
    "Ethicon Inc",
    "DePuy Synthes",
    "Bayer Healthcare",
    "3M Company",
    "Exactech Inc",
    "Abbott Laboratories", 
    "Medtronic Inc",
    "Boston Scientific",
    "Zimmer Biomet",
    "Teleflex Inc",
    "Atrium Medical Corporation",
    "C.R. Bard Inc"
]

# SIMPLE LIST FOR EASY COPY-PASTE
CASE_NAMES_SIMPLE_LIST = [
    # CURRENT HOT CASES
    "Philips CPAP",
    "Philips BiPAP", 
    "Hernia Mesh",
    "Exactech Knee Replacement",
    "Exactech Hip Replacement",
    
    # HISTORIC BIG CASES  
    "DePuy Hip Replacement",
    "Johnson & Johnson Mesh",
    "Bayer Essure",
    "3M Combat Earplugs",
    "Guidant Pacemaker",
    
    # EMERGING CASES
    "Abbott FreeStyle Libre",
    "Medtronic Insulin Pump",
    "Teleflex UroLift", 
    "da Vinci Robot"
]

def export_case_names_for_maude():
    """Export clean case names for MAUDE database comparison."""
    
    print("📋 MEDICAL DEVICE CASE NAMES FOR MAUDE COMPARISON")
    print("=" * 55)
    
    print("\n🔥 CURRENT MAJOR LITIGATION (2020-2025):")
    print("-" * 45)
    for i, case in enumerate(MEDICAL_DEVICE_CASES_FOR_MAUDE["current_major_litigation"], 1):
        print(f"{i:2d}. {case}")
    
    print("\n🏛️  HISTORIC MAJOR CASES (Settled):")
    print("-" * 35)
    for i, case in enumerate(MEDICAL_DEVICE_CASES_FOR_MAUDE["historic_major_cases"], 1):
        print(f"{i:2d}. {case}")
    
    print("\n📈 EMERGING LITIGATION (Watch List):")
    print("-" * 38)
    for i, case in enumerate(MEDICAL_DEVICE_CASES_FOR_MAUDE["emerging_litigation"], 1):
        print(f"{i:2d}. {case}")
    
    print("\n📊 EXACT DEVICE MODEL NAMES (For Precise MAUDE Search):")
    print("-" * 55)
    for category, models in EXACT_DEVICE_MODELS.items():
        print(f"\n{category}:")
        for model in models:
            print(f"  • {model}")
    
    print(f"\n🏭 MANUFACTURER NAMES:")
    print("-" * 20)
    for manufacturer in DEVICE_MANUFACTURERS:
        print(f"• {manufacturer}")
    
    print(f"\n📝 SIMPLE COPY-PASTE LIST:")
    print("-" * 25)
    for case in CASE_NAMES_SIMPLE_LIST:
        print(case)
    
    # Save to file for easy access
    with open('data/raw/maude_device_names.txt', 'w') as f:
        f.write("MEDICAL DEVICE NAMES FOR MAUDE COMPARISON\n")
        f.write("=" * 45 + "\n\n")
        
        f.write("CURRENT MAJOR LITIGATION:\n")
        for case in MEDICAL_DEVICE_CASES_FOR_MAUDE["current_major_litigation"]:
            f.write(f"{case}\n")
        
        f.write("\nHISTORIC MAJOR CASES:\n") 
        for case in MEDICAL_DEVICE_CASES_FOR_MAUDE["historic_major_cases"]:
            f.write(f"{case}\n")
        
        f.write("\nEMERGING LITIGATION:\n")
        for case in MEDICAL_DEVICE_CASES_FOR_MAUDE["emerging_litigation"]:
            f.write(f"{case}\n")
    
    print(f"\n💾 Device names saved to: data/raw/maude_device_names.txt")
    
    return CASE_NAMES_SIMPLE_LIST

if __name__ == "__main__":
    case_list = export_case_names_for_maude()