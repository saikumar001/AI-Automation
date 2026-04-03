# LinkedIn API Setup Guide

This document explains how to obtain LinkedIn API credentials required for this skill to function.

## Steps to Get LinkedIn API Credentials

### 1. Create a LinkedIn Developer App

1. Go to [LinkedIn Developer Portal](https://www.linkedin.com/developers/)
2. Click "Create app" (you may need to verify your LinkedIn account)
3. Fill in the required information:
   - **App name**: Your name or "My OpenClaw Bot"
   - **Company**: Select your company or "Self"
   - **Privacy policy URL**: You can use a placeholder if personal use (e.g., your website or LinkedIn profile)
   - **Business email**: Your email
   - **App logo**: Optional upload
4. Click "Create app"

### 2. Configure OAuth 2.0 Settings

After creating the app:

1. Go to the **Auth** tab
2. Under "OAuth 2.0 settings", add these **Authorized Redirect URLs**:
   ```
   http://localhost:8080/callback
   https://your-openclaw-instance.com/callback
   ```
   (Use a URL where your OpenClaw instance can receive the OAuth callback, or `http://localhost:8080/callback` for local setups)

3. Enable these **Products** (application permissions):
   - **Sign In with LinkedIn** (basic profile)
   - **Share on LinkedIn** (allows posting) → This grants `w_member_social` permission
   - *Note: Some products require LinkedIn approval; "Share on LinkedIn" is typically approved automatically for personal developer apps*

4. Save changes

### 3. Get Your Credentials

In your app dashboard, find these values:

- **Client ID** → `LINKEDIN_CLIENT_ID`
- **Client Secret** → `LINKEDIN_CLIENT_SECRET`

Keep these secure; do not share.

### 4. Generate Access Token

You need an access token with `w_member_social` scope. There are two ways:

#### Option A: Manual Token Generation (Quick, for testing)

1. In the LinkedIn Developer Portal, go to **Tools** → **Access Token** (or "OAuth 2.0 token generator").
2. Select scopes:
   - `r_liteprofile` (basic profile)
   - `w_member_social` (posting)
3. Click "Generate token"
4. Copy the token → `LINKEDIN_ACCESS_TOKEN`

**Note**: This token typically expires in 60 days. You'll need to regenerate.

#### Option B: OAuth Flow (Proper, for long-term)

Implement OAuth 2.0 authorization code flow:

1. Direct user to authorize URL:
   ```
   https://www.linkedin.com/oauth/v2/authorization
     ?response_type=code
     &client_id=YOUR_CLIENT_ID
     &redirect_uri=http://localhost:8080/callback
     &scope=r_liteprofile%20w_member_social
   ```
2. User logs in and authorizes
3. LinkedIn redirects to your callback URL with `?code=AUTHORIZATION_CODE`
4. Exchange code for token:
   ```bash
   curl -X POST https://www.linkedin.com/oauth/v2/accessToken \
     -d grant_type=authorization_code \
     -d code=AUTHORIZATION_CODE \
     -d redirect_uri=http://localhost:8080/callback \
     -d client_id=YOUR_CLIENT_ID \
     -d client_secret=YOUR_CLIENT_SECRET
   ```
5. Response contains `access_token` (and `refresh_token` if enabled)

This skill expects a **long-lived access token**. If you receive a short-lived token (60 days), you'll need to re-run the OAuth flow when it expires.

### 5. Store Credentials Securely

Choose **ONE** method:

#### Method 1: Environment Variables (Recommended for servers)
```bash
export LINKEDIN_CLIENT_ID="your-client-id"
export LINKEDIN_CLIENT_SECRET="your-client-secret"
export LINKEDIN_ACCESS_TOKEN="your-access-token"
```
Add to your shell profile (`~/.bashrc`, `~/.zshrc`) or OpenClaw's environment.

#### Method 2: Config File (Recommended for desktop)
The skill's setup script (`scripts/setup_config.py`) can create `~/.linkedin/config.json`:
```json
{
  "client_id": "your-client-id",
  "client_secret": "your-client-secret",
  "access_token": "your-access-token"
}
```
File should have permissions `600` (read/write for owner only).

#### Method 3: Provide at Runtime
When the skill runs, it will prompt you to enter credentials interactively if not found in env/config.

### 6. Test Your Setup

Run the provided test script:
```bash
python scripts/test_connection.py
```
It should print your LinkedIn profile name and confirm posting permission.

### 7. Troubleshooting

| Issue | Likely Cause | Fix |
|-------|--------------|-----|
| `401 Unauthorized` | Invalid/expired token | Regenerate access token |
| `403 Forbidden` | Missing `w_member_social` permission | Ensure "Share on LinkedIn" product is enabled in app |
| "Invalid redirect_uri" | Redirect URL mismatch | Add your callback URL to app's OAuth settings |
| "Token expired" | 60-day token expired | Regenerate token manually or redo OAuth flow |
| Cannot find products | App not reviewed/approved | "Share on LinkedIn" usually auto-approved; check app status |

### Security Checklist

- [ ] Do NOT commit credentials to git/version control
- [ ] Use environment variables or config file with `chmod 600`
- [ ] Rotate tokens periodically (every 60 days if using manual tokens)
- [ ] Limit app permissions to only `w_member_social` and `r_liteprofile`
- [ ] If sharing machine, ensure credentials are in user-owned file, not global

### LinkedIn API References

- [OAuth 2.0 Documentation](https://docs.microsoft.com/linkedin/shared/authentication/authorization-code-flow)
- [UGC Posts API](https://docs.microsoft.com/linkedin/marketing/integrations/community-management/shares/ugc-post-api)
- [Rate Limits](https://docs.microsoft.com/linkedin/shared/api-guide/concepts/rate-limits)

---

**After setup**, you can use the linkedin-poster skill. Example request:
```
"Post this to LinkedIn: 'Just shipped a new feature! #engineering'"
```

The skill will automatically load credentials from your environment/config and publish.
