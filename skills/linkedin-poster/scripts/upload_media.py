#!/usr/bin/env python3
"""
LinkedIn media (image) upload utilities.
"""

import os
import requests
from pathlib import Path
from typing import Optional

def upload_image(image_path: str, access_token: str, owner: str = "urn:li:person:{person_id}") -> Optional[str]:
    """
    Upload an image to LinkedIn and return the asset URN.

    Args:
        image_path: Path to image file (JPG/PNG, <5MB)
        access_token: LinkedIn access token
        owner: Owner URN (default uses authenticated user). Use format: urn:li:person:{person_id}

    Returns:
        Image asset URN (e.g., "urn:li:digitalmediaAsset:C4D00AAAAbBCDeFGHI") if successful
        None if upload fails
    """
    try:
        # 1. Register upload
        register_url = "https://api.linkedin.com/rest/assets?action=registerUpload"
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
            'LinkedIn-Version': '202401'
        }

        # Get person URN from /me if needed
        if '{person_id}' in owner:
            person_id = get_person_id(access_token)
            if not person_id:
                return None
            owner = owner.format(person_id=person_id)

        register_data = {
            "registerUploadRequest": {
                "owner": owner,
                "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                "serviceRelationships": [
                    {
                        "relationshipType": "OWNER",
                        "identifier": "urn:li:userGeneratedContent"
                    }
                ]
            }
        }

        resp = requests.post(register_url, headers=headers, json=register_data, timeout=30)
        if resp.status_code != 200:
            print(f"Failed to register upload: {resp.status_code} {resp.text}")
            return None

        upload_info = resp.json()
        upload_url = upload_info['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
        asset = upload_info['value']['asset']

        # 2. Upload binary
        with open(image_path, 'rb') as f:
            image_data = f.read()

        upload_resp = requests.put(upload_url, data=image_data, headers={'Content-Type': 'image/jpeg'}, timeout=60)
        if upload_resp.status_code not in (200, 201):
            print(f"Upload failed: {upload_resp.status_code} {upload_resp.text}")
            return None

        return asset

    except Exception as e:
        print(f"Error uploading image: {e}")
        return None

def get_person_id(access_token: str) -> Optional[str]:
    """Get the authenticated user's LinkedIn person ID."""
    try:
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
            return data.get('sub')
        return None
    except Exception:
        return None

def validate_image(image_path: str) -> bool:
    """
    Check if image file is valid for LinkedIn upload.

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
    # Quick test if image path provided
    import sys
    if len(sys.argv) < 3:
        print("Usage: python upload_media.py <image_path> <access_token>")
        sys.exit(1)

    image_path = sys.argv[1]
    token = sys.argv[2]

    if validate_image(image_path):
        print("Valid image, attempting upload...")
        asset = upload_image(image_path, token)
        if asset:
            print(f"✓ Uploaded. Asset URN: {asset}")
        else:
            print("✗ Upload failed")
    else:
        print("✗ Image validation failed")
