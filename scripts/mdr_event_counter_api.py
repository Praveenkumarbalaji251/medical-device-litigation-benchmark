#!/usr/bin/env python3
"""
MAUDE MDR Event Counter API
Simple API to count MDR events, injuries, and deaths for any device
"""

import requests
import json
from datetime import datetime, timedelta
import time

class MAUDEEventCounter:
    """API client to count MAUDE events for medical devices."""
    
    def __init__(self):
        self.base_url = "https://api.fda.gov/device/event.json"
        self.api_key = None  # Optional: Get free key at https://open.fda.gov/apis/authentication/
        
    def count_mdr_events(self, device_name, start_date, end_date, manufacturer=None):
        """
        Count total MDR events for a device in date range.
        
        Args:
            device_name: Device brand name (e.g., "DreamStation")
            start_date: Start date YYYY-MM-DD
            end_date: End date YYYY-MM-DD
            manufacturer: Optional manufacturer name (e.g., "Philips")
        
        Returns:
            dict with total count and breakdown
        """
        
        print(f"📊 Counting MDR Events for: {device_name}")
        print(f"📅 Date Range: {start_date} to {end_date}")
        
        # Format dates for FDA API (YYYYMMDD)
        start_formatted = start_date.replace("-", "")
        end_formatted = end_date.replace("-", "")
        
        # Build search query
        search_parts = []
        
        # Device search
        search_parts.append(f'device.brand_name:"{device_name}"')
        
        # Add manufacturer if provided
        if manufacturer:
            search_parts.append(f'device.manufacturer_d_name:"{manufacturer}"')
        
        # Date range
        date_query = f'date_received:[{start_formatted}+TO+{end_formatted}]'
        
        # Combine
        device_query = '+OR+'.join(search_parts) if manufacturer else search_parts[0]
        full_query = f'({device_query})+AND+{date_query}'
        
        # Get total count using limit=1 (most reliable)
        params = {
            'search': full_query,
            'limit': 1
        }
        
        if self.api_key:
            params['api_key'] = self.api_key
        
        try:
            print(f"🔍 Querying FDA API...")
            response = requests.get(self.base_url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # Get total from meta section
                if 'meta' in data and 'results' in data['meta']:
                    total_events = data['meta']['results'].get('total', 0)
                    
                    print(f"✅ Found {total_events} total MDR events")
                    
                    return {
                        'success': True,
                        'device': device_name,
                        'date_range': f"{start_date} to {end_date}",
                        'total_events': total_events
                    }
                else:
                    print(f"⚠️  No results found")
                    return {
                        'success': True,
                        'device': device_name,
                        'total_events': 0,
                        'message': 'No events found for this device/date range'
                    }
            
            elif response.status_code == 404:
                print(f"❌ No data found (404)")
                return {'success': True, 'total_events': 0, 'message': 'No matching records'}
            
            elif response.status_code == 500:
                print(f"❌ FDA API Server Error (500)")
                return {'success': False, 'error': 'FDA API temporarily unavailable'}
            
            else:
                print(f"❌ API Error {response.status_code}")
                return {'success': False, 'error': f'HTTP {response.status_code}'}
        
        except Exception as e:
            print(f"❌ Request failed: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def count_deaths_and_injuries(self, device_name, start_date, end_date, manufacturer=None):
        """
        Count deaths and serious injuries for a device.
        
        Returns:
            dict with death and injury counts
        """
        
        print(f"\n💀 Counting Deaths and Injuries for: {device_name}")
        
        # Format dates
        start_formatted = start_date.replace("-", "")
        end_formatted = end_date.replace("-", "")
        
        # Build base query
        device_query = f'device.brand_name:"{device_name}"'
        if manufacturer:
            device_query = f'({device_query}+OR+device.manufacturer_d_name:"{manufacturer}")'
        
        date_query = f'date_received:[{start_formatted}+TO+{end_formatted}]'
        
        results = {
            'device': device_name,
            'date_range': f"{start_date} to {end_date}",
            'deaths': 0,
            'serious_injuries': 0,
            'malfunctions': 0
        }
        
        # Count deaths
        death_query = f'{device_query}+AND+{date_query}+AND+event_type:"Death"'
        death_params = {'search': death_query, 'limit': 1}
        
        try:
            response = requests.get(self.base_url, params=death_params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                if 'meta' in data and 'results' in data['meta']:
                    results['deaths'] = data['meta']['results'].get('total', 0)
                    print(f"   Deaths: {results['deaths']}")
        except Exception as e:
            print(f"   Error counting deaths: {e}")
        
        time.sleep(0.3)  # Rate limiting
        
        # Count injuries
        injury_query = f'{device_query}+AND+{date_query}+AND+(event_type:"Injury"+OR+event_type:"Serious+Injury")'
        injury_params = {'search': injury_query, 'limit': 1}
        
        try:
            response = requests.get(self.base_url, params=injury_params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                if 'meta' in data and 'results' in data['meta']:
                    results['serious_injuries'] = data['meta']['results'].get('total', 0)
                    print(f"   Serious Injuries: {results['serious_injuries']}")
        except Exception as e:
            print(f"   Error counting injuries: {e}")
        
        time.sleep(0.3)  # Rate limiting
        
        # Count malfunctions
        malfunction_query = f'{device_query}+AND+{date_query}+AND+event_type:"Malfunction"'
        malfunction_params = {'search': malfunction_query, 'limit': 1}
        
        try:
            response = requests.get(self.base_url, params=malfunction_params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                if 'meta' in data and 'results' in data['meta']:
                    results['malfunctions'] = data['meta']['results'].get('total', 0)
                    print(f"   Malfunctions: {results['malfunctions']}")
        except Exception as e:
            print(f"   Error counting malfunctions: {e}")
        
        return results
    
    def count_monthly_breakdown(self, device_name, start_date, end_date, manufacturer=None):
        """
        Get monthly breakdown of MDR events.
        
        Returns:
            dict with monthly counts
        """
        
        print(f"\n📅 Monthly Breakdown for: {device_name}")
        
        # Parse dates
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        
        monthly_counts = {}
        current = start
        
        while current <= end:
            # Get month range
            month_start = current.strftime("%Y%m%d")
            
            # Last day of month
            if current.month == 12:
                next_month = current.replace(year=current.year + 1, month=1, day=1)
            else:
                next_month = current.replace(month=current.month + 1, day=1)
            
            month_end = (next_month - timedelta(days=1)).strftime("%Y%m%d")
            
            # Don't go past end date
            if datetime.strptime(month_end, "%Y%m%d") > end:
                month_end = end.strftime("%Y%m%d")
            
            # Build query for this month
            device_query = f'device.brand_name:"{device_name}"'
            if manufacturer:
                device_query = f'({device_query}+OR+device.manufacturer_d_name:"{manufacturer}")'
            
            month_query = f'{device_query}+AND+date_received:[{month_start}+TO+{month_end}]'
            
            params = {'search': month_query, 'limit': 1}
            
            try:
                response = requests.get(self.base_url, params=params, timeout=30)
                if response.status_code == 200:
                    data = response.json()
                    count = 0
                    if 'meta' in data and 'results' in data['meta']:
                        count = data['meta']['results'].get('total', 0)
                    
                    month_key = current.strftime("%Y-%m")
                    monthly_counts[month_key] = count
                    print(f"   {month_key}: {count} reports")
                
                time.sleep(0.3)  # Rate limiting
            
            except Exception as e:
                print(f"   Error for {current.strftime('%Y-%m')}: {e}")
            
            # Next month
            current = next_month
        
        return monthly_counts
    
    def analyze_6month_window(self, device_name, litigation_date, manufacturer=None):
        """
        Analyze the critical 6-month window before litigation.
        
        Args:
            device_name: Device name
            litigation_date: When litigation was filed (YYYY-MM-DD)
            manufacturer: Optional manufacturer
        
        Returns:
            Complete analysis with all metrics
        """
        
        print(f"\n🎯 6-MONTH PRE-LITIGATION ANALYSIS")
        print(f"=" * 60)
        
        # Calculate windows
        lit_date = datetime.strptime(litigation_date, "%Y-%m-%d")
        six_months_before = lit_date - timedelta(days=180)
        
        start_date = six_months_before.strftime("%Y-%m-%d")
        end_date = litigation_date
        
        print(f"Device: {device_name}")
        print(f"Litigation Date: {litigation_date}")
        print(f"Analysis Window: {start_date} to {end_date}")
        
        # Get counts
        event_count = self.count_mdr_events(device_name, start_date, end_date, manufacturer)
        
        if not event_count.get('success'):
            print(f"\n⚠️  Could not retrieve data: {event_count.get('error', 'Unknown error')}")
            return None
        
        death_injury_count = self.count_deaths_and_injuries(device_name, start_date, end_date, manufacturer)
        
        monthly_breakdown = self.count_monthly_breakdown(device_name, start_date, end_date, manufacturer)
        
        # Analyze pattern
        months = sorted(monthly_breakdown.keys())
        if len(months) >= 2:
            first_month_count = monthly_breakdown[months[0]]
            last_month_count = monthly_breakdown[months[-1]]
            
            if first_month_count > 0:
                increase_pct = ((last_month_count - first_month_count) / first_month_count) * 100
            else:
                increase_pct = 0
        else:
            increase_pct = 0
        
        # Compile results
        analysis = {
            'device': device_name,
            'litigation_date': litigation_date,
            'analysis_window': f"{start_date} to {end_date}",
            'total_events': event_count.get('total_events', 0),
            'deaths': death_injury_count['deaths'],
            'serious_injuries': death_injury_count['serious_injuries'],
            'malfunctions': death_injury_count['malfunctions'],
            'monthly_breakdown': monthly_breakdown,
            'increase_percentage': round(increase_pct, 1),
            'litigation_indicators': {
                'report_spike': increase_pct > 300,
                'multiple_deaths': death_injury_count['deaths'] > 10,
                'serious_injuries': death_injury_count['serious_injuries'] > 50
            }
        }
        
        # Print summary
        print(f"\n📊 ANALYSIS SUMMARY:")
        print(f"=" * 60)
        print(f"Total MDR Events: {analysis['total_events']}")
        print(f"Deaths: {analysis['deaths']}")
        print(f"Serious Injuries: {analysis['serious_injuries']}")
        print(f"Malfunctions: {analysis['malfunctions']}")
        print(f"Report Increase: {analysis['increase_percentage']:.1f}%")
        
        print(f"\n🚨 LITIGATION INDICATORS:")
        indicators_hit = sum(analysis['litigation_indicators'].values())
        for indicator, hit in analysis['litigation_indicators'].items():
            status = "✅" if hit else "❌"
            print(f"   {status} {indicator.replace('_', ' ').title()}")
        
        print(f"\nRISK SCORE: {indicators_hit}/3")
        
        return analysis


def main():
    """Example usage of the MDR Event Counter API."""
    
    print("🔬 MAUDE MDR EVENT COUNTER API")
    print("=" * 60)
    
    # Initialize counter
    counter = MAUDEEventCounter()
    
    # Example 1: Philips CPAP 6-month analysis
    print("\n" + "="*60)
    print("EXAMPLE 1: Philips CPAP (Validated Case)")
    print("="*60)
    
    result = counter.analyze_6month_window(
        device_name="DreamStation",
        litigation_date="2021-07-01",
        manufacturer="Philips"
    )
    
    if result:
        # Save results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"mdr_count_analysis_{timestamp}.json"
        
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        
        print(f"\n💾 Results saved to: {output_file}")
    
    print(f"\n" + "="*60)
    print("✅ MDR EVENT COUNTER API READY")
    print("="*60)
    print("""
You can now use this API to count MDR events for any device:

Usage:
    counter = MAUDEEventCounter()
    
    # Count total events
    result = counter.count_mdr_events("DreamStation", "2021-01-01", "2021-06-30")
    
    # Count deaths and injuries
    result = counter.count_deaths_and_injuries("DreamStation", "2021-01-01", "2021-06-30")
    
    # Get monthly breakdown
    result = counter.count_monthly_breakdown("DreamStation", "2021-01-01", "2021-06-30")
    
    # Complete 6-month analysis
    result = counter.analyze_6month_window("DreamStation", "2021-07-01")
    """)

if __name__ == "__main__":
    main()