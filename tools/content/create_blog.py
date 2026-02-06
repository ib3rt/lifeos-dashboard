#!/usr/bin/env python3
"""
Blog Content Creator
Creates blog posts from titles and keywords.
"""

import argparse
from datetime import datetime
from pathlib import Path


def create_blog_post(title: str, keyword: str = "", tone: str = "professional") -> dict:
    """Create a blog post structure."""
    
    post = {
        "title": title,
        "slug": title.lower().replace(" ", "-").replace("?", ""),
        "keyword": keyword,
        "tone": tone,
        "created_at": datetime.now().isoformat(),
        "status": "draft",
        "structure": {
            "sections": [
                {"type": "hook", "content": f"Attention-grabbing intro about {keyword}"},
                {"type": "problem", "content": "Define the problem your audience faces"},
                {"type": "solution", "content": f"Introduce {keyword} as the solution"},
                {"type": "main_content", "content": "Expand with 3-5 key points"},
                {"type": "examples", "content": "Case studies and real-world examples"},
                {"type": "cta", "content": "Call to action for engagement"}
            ]
        },
        "seo": {
            "meta_title": title[:60],
            "meta_description": f"Learn about {keyword} and how it can help you...",
            "keywords": [keyword] if keyword else [],
            "headings": [title]
        }
    }
    
    return post


def save_blog(post: dict, output_dir: str = "content/blog"):
    """Save blog post to file."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    filename = f"{output_dir}/{post['slug']}.json"
    with open(filename, 'w') as f:
        import json
        json.dump(post, f, indent=2)
    
    print(f"Blog post saved to {filename}")
    return filename


def generate_content(post: dict) -> str:
    """Generate full blog content from post structure."""
    sections = post.get("structure", {}).get("sections", [])
    
    content = f"# {post['title']}\n\n"
    content += f"*Published on {datetime.now().strftime('%B %d, %Y')}*\n\n"
    
    for section in sections:
        section_type = section.get("type", "")
        content += f"## {section_type.upper().replace('_', ' ')}\n\n"
        content += f"[AI-generated content for {section_type}]\n\n"
    
    content += "---\n\n"
    content += "*This is a draft. Edit and optimize before publishing.*\n"
    
    return content


def main():
    parser = argparse.ArgumentParser(description='Create blog content')
    parser.add_argument('--title', type=str, required=True, help='Blog post title')
    parser.add_argument('--keyword', type=str, default="", help='Target SEO keyword')
    parser.add_argument('--tone', type=str, default="professional", help='Writing tone')
    
    args = parser.parse_args()
    
    post = create_blog_post(args.title, args.keyword, args.tone)
    save_blog(post)
    
    # Generate full content
    full_content = generate_content(post)
    content_file = f"content/blog/{post['slug']}.md"
    with open(content_file, 'w') as f:
        f.write(full_content)
    
    print(f"Full content generated: {content_file}")


if __name__ == "__main__":
    main()
