---
name: twitter-poster
description: Create, format, and publish posts to Twitter/X with optimal hashtags, mentions, and media attachments. Use when asked to draft, optimize, or publish content to Twitter. Supports text tweets, image posts, and polls. Includes guidance on Twitter best practices (character limits, hashtag strategy, timing, engagement). Does NOT handle Twitter API setup - see references/SETUP.md for credential configuration.
---

# Twitter Poster Skill

## Overview

This skill enables creating and publishing Twitter/X posts with proper formatting, hashtag strategy, and media attachments (images, GIFs). It handles the full workflow from drafting to publishing.

## When to Use

Use this skill when the user wants to:
- Write and publish a tweet (immediate)
- Draft a tweet for review before posting
- Optimize existing content for Twitter (hashtags, mentions, length)
- Create posts with images or GIFs
- Get advice on Twitter best practices (timing, thread formatting)

**Do NOT use** for:
- Twitter profile updates (different skill needed)
- Reading timeline or analytics (out of scope)
- Managing DMs or interactions (out of scope)
- Setting up Twitter API credentials (user must do this first)

## Prerequisites

Before using this skill, the user must have Twitter API v2 credentials configured:
- Twitter API Key & Secret (OAuth 1.0a user context)
- Access Token & Secret (with `tweet.write` permission)
- Optional: Bearer token for read operations (not needed for posting)

See `references/SETUP.md` for detailed setup instructions.

## Configuration

The skill expects credentials in one of these locations (in order of precedence):
1. Environment variables:
   - `TWITTER_API_KEY`
   - `TWITTER_API_SECRET`
   - `TWITTER_ACCESS_TOKEN`
   - `TWITTER_ACCESS_TOKEN_SECRET`
2. Config file: `~/.twitter/config.json` (created by setup script)
3. Prompt user to provide at runtime

## Quick Start

### Draft Only (No Publishing)
```
User: Draft a tweet about our new Python library release
Codex: [Creates optimized draft with hashtags, returns for approval]
```

### Draft and Publish
```
User: Tweet this: "Just shipped v2.0! 🚀 New features: async support, 10x faster tests. #Python #OpenSource"
Codex: [Validates content, publishes via API, returns tweet URL]
```

### With Image
```
User: Post this screenshot to Twitter with caption "Bug squashed! Here's the fix in action"
[Attaches image file]
Codex: [Uploads image, creates tweet with media, publishes]
```

## Core Workflows

### 1. Content Creation & Optimization
**Input**: User request + any raw content
**Process**:
- Ensure tweet fits 280 characters (or split into thread)
- Apply Twitter best practices (hashtags 1-3, mentions if relevant, emojis okay)
- Suggest trending/complementary hashtags
- Format for readability (short lines, clear call-to-action)
**Output**: Formatted draft for user review (unless auto-publish requested)

### 2. Publishing
**Input**: Approved tweet content + optional media
**Process**:
- Validate content meets Twitter requirements (length, no duplicate posts if desired)
- Handle media upload (images up to 5MB, GIFs) via Twitter's media/upload endpoint
- Call Twitter API `POST /2/tweets` endpoint
- Handle errors gracefully (rate limits, duplicate content, auth issues)
**Output**: Tweet URL, confirmation message

### 3. Authentication Management
- Check for valid access tokens (OAuth 1.0a signing)
- If missing/invalid, prompt user to run setup or provide credentials
- Store tokens securely (ref: `scripts/auth.py`)

## Important Constraints

- **Character limit**: 280 characters for standard tweets; threads possible but not auto-chained (would require separate skill enhancement)
- **Access token scope**: Must include `tweet.write` (and `users.read` for user info)
- **Rate limits**: Twitter API v2: 300 tweets per 3 hours for user auth (typical); respect 429 responses
- **Media**: Images up to 5MB (JPG/PNG), GIFs up to 15MB; up to 4 images per tweet
- **Duplicate content**: Twitter may reject identical tweets; skill can detect and warn user

## Error Handling

Common errors to handle:
- `401 Unauthorized` → Invalid/expired tokens, regenerate
- `403 Forbidden` → Missing permission, check token scope
- `429 Too Many Requests` → Rate limit hit; implement backoff and inform user
- `400 Bad Request` → Content validation failed (too long, duplicate, invalid media)
- `403 Duplicate content` → Twitter rejects identical tweet; suggest slight variation

## Scripts Reference

See `scripts/` for implementations:

- `auth.py` - Twitter OAuth 1.0a credential loading and validation
- `post.py` - Main posting logic (text tweets, media tweets)
- `format.py` - Content optimization, hashtag suggestions, thread creation
- `upload_media.py` - Image/GIF upload to Twitter
- `setup_config.py` - Interactive credential setup wizard
- `test_connection.py` - Verify credentials and posting permission

## Best Practices (Twitter)

From `references/BEST_PRACTICES.md`:
- **Length**: 70–100 characters ideal for engagement; 280 max
- **Hashtags**: 1–2 max; place at end; over‑tagging reduces engagement
- **Mentions (@)**: Use to tag relevant accounts; increases reach but be genuine
- **Emojis**: 1–3 adds personality; excessive looks spammy
- **First line**: Must hook — appears in timeline and notifications
- **Images**: 1200x675 (16:9) optimal; add alt text for accessibility
- **GIFs**: Use sparingly for emphasis; larger file size
- **Timing**: Weekdays 9–11am and 1–3pm local time typically best
- **Engagement bait**: Avoid "RT if you agree", "Like this post" — Twitter algorithm may demote
- **Threads**: Use (1/…), (2/…) numbering for multi-part stories; each tweet should standalone somewhat

## Examples

**Example 1: Simple tweet**
```
User: Tweet: "New blog post: How we scaled to 100k users. Link: https://example.com/blog"
Codex: Publishes immediately
```

**Example 2: Thread draft**
```
User: Create a Twitter thread about 5 lessons from scaling our startup
Codex: Produces 5 numbered tweets, each with hashtag, offers to publish all or review individually
```

**Example 3: Image tweet**
```
User: Post this chart showing our growth with caption "Q3 was insane! 📈"
[Attach image]
Codex: Uploads image, publishes tweet with image
```

**Example 4: Hashtag optimization**
```
User: Tweet about our open source release but make it catchy
Codex: Drafts: "We're open sourcing our internal tools! 🎉 Now anyone can build like we do. #OpenSource #DevTools #GitHub"
```

## Limitations

- Does NOT schedule tweets for future times (would require cron integration; can be added)
- Does NOT create Twitter polls (separate API endpoint; possible extension)
- Does NOT read timeline/mentions/DMs (out of scope)
- Threads are individual tweets; no automatic numbering thread chain
- Video posts not supported (could be added with media_category=“tweet_video”)

## Security Notes

- Twitter uses OAuth 1.0a; never log access tokens or secrets
- Store credentials in environment variables or encrypted config (`chmod 600`)
- Be mindful of rate limits; avoid retry storms on 429
- Validate user-provided media before upload (file type, size)

## Future Enhancements

- Schedule tweets for optimal times (integrate with calendar/analytics)
- Automatic thread creation from long-form content
- Poll creation support
- Video upload support
- Analytics fetch and performance suggestions
- Auto-retweet/quote-tweet based on keywords

## License

Skill created for OpenClaw. Modify as needed.
