#!/usr/bin/env python3
"""
Official documentation lookup: search for and fetch authoritative docs.
"""

import csv
import os
from pathlib import Path
from typing import Optional, Tuple
import web_search
import web_fetch

# Path to canonical URLs index (optional)
CANONICAL_CSV = Path(__file__).parent.parent / 'references' / 'CANONICAL_URLS.md'

def load_canonical_urls() -> dict:
    """
    Load pre-indexed canonical documentation URLs from CSV format.
    Expected columns: technology,url
    Returns: dict mapping lowercase technology name to URL
    """
    mapping = {}
    if CANONICAL_CSV.exists():
        try:
            with open(CANONICAL_CSV, 'r', encoding='utf-8') as f:
                # Skip header lines starting with # or empty
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    # Parse CSV line
                    parts = next(csv.reader([line]))
                    if len(parts) >= 2:
                        tech, url = parts[0].strip().lower(), parts[1].strip()
                        mapping[tech] = url
        except Exception as e:
            print(f"Warning: could not load canonical URLs: {e}")
    return mapping

def find_official_docs(technology: str, topic: Optional[str] = None) -> Tuple[str, str]:
    """
    Determine the best URL for official documentation.

    Args:
        technology: Name of the technology (e.g., "React", "pandas")
        topic: Optional specific topic (e.g., "hooks", "DataFrame")

    Returns:
        (technology, url) tuple. URL may come from canonical index or search.
    """
    canonical = load_canonical_urls()
    tech_key = technology.strip().lower()

    # Check canonical index first
    if tech_key in canonical:
        return technology, canonical[tech_key]

    # If topic provided, maybe there's a specific canonical entry
    if topic:
        combined_key = f"{technology} {topic}".lower()
        if combined_key in canonical:
            return technology, canonical[combined_key]

    # Fall back to web search to find official docs
    query = f"official {technology} documentation"
    if topic:
        query += f" {topic}"
    print(f"Searching: {query}")
    results = web_search(query=query, count=10, safeSearch='moderate')

    # Score results: prefer official domains
    official_domains = [
        technology.lower() + '.dev',
        technology.lower() + '.org',
        technology.lower() + '.com',
        'docs.' + technology.lower(),
        'developer.' + technology.lower(),
        'api.' + technology.lower(),
        'platform.' + technology.lower(),
    ]
    # Also known official hosts
    trusted_hosts = [
        'mdn.io',
        'developer.mozilla.org',
        'readthedocs.io',
        'readthedocs.org',
        'gitbook.io',
        'github.io',
        'godoc.org',
        'pkg.go.dev',
        'pypi.org',
        'stackoverflow.com'  # not official but often used
    ]

    # Find first result that looks official
    for result in results:
        url = result.get('url', '').lower()
        title = result.get('title', '').lower()
        snippet = result.get('snippet', '').lower()

        # Check if URL matches official patterns
        for domain in official_domains + trusted_hosts:
            if domain in url:
                return technology, result['url']

        # Look for "official" in title/snippet
        if 'official' in title or 'official' in snippet:
            return technology, result['url']

    # If no great match, return the first result anyway
    if results:
        return technology, results[0]['url']

    raise ValueError(f"Could not find documentation for {technology}")

def fetch_and_summarize(url: str, max_chars: int = 4000) -> str:
    """
    Fetch a documentation page and return a summary excerpt.

    Args:
        url: Documentation page URL
        max_chars: Maximum characters to return

    Returns:
        Extracted text content (truncated if needed)
    """
    print(f"Fetching: {url}")
    content = web_fetch(url=url, extractMode='markdown', maxChars=max_chars)
    return content.get('text', '')

def format_response(technology: str, url: str, summary: str) -> str:
    """
    Format the final response to the user.
    """
    # Truncate summary if too long
    if len(summary) > 3000:
        summary = summary[:3000] + "... [truncated]"

    response = f"""**Official Docs: {technology}**

**Source:** {url}

**What's covered:**
{summary[:1500]}...

**Direct link:** {url}

(Visit the link for the complete, up-to-date documentation.)
"""
    return response

def lookup(technology: str, topic: Optional[str] = None) -> str:
    """
    Main entry point: find official docs for a technology and return summary.

    Args:
        technology: Name of the technology (e.g., "React", "Python pandas")
        topic: Optional specific topic (e.g., "hooks", "DataFrame")

    Returns:
        Formatted response string with summary and link
    """
    try:
        tech, url = find_official_docs(technology, topic)
        summary = fetch_and_summarize(url)
        return format_response(tech, url, summary)
    except Exception as e:
        return f"❌ Error looking up documentation: {e}"

if __name__ == '__main__':
    # Simple CLI test
    import sys
    if len(sys.argv) < 2:
        print("Usage: python lookup.py <technology> [topic]")
        sys.exit(1)

    tech = sys.argv[1]
    topic = sys.argv[2] if len(sys.argv) > 2 else None

    print(lookup(tech, topic))
