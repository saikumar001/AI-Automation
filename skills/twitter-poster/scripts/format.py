#!/usr/bin/env python3
"""
Twitter content formatting and optimization.
"""

import re
from typing import List

def optimize_tweet(text: str, add_hashtags: bool = True, add_cta: bool = True) -> str:
    """
    Optimize a tweet for engagement.

    Args:
        text: Raw tweet content
        add_hashtags: Whether to append suggested hashtags (1-2)
        add_cta: Whether to add a call-to-action if none present

    Returns:
        Optimized tweet text (truncated to 280 chars if needed)
    """
    # Clean up whitespace
    text = clean_text(text)

    # Truncate if over 280
    if len(text) > 280:
        text = text[:277] + "..."  # leave room for ellipsis

    # Add CTA if missing and requested
    if add_cta and not has_cta(text):
        text += "\n\nWhat do you think? Drop a reply 👇"

    # Add hashtags if requested and not already present
    if add_hashtags and not has_hashtags(text):
        suggested = suggest_hashtags(text)
        if suggested:
            # Ensure we don't exceed limit
            hashtag_str = " " + " ".join(suggested)
            if len(text) + len(hashtag_str) <= 280:
                text = text.rstrip() + hashtag_str
            else:
                # Remove CTA to fit hashtags, or truncate differently
                pass

    # Final truncate in case adding hashtags pushed it over
    if len(text) > 280:
        text = text[:277] + "..."

    return text

def clean_text(text: str) -> str:
    """Normalize whitespace."""
    text = re.sub(r'\s+', ' ', text)  # replace multiple spaces/newlines with single space
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
        'retweet',
        'like if',
        'thoughts?',
        'what about you',
        'drop a reply'
    ]
    text_lower = text.lower()
    return any(phrase in text_lower for phrase in cta_phrases)

def suggest_hashtags(text: str, num: int = 2) -> List[str]:
    """
    Suggest relevant hashtags based on text content.

    Args:
        text: Tweet content
        num: Number of hashtags to suggest (default 2 because Twitter optimal is 1-2)

    Returns:
        List of suggested hashtags
    """
    text_lower = text.lower()
    suggestions = set()

    # Keyword mapping (keyword → hashtag)
    keyword_map = {
        'python': '#Python',
        'javascript': '#JavaScript',
        'java': '#Java',
        'ai': '#AI',
        'machine learning': '#MachineLearning',
        'ml': '#ML',
        'data science': '#DataScience',
        'devops': '#DevOps',
        'cloud': '#Cloud',
        'aws': '#AWS',
        'azure': '#Azure',
        'gcp': '#GCP',
        'cyber': '#Cybersecurity',
        'security': '#Security',
        'startup': '#Startup',
        'founder': '#Founder',
        'saas': '#SaaS',
        'tech': '#Tech',
        'coding': '#Coding',
        'programming': '#Programming',
        'engineer': '#Engineering',
        'engineering': '#Engineering',
        'docker': '#Docker',
        'kubernetes': '#Kubernetes',
        'k8s': '#K8s',
        'react': '#React',
        'vue': '#Vue',
        'angular': '#Angular',
        'node': '#NodeJS',
        'opensource': '#OpenSource',
        'hiring': '#Hiring',
        'job': '#Job'
    }

    for keyword, tag in keyword_map.items():
        if keyword in text_lower and tag not in suggestions:
            suggestions.add(tag)

    # If we have no tech hashtags, add a broad #Tech or #Startup
    if not suggestions:
        suggestions.add('#Tech')

    # Fill up to num
    return list(suggestions)[:num]

def create_thread_parts(text: str, max_length: int = 280) -> List[str]:
    """
    Split a long text into thread parts.

    Args:
        text: Full content (may exceed 280)
        max_length: Max characters per tweet (including any numbering like "(1/5)")

    Returns:
        List of tweet texts (numbered (1/n), (2/n), etc.)
    """
    # If text already fits, return as single
    if len(text) <= max_length - 10:  # leave room for numbering
        return [text]

    # Split into roughly equal parts, trying to break at sentence boundaries
    sentences = re.split(r'(?<=[.!?])\s+', text)
    parts = []
    current = ""
    total_parts_estimate = max(1, len(text) // (max_length - 10)) + 1

    for sentence in sentences:
        # Account for numbering later; we'll add "(i/N) " prefix later
        candidate = (current + " " + sentence).strip() if current else sentence
        if len(candidate) <= max_length - 15:  # leave extra margin for "(x/yy) "
            current = candidate
        else:
            if current:
                parts.append(current)
            current = sentence

    if current:
        parts.append(current)

    # If we have too many parts, we may need to split sentences further
    while len(parts) > total_parts_estimate:
        # Try to recombine short parts
        new_parts = []
        i = 0
        while i < len(parts):
            if i + 1 < len(parts) and len(parts[i]) + len(parts[i+1]) < max_length - 10:
                new_parts.append(parts[i] + " " + parts[i+1])
                i += 2
            else:
                new_parts.append(parts[i])
                i += 1
        parts = new_parts

    # Apply numbering
    n = len(parts)
    for i, part in enumerate(parts, 1):
        prefix = f"({i}/{n}) "
        # If part is too long even after prefix, truncate
        if len(prefix + part) > max_length:
            available = max_length - len(prefix)
            parts[i-1] = prefix + part[:available-3] + "..."
        else:
            parts[i-1] = prefix + part

    return parts

if __name__ == '__main__':
    # Demo
    sample = "Just shipped a new Python microservice using FastAPI. It handles 10k RPS. Here's what I learned about async and event loops. Thread (1/3)."
    optimized = optimize_tweet(sample, add_hashtags=False)
    print("Original:", sample)
    print("Optimized:", optimized)
    print("Suggestions:", suggest_hashtags(sample))

    long_text = "I spent the last 6 months building a new product from scratch. Here's what I wish I knew before starting: 1) The importance of nailing the problem before building the solution. 2) How to say no to feature creep. 3) Why early adopters are everything. 4) The need for fast iteration cycles. 5) That shipping beats perfection. Each lesson cost time and money. Hope this helps other founders avoid my mistakes."
    print("\nLong text thread demo:")
    for i, part in enumerate(create_thread_parts(long_text), 1):
        print(f"{i}. ({len(part)} chars) {part[:80]}...")
