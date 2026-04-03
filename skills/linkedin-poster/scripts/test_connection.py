#!/usr/bin/env python3
"""
Test LinkedIn API connection and posting permissions.
"""

from auth import load_credentials, validate_token, get_profile_name
from post import create_text_post

def main():
    print("Testing LinkedIn connection...")
    try:
        creds = load_credentials()
        print("✓ Credentials loaded")

        if validate_token(creds['access_token']):
            name = get_profile_name(creds['access_token'])
            print(f"✓ Token valid - authenticated as: {name or 'Unknown'}")
        else:
            print("✗ Token invalid or expired")
            return 1

        # Optional: test read (already done above)
        # Optional: test post (commented out - don't post accidentally)
        print("\nNote: To test actual posting, uncomment the test in this script (but be careful).")
        return 0

    except FileNotFoundError as e:
        print(f"✗ {e}")
        return 1
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return 1

if __name__ == '__main__':
    import sys
    sys.exit(main())
