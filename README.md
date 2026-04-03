# OpenClaw Social Media Poster Skills

A collection of OpenClaw skills for publishing professional social media content with automatic best‑practice formatting.

## 📦 What's Included

- `skills/linkedin-poster/` – LinkedIn posting skill (text, images, links)
- `skills/twitter-poster/` – Twitter/X posting skill (text, images)

Each skill contains:
- `SKILL.md` – Skill definition and usage guide
- `scripts/` – Implementation (auth, posting, image upload, formatting)
- `references/` – Setup guide and best practices

## 🚀 Quick Start

### 1. Install a Skill

Copy or symlink the skill to your OpenClaw skills directory:

```bash
cp -r skills/linkedin-poster ~/.npm-global/lib/node_modules/openclaw/skills/
# or
ln -s $(pwd)/skills/linkedin-poster ~/.npm-global/lib/node_modules/openclaw/skills/
```

Repeat for `twitter-poster` if desired.

Restart OpenClaw TUI to load the skill.

### 2. Configure API Credentials

Each skill requires its own API credentials.

- **LinkedIn**: Follow `skills/linkedin-poster/references/SETUP.md`
- **Twitter**: Follow `skills/twitter-poster/references/SETUP.md`

Briefly:
- Create a Developer App on the platform
- Enable required permissions (Share on LinkedIn; Read & Write for Twitter)
- Generate Access Token with appropriate scopes
- Store credentials via environment variables or `~/.platform/config.json`

Test with:
```bash
python3 skills/linkedin-poster/scripts/test_connection.py
python3 skills/twitter-poster/scripts/test_connection.py
```

### 3. Use It

Ask your OpenClaw assistant to post:

- *"Post this to LinkedIn: [your text]"*
- *"Tweet this: [your text]"*
- *"Share this image on Twitter with caption [text]"* (attach image)

The skill handles formatting, hashtags, media upload, and publishing.

## 📚 Documentation

- **LinkedIn usage:** `skills/linkedin-poster/SKILL.md`
- **Twitter usage:** `skills/twitter-poster/SKILL.md`
- **Setup guides:** `skills/*/references/SETUP.md`
- **Best practices:** `skills/*/references/BEST_PRACTICES.md`

## ✨ Features

- Optimized content (hashtag suggestions, emoji placement, length)
- Image upload support (LinkedIn: up to 9 images; Twitter: up to 4)
- Link previews (LinkedIn auto‑generates; Twitter auto‑generates)
- Secure credential management (env vars or config files)
- Comprehensive troubleshooting in setup docs

## 🐛 Issues

See the `SETUP.md` troubleshooting sections for each skill.

## 📄 License

Skills created for OpenClaw. Modify as needed for your workflow.
