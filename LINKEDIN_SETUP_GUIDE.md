# LinkedIn Integration Setup Guide

This document records everything needed to set up LinkedIn posting from an OpenClaw agent using the `linkedin-poster` skill. Follow this to reproduce the environment on a new server.

---

## 1. Prerequisites

- OpenClaw installed and running
- Python 3.8+
- `pip install requests` (if not already)
- LinkedIn Developer account

---

## 2. Create LinkedIn App

1. Go to [LinkedIn Developer Portal](https://www.linkedin.com/developers/)
2. Click **Create app**
3. Fill in:
   - App name: `OpenClaw Bot` (or your choice)
   - Company: Select your company or “Self”
   - Privacy policy URL: Use placeholder if needed (e.g., your LinkedIn profile)
   - Business email: your email
4. Create app
5. In the app dashboard:
   - Go to **App Settings** → set **Application status** to **Enabled** (Live)
   - Go to **Auth** tab → add **Authorized Redirect URL**: `http://localhost:8080/callback`
   - Go to **Products** tab → enable:
     - ✅ **Sign In with LinkedIn using OpenID Connect**
     - ✅ **Share on LinkedIn**
   - Save changes

6. In **Auth** tab, note:
   - **Client ID** (e.g., `86q1bxa121vslb`)
   - **Client Secret** (click Show)

---

## 3. Generate Access Token (3‑Legged, with scopes)

**Method A – OAuth Authorization Code (recommended)**

1. Open your personal browser (not server)
2. Visit:
   ```
   https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=http://localhost:8080/callback&scope=r_liteprofile%20w_member_social%20openid
   ```
   (Replace `YOUR_CLIENT_ID`)
3. Log in, click **Allow**
4. You’ll be redirected to `localhost:8080` – page error is fine. Copy the full URL from address bar (contains `code=...`)
5. Exchange for token via curl (replace placeholders):
   ```bash
   curl -X POST https://www.linkedin.com/oauth/v2/accessToken \
     -d grant_type=authorization_code \
     -d code=PASTE_CODE_HERE \
     -d redirect_uri=http://localhost:8080/callback \
     -d client_id=YOUR_CLIENT_ID \
     -d client_secret=YOUR_CLIENT_SECRET
   ```
   Response: `{"access_token":"...","expires_in":5184000,...}`
6. Copy the `access_token` value.

**Method B – OAuth Token Generator (quicker but may produce app token)**

1. In app dashboard → **Tools** → **OAuth 2.0 token generator**
2. Select scopes: `openid`, `profile`, `w_member_social`
3. Click **Generate token**
4. Copy the token
5. If later API calls fail with 403, regenerate using Method A.

---

## 4. Store Credentials

Create config file:

```bash
mkdir -p ~/.linkedin
nano ~/.linkedin/config.json
```

Paste:

```json
{
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET",
  "access_token": "YOUR_ACCESS_TOKEN"
}
```

Set permissions (optional but recommended):

```bash
chmod 600 ~/.linkedin/config.json
```

---

## 5. Install/Verify LinkedIn‑Poster Skill

The skill should already exist in your workspace at:

```
/home/ubuntu/.openclaw/workspace/skills/linkedin-poster/
```

If not present, copy the entire directory from a backup or recreate from the script files below.

**File structure:**

```
skills/linkedin-poster/
├── SKILL.md
├── scripts/
│   ├── __init__.py
│   ├── auth.py
│   ├── post.py
│   ├── upload_media.py
│   ├── format.py
│   ├── test_connection.py
│   └── setup_config.py
└── references/
    ├── SETUP.md
    └── BEST_PRACTICES.md
```

---

## 6. Patched Skill Code (important)

The original skill had LinkedIn API version issues. The following patches were applied:

### `scripts/auth.py`

- Use `X-Restli-Protocol-Version: 2.0.0` header (not `LinkedIn-Version`)
- Call `https://api.linkedin.com/v2/userinfo` (not `/v2/me`)
- Extract name from `given_name` and `family_name` fields

**Key functions:**

```python
def validate_token(access_token: str) -> bool:
    import requests
    headers = {
        'Authorization': f'Bearer {access_token}',
        'X-Restli-Protocol-Version': '2.0.0'
    }
    resp = requests.get('https://api.linkedin.com/v2/userinfo', headers=headers, timeout=10)
    return resp.status_code == 200

def get_profile_name(access_token: str) -> Optional[str]:
    import requests
    headers = {
        'Authorization': f'Bearer {access_token}',
        'X-Restli-Protocol-Version': '2.0.0'
    }
    resp = requests.get('https://api.linkedin.com/v2/userinfo', headers=headers, timeout=10)
    if resp.status_code == 200:
        data = resp.json()
        first = data.get('given_name', '')
        last = data.get('family_name', '')
        return f"{first} {last}".strip()
    return None
```

### `scripts/post.py`

- `get_person_id()` fetches `sub` from `/v2/userinfo` to get the person URN component
- `create_text_post()` and `create_image_post()`:
  - Use `API_BASE = "https://api.linkedin.com/v2"`
  - Headers: `Authorization: Bearer <token>`, `Content-Type: application/json`, `X-Restli-Protocol-Version: 2.0.0`
  - Author URN: `urn:li:person:{person_id}`

```python
def get_person_id(access_token: str) -> Optional[str]:
    import requests
    headers = {
        'Authorization': f'Bearer {access_token}',
        'X-Restli-Protocol-Version': '2.0.0'
    }
    resp = requests.get('https://api.linkedin.com/v2/userinfo', headers=headers, timeout=10)
    if resp.status_code == 200:
        return resp.json().get('sub')
    return None
```

### `scripts/upload_media.py`

- Same `get_person_id()` update as above.

---

## 7. Test Connection

```bash
cd /home/ubuntu/.openclaw/workspace
python3 skills/linkedin-poster/scripts/test_connection.py
```

Expected output:

```
Testing LinkedIn connection...
✓ Credentials loaded
✓ Token valid - authenticated as: Your Name
```

---

## 8. Create a Post

```bash
cd /home/ubuntu/.openclaw/workspace
python3 -c "
import sys
sys.path.insert(0, 'skills/linkedin-poster/scripts')
from auth import load_credentials
from post import create_text_post

creds = load_credentials()
token = creds['access_token']
text = 'Your LinkedIn post text here.'

result = create_text_post(text, token, visibility='connections')
if result:
    print('✅ Post successful!')
    print('Post ID:', result.get('id'))
    print('Link:', result.get('permalink'))
else:
    print('❌ Failed to post')
"
```

Replace the `text` with your desired content.

---

## 9. Delete a Post

```bash
POST_ID="urn:li:share:POST_ID_HERE"
TOKEN=$(jq -r .access_token ~/.linkedin/config.json)
curl -X DELETE -H "Authorization: Bearer $TOKEN" \
     -H "X-Restli-Protocol-Version: 2.0.0" \
     "https://api.linkedin.com/v2/shares/$POST_ID" -i
```

For UGC‑style posts, the identifier is the full URN (`urn:li:share:...`). Use only the numeric part for this endpoint.

---

## 10. Important Notes

- **OAuth token lifetime**: 2 months. After expiration, generate a new token.
- **Rate limits**: Respect LinkedIn’s limits. Avoid tight loops.
- **Headers**: The `/ugcPosts` endpoint requires only `X-Restli-Protocol-Version: 2.0.0`; do not send `LinkedIn-Version` (causes `NONEXISTENT_VERSION`).
- **User ID**: Use `/v2/userinfo` → field `sub` to get the person ID; build URN as `urn:li:person:{sub}`.
- **Visibility options**: `connections` (default) or `public` (map to `CONNECTIONS`/`PUBLIC`).
- **Images**: Not covered in this brief; see `upload_media.py` for registration flow.

---

## 11. Quick Reference Commands

```bash
# Test
python3 skills/linkedin-poster/scripts/test_connection.py

# Post (inline python one‑liner)
cd /home/ubuntu/.openclaw/workspace && python3 -c "import sys; sys.path.insert(0, 'skills/linkedin-poster/scripts'); from auth import load_credentials; from post import create_text_post; creds=load_credentials(); result=create_text_post('Your text', creds['access_token']); print(result)"

# Delete
POST_ID=urn:li:share:7445944291098624000
TOKEN=$(jq -r .access_token ~/.linkedin/config.json)
curl -X DELETE -H "Authorization: Bearer $TOKEN" -H "X-Restli-Protocol-Version: 2.0.0" "https://api.linkedin.com/v2/shares/$(echo $POST_ID | cut -d: -f3)"
```

---

## 12. Automated Posts (Cron Example)

```bash
# Edit crontab
crontab -e

# Add: every day at 9 AM, send message to main OpenClaw session
0 9 * * * /usr/bin/openclaw sessions send main "Post to LinkedIn: Good morning! #DevOps #Automation"
```

Or use a script that calls `create_text_post.py` directly.

---

**Last updated:** 2026‑04‑03 (tested on Ubuntu 22.04, OpenClaw 2026.4.2)
