#!/usr/bin/env python3
"""SubstackAssistant v1

A simple command-line tool that analyzes past Substack post data and generates
recommendations and a Markdown draft for the next post.
"""

import json
import sys
from collections import Counter
from datetime import datetime, timedelta

STOPWORDS = {
    'the', 'and', 'to', 'of', 'a', 'in', 'for', 'is', 'on', 'i', 'it', 'this',
    'that', 'you', 'my', 'with', 'be', 'about', 'how', 'do', 'what', 'more'
}

PERSONA_KEYWORDS = {
    'aspiring creator': {'creator', 'create', 'new', 'start', 'beginner'},
    'data-driven student': {'data', 'analytics', 'metric', 'numbers'},
    'hustling entrepreneur': {'revenue', 'profit', 'business', 'monetization'},
    'community seeker': {'community', 'together', 'share', 'engage'},
}

def load_input(path):
    with open(path, 'r') as f:
        return json.load(f)


def top_pain_point(comments):
    words = []
    for comment in comments:
        for word in comment.lower().split():
            word = word.strip('.,!?:;"\'')
            if word and word not in STOPWORDS:
                words.append(word)
    if not words:
        return None
    counts = Counter(words)
    return counts.most_common(1)[0][0]


def persona_from_comments(comments):
    comment_text = ' '.join(comments).lower()
    personas = []
    for persona, keys in PERSONA_KEYWORDS.items():
        if any(k in comment_text for k in keys):
            personas.append(persona)
    if not personas:
        personas.append('aspiring creator')
    return personas


def generate_topic(pain_point, objective):
    base = pain_point if pain_point else 'growth'
    return f"Solving {base} to {objective}"


def generate_hooks(pain_point):
    if not pain_point:
        pain_point = 'newsletter growth'
    hook1 = f"Struggling with {pain_point}? You're not alone."
    hook2 = f"Here's a data-backed way to overcome {pain_point}."
    return [hook1, hook2]


def generate_structure():
    return [
        {"heading": "Introduction", "word_count": 150},
        {"heading": "Key Insights", "word_count": 300},
        {"heading": "Action Steps", "word_count": 200},
        {"heading": "Call to Action", "word_count": 100},
    ]


def build_markdown(title, preview, hook, structure, cta):
    lines = [f"# {title}", '', preview, '', hook, '']
    for section in structure:
        lines.append(f"## {section['heading']}")
        lines.append('Lorem ipsum dolor sit amet...')
        lines.append('')
    lines.append(cta)
    return '\n'.join(lines)


def recommended_send_time():
    now = datetime.now()
    # default to next Tuesday 10am
    days_ahead = (1 - now.weekday()) % 7
    target = now + timedelta(days=days_ahead)
    return target.replace(hour=10, minute=0, second=0, microsecond=0).isoformat()


def generate_output(data):
    all_comments = []
    best_post = None
    for post in data.get('previous_posts', []):
        all_comments.extend(post.get('top_comments', []))
        if not best_post or post.get('open_rate', 0) > best_post.get('open_rate', 0):
            best_post = post

    pain = top_pain_point(all_comments)
    personas = persona_from_comments(all_comments)
    topic = generate_topic(pain, data.get('objective', 'engage readers'))
    structure = generate_structure()
    hooks = generate_hooks(pain)

    title = topic[:60]
    preview_text = f"{best_post.get('title', '')} resonated—let's build on it."[:155]
    cta = "**Reply** with your biggest takeaway or share this post."

    markdown = build_markdown(title, preview_text, hooks[0], structure, cta)

    output = {
        "brief": {
            "recommended_topic": topic,
            "structure": structure,
            "hooks": hooks,
            "personas_addressed": personas,
        },
        "draft_markdown": markdown,
        "optimization_notes": {
            "send_datetime": recommended_send_time(),
            "preview_text": preview_text,
            "images_or_links": [],
            "test_suggestions": {
                "A": f"{title} [A]",
                "B": f"{title} [B]",
            },
        },
        "next_steps_checklist": [
            "Copy draft_markdown into Substack editor",
            "Set send_datetime",
            "Upload any images with descriptive alt text",
            "Schedule A/B test for subject lines",
            "Monitor opens, clicks, and replies",
        ],
    }
    return output


def main():
    if len(sys.argv) < 2:
        print("Usage: substack_assistant.py <input.json>", file=sys.stderr)
        return 1
    data = load_input(sys.argv[1])
    result = generate_output(data)
    json.dump(result, sys.stdout, indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
