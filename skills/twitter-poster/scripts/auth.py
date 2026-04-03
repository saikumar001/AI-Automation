#!/usr/bin/env python3
"""
Twitter authentication and credential management.
"""

import os
import json
from pathlib import Path
from typing import Optional, Dict

CONFIG_PATH = Path.home() / '.twitter' / 'config.json'

def load_credentials() -> Dict[str, str]:
    """
    Load Twitter credentials from environment variables or config file.

    Returns:
        Dict with keys: api_key, api_secret, access_token, access_token_secret

    Raises:
        FileNotFoundError: If credentials not found anywhere
        ValueError: If credentials are incomplete
    """
    # Try environment variables first
    env_creds = {
        'api_key': os.getenv('TWITTER_API_KEY'),
        'api_secret': os.getenv('TWITTER_API_SECRET'),
        'access_token': os.getenv('TWITTER_ACCESS_TOKEN'),
        'access_token_secret': os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    }

    # Filter out None values
    env_creds = {k: v for k, v in env_creds.items() if v is not None}

    if env_creds and all(k in env_creds for k in ['api_key', 'api_secret', 'access_token', 'access_token_secret']):
        return env_creds

    # Try config file
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, 'r') as f:
                config = json.load(f)
            if all(k in config for k in ['api_key', 'api_secret', 'access_token', 'access_token_secret']):
                return config
        except (json.JSONDecodeError, KeyError) as e:
            raise ValueError(f"Invalid config file at {CONFIG_PATH}: {e}")

    raise FileNotFoundError(
        "Twitter credentials not found. Set environment variables:\n"
        "  TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET\n"
        f"or run setup to create {CONFIG_PATH}.\n\n"
        "See references/SETUP.md for instructions."
    )

def validate_token(credentials: Dict[str, str]) -> bool:
    """
    Check if the access token is valid by making a test API call.

    Args:
        credentials: Dict with Twitter OAuth 1.0a credentials

    Returns:
        True if token is valid (can fetch user), False otherwise
    """
    try:
        import requests
        from requests_oauthlib import OAuth1

        auth = OAuth1(
            credentials['api_key'],
            credentials['api_secret'],
            credentials['access_token'],
            credentials['access_token_secret']
        )

        resp = requests.get(
            'https://api.twitter.com/2/users/me',
            auth=auth,
            timeout=10
        )
        return resp.status_code == 200
    except Exception as e:
        print(f"Validation error: {e}")
        return False

def get_username(credentials: Dict[str, str]) -> Optional[str]:
    """Get the authenticated user's Twitter username."""
    try:
        import requests
        from requests_oauthlib import OAuth1

        auth = OAuth1(
            credentials['api_key'],
            credentials['api_secret'],
            credentials['access_token'],
            credentials['access_token_secret']
        )

        resp = requests.get(
            'https://api.twitter.com/2/users/me',
            auth=auth,
            params={'user.fields': 'username'},
            timeout=10
        )
        if resp.status_code == 200:
            data = resp.json()
            return data.get('data', {}).get('username')
        return None
    except Exception as e:
        print(f"Error getting username: {e}")
        return None

if __name__ == '__main__':
    # Simple test: load credentials and validate
    try:
        creds = load_credentials()
        print("✓ Credentials loaded")
        if validate_token(creds):
            username = get_username(creds)
            print(f"✓ Token valid - authenticated as: @{username or 'unknown'}")
        else:
            print("✗ Token invalid or expired")
    except Exception as e:
        print(f"✗ Error: {e}")
