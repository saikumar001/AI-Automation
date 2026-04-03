#!/usr/bin/env python3
import sys
sys.path.insert(0, '/home/ubuntu/.openclaw/workspace/skills/linkedin-poster/scripts')
from post import create_image_post
from auth import load_credentials

# Load credentials
creds = load_credentials()
token = creds['access_token']

# Read the post content
with open('/home/ubuntu/.openclaw/workspace/temp_linkedin_devops_post.txt', 'r') as f:
    content = f.read()

# Image path
image_path = '/home/ubuntu/.openclaw/media/inbound/file_0---f4893c57-b7f6-4745-b4c3-5ac98aab3078.jpg'

# Publish with image
result = create_image_post(content, [image_path], token, visibility='connections')
if result:
    print('✓ Image post published successfully!')
    print(f'Post URL: {result.get("permalink")}')
    print(f'Post ID: {result.get("id")}')
    print(f'Images uploaded: {result.get("images_uploaded")}')
else:
    print('✗ Post failed')
    sys.exit(1)