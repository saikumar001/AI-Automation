#!/usr/bin/env python3
"""
LinkedIn post creation and publishing.
"""

import os
import json
import requests
from typing import Dict, List, Optional
from datetime import datetime

from auth import load_credentials, validate_token, get_profile_name
from upload_media import upload_image, validate_image

API_BASE = "https://api.linkedin.com/v2"

def create_text_post(text: str, access_token: str, visibility: str = "connections") -> Optional[Dict]:
    """
    Publish a text-only post to LinkedIn.

    Args:
        text: Post content (300-3000 chars)
        access_token: OAuth access token
        visibility: "connections" (default) or "public"

    Returns:
        Post response dict with 'id' and 'permalink' if successful, None otherwise
    """
    try:
        # Validate token
        if not validate_token(access_token):
            raise ValueError("Invalid or expired access token")

        # Get person ID
        person_id = get_person_id(access_token)
        if not person_id:
            raise ValueError("Could not retrieve user profile")

        # Prepare post data
        post_data = {
            "author": f"urn:li:person:{person_id}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": visibility.upper()
            }
        }

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0'
        }

        resp = requests.post(
            f"{API_BASE}/ugcPosts",
            headers=headers,
            json=post_data,
            timeout=30
        )

        if resp.status_code in (200, 201):
            result = resp.json()
            post_id = result.get('id')
            # LinkedIn API doesn't always return permalink; construct it
            permalink = f"https://www.linkedin.com/feed/update/{post_id}/"
            return {'id': post_id, 'permalink': permalink}
        else:
            print(f"Failed to create post: {resp.status_code} {resp.text}")
            return None

    except Exception as e:
        print(f"Error creating post: {e}")
        return None

def create_image_post(text: str, image_paths: List[str], access_token: str, visibility: str = "connections") -> Optional[Dict]:
    """
    Publish a post with one or more images.

    Args:
        text: Post caption
        image_paths: List of image file paths (1-9 images)
        access_token: OAuth access token
        visibility: "connections" or "public"

    Returns:
        Post response dict with 'id' and 'permalink' if successful, None otherwise
    """
    try:
        if not validate_token(access_token):
            raise ValueError("Invalid or expired access token")

        person_id = get_person_id(access_token)
        if not person_id:
            raise ValueError("Could not retrieve user profile")

        # Upload all images
        assets = []
        for img_path in image_paths:
            if not validate_image(img_path):
                print(f"Skipping invalid image: {img_path}")
                continue
            print(f"Uploading {img_path}...")
            asset_urn = upload_image(img_path, access_token, f"urn:li:person:{person_id}")
            if asset_urn:
                assets.append(asset_urn)
            else:
                print(f"Failed to upload {img_path}")

        if not assets:
            print("No images uploaded successfully")
            return None

        # Build media array for post
        media_items = []
        for i, asset in enumerate(assets):
            media_items.append({
                "status": "READY",
                "description": {
                    "text": f"Image {i+1}"
                },
                "media": asset,
                "title": {
                    "text": f"Image {i+1}"
                }
            })

        post_data = {
            "author": f"urn:li:person:{person_id}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text
                    },
                    "shareMediaCategory": "IMAGE",
                    "media": media_items
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": visibility.upper()
            }
        }

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0'
        }

        resp = requests.post(
            f"{API_BASE}/ugcPosts",
            headers=headers,
            json=post_data,
            timeout=60
        )

        if resp.status_code in (200, 201):
            result = resp.json()
            post_id = result.get('id')
            permalink = f"https://www.linkedin.com/feed/update/{post_id}/"
            return {'id': post_id, 'permalink': permalink, 'images_uploaded': len(assets)}
        else:
            print(f"Failed to create image post: {resp.status_code} {resp.text}")
            return None

    except Exception as e:
        print(f"Error creating image post: {e}")
        return None

def create_link_post(text: str, link: str, access_token: str, visibility: str = "connections") -> Optional[Dict]:
    """
    Publish a post with a link (LinkedIn will generate preview automatically).

    Args:
        text: Post caption (with or without link URL in it)
        link: URL to share (will be added to post and generates preview)
        access_token: OAuth access token
        visibility: "connections" or "public"

    Returns:
        Post response dict with 'id' and 'permalink' if successful, None otherwise
    """
    # For LinkedIn UGcPosts, just include the URL in the text and it auto-generates preview
    # However, LinkedIn API also supports a separate "shareContent" with external link
    # Simpler: just append URL to text if not already present

    full_text = text.strip()
    if link not in full_text:
        full_text = f"{full_text}\n\n{link}"

    return create_text_post(full_text, access_token, visibility)

def get_person_id(access_token: str) -> Optional[str]:
    """Helper: get LinkedIn person ID."""
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
            return data.get('sub')  # 'sub' is the person ID in userinfo response
        return None
    except Exception as e:
        print(f"Error getting person ID: {e}")
        return None

if __name__ == '__main__':
    # Simple manual test
    creds = load_credentials()
    token = creds['access_token']

    # Example: post a test message (commented out)
    # result = create_text_post("Testing LinkedIn API from OpenClaw skill 🚀 #test", token)
    # if result:
    #     print(f"Posted! {result['permalink']}")
    # else:
    #     print("Failed")

    print("This script is meant to be imported by the skill, not run directly.")
