# LinkedIn Poster Skill for OpenClaw

A robust, self-hosted OpenClaw skill to publish posts to LinkedIn using the official LinkedIn API.

## Features

- Post text-only updates
- Supports mentions, hashtags, and proper character limits
- Robust error handling and token validation
- Uses latest LinkedIn API requirements (`/v2/userinfo`, `X-Restli-Protocol-Version`)
- Configurable visibility (connections/public)

## Quick Start

1. **Create a LinkedIn app** in the [LinkedIn Developer Portal](https://www.linkedin.com/developers/)
   - Enable products: **Sign In with LinkedIn using OpenID Connect** and **Share on LinkedIn**
   - Set app status to **Enabled**
   - Add redirect URL: `http://localhost:8080/callback`

2. **Obtain credentials**
   - Client ID and Client Secret from the Auth tab
   - Generate a 3‑legged access token with scopes `openid`, `profile`, `w_member_social`

3. **Store credentials**
   ```bash
   mkdir -p ~/.linkedin
   cat > ~/.linkedin/config.json <<EOF
   {
     "client_id": "YOUR_CLIENT_ID",
     "client_secret": "YOUR_CLIENT_SECRET",
     "access_token": "YOUR_ACCESS_TOKEN"
   }
   EOF
   chmod 600 ~/.linkedin/config.json
   ```

4. **Test connection**
   ```bash
   cd /path/to/workspace
   python3 skills/linkedin-poster/scripts/test_connection.py
   ```

5. **Post**
   ```bash
   cd /path/to/workspace
   python3 -c "
   import sys
   sys.path.insert(0, 'skills/linkedin-poster/scripts')
   from auth import load_credentials
   from post import create_text_post
   creds = load_credentials()
   create_text_post('Your LinkedIn post text', creds['access_token'])
   "
   ```

## Files

- `skills/linkedin-poster/scripts/auth.py` – credential loading, token validation, profile fetch
- `skills/linkedin-poster/scripts/post.py` – post creation (text and images)
- `skills/linkedin-poster/scripts/upload_media.py` – image upload support
- `skills/linkedin-poster/scripts/setup_config.py` – interactive config setup
- `skills/linkedin-poster/scripts/test_connection.py` – connection test
- `skills/linkedin-poster/SKILL.md` – OpenClaw skill definition

See `LINKEDIN_SETUP_GUIDE.md` and `LINKEDIN_TROUBLESHOOTING.md` for detailed instructions and known issues.

## License

MIT – use freely.
