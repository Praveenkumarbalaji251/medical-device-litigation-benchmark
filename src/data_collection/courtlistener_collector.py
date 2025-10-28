"""
CourtListener API client for collecting medical device litigation cases.
"""

import requests
import pandas as pd
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

class CourtListenerCollector:
    """
    Collects medical device litigation cases from CourtListener API.
    """
    
    def __init__(self, api_token: Optional[str] = None):
        """
        Initialize CourtListener client.
        
        Args:
            api_token: CourtListener API token (optional but recommended for higher rate limits)
        """
        self.base_url = "https://www.courtlistener.com/api/rest/v4/"
        self.headers = {
            'User-Agent': 'MedicalDeviceLegalBenchmark/1.0',
        }
        
        # Try to load API token from config if not provided
        if not api_token:
            api_token = self._load_saved_token()
            
        if api_token:
            self.headers['Authorization'] = f'Token {api_token}'
        
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.logger = logging.getLogger(__name__)
        
        # Medical device search terms
        self.medical_device_terms = [
            "medical device",
            "implant",
            "pacemaker", 
            "defibrillator",
            "hip replacement",
            "knee replacement",
            "hernia mesh",
            "IVC filter",
            "CPAP",
            "BiPAP",
            "Philips CPAP",
            "insulin pump",
            "breast implant",
            "surgical mesh",
            "spinal fusion",
            "cochlear implant"
        ]
        
    def search_cases(self, 
                    start_date: str = None, 
                    end_date: str = None,
                    case_types: List[str] = None) -> List[Dict]:
        """
        Search for medical device cases within date range.
        
        Args:
            start_date: Start date (YYYY-MM-DD format)
            end_date: End date (YYYY-MM-DD format) 
            case_types: List of case types to filter
            
        Returns:
            List of case dictionaries
        """
        if not start_date:
            # Default to last 2 months
            start_date = (datetime.now() - timedelta(days=60)).strftime('%Y-%m-%d')
        
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
            
        all_cases = []
        
        for term in self.medical_device_terms:
            self.logger.info(f"Searching for cases with term: {term}")
            cases = self._search_by_term(term, start_date, end_date, case_types)
            all_cases.extend(cases)
            
            # Rate limiting - be respectful to the API
            time.sleep(1)
        
        # Remove duplicates based on case ID
        unique_cases = {case['id']: case for case in all_cases}.values()
        
        self.logger.info(f"Found {len(unique_cases)} unique cases")
        return list(unique_cases)
    
    def _search_by_term(self, 
                       search_term: str,
                       start_date: str,
                       end_date: str, 
                       case_types: List[str] = None) -> List[Dict]:
        """Search cases by specific term."""
        params = {
            'q': search_term,
            'type': 'r',  # RECAP documents (federal cases)
            'format': 'json'
        }
        
        # Add date filters if provided
        if start_date:
            params['filed_after'] = start_date
        if end_date:
            params['filed_before'] = end_date
        
        if case_types:
            params['nature_of_suit'] = ','.join(case_types)
        
        cases = []
        url = f"{self.base_url}search/"
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            cases.extend(data.get('results', []))
            
            # Handle pagination
            next_url = data.get('next')
            while next_url:
                response = self.session.get(next_url)
                response.raise_for_status()
                data = response.json()
                cases.extend(data.get('results', []))
                next_url = data.get('next')
                time.sleep(0.5)  # Rate limiting
                
        except requests.RequestException as e:
            self.logger.error(f"Error searching for {search_term}: {e}")
            
        return cases
    
    def get_case_details(self, case_id: int) -> Dict:
        """
        Get detailed information for a specific case.
        
        Args:
            case_id: CourtListener case ID
            
        Returns:
            Detailed case information
        """
        url = f"{self.base_url}dockets/{case_id}/"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
            
        except requests.RequestException as e:
            self.logger.error(f"Error getting case details for {case_id}: {e}")
            return {}
    
    def get_mdl_cases(self, start_date: str = None, end_date: str = None) -> List[Dict]:
        """
        Search specifically for MDL cases involving medical devices.
        
        Args:
            start_date: Start date (YYYY-MM-DD format)
            end_date: End date (YYYY-MM-DD format)
            
        Returns:
            List of MDL cases
        """
        mdl_terms = [
            "MDL",
            "multidistrict litigation", 
            "mass tort",
            "consolidated cases"
        ]
        
        all_cases = []
        
        for term in mdl_terms:
            for device_term in self.medical_device_terms[:5]:  # Limit to avoid too many requests
                search_query = f"{term} AND {device_term}"
                cases = self._search_by_term(search_query, start_date, end_date)
                all_cases.extend(cases)
                time.sleep(1)
        
        return list({case['id']: case for case in all_cases}.values())
    
    def export_to_dataframe(self, cases: List[Dict]) -> pd.DataFrame:
        """
        Convert cases list to pandas DataFrame.
        
        Args:
            cases: List of case dictionaries
            
        Returns:
            DataFrame with case information
        """
        if not cases:
            return pd.DataFrame()
        
        # Extract key fields
        case_data = []
        for case in cases:
            case_info = {
                'case_id': case.get('id'),
                'case_name': case.get('case_name', ''),
                'docket_number': case.get('docket_number', ''),
                'court': case.get('court', {}).get('full_name', ''),
                'date_filed': case.get('date_filed'),
                'date_terminated': case.get('date_terminated'),
                'nature_of_suit': case.get('nature_of_suit', ''),
                'cause': case.get('cause', ''),
                'jurisdiction_type': case.get('jurisdiction_type', ''),
                'jury_demand': case.get('jury_demand', ''),
                'mdl_status': case.get('mdl_status', ''),
                'assigned_to': case.get('assigned_to', {}).get('name_full', ''),
                'referred_to': case.get('referred_to', {}).get('name_full', ''),
                'parties': self._extract_parties(case.get('parties', [])),
                'source_url': f"https://www.courtlistener.com{case.get('absolute_url', '')}"
            }
            case_data.append(case_info)
        
        return pd.DataFrame(case_data)
    
    def _load_saved_token(self) -> Optional[str]:
        """Load saved API token from config file."""
        try:
            from pathlib import Path
            import json
            
            config_file = Path("config/api_tokens.json")
            if config_file.exists():
                with open(config_file, 'r') as f:
                    config = json.load(f)
                return config.get('courtlistener')
        except Exception:
            pass
        return None
    
    def _extract_parties(self, parties: List[Dict]) -> str:
        """Extract party names from parties list."""
        if not parties:
            return ""
        
        party_names = []
        for party in parties:
            name = party.get('name', '')
            if name:
                party_names.append(name)
        
        return "; ".join(party_names)
    
    def save_cases(self, cases: List[Dict], output_path: str):
        """
        Save cases to JSON file.
        
        Args:
            cases: List of case dictionaries
            output_path: Path to save the file
        """
        with open(output_path, 'w') as f:
            json.dump(cases, f, indent=2, default=str)
        
        self.logger.info(f"Saved {len(cases)} cases to {output_path}")


def collect_recent_medical_device_cases(api_token: str = None, 
                                      months_back: int = 2,
                                      output_dir: str = "data/raw") -> str:
    """
    Collect recent medical device cases from CourtListener.
    
    Args:
        api_token: CourtListener API token
        months_back: How many months back to search
        output_dir: Directory to save results
        
    Returns:
        Path to saved file
    """
    import os
    
    collector = CourtListenerCollector(api_token)
    
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=months_back * 30)
    
    # Search for cases
    cases = collector.search_cases(
        start_date=start_date.strftime('%Y-%m-%d'),
        end_date=end_date.strftime('%Y-%m-%d')
    )
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Save raw cases
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    cases_file = f"{output_dir}/medical_device_cases_{timestamp}.json"
    collector.save_cases(cases, cases_file)
    
    # Save as DataFrame  
    df = collector.export_to_dataframe(cases)
    csv_file = f"{output_dir}/medical_device_cases_{timestamp}.csv"
    df.to_csv(csv_file, index=False)
    
    print(f"✅ Collected {len(cases)} cases")
    print(f"📄 Raw data: {cases_file}")
    print(f"📊 CSV file: {csv_file}")
    
    return csv_file