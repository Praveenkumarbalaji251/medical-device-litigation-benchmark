#!/usr/bin/env python3
"""
Setup script for CourtListener API token and test connection.
"""

import os
import sys
from pathlib import Path
import requests
import json

def test_api_token(token):
    """Test if API token works."""
    headers = {
        'Authorization': f'Token {token}',
        'User-Agent': 'MedicalDeviceLegalBenchmark/1.0'
    }
    
    # Simple test request
    url = "https://www.courtlistener.com/api/rest/v4/courts/"
    
    try:
        response = requests.get(url, headers=headers, params={'format': 'json'})
        response.raise_for_status()
        
        data = response.json()
        print(f"✅ API token is working!")
        print(f"📊 Available courts: {data.get('count', 'Unknown')}")
        return True
        
    except requests.RequestException as e:
        print(f"❌ API token test failed: {e}")
        return False

def save_api_token(token):
    """Save API token to config file."""
    config_dir = Path("config")
    config_dir.mkdir(exist_ok=True)
    
    config_file = config_dir / "api_tokens.json"
    
    # Load existing config or create new
    if config_file.exists():
        with open(config_file, 'r') as f:
            config = json.load(f)
    else:
        config = {}
    
    config['courtlistener'] = token
    
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"💾 Token saved to {config_file}")

def main():
    """Main setup function."""
    print("🏛️  CourtListener API Setup")
    print("=" * 40)
    
    print("\n📋 Steps to get your API token:")
    print("1. Visit: https://www.courtlistener.com")
    print("2. Create free account (Sign Up)")
    print("3. Log in and go to Profile/API section")
    print("4. Generate API token")
    print("5. Copy the token and paste it below")
    
    print("\n" + "="*40)
    
    token = input("🔑 Paste your CourtListener API token: ").strip()
    
    if not token:
        print("❌ No token provided. Exiting.")
        return 1
    
    print("\n🧪 Testing API token...")
    
    if test_api_token(token):
        save_api_token(token)
        print(f"\n🎉 Setup complete!")
        print(f"\n📋 Next steps:")
        print(f"1. Run: python scripts/collect_cases.py")
        print(f"2. The script will automatically use your saved token")
        print(f"3. Start collecting medical device cases!")
        return 0
    else:
        print(f"\n❌ Token doesn't work. Please check:")
        print(f"   - Token is copied correctly")
        print(f"   - Account is activated") 
        print(f"   - Try generating a new token")
        return 1

if __name__ == "__main__":
    exit(main())