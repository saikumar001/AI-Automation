#!/usr/bin/env python3
"""
Documentation summarizer: extract key sections from HTML/markdown content.
"""

import re
from typing import List

def extract_headings(content: str) -> List[str]:
    """Extract headings (lines starting with # or <h[1-6]>)."""
    headings = []
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        # Markdown headings
        if line.startswith('#'):
            # Count # depth
            depth = len(line) - len(line.lstrip('#'))
            if depth <= 3:  # Only main headings (h1-h3 equivalent)
                headings.append(line.lstrip('#').strip())
        # HTML headings (basic)
        elif re.match(r'<h[1-6][^>]*>', line, re.IGNORECASE):
            # Strip tags simply
            text = re.sub(r'<[^>]+>', '', line)
            headings.append(text.strip())
    return headings

def extract_paragraphs(content: str, max_paragraphs: int = 10) -> List[str]:
    """Extract first few meaningful paragraphs (non-empty, not too short)."""
    paragraphs = []
    # Split by double newlines (common markdown/HTML separation)
    blocks = re.split(r'\n\s*\n', content)
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        # Skip lines that are just headings (already captured)
        if block.startswith('#'):
            continue
        # Skip HTML tags only blocks
        if re.match(r'<[^>]+>.*</[^>]+>', block) and len(block) < 50:
            continue
        # Keep blocks that look like real content (have multiple words)
        words = block.split()
        if len(words) < 5:
            continue
        paragraphs.append(block)
        if len(paragraphs) >= max_paragraphs:
            break
    return paragraphs

def extract_code_blocks(content: str, max_examples: int = 3) -> List[str]:
    """Extract code blocks (indented or fenced)."""
    code_blocks = []
    lines = content.split('\n')
    in_fence = False
    current_block = []
    fence_char = '```'

    for line in lines:
        stripped = line.strip()
        if stripped.startswith(fence_char):
            if in_fence:
                # End of fenced block
                code = '\n'.join(current_block).strip()
                if code:
                    code_blocks.append(code)
                current_block = []
                in_fence = False
            else:
                # Start fenced block
                in_fence = True
        elif in_fence:
            current_block.append(line)
        elif line.startswith('    ') and not stripped.startswith('#'):
            # Indented code (4 spaces) – might be a code block
            current_block.append(line[4:])
        elif current_block:
            # End of indented block
            code = '\n'.join(current_block).strip()
            if code:
                code_blocks.append(code)
            current_block = []

    # If still in block at end
    if in_fence and current_block:
        code_blocks.append('\n'.join(current_block).strip())

    # Deduplicate and limit
    unique = []
    for cb in code_blocks:
        if cb not in unique:
            unique.append(cb)
    return unique[:max_examples]

def summarize_documentation(content: str, max_length: int = 3000) -> str:
    """
    Create a concise summary of documentation content.

    Strategy:
    1. Extract headings to show structure
    2. Extract key paragraphs (first several)
    3. Include a few code examples if present
    4. Combine into a readable summary

    Args:
        content: Full page content (markdown or simplified HTML)
        max_length: Maximum summary length

    Returns:
        Summarized text
    """
    headings = extract_headings(content)
    paragraphs = extract_paragraphs(content)
    code_blocks = extract_code_blocks(content)

    summary_parts = []

    if headings:
        summary_parts.append("**Structure:**")
        # Show top 5 headings
        for h in headings[:5]:
            summary_parts.append(f"- {h}")
        if len(headings) > 5:
            summary_parts.append(f"... and {len(headings)-5} more sections")
        summary_parts.append("")

    if paragraphs:
        summary_parts.append("**Key content:**")
        # Join first 2-3 paragraphs (already trimmed)
        para_text = ' '.join(paragraphs[:3])
        summary_parts.append(para_text)
        summary_parts.append("")

    if code_blocks:
        summary_parts.append("**Examples:**")
        for i, code in enumerate(code_blocks[:2], 1):
            # Truncate long examples
            if len(code) > 500:
                code = code[:500] + "..."
            summary_parts.append(f"```\n{code}\n```")
        summary_parts.append("")

    summary = '\n'.join(summary_parts)

    if len(summary) > max_length:
        summary = summary[:max_length-3] + "..."

    return summary.strip()

if __name__ == '__main__':
    # Quick test: read a file or stdin
    import sys
    if len(sys.argv) < 2:
        print("Usage: python summarizer.py <file>")
        sys.exit(1)

    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        content = f.read()

    print(summarize_documentation(content))
