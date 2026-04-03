#!/usr/bin/env python3
"""
LinkedIn content formatting and optimization.
"""

import re
import random
from typing import List, Dict, Tuple

# Common LinkedIn hashtags by category (for suggestions)
HASHTAG_CATEGORIES = {
    'broad': [
        '#technology', '#business', '#innovation', '#leadership',
        '#startup', '#entrepreneurship', '#digital', '#growth'
    ],
    'tech': [
        '#softwareengineering', '#devops', '#python', '#javascript',
        '#ai', '#machinelearning', '#cloud', '#cybersecurity',
        '#data', '#webdevelopment', '#mobile', '#architecture'
    ],
    'industry': [
        '#fintech', '#healthtech', '#edtech', '#retail',
        '#manufacturing', '#realestate', '#marketing', '#sales'
    ],
    'career': [
        '#career', '#jobs', '#hiring', '#networking',
        '#mentorship', '#womenintech', '#diversityintech'
    ],
    'event': [
        '#conference', '#webinar', '#meetup', '#techconf',
        '#summit', '#workshop', '#hackathon'
    ]
}

def optimize_post(text: str, add_hashtags: bool = True, add_cta: bool = True) -> str:
    """
    Optimize a LinkedIn post for engagement.

    Args:
        text: Raw post content
        add_hashtags: Whether to append suggested hashtags
        add_cta: Whether to add a CTA if none present

    Returns:
        Optimized post text
    """
    # Clean up whitespace
    text = clean_text(text)

    # Check if already optimized (has line breaks, not too long)
    if len(text) > 3000:
        text = text[:3000]  # Truncate to LinkedIn limit

    # Add CTA if missing and add_cta=True
    if add_cta and not has_cta(text):
        text += "\n\nWhat are your thoughts? Share in the comments below."

    # Add hashtags if requested and not already present
    if add_hashtags and not has_hashtags(text):
        suggested = suggest_hashtags(text)
        if suggested:
            text = text.rstrip() + "\n\n" + " ".join(suggested)

    return text

def clean_text(text: str) -> str:
    """Normalize whitespace and remove trailing spaces."""
    # Replace multiple newlines with max 2
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Strip trailing/leading whitespace
    return text.strip()

def has_hashtags(text: str) -> bool:
    """Check if text already contains hashtags."""
    return bool(re.search(r'#\w+', text))

def has_cta(text: str) -> bool:
    """Check if text contains a call-to-action phrase."""
    cta_phrases = [
        'what do you think',
        'share your thoughts',
        'let me know',
        'comment below',
        'agree or disagree',
        'dm me',
        'repost',
        'anyone else',
        'thoughts?'
    ]
    text_lower = text.lower()
    return any(phrase in text_lower for phrase in cta_phrases)

def suggest_hashtags(text: str, num: int = 5) -> List[str]:
    """
    Suggest relevant hashtags based on text content.

    Simple keyword-based matching. Could be enhanced with NLP or external API.

    Args:
        text: Post content
        num: Number of hashtags to suggest (default 5)

    Returns:
        List of suggested hashtags (no duplicates)
    """
    text_lower = text.lower()
    suggestions = set()

    # Keyword mapping (keyword → hashtag)
    keyword_map = {
        'python': '#python',
        'javascript': '#javascript',
        'java': '#java',
        'ai': '#ai',
        'machine learning': '#machinelearning',
        'ml': '#machinelearning',
        'data science': '#data',
        'devops': '#devops',
        'cloud': '#cloud',
        'aws': '#cloud',
        'azure': '#cloud',
        'gcp': '#cloud',
        'cyber': '#cybersecurity',
        'security': '#cybersecurity',
        'startup': '#startup',
        'entrepreneur': '#entrepreneurship',
        'leadership': '#leadership',
        'marketing': '#marketing',
        'sales': '#sales',
        'hiring': '#hiring',
        'job': '#jobs',
        'tech': '#technology',
        'engineering': '#softwareengineering',
        'software': '#softwareengineering',
        'conference': '#conference',
        'webinar': '#webinar',
        'meetup': '#meetup'
    }

    for keyword, tag in keyword_map.items():
        if keyword in text_lower and tag not in suggestions:
            suggestions.add(tag)

    # Always include at least one broad tech hashtag if none from tech categories
    if not any(tag in suggestions for tag in HASHTAG_CATEGORIES['tech']):
        suggestions.add(random.choice(HASHTAG_CATEGORIES['tech'][:2]))

    # Fill up to `num` with broad picks if we're short
    broad_pool = [h for h in HASHTAG_CATEGORIES['broad'] if h not in suggestions]
    while len(suggestions) < num and broad_pool:
        suggestions.add(broad_pool.pop(0))

    return list(suggestions)[:num]

def format_post_with_media(text: str, image_paths: List[str] = None) -> Dict:
    """
    Prepare post content with media references.

    Args:
        text: Post text
        image_paths: List of image file paths (will be uploaded separately)

    Returns:
        Dict with keys: 'text', 'images' (list of paths), 'num_images'
    """
    return {
        'text': optimize_post(text),
        'images': image_paths or [],
        'num_images': len(image_paths) if image_paths else 0
    }

def truncate_for_preview(text: str, max_length: int = 200) -> str:
    """
    Truncate text to a preview length, adding ellipsis if needed.
    Useful for user confirmation before posting.
    """
    if len(text) <= max_length:
        return text
    return text[:max_length].rstrip() + "..."

if __name__ == '__main__':
    # Demo
    sample = "Just shipped a new Python microservice using FastAPI. It handles 10k RPS. Here's what I learned about async... #python #coding"
    optimized = optimize_post(sample, add_hashtags=False)
    print("Original:", sample)
    print("Optimized:", optimized)
    print("Suggestions:", suggest_hashtags(sample))
