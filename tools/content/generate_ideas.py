#!/usr/bin/env python3
"""
Content Idea Generator
Generates content ideas based on topics and trends.
"""

import argparse
import json
from datetime import datetime
from pathlib import Path


def generate_ideas(topic: str, count: int = 10) -> list:
    """Generate content ideas for a given topic."""
    
    # Idea templates by category
    idea_templates = {
        "how_to": [
            f"How to Master {topic} in 30 Days",
            f"The Ultimate Guide to {topic}",
            f"Step-by-Step: {topic} for Beginners",
            f"Advanced {topic} Techniques",
        ],
        "listicle": [
            f"10 {topic} Mistakes to Avoid",
            f"15 Tools for Better {topic}",
            f"7 Secrets About {topic} Nobody Tells You",
            f"20 Tips for {topic} Success",
        ],
        "why": [
            f"Why {topic} Matters More Than Ever",
            f"Why Most People Fail at {topic}",
            f"The Science Behind {topic}",
        ],
        "comparison": [
            f"{topic} vs. The Competition: A Complete Comparison",
            f"Traditional vs. Modern {topic}",
            f"DIY vs. Professional {topic}",
        ],
        "case_study": [
            f"How [Company] Increased Results by 200% with {topic}",
            f"Case Study: {topic} Success Story",
            f"From Zero to Hero: {topic} Journey",
        ]
    }
    
    ideas = []
    for category, templates in idea_templates.items():
        for template in templates[:max(1, count // len(idea_templates))]:
            ideas.append({
                "title": template,
                "category": category,
                "topic": topic,
                "created_at": datetime.now().isoformat(),
                "status": "pending"
            })
    
    return ideas[:count]


def save_ideas(ideas: list, output_file: str):
    """Save ideas to a file."""
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(ideas, f, indent=2)
    
    print(f"Saved {len(ideas)} ideas to {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Generate content ideas')
    parser.add_argument('--topic', type=str, required=True, help='Topic for ideas')
    parser.add_argument('--count', type=int, default=10, help='Number of ideas')
    parser.add_argument('--output', type=str, default='content/ideas.json', help='Output file')
    
    args = parser.parse_args()
    
    ideas = generate_ideas(args.topic, args.count)
    save_ideas(ideas, args.output)
    
    print("\nGenerated Ideas:")
    for i, idea in enumerate(ideas, 1):
        print(f"{i}. {idea['title']} ({idea['category']})")


if __name__ == "__main__":
    main()
