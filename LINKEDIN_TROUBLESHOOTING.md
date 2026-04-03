# LinkedIn Integration – Troubleshooting & Errors Found

This log captures the specific errors we encountered and how we fixed them. Keep this alongside the setup guide to avoid repeating work.

---

## 1. Error: `403 ACCESS_DENIED – Not enough permissions to access: me.GET.NO_VERSION`

**Cause:** Using `https://api.linkedin.com/v2/me` endpoint without proper version header or with wrong header.

**Initial wrong approach:**
- Header used: `LinkedIn-Version: 202603`
- Endpoint: `/v2/me`

**Fix discovered:** LinkedIn now expects either:
- Omit `LinkedIn-Version` and use `X-Restli-Protocol-Version: 2.0.0`
- But `/v2/me` may still fail because it requires `openid` scope and the endpoint is being phased out.

Better: Use `/v2/userinfo` with `X-Restli-Protocol-Version` header.

---

## 2. Error: `426 NONEXISTENT_VERSION – Requested version 20260301 is not active`

**Cause:** Using `LinkedIn-Version` header with a future or inactive version number. LinkedIn rejects versions that are not yet active or have been retired.

**What happened:** We tried `LinkedIn-Version: 202603`, `202604`, `202402`, `202404` and all returned non‑existent.

**Fix:** Do not send `LinkedIn-Version` for `/ugcPosts` endpoint. Only send `X-Restli-Protocol-Version: 2.0.0`.

---

## 3. Error: `403 ACCESS_DENIED – Not enough permissions to access: userinfo.GET.NO_VERSION`

**Cause:** Missing `X-Restli-Protocol-Version` header on the `/v2/userinfo` request.

**Fix:** Include header `X-Restli-Protocol-Version: 2.0.0` when calling `/v2/userinfo`.

---

## 4. Token Scope Issues

Initially, the token generator produced an **app access token** (client credentials flow) instead of a **3‑legged user token**. This caused `/me` or `/userinfo` to return 403/401.

**Fix:** Ensure token is 3‑legged:
- Either use OAuth Authorization Code flow with redirect
- Or in token generator, select `openid`, `profile`, `w_member_social` scopes and generate.

---

## 5. Required Scopes

For posting on behalf of a user:
- `w_member_social` (mandatory)
- `r_liteprofile` or `profile` (to read user info)
- `openid` (required to call `/v2/userinfo`)

If any scope missing, API returns 403.

---

## 6. Final Working Configuration

### Headers to use:

**For GET `/v2/userinfo` (to fetch user profile and ID):**
```
Authorization: Bearer <access_token>
X-Restli-Protocol-Version: 2.0.0
```

**For POST `/v2/ugcPosts` (to create a post):**
```
Authorization: Bearer <access_token>
Content-Type: application/json
X-Restli-Protocol-Version: 2.0.0
```

**Do NOT send** `LinkedIn-Version` header for posting.

---

## 7. API Endpoints Used

| Purpose | Endpoint | Required headers |
|---------|----------|------------------|
| Validate token / get profile name | `GET https://api.linkedin.com/v2/userinfo` | `Authorization`, `X-Restli-Protocol-Version: 2.0.0` |
| Get person ID (for author URN) | `GET https://api.linkedin.com/v2/userinfo` | same as above; read field `sub` |
| Create text post | `POST https://api.linkedin.com/v2/ugcPosts` | `Authorization`, `Content-Type: application/json`, `X-Restli-Protocol-Version: 2.0.0` |
| Delete post | `DELETE https://api.linkedin.com/v2/shares/{shareId}` | `Authorization`, `X-Restli-Protocol-Version: 2.0.0` |
| (Upload image – separate flow) | `POST https://api.linkedin.com/rest/assets?action=registerUpload` ... | `Authorization`, `X-Restli-Protocol-Version: 2.0.0` |

---

## 8. Reference from GitHub

The issue that led to these fixes:  
https://github.com/linkedin-developers/linkedin-api-js-client/issues/35

Key points from that thread:
- Use `/v2/userinfo` instead of `/v2/me`
- Required header: `X-Restli-Protocol-Version: 2.0.0`
- User ID (`sub`) from `/userinfo` response → `urn:li:person:{sub}`
- Some users still get `userinfo.GET.NO_VERSION` when header missing

---

## 9. Skill File Changes Summary

### `scripts/auth.py`
- `validate_token()`: uses `/v2/userinfo`, header `X-Restli-Protocol-Version: 2.0.0`
- `get_profile_name()`: reads `given_name`/`family_name` from `/v2/userinfo` response

### `scripts/post.py`
- `API_BASE = "https://api.linkedin.com/v2"` (changed from `/rest`)
- `get_person_id()`: calls `/v2/userinfo`, returns `sub`
- `create_text_post()`: headers include `X-Restli-Protocol-Version: 2.0.0` (removed `LinkedIn-Version`)
- `create_image_post()`: same header

### `scripts/upload_media.py`
- `get_person_id()`: same as above

---

## 10. Quick Command to Test Headers

```bash
TOKEN=$(jq -r .access_token ~/.linkedin/config.json)
# Test with X-Restli-Protocol-Version only
curl -i -H "Authorization: Bearer $TOKEN" -H "X-Restli-Protocol-Version: 2.0.0" "https://api.linkedin.com/v2/userinfo"
```

If this returns 200 and JSON with `sub`, you’re good.

---

## 11. Common Pitfalls

- Sending `LinkedIn-Version` header causes `NONEXISTENT_VERSION`
- Using `/v2/me` returns 403 unless very old token with correct scopes
- Using token from “Access Token” generator may be an app token; confirm by decoding JWT (`.` split 3 parts)
- If `userinfo` returns 403 with `NO_VERSION` -> double‑check `X-Restli-Protocol-Version` header spelling
- LinkedIn may block server IPs (451) – perform OAuth from personal device

---

**Last updated:** 2026‑04‑03
