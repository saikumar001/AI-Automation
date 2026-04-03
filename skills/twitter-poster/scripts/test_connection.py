#!/usr/bin/env python3
"""
Test Twitter API connection and posting permissions.
"""

from auth import load_credentials, validate_token, get_username

def main():
    print("Testing Twitter connection...")
    try:
        creds = load_credentials()
        print("✓ Credentials loaded")

        if validate_token(creds):
            username = get_username(creds)
            print(f"✓ Token valid - authenticated as: @{username or 'Unknown'}")
        else:
            print("✗ Token invalid or expired")
            return 1

        print("\nNote: To test actual posting, use the skill or call post.create_tweet() (commented out).")
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
