---
name: prompt-refiner
description: Refine vague prompts into clear, actionable instructions. Use when user gives a brief or ambiguous request. The skill asks clarifying questions (context, format, constraints, success criteria), synthesizes answers into an optimized prompt, and returns it for confirmation. Can optionally execute the refined prompt immediately or store for later. Improves outcome quality by ensuring all necessary details are captured before work begins.
---

# Prompt Refiner Skill

## Overview

This skill improves any user request by asking targeted clarifying questions before work begins. It transforms vague, high-level prompts into detailed, executable instructions, reducing back-and-forth and ensuring the final output meets expectations.

## When to Use

Use this skill when the user:
- Gives a short, ambiguous request (e.g., "Build me a website", "Analyze this data")
- Omits key details (audience, format, constraints, deliverable format)
- Might benefit from structured thinking before execution
- Wants higher quality outcomes with fewer revisions

**Do NOT use** when:
- The request is already specific and complete
- User explicitly says "just do it" or "no questions"
- Time is critical and user prefers rapid iteration over upfront planning

## How It Works

1. **Initial Assessment** – Parse the user's prompt to identify the task type (coding, writing, analysis, design, etc.)
2. **Question Generation** – Based on task type and missing information, generate 3–5 clarifying questions covering:
   - **Context**: Who is this for? What's the background?
   - **Goal**: What does success look like? Any specific outcomes?
   - **Constraints**: Budget, timeline, tools, format, length, style?
   - **Audience**: Who will consume this? (technical level, demographics)
   - **Examples**: Any reference materials, templates, or similar past work?
3. **Interactive Dialogue** – Present questions to user, collect answers
4. **Prompt Synthesis** – Combine original prompt + answers into a refined, structured prompt
5. **Confirmation Loop** – Show refined prompt; user can approve, tweak, or restart
6. **Execution** – Either:
   - Return the refined prompt for user to use elsewhere
   - Optionally execute it immediately (if within OpenClaw capability)

## Quick Example

**User:** "Build me a website"

**Prompt Refiner:** "Sure! To build the right website, I need to ask a few questions:

1. What's the purpose of the website? (e.g., portfolio, e-commerce, blog, business card)
2. Who is the target audience? (e.g., tech recruiters, general consumers)
3. Any specific features you need? (contact form, payment, blog, etc.)
4. Do you have a preferred tech stack? (or should I choose)
5. Any example sites you like that I can use as reference?

Please answer these so I can create a detailed plan."

**User:** [answers]

**Prompt Refiner:** "Based on your answers, here's a refined prompt:

'Build a responsive portfolio website for a freelance graphic designer targeting advertising agencies. The site should have: home page with hero, about, portfolio gallery (image grid), contact form, and a blog section. Use React with Vite and Tailwind CSS for styling. Include mobile-first design. Provide a component outline, file structure, and starter code. Deploy to Vercel.'

Is this accurate? Should I proceed to generate the code?"

## Scripts

- `refine.py` – Main entry point: takes prompt, generates questions, synthesizes refined version
- `question_bank.py` – Library of question templates per task category
- `synthesizer.py` – Combines input + answers into structured prompt
- `execute.py` (optional) – After confirmation, runs the refined prompt through appropriate skill

## Configuration

Optional: Customize question sets in `references/QUESTION_TEMPLATES.md` to match your common workflows.

## Limitations

- Relies on user providing truthful/complete answers
- Cannot foresee every missing detail; user should review refined prompt
- Execution depends on other installed skills (coding, writing, etc.)

## Future Enhancements

- Learn from past refinements to ask better questions
- Auto-detect task type more accurately
- Integrate with skill router to automatically dispatch refined prompt to best skill
- Save refined prompts as reusable templates

## License

Skill created for OpenClaw. Adapt to your workflow.
