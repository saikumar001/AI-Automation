#!/usr/bin/env python3
"""
Interactive setup script for Twitter credentials.
"""

import json
import os
from pathlib import Path

CONFIG_DIR = Path.home() / '.twitter'
CONFIG_FILE = CONFIG_DIR / 'config.json'

def prompt_credentials():
    print("=" * 60)
    print("Twitter API Credential Setup")
    print("=" * 60)
    print("\nYou need to obtain these credentials from the Twitter Developer Portal first.")
    print("See references/SETUP.md for detailed instructions.\n")

    api_key = input("Enter your Twitter API Key (Consumer Key): ").strip()
    api_secret = input("Enter your Twitter API Secret (Consumer Secret): ").strip()
    access_token = input("Enter your Access Token: ").strip()
    access_token_secret = input("Enter your Access Token Secret: ").strip()

    return {
        'api_key': api_key,
        'api_secret': api_secret,
        'access_token': access_token,
        'access_token_secret': access_token_secret
    }

def save_config(creds: dict, use_env: bool = False):
    if use_env:
        print("\nTo use environment variables, add to your shell profile:")
        print(f"  export TWITTER_API_KEY='{creds['api_key']}'")
        print(f"  export TWITTER_API_SECRET='{creds['api_secret']}'")
        print(f"  export TWITTER_ACCESS_TOKEN='{creds['access_token']}'")
        print(f"  export TWITTER_ACCESS_TOKEN_SECRET='{creds['access_token_secret']}'")
    else:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, 'w') as f:
            json.dump(creds, f, indent=2)
        os.chmod(CONFIG_FILE, 0o600)  # rw-------
        print(f"\n✓ Credentials saved to {CONFIG_FILE}")

    print("\nSetup complete! You can now use the twitter-poster skill.")
    print("Test with: python scripts/test_connection.py")

def main():
    creds = prompt_credentials()

    # Quick validation check
    print("\nValidating credentials...")
    try:
        from auth import validate_token, get_username
        if validate_token(creds):
            username = get_username(creds)
            print(f"✓ Token appears valid for: @{username or 'Unknown'}")
        else:
            print("⚠ Token validation failed: credentials may be incorrect or expired")
            print("You can proceed but posting may fail.")
    except ImportError:
        print("⚠ Could not validate: auth module not available. Run test_connection.py later.")
    except Exception as e:
        print(f"⚠ Could not validate: {e}")

    print("\nHow would you like to store credentials?")
    print("1) Save to config file (~/.twitter/config.json) - recommended for desktop")
    print("2) Use environment variables - recommended for servers")
    choice = input("Choose (1/2): ").strip()

    use_env = (choice == '2')
    save_config(creds, use_env=use_env)

if __name__ == '__main__':
    main()
