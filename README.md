# OpenClaw Skills Collection

A curated set of OpenClaw skills for social media posting, documentation lookup, and prompt refinement.

## 📦 Skills

| Skill | Purpose | Key Features |
|-------|---------|--------------|
| `linkedin-poster` | Publish LinkedIn posts | Text, images (up to 9), hashtag optimization, best practices |
| `twitter-poster` | Publish Twitter/X posts | Text, images (up to 4), hashtag suggestions, thread support |
| `official-docs-lookup` | Find official docs | 100+ pre-indexed tech docs, web search fallback, summaries |
| `prompt-refiner` | Clarify vague requests | Interactive Q&A, category-specific questions, optimized prompt output |

## 🚀 Quick Start

### 1. Install Skills

Copy or symlink desired skills to your OpenClaw skills directory:

```bash
cp -r skills/linkedin-poster ~/.npm-global/lib/node_modules/openclaw/skills/
cp -r skills/twitter-poster ~/.npm-global/lib/node_modules/openclaw/skills/
cp -r skills/official-docs-lookup ~/.npm-global/lib/node_modules/openclaw/skills/
cp -r skills/prompt-refiner ~/.npm-global/lib/node_modules/openclaw/skills/
# Or use ln -s for development symlinks
```

Restart OpenClaw TUI to load the skills.

### 2. Configure API Credentials (Social Skills Only)

- **LinkedIn**: `skills/linkedin-poster/references/SETUP.md`
- **Twitter**: `skills/twitter-poster/references/SETUP.md`

Briefly: create Developer App, obtain tokens, store via env vars or `~/.linkedin/config.json` / `~/.twitter/config.json`.

Test:
```bash
python3 skills/linkedin-poster/scripts/test_connection.py
python3 skills/twitter-poster/scripts/test_connection.py
```

### 3. Use It

- **Social posting**: *"Post this to LinkedIn: [text]"*, *"Tweet this: [text]"*
- **Image posts**: Attach image and say *"Post this image to Twitter with caption..."*
- **Docs lookup**: *"What are the official docs for Kubernetes?"*
- **Prompt refinement**: *"Help me clarify this request: [your prompt]"* (interactive)

## 📚 Documentation

- Individual skill usage: `skills/<skill>/SKILL.md`
- Setup guides: `skills/*/references/SETUP.md`
- Best practices: `skills/*/references/BEST_PRACTICES.md`
- Question templates: `skills/prompt-refiner/references/QUESTION_TEMPLATES.md`
- Canonical URLs: `skills/official-docs-lookup/references/CANONICAL_URLS.md`

## 🏛️ Repository Structure

```
.
├── README.md
├── .gitignore
└── skills/
    ├── linkedin-poster/
    │   ├── SKILL.md
    │   ├── references/
    │   │   ├── SETUP.md
    │   │   └── BEST_PRACTICES.md
    │   └── scripts/
    │       ├── auth.py
    │       ├── format.py
    │       ├── post.py
    │       ├── setup_config.py
    │       ├── test_connection.py
    │       └── upload_media.py
    ├── twitter-poster/      (similar structure)
    ├── official-docs-lookup/
    │   ├── SKILL.md
    │   ├── references/
    │   │   └── CANONICAL_URLS.md
    │   └── scripts/
    │       ├── lookup.py
    │       └── summarizer.py
    └── prompt-refiner/
        ├── SKILL.md
        ├── references/
        │   └── QUESTION_TEMPLATES.md
        └── scripts/
            ├── refine.py
            └── question_templates.py
```

## ✨ Features Overview

- **Optimized content**: Hashtag suggestions, emoji placement, length optimization
- **Media support**: Image upload for LinkedIn and Twitter
- **Official docs**: Fast lookup from verified sources with summarization
- **Prompt quality**: Interactive refinement for ambiguous requests
- **Secure credentials**: env vars or config files with restrictive permissions
- **Comprehensive troubleshooting**: Each skill includes detailed setup help

## 📄 License

Skills created for OpenClaw. Modify and integrate as needed.
