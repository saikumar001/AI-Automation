---
name: linkedin-poster
description: Create, format, and publish LinkedIn posts with proper hashtags, mentions, and media attachments. Use when asked to draft, optimize, or publish content to LinkedIn. Supports text posts, link shares, and image posts. Includes guidance on LinkedIn best practices (length, formatting, hashtags, call-to-action). Does NOT handle LinkedIn API setup - see references/SETUP.md for credential configuration.
---

# LinkedIn Poster Skill

## Overview

This skill enables creating and publishing LinkedIn posts with professional formatting, optimal hashtags, and appropriate media attachments. It handles the full workflow from drafting to publishing.

## When to Use

Use this skill when the user wants to:
- Write and publish a LinkedIn post (immediate or scheduled)
- Draft a LinkedIn post for review before posting
- Optimize existing content for LinkedIn (hashtags, length, formatting)
- Create posts with images, links, or mentions
- Get advice on LinkedIn best practices

**Do NOT use** for:
- LinkedIn profile updates (different skill needed)
- Reading LinkedIn feed/analytics (out of scope)
- Connecting with people (out of scope)
- Setting up LinkedIn API credentials (user must do this first)

## Prerequisites

Before using this skill, the user must have LinkedIn API credentials configured:
- LinkedIn Client ID
- LinkedIn Client Secret
- Access Token (with `w_member_social` permission)

See `references/SETUP.md` for detailed setup instructions.

## Configuration

The skill expects credentials in one of these locations (in order of precedence):
1. Environment variables: `LINKEDIN_CLIENT_ID`, `LINKEDIN_CLIENT_SECRET`, `LINKEDIN_ACCESS_TOKEN`
2. Config file: `~/.linkedin/config.json` (created by setup script)
3. Prompt user to provide at runtime

## Quick Start

### Draft Only (No Publishing)
```
User: Draft a LinkedIn post about my new role as a software engineer
Codex: [Creates optimized draft with hashtags, returns to user for approval]
```

### Draft and Publish
```
User: Post this to LinkedIn: "Just shipped a major feature! #engineering"
Codex: [Validates content, publishes via API, returns post URL]
```

### With Image
```
User: Post this image and caption to LinkedIn
[Attaches image file]
Codex: [Uploads image to LinkedIn, creates post with image, publishes]
```

## Core Workflows

### 1. Content Creation & Optimization
**Input**: User request + any raw content
**Process**:
- Determine post type (text, link, image)
- Apply LinkedIn best practices (300-3000 chars, line breaks, emojis sparingly)
- Suggest relevant hashtags (3-5, mix of broad + niche)
- Include call-to-action if appropriate
- Format for readability (paragraphs, not walls of text)
**Output**: Formatted draft for user review (unless auto-publish requested)

### 2. Publishing
**Input**: Approved post content + optional media
**Process**:
- Validate content meets LinkedIn requirements
- Handle media upload if images/links present
- Call LinkedIn API `POST /ugcPosts` endpoint
- Handle errors gracefully (rate limits, auth issues)
**Output**: Post URL, confirmation message

### 3. Authentication Management
- Check for valid access token
- If expired/no token, prompt user to run setup or provide credentials
- Store tokens securely (ref: `scripts/auth.py`)

## Important Constraints

- **Access token scope**: Must include `w_member_social` for posting
- **Post visibility**: Default to user's network (not public) unless specified
- **Rate limits**: LinkedIn allows ~100 posts per day per app; respect 429 responses
- **Content policy**: LinkedIn prohibits certain content (spam, hate speech, etc.) - flag risky content before attempting to post
- **Image uploads**: Must use LinkedIn's image upload API first, then reference returned asset in post

## Error Handling

Common errors to handle:
- `401 Unauthorized` → Token expired, user must re-authenticate
- `403 Forbidden` → Missing permission, check token scope
- `429 Too Many Requests` → Rate limit hit, implement exponential backoff
- `400 Bad Request` → Content validation failed (too long, invalid media, etc.)
- Network errors → Retry with backoff, report to user

## Scripts Reference

See `scripts/` for implementations:

- `auth.py` - Token management and validation
- `post.py` - Main posting logic (text, link, image)
- `format.py` - Content optimization, hashtag suggestions
- `upload_media.py` - Image/video upload to LinkedIn

## Best Practices (LinkedIn)

From `references/BEST_PRACTICES.md`:
- **Length**: 300-1300 characters optimal for engagement
- **Hashtags**: 3-5 maximum; place at end; mix reach (#technology) + niche (#PythonAsync)
- **Mentions**: Use `@` for companies/people when relevant
- **Emojis**: 1-3 max, sparingly
- **First line**: Must hook attention; appears in feed preview
- **Links**: LinkedIn previews automatically; use short, clean URLs
- **Images**: 1200x627 (1.91:1) for link previews; 1080x1080 for square posts
- **Call-to-action**: Ask a question or direct to comments for better engagement
- **Timing**: Weekdays 8-10am or 12-2pm local time typically best

## Examples

**Example 1: Simple text post**
```
User: Post "Excited to join the team at @Acme Corp! #newjourney #softwareengineer"
Codex: [Publishes immediately, returns post URL]
```

**Example 2: Draft with optimization**
```
User: Help me write a LinkedIn post about completing a marathon
Codex: Provides 2-3 draft options with hashtags, user picks one, asks "Post now?" → publishes on confirmation
```

**Example 3: Post with image**
```
User: Share this photo from the conference on LinkedIn with caption "Great talks at #TechConf2026"
[User provides image path]
Codex: Uploads image, creates post, publishes
```

**Example 4: LinkedIn article (long-form)**
```
User: Publish this as a LinkedIn article
[Provides long text > 3000 chars]
Codex: Uses LinkedIn Articles API (different endpoint), formats with headings, publishes
```

**Example 5: Schedule for later**
```
User: Schedule this post for tomorrow at 9am: [content]
Codex: [Stores scheduled time, executes at correct time via cron/background job]
```

## Limitations

- Does NOT create LinkedIn Stories or short videos
- Does NOT edit existing posts (LinkedIn API limitations)
- Does NOT manage comments/messages (separate skill)
- Does NOT read analytics/insights (separate skill)
- Image upload limited to 5MB per image (LinkedIn constraint)

## Security Notes

- Never log access tokens in plaintext
- Store credentials in secure locations (environment variables or encrypted config)
- Refresh tokens if LinkedIn issues them (current API uses long-lived tokens mostly)
- Validate user-provided content before posting to prevent accidental spam

## Future Enhancements

Potential additions:
- A/B testing multiple post variations
- Auto-scheduling based on optimal times (requires analytics)
- Post performance tracking integration
- Template library for common post types (announcements, achievements, articles)
- LinkedIn poll creation
- Video post support
