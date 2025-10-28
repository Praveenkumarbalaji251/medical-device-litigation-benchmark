"""
Multi-source legal data collection for maximum accuracy and completeness.
"""

import requests
import pandas as pd
from typing import List, Dict
import time
import logging

class MultiSourceCollector:
    """
    Collects and cross-references legal data from multiple sources.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.sources = {
            'courtlistener': {
                'name': 'CourtListener',
                'api_base': 'https://www.courtlistener.com/api/rest/v4/',
                'reliability': 'High',
                'cost': 'Free',
                'coverage': 'Federal courts comprehensive'
            },
            'pacer': {
                'name': 'PACER',
                'api_base': 'https://pcl.uscourts.gov/',
                'reliability': 'Highest',
                'cost': 'Paid ($0.10/page)',
                'coverage': 'Official federal court records'
            },
            'justia': {
                'name': 'Justia',
                'api_base': 'https://dockets.justia.com/',
                'reliability': 'Medium',
                'cost': 'Free',
                'coverage': 'Major cases, some gaps'
            },
            'law360': {
                'name': 'Law360',
                'reliability': 'High',
                'cost': 'Subscription',
                'coverage': 'Major litigation news'
            }
        }
    
    def get_recommended_sources(self, budget: str = 'free') -> List[str]:
        """
        Get recommended data sources based on budget and needs.
        
        Args:
            budget: 'free', 'low', 'medium', 'high'
            
        Returns:
            List of recommended source keys
        """
        if budget == 'free':
            return ['courtlistener', 'justia']
        elif budget == 'low':
            return ['courtlistener', 'pacer']  # Limited PACER use
        elif budget == 'medium':
            return ['courtlistener', 'pacer', 'law360']
        else:  # high budget
            return list(self.sources.keys())
    
    def collect_from_multiple_sources(self, 
                                    search_terms: List[str],
                                    sources: List[str] = None,
                                    date_range: tuple = None) -> Dict:
        """
        Collect cases from multiple sources and merge results.
        
        Args:
            search_terms: List of search terms
            sources: List of source keys to use
            date_range: (start_date, end_date) tuple
            
        Returns:
            Merged and validated results
        """
        if not sources:
            sources = self.get_recommended_sources('free')
        
        all_results = {}
        
        for source in sources:
            self.logger.info(f"Collecting from {self.sources[source]['name']}...")
            
            try:
                if source == 'courtlistener':
                    results = self._collect_courtlistener(search_terms, date_range)
                elif source == 'justia':
                    results = self._collect_justia(search_terms, date_range)
                # Add other sources as needed
                else:
                    self.logger.warning(f"Source {source} not yet implemented")
                    continue
                
                all_results[source] = results
                time.sleep(1)  # Be respectful to APIs
                
            except Exception as e:
                self.logger.error(f"Error collecting from {source}: {e}")
        
        # Merge and deduplicate results
        merged_results = self._merge_sources(all_results)
        
        return {
            'merged_cases': merged_results,
            'source_coverage': {source: len(results) for source, results in all_results.items()},
            'total_unique_cases': len(merged_results),
            'data_quality_report': self._assess_quality(merged_results)
        }
    
    def _collect_courtlistener(self, search_terms: List[str], date_range: tuple = None) -> List[Dict]:
        """Collect from CourtListener API."""
        from .courtlistener_collector import CourtListenerCollector
        
        collector = CourtListenerCollector()
        
        all_cases = []
        for term in search_terms:
            cases = collector._search_by_term(
                term, 
                date_range[0] if date_range else None,
                date_range[1] if date_range else None
            )
            all_cases.extend(cases)
        
        return all_cases
    
    def _collect_justia(self, search_terms: List[str], date_range: tuple = None) -> List[Dict]:
        """Collect from Justia (would need web scraping)."""
        # Placeholder - would implement web scraping
        return []
    
    def _merge_sources(self, source_results: Dict[str, List[Dict]]) -> List[Dict]:
        """Merge results from different sources, removing duplicates."""
        merged = {}
        
        for source, cases in source_results.items():
            for case in cases:
                # Use docket number as primary key for deduplication
                docket = case.get('docketNumber') or case.get('docket_number')
                case_name = case.get('caseName') or case.get('case_name')
                
                if docket:
                    key = f"{docket}_{case_name}"
                    
                    if key not in merged:
                        merged[key] = case.copy()
                        merged[key]['sources'] = [source]
                    else:
                        # Merge additional information
                        merged[key]['sources'].append(source)
                        # Prefer more complete data
                        for field, value in case.items():
                            if value and not merged[key].get(field):
                                merged[key][field] = value
        
        return list(merged.values())
    
    def _assess_quality(self, cases: List[Dict]) -> Dict:
        """Assess overall data quality."""
        total_cases = len(cases)
        
        # Count cases with multiple source verification
        multi_source_cases = len([c for c in cases if len(c.get('sources', [])) > 1])
        
        # Count complete cases (all required fields present)
        required_fields = ['caseName', 'court', 'dateFiled', 'docketNumber']
        complete_cases = len([
            c for c in cases 
            if all(c.get(field) for field in required_fields)
        ])
        
        return {
            'total_cases': total_cases,
            'multi_source_verified': multi_source_cases,
            'verification_rate': multi_source_cases / total_cases if total_cases > 0 else 0,
            'completeness_rate': complete_cases / total_cases if total_cases > 0 else 0,
            'quality_score': (multi_source_cases * 0.6 + complete_cases * 0.4) / total_cases if total_cases > 0 else 0
        }

def get_data_collection_strategy() -> Dict:
    """
    Get recommended data collection strategy for legal professionals.
    
    Returns:
        Strategy recommendations
    """
    return {
        'primary_sources': {
            'courtlistener': {
                'priority': 1,
                'reason': 'Free, comprehensive, API access',
                'limitations': 'Rate limits without token'
            },
            'pacer': {
                'priority': 2, 
                'reason': 'Official source, most authoritative',
                'limitations': 'Costs $0.10 per page viewed'
            }
        },
        'verification_sources': {
            'justia': 'Free cross-reference for major cases',
            'google_scholar': 'Additional case law research',
            'law_firm_databases': 'Westlaw/Lexis for comprehensive research'
        },
        'quality_assurance': {
            'cross_reference': 'Always verify with 2+ sources for important cases',
            'manual_review': 'Manually review high-value cases',
            'date_validation': 'Verify filing dates and status',
            'attorney_verification': 'Confirm attorney information separately'
        },
        'best_practices': [
            'Start with CourtListener for bulk collection',
            'Use PACER for official verification of key cases', 
            'Cross-reference settlement amounts with news sources',
            'Maintain audit trail of all data sources',
            'Regular updates to catch new filings',
            'Document search methodology for transparency'
        ]
    }