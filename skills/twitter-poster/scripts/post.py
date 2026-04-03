#!/usr/bin/env python3
"""
Twitter posting and publishing.
"""

import os
import requests
from requests_oauthlib import OAuth1
from typing import Dict, List, Optional

from auth import load_credentials, validate_token, get_username
from upload_media import upload_media

API_BASE = "https://api.twitter.com/2"

def create_tweet(text: str, credentials: Dict[str, str], media_ids: Optional[List[str]] = None, reply_settings: Optional[str] = None, in_reply_to_tweet_id: Optional[str] = None) -> Optional[Dict]:
    """
    Publish a tweet to Twitter.

    Args:
        text: Tweet content (must be <= 280 chars)
        credentials: OAuth 1.0a credentials dict
        media_ids: List of media IDs to attach (from upload_media)
        reply_settings: "following" or "everyone" (optional)
        in_reply_to_tweet_id: ID of tweet to reply to (optional)

    Returns:
        Tweet response dict with 'id' and 'url' if successful, None otherwise
    """
    try:
        # Validate token
        if not validate_token(credentials):
            raise ValueError("Invalid or expired credentials")

        # Prepare payload
        payload = {
            "text": text
        }

        if media_ids:
            payload["media"] = {"media_ids": media_ids}

        if reply_settings:
            payload["reply_settings"] = reply_settings

        if in_reply_to_tweet_id:
            payload["reply"] = {"in_reply_to_tweet_id": in_reply_to_tweet_id}

        auth = OAuth1(
            credentials['api_key'],
            credentials['api_secret'],
            credentials['access_token'],
            credentials['access_token_secret']
        )

        headers = {
            'Content-Type': 'application/json'
        }

        resp = requests.post(
            f"{API_BASE}/tweets",
            json=payload,
            auth=auth,
            headers=headers,
            timeout=30
        )

        if resp.status_code in (200, 201):
            result = resp.json()
            tweet_id = result.get('data', {}).get('id')
            username = get_username(credentials) or ''
            if tweet_id and username:
                url = f"https://twitter.com/{username}/status/{tweet_id}"
            else:
                url = None
            return {'id': tweet_id, 'url': url, 'data': result.get('data')}
        else:
            print(f"Failed to create tweet: {resp.status_code} {resp.text}")
            return None

    except Exception as e:
        print(f"Error creating tweet: {e}")
        return None

def create_tweet_with_image(text: str, image_paths: List[str], credentials: Dict[str, str]) -> Optional[Dict]:
    """
    Publish a tweet with one or more images.

    Args:
        text: Tweet caption
        image_paths: List of image file paths (1–4 images)
        credentials: OAuth 1.0a credentials

    Returns:
        Tweet response dict if successful, None otherwise
    """
    try:
        # Upload all images first
        media_ids = []
        for img_path in image_paths:
            media_id = upload_media(img_path, credentials)
            if media_id:
                media_ids.append(media_id)
            else:
                print(f"Failed to upload {img_path}")

        if not media_ids:
            print("No images uploaded successfully")
            return None

        # Create tweet with media_ids
        return create_tweet(text, credentials, media_ids=media_ids)

    except Exception as e:
        print(f"Error creating image tweet: {e}")
        return None

def delete_tweet(tweet_id: str, credentials: Dict[str, str]) -> bool:
    """
    Delete a tweet.

    Args:
        tweet_id: The Twitter tweet ID (not full URL)
        credentials: OAuth 1.0a credentials

    Returns:
        True if deleted, False otherwise
    """
    try:
        auth = OAuth1(
            credentials['api_key'],
            credentials['api_secret'],
            credentials['access_token'],
            credentials['access_token_secret']
        )

        resp = requests.delete(
            f"{API_BASE}/tweets/{tweet_id}",
            auth=auth,
            timeout=30
        )

        return resp.status_code in (200, 204)
    except Exception as e:
        print(f"Error deleting tweet: {e}")
        return False

if __name__ == '__main__':
    # Manual test (commented out to avoid accidental posting)
    creds = load_credentials()
    # result = create_tweet("Testing Twitter API from OpenClaw skill 🚀 #testing", creds)
    # if result:
    #     print(f"Tweeted! URL: {result['url']}")
    # else:
    #     print("Failed")
    print("This script is meant to be imported by the skill, not run directly.")
