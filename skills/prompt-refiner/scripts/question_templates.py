"""
Question templates for prompt refinement.
"""

CATEGORY_QUESTIONS = {
    'coding': [
        "What programming language or framework do you prefer? (or should I choose)",
        "What is the primary function or feature needed?",
        "Should the code be production-ready, or is a prototype/demo okay?",
        "Any specific libraries, APIs, or services to integrate?",
        "Are there performance, security, or scalability considerations?",
        "Do you need tests, documentation, or deployment instructions?"
    ],
    'writing': [
        "What is the topic or subject?",
        "What tone or style? (formal, casual, persuasive, technical)",
        "Target audience? (experts, general public, specific demographic)",
        "Desired length? (word count, page count, duration)",
        "Format? (blog post, email, report, script, social media)",
        "Any specific points to include or avoid?",
        "Call-to-action? (inform, persuade, entertain, educate)"
    ],
    'analysis': [
        "What data do you have? (format, size, source)",
        "What specific questions are you trying to answer?",
        "Desired output format? (report, visualization, summary, predictions)",
        "Tools preference? (Python/R, pandas, specific libraries)",
        "Any statistical methods or models to apply?",
        "Timeline and depth? (quick exploratory vs. comprehensive)"
    ],
    'design': [
        "What is the project? (logo, UI, poster, infographic)",
        "Brand guidelines? (colors, fonts, style)",
        "Audience and use case?",
        "Reference examples or inspiration?",
        "Deliverable formats? (SVG, PNG, PDF, source files)",
        "Any specific elements to include or avoid?"
    ],
    'social': [
        "Which platform? (LinkedIn, Twitter/X, Instagram, etc.)",
        "Goal? (brand awareness, lead gen, announcement, engagement)",
        "Target audience demographics?",
        "Content type? (text, image, carousel, video)",
        "Any hashtags, mentions, or links to include?",
        "Tone? (professional, casual, promotional, educational)",
        "Call-to-action?"
    ],
    'automation': [
        "What triggers the automation? (time, event, condition)",
        "What action should be taken? (send email, post, scrape, notify)",
        "Frequency? (once, recurring, continuous)",
        "Any input parameters or configuration needed?",
        "Where should results go? (email, Slack, file, database)",
        "Error handling expectations?"
    ],
    'research': [
        "What topic do you want to learn about?",
        "Current knowledge level? (beginner, intermediate, advanced)",
        "Preferred learning format? (step-by-step, theory, examples, video)",
        "Specific subtopics to focus on?",
        "Application context? (project, exam, curiosity)",
        "Depth? (overview vs. deep dive)"
    ],
    'business': [
        "What type of plan? (business, project, marketing, product)",
        "Scope and timeframe? (3 months, 1 year)",
        "Key stakeholders?",
        "Existing resources or constraints?",
        "Success metrics?",
        "Format? (slide deck, document, spreadsheet)"
    ],
    'general': [
        "What is the main goal or desired outcome?",
        "Who is the audience or end-user?",
        "Are there any specific constraints (time, budget, tools, format)?",
        "Do you have any examples or references that illustrate what you want?",
        "What does 'done' look like?"
    ]
}

def detect_category(prompt: str) -> str:
    """
    Heuristic to guess task category from prompt keywords.
    Returns one of the keys in CATEGORY_QUESTIONS.
    """
    prompt_lower = prompt.lower()

    # Ordered by specificity
    categories = [
        ('coding', ['code', 'program', 'script', 'api', 'function', 'class', 'app', 'website', 'web', 'react', 'python', 'javascript', 'build', 'develop', 'deploy', 'software', 'application']),
        ('writing', ['write', 'draft', 'blog', 'article', 'email', 'post', 'content', 'copy', 'script', 'story', 'essay', 'letter', 'newsletter']),
        ('analysis', ['analyze', 'analysis', 'data', 'report', 'research', 'study', 'insights', 'metrics', 'dashboard', 'statistics', 'dataset']),
        ('design', ['design', 'logo', 'ui', 'ux', 'graphic', 'infographic', 'visual', 'layout', 'style', 'mockup', 'prototype']),
        ('social', ['linkedin', 'twitter', 'instagram', 'tweet', 'post', 'social media', 'hashtag', 'engagement', 'followers']),
        ('automation', ['automate', 'schedule', 'trigger', 'workflow', 'cron', 'bot', 'notify', 'alert', 'integration']),
        ('research', ['learn', 'explain', 'how', 'tutorial', 'guide', 'understand', 'concepts', 'fundamentals', 'introduction']),
        ('business', ['plan', 'strategy', 'business', 'marketing', 'project', 'proposal', 'budget', 'pitch', 'startup'])
    ]

    scores = {}
    for cat, keywords in categories:
        score = sum(1 for kw in keywords if kw in prompt_lower)
        scores[cat] = score

    best = max(scores.items(), key=lambda x: x[1])
    if best[1] > 0:
        return best[0]

    return 'general'
