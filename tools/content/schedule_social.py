#!/usr/bin/env python3
"""
Social Media Scheduler
Reads calendar and schedules social posts.
"""

import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path


def load_calendar(calendar_file: str) -> dict:
    """Load content calendar."""
    with open(calendar_file, 'r') as f:
        return json.load(f)


def get_social_templates() -> dict:
    """Get social media post templates."""
    return {
        "twitter": {
            "max_chars": 280,
            "structure": "{hook}\n\n{value}\n\n{cta}\n\n#{tags}",
            "best_times": ["08:00", "12:00", "17:00"]
        },
        "linkedin": {
            "max_chars": 3000,
            "structure": "{insight}\n\n{experience}\n\nKey takeaways:\n{points}\n\n{question}\n\n{cta}",
            "best_times": ["08:00", "10:00", "12:00"]
        },
        "instagram": {
            "max_chars": 2200,
            "structure": "{caption}\n\n.\n.\n.\n\n{cta}",
            "best_times": ["09:00", "12:00", "19:00"]
        },
        "facebook": {
            "max_chars": 63206,
            "structure": "{update}\n\n{link}\n\n{cta}",
            "best_times": ["09:00", "13:00", "16:00"]
        }
    }


def generate_social_post(content_title: str, platform: str) -> dict:
    """Generate a social post from content title."""
    templates = get_social_templates()
    
    if platform not in templates:
        raise ValueError(f"Unknown platform: {platform}")
    
    template = templates[platform]
    
    post = {
        "content_title": content_title,
        "platform": platform,
        "generated_at": datetime.now().isoformat(),
        "body": f"New content alert! {content_title}\n\nCheck it out and let me know your thoughts.\n\n#content #tips",
        "scheduled_time": template["best_times"][0],
        "status": "draft"
    }
    
    return post


def schedule_posts(calendar: dict) -> list:
    """Schedule all social posts from calendar."""
    scheduled = []
    
    for event in calendar.get("events", []):
        content_type = event.get("type", "")
        platforms = event.get("platforms", [])
        
        if content_type in ["blog", "social"]:
            for platform in platforms:
                post = generate_social_post(event.get("title", ""), platform)
                scheduled.append(post)
    
    return scheduled


def save_scheduled_posts(posts: list, output_file: str):
    """Save scheduled posts."""
    with open(output_file, 'w') as f:
        json.dump(posts, f, indent=2)
    
    print(f"Saved {len(posts)} scheduled posts to {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Schedule social media posts')
    parser.add_argument('--calendar', type=str, default='content/calendar.md',
                        help='Calendar file path')
    
    args = parser.parse_args()
    
    try:
        calendar = load_calendar(args.calendar)
        posts = schedule_posts(calendar)
        save_scheduled_posts(posts, "content/scheduled_posts.json")
        
        print("\nScheduled Posts:")
        for post in posts:
            print(f"- [{post['platform']}] {post['content_title']}")
            
    except FileNotFoundError:
        print(f"Calendar file not found: {args.calendar}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
