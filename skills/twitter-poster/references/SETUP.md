# Twitter API Setup Guide

This document explains how to obtain Twitter API v2 credentials required for this skill to function.

## Steps to Get Twitter API Credentials

### 1. Create a Twitter Developer Project & App

1. Go to [Twitter Developer Portal](https://developer.twitter.com/)
2. Sign in with your Twitter account
3. Click **"Projects & Apps"** → **"Create Project"**
   - **Project name**: Your name or "OpenClaw Bot"
   - **Description**: "Automated posting for my OpenClaw assistant"
   - **Use case**: "Automation" or "Bots"
4. Create an **App** within the project:
   - **App name**: e.g., "OpenClaw Twitter Poster"
   - **App permissions**: Choose **"Read and Write"** (this enables `tweet.write`)
   - **Environment**: Development
5. Note your **API Key** and **API Secret Key** (these are Consumer Key/Secret)

### 2. Configure OAuth 1.0a Settings

In your App settings:

1. Under **"Authentication Settings"** or **"User authentication settings"**:
   - Enable **OAuth 1.0a** (required for user context posting)
   - **Callback URLs**: Add `http://localhost:8080/callback` (or your OpenClaw callback URL if different)
   - **Website URL**: Your website or placeholder (e.g., `http://localhost`)
2. Save changes

### 3. Generate Access Token & Secret

In your App dashboard:

1. Go to **"Keys and tokens"** tab
2. Under **"Access token & secret"**, click **"Generate"** (if not already generated)
3. Copy:
   - **Access Token**
   - **Access Token Secret**

These tokens represent the Twitter user who will post. They must have **write** permission.

### 4. Store Credentials Securely

Choose **ONE** method:

#### Method 1: Environment Variables (recommended for servers)
```bash
export TWITTER_API_KEY="your-api-key"
export TWITTER_API_SECRET="your-api-secret"
export TWITTER_ACCESS_TOKEN="your-access-token"
export TWITTER_ACCESS_TOKEN_SECRET="your-access-token-secret"
```
Add to your shell profile (`~/.bashrc`, `~/.zshrc`) or OpenClaw's environment.

#### Method 2: Config File (recommended for desktop)
The skill's setup script (`scripts/setup_config.py`) can create `~/.twitter/config.json`:
```json
{
  "api_key": "your-api-key",
  "api_secret": "your-api-secret",
  "access_token": "your-access-token",
  "access_token_secret": "your-access-token-secret"
}
```
File should have permissions `600` (read/write for owner only).

#### Method 3: Provide at Runtime
If credentials not found, the skill will prompt you to enter them interactively.

### 5. Test Your Setup

Run the provided test script:
```bash
python scripts/test_connection.py
```
It should:
- Load credentials
- Verify they work by fetching your user profile
- Confirm posting permission

### 6. Troubleshooting

| Issue | Likely Cause | Fix |
|-------|--------------|-----|
| `401 Unauthorized` | Invalid or expired tokens | Regenerate Access Token & Secret |
| `403 Forbidden` | App permissions are "Read-only" | Set App permissions to "Read and Write" and regenerate tokens |
| "Invalid or expired token" on upload | OAuth signature mismatch | Ensure using OAuth 1.0a (not Bearer token) for posting |
| `429 Too Many Requests` | Rate limit exceeded | Twitter user auth limit: 300 tweets per 3 hours. Wait or reduce posting frequency |
| "Could not authenticate" | Callback URL mismatch | Add your callback URL to App's OAuth settings |
| Media upload fails | File too large or wrong format | Images: <5MB, JPG/PNG; GIFs: <15MB |

### Security Checklist

- [ ] Do **NOT** commit credentials to git/version control
- [ ] Use environment variables or config file with `chmod 600`
- [ ] Regenerate tokens if you suspect compromise
- [ ] Limit app permissions to only `Tweet.write` and `Users.read`
- [ ] If sharing machine, ensure credentials are in user-owned file, not global

### Twitter API References

- [OAuth 1.0a Documentation](https://developer.twitter.com/en/docs/authentication/oauth-1-0a)
- [Tweet POST endpoint](https://developer.twitter.com/en/docs/twitter-api/tweets/manage-tweets/api-reference/post-tweets)
- [Media upload endpoint](https://developer.twitter.com/en/docs/twitter-api/media/upload-media/api-reference/post-media-upload)
- [Rate limits](https://developer.twitter.com/en/docs/twitter-api/rate-limits)

---

**After setup**, you can use the twitter-poster skill. Example request:
```
"Tweet this: 'Just shipped a new feature! #dev #opensource'"
```

The skill will automatically load credentials and publish.
