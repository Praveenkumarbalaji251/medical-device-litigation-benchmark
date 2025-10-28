"""
Data validation and quality assurance for legal case collection.
"""

import requests
import pandas as pd
from datetime import datetime
import re
import logging

class LegalDataValidator:
    """
    Validates and cross-references legal case data for accuracy.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def validate_case_data(self, case_data: dict) -> dict:
        """
        Validate individual case data for completeness and format.
        
        Args:
            case_data: Raw case data from API
            
        Returns:
            Validation results with confidence scores
        """
        validation_results = {
            'case_id': case_data.get('docket_id'),
            'case_name': case_data.get('caseName', ''),
            'confidence_score': 0,
            'validation_flags': [],
            'data_quality': 'Unknown'
        }
        
        # Check required fields
        required_fields = ['caseName', 'court', 'dateFiled', 'docketNumber']
        missing_fields = [field for field in required_fields if not case_data.get(field)]
        
        if missing_fields:
            validation_results['validation_flags'].append(f"Missing fields: {missing_fields}")
        else:
            validation_results['confidence_score'] += 25
        
        # Validate docket number format
        docket_num = case_data.get('docketNumber', '')
        if self._validate_docket_format(docket_num):
            validation_results['confidence_score'] += 25
        else:
            validation_results['validation_flags'].append("Invalid docket number format")
        
        # Validate date format
        file_date = case_data.get('dateFiled', '')
        if self._validate_date_format(file_date):
            validation_results['confidence_score'] += 25
        else:
            validation_results['validation_flags'].append("Invalid date format")
        
        # Check for medical device relevance
        if self._is_medical_device_related(case_data):
            validation_results['confidence_score'] += 25
            validation_results['validation_flags'].append("Confirmed medical device case")
        
        # Determine data quality level
        if validation_results['confidence_score'] >= 75:
            validation_results['data_quality'] = 'High'
        elif validation_results['confidence_score'] >= 50:
            validation_results['data_quality'] = 'Medium'
        else:
            validation_results['data_quality'] = 'Low'
        
        return validation_results
    
    def _validate_docket_format(self, docket_num: str) -> bool:
        """Validate federal court docket number format."""
        if not docket_num:
            return False
        
        # Common federal docket patterns
        patterns = [
            r'^\d+:\d{2}-cv-\d+',  # e.g., 1:20-cv-12345
            r'^\d+:\d{2}-md-\d+',  # MDL cases
            r'^\d+:\d{2}-cr-\d+',  # Criminal cases
            r'^\d+-\d+-\d+',       # Bankruptcy format
        ]
        
        return any(re.match(pattern, docket_num) for pattern in patterns)
    
    def _validate_date_format(self, date_str: str) -> bool:
        """Validate date format."""
        if not date_str:
            return False
        
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    
    def _is_medical_device_related(self, case_data: dict) -> bool:
        """Check if case is actually medical device related."""
        case_name = case_data.get('caseName', '').lower()
        nature = case_data.get('suitNature', '').lower()
        
        medical_device_terms = [
            'medical device', 'implant', 'pacemaker', 'defibrillator',
            'hip replacement', 'knee replacement', 'hernia mesh',
            'ivc filter', 'cpap', 'bipap', 'philips', 'insulin pump',
            'breast implant', 'surgical mesh', 'spinal fusion',
            'cochlear implant', 'stent', 'catheter'
        ]
        
        text_to_search = f"{case_name} {nature}"
        return any(term in text_to_search for term in medical_device_terms)

class CrossReferenceValidator:
    """
    Cross-reference cases with multiple sources for verification.
    """
    
    def __init__(self):
        self.pacer_base = "https://pcl.uscourts.gov"
        self.justia_base = "https://dockets.justia.com"
        
    def cross_reference_case(self, docket_number: str, court: str) -> dict:
        """
        Cross-reference case with other sources.
        
        Args:
            docket_number: Federal docket number
            court: Court identifier
            
        Returns:
            Cross-reference results
        """
        results = {
            'docket_number': docket_number,
            'court': court,
            'sources_checked': [],
            'matches_found': 0,
            'discrepancies': []
        }
        
        # Check Justia (free alternative)
        justia_result = self._check_justia(docket_number, court)
        if justia_result:
            results['sources_checked'].append('Justia')
            if justia_result.get('found'):
                results['matches_found'] += 1
        
        # Note: PACER requires paid access
        results['sources_checked'].append('CourtListener (primary)')
        
        return results
    
    def _check_justia(self, docket_number: str, court: str) -> dict:
        """Check case on Justia (free legal database)."""
        # This would require web scraping - just return structure for now
        return {
            'found': False,
            'url': f"{self.justia_base}/docket/{court}/{docket_number}",
            'note': 'Web scraping implementation needed'
        }

def create_data_quality_report(cases_df: pd.DataFrame) -> dict:
    """
    Create comprehensive data quality report.
    
    Args:
        cases_df: DataFrame of collected cases
        
    Returns:
        Quality report dictionary
    """
    validator = LegalDataValidator()
    
    # Validate all cases
    validation_results = []
    for _, case in cases_df.iterrows():
        case_dict = case.to_dict()
        validation = validator.validate_case_data(case_dict)
        validation_results.append(validation)
    
    validation_df = pd.DataFrame(validation_results)
    
    # Generate report
    report = {
        'total_cases': len(cases_df),
        'high_quality_cases': len(validation_df[validation_df['data_quality'] == 'High']),
        'medium_quality_cases': len(validation_df[validation_df['data_quality'] == 'Medium']),
        'low_quality_cases': len(validation_df[validation_df['data_quality'] == 'Low']),
        'average_confidence': validation_df['confidence_score'].mean(),
        'common_issues': validation_df['validation_flags'].explode().value_counts().to_dict(),
        'recommendations': []
    }
    
    # Add recommendations
    if report['low_quality_cases'] > report['total_cases'] * 0.2:
        report['recommendations'].append("High number of low-quality cases - consider refining search criteria")
    
    if report['average_confidence'] < 60:
        report['recommendations'].append("Low average confidence - manual review recommended")
    
    return report