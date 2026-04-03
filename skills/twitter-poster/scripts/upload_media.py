#!/usr/bin/env python3
"""
Twitter media (image/GIF) upload utilities.
"""

import os
import requests
from pathlib import Path
from typing import Optional
from requests_oauthlib import OAuth1

def upload_media(image_path: str, credentials: Dict[str, str]) -> Optional[str]:
    """
    Upload an image to Twitter and return the media ID.

    Args:
        image_path: Path to image file (JPG/PNG, <5MB)
        credentials: OAuth 1.0a credentials dict

    Returns:
        Media ID string if successful, None otherwise
    """
    try:
        # Validate
        if not validate_image(image_path):
            return None

        # Prepare OAuth1 auth
        auth = OAuth1(
            credentials['api_key'],
            credentials['api_secret'],
            credentials['access_token'],
            credentials['access_token_secret']
        )

        # Twitter media upload endpoint
        upload_url = "https://upload.twitter.com/1.1/media/upload.json"

        with open(image_path, 'rb') as f:
            files = {'media': f}
            resp = requests.post(upload_url, files=files, auth=auth, timeout=60)

        if resp.status_code in (200, 201):
            data = resp.json()
            media_id = data.get('media_id_string')
            return media_id
        else:
            print(f"Media upload failed: {resp.status_code} {resp.text}")
            return None

    except Exception as e:
        print(f"Error uploading media: {e}")
        return None

def validate_image(image_path: str) -> bool:
    """
    Check if image file is valid for Twitter upload.

    - Exists
    - Extensions: .jpg, .jpeg, .png
    - Size < 5MB
    """
    path = Path(image_path)
    if not path.exists():
        print(f"Image not found: {image_path}")
        return False

    if path.suffix.lower() not in ('.jpg', '.jpeg', '.png'):
        print(f"Unsupported image format: {path.suffix} (use JPG or PNG)")
        return False

    if path.stat().st_size > 5 * 1024 * 1024:  # 5MB
        print(f"Image too large: {path.stat().st_size / 1024 / 1024:.1f}MB (max 5MB)")
        return False

    return True

if __name__ == '__main__':
    # Quick test if image path provided and credentials set
    import sys
    from auth import load_credentials

    if len(sys.argv) < 2:
        print("Usage: python upload_media.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    try:
        creds = load_credentials()
        if validate_image(image_path):
            print("Valid image, attempting upload...")
            media_id = upload_media(image_path, creds)
            if media_id:
                print(f"✓ Uploaded. Media ID: {media_id}")
            else:
                print("✗ Upload failed")
        else:
            print("✗ Image validation failed")
    except Exception as e:
        print(f"✗ Error: {e}")
