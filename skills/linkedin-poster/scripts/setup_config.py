#!/usr/bin/env python3
"""
Interactive setup script for LinkedIn credentials.
"""

import json
import os
from pathlib import Path

CONFIG_DIR = Path.home() / '.linkedin'
CONFIG_FILE = CONFIG_DIR / 'config.json'

def prompt_credentials():
    print("=" * 60)
    print("LinkedIn API Credential Setup")
    print("=" * 60)
    print("\nYou need to obtain these credentials from the LinkedIn Developer Portal first.")
    print("See references/SETUP.md for detailed instructions.\n")

    client_id = input("Enter your LinkedIn Client ID: ").strip()
    client_secret = input("Enter your LinkedIn Client Secret: ").strip()
    access_token = input("Enter your LinkedIn Access Token (with w_member_social): ").strip()

    return {
        'client_id': client_id,
        'client_secret': client_secret,
        'access_token': access_token
    }

def save_config(creds: dict, use_env: bool = False):
    if use_env:
        # Suggest environment variables
        print("\nTo use environment variables, add to your shell profile:")
        print(f"  export LINKEDIN_CLIENT_ID='{creds['client_id']}'")
        print(f"  export LINKEDIN_CLIENT_SECRET='{creds['client_secret']}'")
        print(f"  export LINKEDIN_ACCESS_TOKEN='{creds['access_token']}'")
    else:
        # Save to config file
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, 'w') as f:
            json.dump(creds, f, indent=2)
        os.chmod(CONFIG_FILE, 0o600)  # rw-------
        print(f"\n✓ Credentials saved to {CONFIG_FILE}")

    print("\nSetup complete! You can now use the linkedin-poster skill.")
    print("Test with: python scripts/test_connection.py")

def main():
    creds = prompt_credentials()

    # Quick validation check
    print("\nValidating token...")
    try:
        import requests
        resp = requests.get(
            'https://api.linkedin.com/v2/me',
            headers={'Authorization': f'Bearer {creds["access_token"]}'},
            timeout=10
        )
        if resp.status_code == 200:
            name = resp.json().get('localizedFirstName', '')
            last = resp.json().get('localizedLastName', '')
            print(f"✓ Token appears valid for: {name} {last}")
        else:
            print(f"⚠ Token validation failed: {resp.status_code} {resp.text}")
            print("You can proceed anyway but posting may fail.")
    except Exception as e:
        print(f"⚠ Could not validate: {e}")

    print("\nHow would you like to store credentials?")
    print("1) Save to config file (~/.linkedin/config.json) - recommended for desktop")
    print("2) Use environment variables - recommended for servers")
    choice = input("Choose (1/2): ").strip()

    use_env = (choice == '2')
    save_config(creds, use_env=use_env)

if __name__ == '__main__':
    main()
