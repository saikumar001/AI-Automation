#!/usr/bin/env python3
"""
LinkedIn authentication and credential management.
"""

import os
import json
from pathlib import Path
from typing import Optional, Dict

CONFIG_PATH = Path.home() / '.linkedin' / 'config.json'

def load_credentials() -> Dict[str, str]:
    """
    Load LinkedIn credentials from environment variables or config file.

    Returns:
        Dict with keys: client_id, client_secret, access_token

    Raises:
        FileNotFoundError: If credentials not found anywhere
        ValueError: If credentials are incomplete
    """
    # Try environment variables first
    env_creds = {
        'client_id': os.getenv('LINKEDIN_CLIENT_ID'),
        'client_secret': os.getenv('LINKEDIN_CLIENT_SECRET'),
        'access_token': os.getenv('LINKEDIN_ACCESS_TOKEN')
    }

    # Filter out None values
    env_creds = {k: v for k, v in env_creds.items() if v is not None}

    if env_creds and all(k in env_creds for k in ['client_id', 'client_secret', 'access_token']):
        return env_creds

    # Try config file
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, 'r') as f:
                config = json.load(f)
            if all(k in config for k in ['client_id', 'client_secret', 'access_token']):
                return config
        except (json.JSONDecodeError, KeyError) as e:
            raise ValueError(f"Invalid config file at {CONFIG_PATH}: {e}")

    raise FileNotFoundError(
        "LinkedIn credentials not found. Set environment variables LINKEDIN_CLIENT_ID, "
        "LINKEDIN_CLIENT_SECRET, LINKEDIN_ACCESS_TOKEN, or run setup to create "
        f"~/.linkedin/config.json.\n\nSee references/SETUP.md for instructions."
    )

def validate_token(access_token: str) -> bool:
    """
    Check if the access token is valid by making a test API call.

    Args:
        access_token: LinkedIn access token

    Returns:
        True if token is valid, False otherwise
    """
    try:
        import requests
        headers = {
            'Authorization': f'Bearer {access_token}',
            'X-Restli-Protocol-Version': '2.0.0'
        }
        resp = requests.get(
            'https://api.linkedin.com/v2/userinfo',
            headers=headers,
            timeout=10
        )
        return resp.status_code == 200
    except Exception:
        return False

def get_profile_name(access_token: str) -> Optional[str]:
    """Get the user's LinkedIn profile name (first + last)."""
    try:
        import requests
        headers = {
            'Authorization': f'Bearer {access_token}',
            'X-Restli-Protocol-Version': '2.0.0'
        }
        resp = requests.get(
            'https://api.linkedin.com/v2/userinfo',
            headers=headers,
            timeout=10
        )
        if resp.status_code == 200:
            data = resp.json()
            first = data.get('given_name', '')
            last = data.get('family_name', '')
            return f"{first} {last}".strip()
        return None
    except Exception:
        return None

if __name__ == '__main__':
    # Simple test: load credentials and validate
    try:
        creds = load_credentials()
        print("✓ Credentials loaded")
        if validate_token(creds['access_token']):
            name = get_profile_name(creds['access_token'])
            print(f"✓ Token valid - authenticated as: {name or 'Unknown'}")
        else:
            print("✗ Token invalid or expired")
    except Exception as e:
        print(f"✗ Error: {e}")
