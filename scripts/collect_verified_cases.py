#!/usr/bin/env python3
"""
Best practice medical device case collection with validation.
"""

import sys
from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from data_collection.multi_source_collector import MultiSourceCollector, get_data_collection_strategy
from data_collection.data_validator import LegalDataValidator, create_data_quality_report

def collect_verified_medical_device_cases():
    """
    Collect medical device cases using best practices for accuracy.
    """
    print("🏛️  Medical Device Legal Case Collection - Best Practices")
    print("=" * 65)
    
    # Show recommended strategy
    strategy = get_data_collection_strategy()
    print("\n📋 RECOMMENDED DATA COLLECTION STRATEGY:")
    print("-" * 45)
    
    print("\n🥇 Primary Sources:")
    for source, info in strategy['primary_sources'].items():
        print(f"   {info['priority']}. {source.title()}")
        print(f"      ✅ {info['reason']}")
        print(f"      ⚠️  {info['limitations']}")
    
    print(f"\n🔍 Verification Sources:")
    for source, desc in strategy['verification_sources'].items():
        print(f"   • {source.replace('_', ' ').title()}: {desc}")
    
    print(f"\n✅ Best Practices:")
    for practice in strategy['best_practices']:
        print(f"   • {practice}")
    
    print(f"\n" + "="*65)
    
    # Initialize collectors
    collector = MultiSourceCollector()
    validator = LegalDataValidator()
    
    # Define medical device search terms
    medical_device_terms = [
        "Philips CPAP",
        "hernia mesh", 
        "medical device class action",
        "IVC filter",
        "hip replacement lawsuit",
        "pacemaker recall"
    ]
    
    print(f"\n🔍 COLLECTING CASES...")
    print(f"Search terms: {medical_device_terms}")
    
    # Collect from multiple sources
    results = collector.collect_from_multiple_sources(
        search_terms=medical_device_terms,
        sources=['courtlistener'],  # Start with free source
        date_range=((datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d'), 
                   datetime.now().strftime('%Y-%m-%d'))
    )
    
    cases = results['merged_cases']
    print(f"\n📊 COLLECTION RESULTS:")
    print(f"   • Total unique cases found: {results['total_unique_cases']}")
    print(f"   • Source coverage: {results['source_coverage']}")
    
    if cases:
        # Convert to DataFrame for analysis
        cases_df = pd.DataFrame(cases)
        
        # Validate data quality
        quality_report = create_data_quality_report(cases_df)
        
        print(f"\n📈 DATA QUALITY ASSESSMENT:")
        print(f"   • Total cases: {quality_report['total_cases']}")
        print(f"   • High quality: {quality_report['high_quality_cases']} ({quality_report['high_quality_cases']/quality_report['total_cases']*100:.1f}%)")
        print(f"   • Medium quality: {quality_report['medium_quality_cases']} ({quality_report['medium_quality_cases']/quality_report['total_cases']*100:.1f}%)")
        print(f"   • Low quality: {quality_report['low_quality_cases']} ({quality_report['low_quality_cases']/quality_report['total_cases']*100:.1f}%)")
        print(f"   • Average confidence: {quality_report['average_confidence']:.1f}%")
        
        if quality_report['common_issues']:
            print(f"\n⚠️  COMMON DATA ISSUES:")
            for issue, count in list(quality_report['common_issues'].items())[:3]:
                print(f"   • {issue}: {count} cases")
        
        if quality_report['recommendations']:
            print(f"\n💡 RECOMMENDATIONS:")
            for rec in quality_report['recommendations']:
                print(f"   • {rec}")
        
        # Save results with quality scores
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"data/raw/verified_cases_{timestamp}.csv"
        cases_df.to_csv(output_file, index=False)
        
        # Save quality report
        quality_file = f"data/raw/quality_report_{timestamp}.json"
        import json
        with open(quality_file, 'w') as f:
            json.dump(quality_report, f, indent=2, default=str)
        
        print(f"\n💾 FILES SAVED:")
        print(f"   • Cases: {output_file}")
        print(f"   • Quality report: {quality_file}")
        
        # Show sample high-quality cases
        high_quality_cases = cases_df.head(5)
        print(f"\n📋 SAMPLE HIGH-QUALITY CASES:")
        print("-" * 80)
        for i, (_, case) in enumerate(high_quality_cases.iterrows(), 1):
            print(f"{i}. {case.get('caseName', 'Unknown')[:60]}")
            print(f"   Court: {case.get('court', 'Unknown')}")
            print(f"   Filed: {case.get('dateFiled', 'Unknown')}")
            print(f"   Docket: {case.get('docketNumber', 'Unknown')}")
            sources = case.get('sources', ['Unknown'])
            print(f"   Sources: {', '.join(sources)}")
            print()
    
    else:
        print(f"\n❌ No cases found. Try:")
        print(f"   • Different search terms")
        print(f"   • Broader date range") 
        print(f"   • API token for higher limits")
    
    print(f"\n🎯 NEXT STEPS FOR LEGAL PROFESSIONALS:")
    print(f"   1. Review high-quality cases manually")
    print(f"   2. Cross-reference important cases with PACER") 
    print(f"   3. Verify settlement amounts with news sources")
    print(f"   4. Create case tracking spreadsheet")
    print(f"   5. Set up alerts for new filings")

if __name__ == "__main__":
    collect_verified_medical_device_cases()