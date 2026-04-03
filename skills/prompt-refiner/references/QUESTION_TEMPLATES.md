# Question Templates for Prompt Refinement

This file defines standard clarifying questions for different task categories. The `prompt-refiner` skill uses these to ask targeted questions based on the user's initial prompt.

## Format

Each category has a list of questions. The skill selects relevant ones based on task type detection.

---

## General (fallback)

- What is the main goal or desired outcome?
- Who is the audience or end-user?
- Are there any specific constraints (time, budget, tools, format)?
- Do you have any examples or references that illustrate what you want?
- What does "done" look like?

## Coding / Development

- What programming language or framework do you prefer? (or should I choose)
- What is the primary function or feature needed?
- Should the code be production-ready, or is a prototype/demo okay?
- Any specific libraries, APIs, or services to integrate?
- Are there performance, security, or scalability considerations?
- Do you need tests, documentation, or deployment instructions?

## Writing / Content

- What is the topic or subject?
- What tone or style? (formal, casual, persuasive, technical)
- Target audience? (experts, general public, specific demographic)
- Desired length? (word count, page count, duration)
- Format? (blog post, email, report, script, social media)
- Any specific points to include or avoid?
- Call-to-action? (inform, persuade, entertain, educate)

## Data Analysis / Research

- What data do you have? (format, size, source)
- What specific questions are you trying to answer?
- Desired output format? (report, visualization, summary, predictions)
- Tools preference? (Python/R, pandas, specific libraries)
- Any statistical methods or models to apply?
- Timeline and depth? (quick exploratory vs. comprehensive)

## Design / Creative

- What is the project? (logo, UI, poster, infographic)
- Brand guidelines? (colors, fonts, style)
- Audience and use case?
- Reference examples or inspiration?
- Deliverable formats? (SVG, PNG, PDF, source files)
- Any specific elements to include or avoid?

## Social Media / Marketing

- Which platform? (LinkedIn, Twitter/X, Instagram, etc.)
- Goal? (brand awareness, lead gen, announcement, engagement)
- Target audience demographics?
- Content type? (text, image, carousel, video)
- Any hashtags, mentions, or links to include?
- Tone? (professional, casual, promotional, educational)
- Call-to-action?

## Scheduling / Automation

- What triggers the automation? (time, event, condition)
- What action should be taken? (send email, post, scrape, notify)
- Frequency? (once, recurring, continuous)
- Any input parameters or configuration needed?
- Where should results go? (email, Slack, file, database)
- Error handling expectations?

## Research / Learning

- What topic do you want to learn about?
- Current knowledge level? (beginner, intermediate, advanced)
- Preferred learning format? (step-by-step, theory, examples, video)
- Specific subtopics to focus on?
- Application context? (project, exam, curiosity)
- Depth? (overview vs. deep dive)

## Business / Planning

- What type of plan? (business, project, marketing, product)
- Scope and timeframe? (3 months, 1 year)
- Key stakeholders?
- Existing resources or constraints?
- Success metrics?
- Format? (slide deck, document, spreadsheet)

---

**Extensibility:** Add new categories by following the same pattern. The skill will automatically pick up questions for any category listed here. For unknown categories, it falls back to General questions.
