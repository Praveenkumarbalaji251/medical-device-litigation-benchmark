#!/usr/bin/env python3
"""
Smart case selection tool for building a 50-case medical device benchmark.
"""

import pandas as pd
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

def create_case_selection_framework():
    """Create framework for selecting 50 representative medical device cases."""
    
    print("🎯 Medical Device Case Benchmark - 50 Case Selection Framework")
    print("=" * 70)
    
    # Define target case distribution
    target_distribution = {
        'Philips CPAP': {
            'total': 15,
            'subcategories': {
                'Mild complications (sleep disruption)': 5,
                'Moderate complications (respiratory issues)': 5, 
                'Severe complications (cancer, pneumonia)': 5
            },
            'search_terms': ['Philips CPAP', 'Philips BiPAP', 'Philips DreamStation']
        },
        'Hernia Mesh': {
            'total': 15,
            'subcategories': {
                'Infection/erosion cases': 5,
                'Revision surgery required': 5,
                'Chronic pain cases': 5
            },
            'search_terms': ['hernia mesh', 'surgical mesh', 'mesh erosion']
        },
        'Hip/Knee Replacement': {
            'total': 10,
            'subcategories': {
                'DePuy hip replacement': 5,
                'Other manufacturer failures': 5
            },
            'search_terms': ['DePuy hip', 'hip replacement', 'knee replacement']
        },
        'Other Medical Devices': {
            'total': 10,
            'subcategories': {
                'IVC filter complications': 3,
                'Pacemaker/defibrillator issues': 3,
                'Breast implant problems': 2,
                'Spinal hardware failures': 2
            },
            'search_terms': ['IVC filter', 'pacemaker', 'breast implant', 'spinal fusion']
        }
    }
    
    print("\n📊 TARGET CASE DISTRIBUTION:")
    print("-" * 50)
    
    total_cases = 0
    for category, info in target_distribution.items():
        print(f"\n{category}: {info['total']} cases")
        for subcat, count in info['subcategories'].items():
            print(f"  • {subcat}: {count}")
        total_cases += info['total']
    
    print(f"\nTOTAL TARGET: {total_cases} cases")
    
    # Create case tracking template
    case_template = create_case_tracking_template()
    
    # Save framework
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    framework_file = f"data/raw/case_selection_framework_{timestamp}.json"
    
    import json
    with open(framework_file, 'w') as f:
        json.dump(target_distribution, f, indent=2)
    
    template_file = f"data/raw/case_tracking_template_{timestamp}.csv"
    case_template.to_csv(template_file, index=False)
    
    print(f"\n💾 FILES CREATED:")
    print(f"   • Framework: {framework_file}")
    print(f"   • Tracking template: {template_file}")
    
    print(f"\n🎯 NEXT STEPS:")
    print(f"1. Use CourtListener to find cases for each category")
    print(f"2. Fill in the tracking template as you research each case")
    print(f"3. Focus on cases from last 3-5 years for relevance")
    print(f"4. Prioritize cases with known outcomes (settlements)")
    print(f"5. Include mix of federal districts for geographic diversity")
    
    return target_distribution

def create_case_tracking_template():
    """Create CSV template for tracking the 50 selected cases."""
    
    columns = [
        # Basic Case Info
        'case_id', 'case_name', 'docket_number', 'court', 'filing_date',
        
        # Device Information  
        'device_category', 'device_manufacturer', 'device_model',
        'complication_type', 'severity_level',
        
        # Legal Information
        'plaintiff_attorney', 'defense_attorney', 'judge_assigned',
        'case_type', 'mdl_status', 'class_action_status',
        
        # Timeline
        'discovery_start', 'discovery_end', 'trial_date', 'resolution_date',
        'total_duration_months',
        
        # Outcomes
        'case_status', 'resolution_type', 'settlement_amount',
        'attorney_fee_percent', 'case_expenses', 'net_recovery',
        
        # Strategic Info
        'key_expert_witnesses', 'critical_motions', 'appellate_history',
        'precedent_value', 'notes',
        
        # Quality Metrics
        'data_quality_score', 'source_reliability', 'verification_status'
    ]
    
    # Create empty template with example row
    template_data = {col: [''] for col in columns}
    
    # Add example case
    example_case = {
        'case_id': 'EXAMPLE_001',
        'case_name': 'Smith v. Philips Healthcare Inc.',
        'docket_number': '1:21-cv-12345',
        'court': 'District Court, S.D. New York',
        'filing_date': '2021-03-15',
        'device_category': 'Philips CPAP',
        'device_manufacturer': 'Philips Healthcare',
        'device_model': 'DreamStation',
        'complication_type': 'Foam degradation causing respiratory issues',
        'severity_level': 'Moderate',
        'case_status': 'Settled',
        'resolution_type': 'Confidential Settlement', 
        'settlement_amount': '$275000',
        'attorney_fee_percent': '33',
        'total_duration_months': '18',
        'notes': 'Good benchmark case - clear causation, moderate damages'
    }
    
    for col in columns:
        if col in example_case:
            template_data[col][0] = example_case[col]
    
    return pd.DataFrame(template_data)

def generate_search_strategy():
    """Generate specific search strategy for finding 50 cases."""
    
    strategy = {
        'Phase 1 - Recent High-Value Cases (Weeks 1-2)': [
            'Search "Philips CPAP settlement" for 2021-2025 cases',
            'Focus on cases with known settlement amounts',
            'Target federal courts in major districts (SDNY, CD Cal, etc.)'
        ],
        'Phase 2 - MDL and Class Actions (Weeks 3-4)': [
            'Review major MDL proceedings for medical devices',
            'Identify bellwether trials with outcomes',
            'Collect representative cases from different MDLs'
        ],
        'Phase 3 - Geographic and Temporal Diversity (Weeks 5-6)': [
            'Ensure cases from multiple federal districts',
            'Include cases from 2020-2025 timeframe',
            'Balance settled vs. ongoing cases'
        ],
        'Phase 4 - Validation and Analysis (Weeks 7-8)': [
            'Verify case details with PACER if needed',
            'Cross-reference with legal news sources',
            'Calculate preliminary benchmarks'
        ]
    }
    
    print(f"\n📋 8-WEEK CASE COLLECTION STRATEGY:")
    print("-" * 50)
    
    for phase, tasks in strategy.items():
        print(f"\n{phase}:")
        for task in tasks:
            print(f"  • {task}")
    
    return strategy

if __name__ == "__main__":
    framework = create_case_selection_framework()
    strategy = generate_search_strategy()
    
    print(f"\n🚀 READY TO START!")
    print(f"You now have a systematic approach to build your 50-case benchmark.")
    print(f"This will give you a competitive advantage in medical device litigation!")