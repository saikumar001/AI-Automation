---
name: official-docs-lookup
description: Search for and retrieve official documentation for any technology (APIs, frameworks, LLMs, tools). Use when user asks for official docs, reference materials, or authoritative guides. The skill searches the web for official sources, fetches the most relevant documentation page, and returns a summary with links. Prioritizes .org, .io, official vendor domains, and well-known docs hosts (MDN, ReadTheDocs, etc.). For known popular technologies, can also direct to pre-indexed canonical URLs.
---

# Official Docs Lookup Skill

## Overview

This skill helps you quickly find and access official documentation for any software, API, framework, or tool. It performs targeted web searches to locate authoritative sources, fetches the most relevant page, and summarizes the key information with direct links for further reading.

## When to Use

Use this skill when the user wants:
- Official documentation for a specific technology (e.g., "Find the official docs for React Hooks")
- API reference materials (e.g., "Show me the official OpenAI API docs for chat completions")
- Authoritative guides or tutorials (e.g., "Where is the official guide for Docker Compose?")
- Clarification on what counts as "official" docs for a given project
- Quick access to parameter descriptions, endpoint specs, or configuration options

**Do NOT use** for:
- Unofficial blog posts or third‑party tutorials (unless no official docs exist)
- General web search for opinions or comparisons
- Downloading entire documentation sites (respects copyright, fetches one page at a time)

## How It Works

1. **Query parsing** – Identify the technology name and specific topic (if any)
2. **Search** – Use web search with query like `"official [technology] documentation [topic]"`
3. **Filter results** – Prioritize:
   - Official project domains (e.g., `react.dev`, `docs.python.org`, `developer.apple.com`)
   - Well‑known docs hosts (MDN, ReadTheDocs, GitBook)
   - GitHub repositories with `README.md` or `docs/` folder
   - Sites with `official` in title/snippet
4. **Fetch** – Retrieve the top candidate URL
5. **Summarize** – Extract key sections, headings, code examples (if any)
6. **Return** – Provide summary + direct link + notes on what's covered

## Quick Examples

```
User: What are the official docs for pandas DataFrame?
Codex: [Fetches pandas.pydata.org/docs/reference/api/pandas.DataFrame.html, summarizes constructors, attributes, methods with links]

User: Show me the official Docker run command reference
Codex: [Fetches docs.docker.com/engine/reference/run/, lists flags, examples, notes]

User: Where is the official TypeScript handbook?
Codex: [Fetches www.typescriptlang.org/docs/handbook/, provides chapter outline and key concepts]
```

## Configuration

No special configuration needed. The skill uses existing `web_search` and `web_fetch` tools.

Optionally, you can pre‑index canonical URLs for popular technologies in `references/CANONICAL_URLS.md` (format: `technology | URL`). The skill will check there first before searching.

## Advanced: Known Technologies Index

For faster lookup of popular docs, maintain a `references/CANONICAL_URLS.md` file:

```markdown
# Canonical Documentation URLs

technology,url
React,https://react.dev
Vue,https://vuejs.org/guide/introduction.html
Angular,https://angular.io/docs
Python,https://docs.python.org/3/
Django,https://docs.djangoproject.com/en/stable/
Flask,https://flask.palletsprojects.com/
FastAPI,https://fastapi.tiangolo.com/
OpenAI,https://platform.openai.com/docs/api-reference
Anthropic,https://docs.anthropic.com/claude/reference
PostgreSQL,https://www.postgresql.org/docs/
Docker,https://docs.docker.com/
Kubernetes,https://kubernetes.io/docs/concepts/
TensorFlow,https://www.tensorflow.org/api_docs
PyTorch,https://pytorch.org/docs/stable/
```

If a known technology is queried, the skill can directly fetch from the canonical URL instead of searching.

## Limitations

- **Copyright:** Only fetches small excerpts for summarization; does not store full docs. Users should visit the official site for complete information.
- **Rate limits:** Respects site policies; adds delays between requests if needed.
- **Accuracy:** Summaries are automated; critical details should be verified against the source.
- **Dynamic content:** Some sites require JavaScript rendering; the fetch may miss content. In such cases, the skill can return the direct link for manual review.

## Scripts

- `lookup.py` – Main entry point: search, fetch, summarize
- `summarizer.py` – Extract key information from HTML (uses readability or similar)
- `canonical.py` – Check pre‑indexed URLs before searching

## Example Output

```
**Official Docs: pandas DataFrame**

Source: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html

**What it covers:**
- DataFrame constructor parameters (data, index, columns, dtype, copy)
- Core attributes (values, columns, index, dtypes)
- Key methods (head, tail, describe, groupby, merge, pivot_table, etc.)
- Examples for creating, slicing, and transforming DataFrames

**Direct link:** https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html

(You can ask follow-up questions about specific methods or parameters.)
```

## Future Enhancements

- Add more technologies to canonical index
- Support versioned docs (e.g., `docs.python.org/3.11/` vs `3.12/`)
- Search within a specific documentation site (scope query)
- Generate cheat‑sheet style summary of all methods/parameters for a class
- Cache summaries locally to avoid re‑fetching same pages (respecting copyright)

## License

Skill created for OpenClaw. Use responsibly and respect documentation site terms of service.
