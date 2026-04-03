#!/usr/bin/env python3
"""
Prompt Refiner: Ask clarifying questions and synthesize better prompts.
"""

import sys
from pathlib import Path

# Add skill's scripts directory to path for relative imports
SKILL_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_DIR / 'scripts'))

from question_templates import CATEGORY_QUESTIONS, detect_category

import re
from typing import List, Dict

def select_questions(prompt: str, max_questions: int = 5) -> List[str]:
    """
    Select relevant clarifying questions based on detected category.
    """
    category = detect_category(prompt)
    questions = CATEGORY_QUESTIONS.get(category, CATEGORY_QUESTIONS['general'])
    return questions[:max_questions]

def synthesize_prompt(original: str, answers: Dict[str, str]) -> str:
    """
    Combine original prompt with answers into a refined, structured prompt.
    """
    category = detect_category(original)
    parts = []

    parts.append("## Refined Task Prompt\n")
    parts.append(f"**Original request:** {original}\n")

    parts.append("**Clarifications:**")
    for q, a in answers.items():
        parts.append(f"- {q.strip('?')}: {a}")
    parts.append("")

    parts.append("**Optimized Prompt:**\n")

    # Route to appropriate synthesizer
    if category == 'coding':
        parts.append(synthesize_coding(original, answers))
    elif category == 'writing':
        parts.append(synthesize_writing(original, answers))
    elif category == 'social':
        parts.append(synthesize_social(original, answers))
    elif category == 'design':
        parts.append(synthesize_design(original, answers))
    elif category == 'analysis':
        parts.append(synthesize_analysis(original, answers))
    else:
        parts.append(synthesize_general(original, answers))

    parts.append("\n---")
    parts.append("Please confirm if this refined prompt accurately captures your needs. Reply 'confirm' to proceed, or suggest edits.")

    return '\n'.join(parts)

def synthesize_general(original: str, answers: Dict[str, str]) -> str:
    goal = answers.get("What is the main goal or desired outcome?", "")
    audience = answers.get("Who is the audience or end-user?", "")
    constraints = answers.get("Are there any specific constraints (time, budget, tools, format)?", "")
    examples = answers.get("Do you have any examples or references that illustrate what you want?", "")
    done = answers.get("What does 'done' look like?", "")

    parts = [f"Task: {original}"]
    if goal: parts.append(f"Goal: {goal}")
    if audience: parts.append(f"Audience: {audience}")
    if constraints: parts.append(f"Constraints: {constraints}")
    if examples: parts.append(f"References: {examples}")
    if done: parts.append(f"Success criteria: {done}")
    return '\n'.join(parts)

def synthesize_coding(original: str, answers: Dict[str, str]) -> str:
    tech = answers.get("What programming language or framework do you prefer? (or should I choose)", "")
    function = answers.get("What is the primary function or feature needed?", original)
    quality = answers.get("Should the code be production-ready, or is a prototype/demo okay?", "production-ready")
    integrations = answers.get("Any specific libraries, APIs, or services to integrate?", "")
    considerations = answers.get("Are there performance, security, or scalability considerations?", "")
    tests = answers.get("Do you need tests, documentation, or deployment instructions?", "Yes, include tests and basic documentation")

    return f"""Build a {quality} solution with the following specifications:

**Task:** {function}

**Tech Stack:** {tech if tech else 'Choose appropriate modern stack'}

**Integrations:** {integrations if integrations else 'None'}

**Considerations:** {considerations if considerations else 'Standard best practices'}

**Deliverables:**
- Clean, well-documented code
- {tests}
- Brief README with setup instructions
"""

def synthesize_writing(original: str, answers: Dict[str, str]) -> str:
    topic = answers.get("What is the topic or subject?", original)
    tone = answers.get("What tone or style? (formal, casual, persuasive, technical)", "professional")
    audience = answers.get("Target audience? (experts, general public, specific demographic)", "general")
    length = answers.get("Desired length? (word count, page count, duration)", "500-800 words")
    fmt = answers.get("Format? (blog post, email, report, script, social media)", "blog post")
    points = answers.get("Any specific points to include or avoid?", "")
    cta = answers.get("Call-to-action? (inform, persuade, entertain, educate)", "inform and engage")

    return f"""Write a {fmt} with the following specifications:

**Topic:** {topic}

**Tone:** {tone}

**Audience:** {audience}

**Length:** {length}

**Key Points to Cover:** {points if points else 'Derive from topic'}

**Call-to-Action:** {cta}

**Deliverable:** A complete, polished {fmt} ready to publish.
"""

def synthesize_social(original: str, answers: Dict[str, str]) -> str:
    platform = answers.get("Which platform? (LinkedIn, Twitter/X, Instagram, etc.)", "LinkedIn")
    goal = answers.get("Goal? (brand awareness, lead gen, announcement, engagement)", "engagement")
    audience = answers.get("Target audience demographics?", "")
    content_type = answers.get("Content type? (text, image, carousel, video)", "text + image if available")
    hashtags = answers.get("Any hashtags, mentions, or links to include?", "")
    tone = answers.get("Tone? (professional, casual, promotional, educational)", "professional")
    cta = answers.get("Call-to-action?", "Ask a question to encourage comments")

    return f"""Write a {platform} post with the following specifications:

**Purpose:** {goal}

**Target Audience:** {audience}

**Content Type:** {content_type}

**Tone:** {tone}

**Hashtags/Mentions:** {hashtags if hashtags else '3-5 relevant hashtags'}

**Call-to-Action:** {cta}

**Additional Notes:** {original}

Create an optimized post ready to publish.
"""

def synthesize_design(original: str, answers: Dict[str, str]) -> str:
    project_type = answers.get("What is the project? (logo, UI, poster, infographic)", original)
    brand = answers.get("Brand guidelines? (colors, fonts, style)", "")
    audience = answers.get("Audience and use case?", "")
    references = answers.get("Reference examples or inspiration?", "")
    formats = answers.get("Deliverable formats? (SVG, PNG, PDF, source files)", "SVG and PNG")
    avoid = answers.get("Any specific elements to include or avoid?", "")

    return f"""Design {project_type} with the following specifications:

**Brand Guidelines:** {brand if brand else 'Modern, clean aesthetic'}

**Target Audience:** {audience}

**References/Inspiration:** {references if references else 'Use best practices for the type'}

**Deliverable Formats:** {formats}

**Must Include / Avoid:** {avoid if avoid else 'No specific restrictions'}

Provide design rationale and source files if applicable.
"""

def synthesize_analysis(original: str, answers: Dict[str, str]) -> str:
    data_desc = answers.get("What data do you have? (format, size, source)", "Data will be provided separately")
    questions = answers.get("What specific questions are you trying to answer?", original)
    output = answers.get("Desired output format? (report, visualization, summary, predictions)", "Jupyter notebook with analysis and visualizations")
    tools = answers.get("Tools preference? (Python/R, pandas, specific libraries)", "Python with pandas, matplotlib, seaborn")
    methods = answers.get("Any statistical methods or models to apply?", "Descriptive stats, correlation analysis, basic visualizations")
    depth = answers.get("Timeline and depth? (quick exploratory vs. comprehensive)", "comprehensive")

    return f"""Perform {depth} data analysis with the following specifications:

**Data Description:** {data_desc}

**Key Questions:** {questions}

**Tools & Libraries:** {tools}

**Methods:** {methods if methods else 'Standard exploratory data analysis'}

**Deliverable:** {output}

Include clear visualizations, insights, and actionable recommendations.
"""

def interactive_refine(prompt: str) -> str:
    """
    Main interactive flow: ask questions, get answers, synthesize refined prompt.

    Args:
        prompt: User's initial prompt

    Returns:
        Refined prompt string
    """
    print(f"\n🤔 Let's refine your request to make it crystal clear.\n")
    print(f"Original: {prompt}\n")

    questions = select_questions(prompt)
    answers = {}

    for q in questions:
        print(f"Q: {q}")
        ans = input("A: ").strip()
        if not ans:
            print("   (skipped)")
            continue
        answers[q] = ans

    print("\n🔄 Synthesizing refined prompt...\n")
    refined = synthesize_prompt(prompt, answers)
    print(refined)

    return refined

if __name__ == '__main__':
    # Quick test
    test_prompt = "Build me a website"
    result = interactive_refine(test_prompt)
    print("\n\n=== FINAL REFINED PROMPT ===\n")
    print(result)
