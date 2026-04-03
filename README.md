# OpenClaw LinkedIn Poster Skill

A robust OpenClaw skill for creating, optimizing, and publishing LinkedIn posts with text, images, and automatic best-practice formatting.

## 📦 What's Included

- `skills/linkedin-poster/` – Complete skill package
  - `SKILL.md` – Skill definition and usage guide
  - `scripts/` – Implementation (auth, posting, image upload, formatting)
  - `references/` – Setup guide and best practices

## 🚀 Quick Start

### 1. Install the Skill

Copy or symlink the skill to your OpenClaw skills directory:

```bash
cp -r skills/linkedin-poster ~/.npm-global/lib/node_modules/openclaw/skills/
# or
ln -s $(pwd)/skills/linkedin-poster ~/.npm-global/lib/node_modules/openclaw/skills/
```

Restart OpenClaw TUI to load the skill.

### 2. Configure LinkedIn API

Follow the detailed setup guide:
[skills/linkedin-poster/references/SETUP.md](skills/linkedin-poster/references/SETUP.md)

Briefly:
- Create a LinkedIn Developer app with "Share on LinkedIn" product
- Generate Client ID, Client Secret, and Access Token (`w_member_social` scope)
- Store credentials via environment variables or `~/.linkedin/config.json`

Test with:
```bash
python3 skills/linkedin-poster/scripts/test_connection.py
```

### 3. Use It

Ask your OpenClaw assistant to post:

- *"Post this to LinkedIn: [your text]"*
- *"Share this image with caption [text]"* (attach image)
- *"Draft a LinkedIn post about [topic]"*

The skill handles formatting, hashtags, and publishing automatically.

## 📚 Documentation

- **Skill usage & examples:** `skills/linkedin-poster/SKILL.md`
- **LinkedIn setup:** `skills/linkedin-poster/references/SETUP.md`
- **Best practices:** `skills/linkedin-poster/references/BEST_PRACTICES.md`
- **Troubleshooting:** See SETUP.md troubleshooting table

## ✨ Features

- Text posts (optimized for engagement)
- Image posts (upload up to 9 images)
- Link sharing (auto preview)
- Hashtag & emoji optimization
- Professional formatting
- Secure credential management

## 🐛 Known Issues

None. If you encounter problems, check SETUP.md troubleshooting section.

## 📄 License

Skill created for OpenClaw. Modify as needed for your workflow.
