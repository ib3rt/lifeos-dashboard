#!/usr/bin/env python3
"""
Content Pipeline Status Tracker
Monitors and reports on content pipeline stages.
"""

import json
from datetime import datetime
from pathlib import Path


def get_pipeline_stages() -> list:
    """Define pipeline stages."""
    return [
        {"name": "idea", "label": "💡 Ideation"},
        {"name": "outline", "label": "📝 Outlining"},
        {"name": "draft", "label": "✍️ Drafting"},
        {"name": "edit", "label": "📖 Editing"},
        {"name": "optimize", "label": "🎯 Optimizing"},
        {"name": "approve", "label": "✅ Approval"},
        {"name": "publish", "label": "🚀 Published"},
        {"name": "promote", "label": "📢 Promotion"},
        {"name": "analyze", "label": "📊 Analysis"}
    ]


def load_content_items() -> list:
    """Load all content items."""
    content_dir = Path("content/blog")
    
    items = []
    if content_dir.exists():
        for file in content_dir.glob("*.json"):
            with open(file, 'r') as f:
                items.append(json.load(f))
    
    # Also load ideas
    ideas_file = Path("content/ideas_latest.json")
    if ideas_file.exists():
        with open(ideas_file, 'r') as f:
            ideas = json.load(f)
            items.extend(ideas)
    
    return items


def count_by_stage(items: list) -> dict:
    """Count items by their current stage."""
    stages = {s["name"]: {"count": 0, "label": s["label"]} for s in get_pipeline_stages()}
    
    for item in items:
        stage = item.get("status", "idea")
        if stage in stages:
            stages[stage]["count"] += 1
    
    return stages


def print_status():
    """Print current pipeline status."""
    print("\n" + "="*60)
    print("CONTENT PIPELINE STATUS")
    print(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*60)
    
    items = load_content_items()
    stage_counts = count_by_stage(items)
    
    total = sum(s["count"] for s in stage_counts.values())
    print(f"\nTotal Content Items: {total}")
    print("-"*40)
    
    for stage in get_pipeline_stages():
        name = stage["name"]
        count = stage_counts[name]["count"]
        bar = "█" * count
        print(f"{stage['label']:15} {bar} ({count})")
    
    print("-"*40)
    
    # Recent activity
    print("\n📌 Recent Activity:")
    for item in items[:5]:
        title = item.get("title", item.get("content_title", "Unknown"))
        status = item.get("status", "unknown")
        print(f"  - [{status}] {title[:50]}")


def main():
    print_status()


if __name__ == "__main__":
    main()
