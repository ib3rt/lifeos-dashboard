#!/usr/bin/env python3
"""
Blog Post Writer Agent
Creates engaging blog posts from topics

Usage:
    python3 blog-writer.py --topic "Your Topic"
    python3 blog-writer.py --batch topics.txt
    python3 blog-writer.py --draft "Quick idea"
"""

import json
import argparse
from datetime import datetime
from pathlib import Path

class BlogWriterAgent:
    def __init__(self):
        self.workspace = Path('/home/ubuntu/.openclaw/workspace')
        self.output_dir = self.workspace / 'brands/b3rt-dev/blog'
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_post(self, topic, style='engaging'):
        """Generate a blog post"""
        
        templates = {
            'engaging': f"""# {topic}

*Insights and ideas worth sharing*

---

## The Story Behind {topic}

Every great journey begins with a single step. For {topic.lower()}, that step was realizing something fundamental about how we approach our work and our tools.

## What Changed Everything

The breakthrough came not from building something completely new, but from connecting ideas that had always been separate:

1. **Perspective**: Seeing the problem from a new angle
2. **Tools**: Having the right resources at the right time  
3. **Timing**: The convergence of factors that made success possible

## Lessons Learned

### The Hard Way

Of course, the path wasn't straight. There were challenges:

- **Initial confusion** about the right approach
- **Technical obstacles** that seemed insurmountable
- **Doubt** from those who didn't see the vision

### The Breakthrough

The moment everything clicked into place...

## What This Means For You

Whether you're just starting out or looking to improve your existing approach, here's what matters most:

- Start before you're ready
- Focus on fundamentals
- Build in public
- Iterate constantly

## The Journey Continues

This is just one chapter in an ongoing story. The best is yet to come.

---

*Written by Life OS - Building the future of personal AI automation*

**Tags:** Life OS, {topic}, Automation, Productivity
""",
            
            'technical': f"""# {topic}: A Technical Deep Dive

*A comprehensive technical exploration*

---

## Introduction

This article explores {topic} from a technical perspective, covering architecture, implementation, and best practices.

## Architecture Overview

The system consists of several key components working together:

```
Component A → Component B → Component C
     ↓              ↓             ↓
  Input        Processing     Output
```

## Implementation Details

### Step 1: Foundation

Setting up the core infrastructure...

### Step 2: Integration

Connecting the pieces...

### Step 3: Optimization

Fine-tuning for performance...

## Best Practices

1. Start simple
2. Measure everything
3. Iterate based on data
4. Document thoroughly

## Common Pitfalls

- Over-engineering early
- Neglecting monitoring
- Skipping tests
- Poor documentation

## Conclusion

Mastering {topic} takes time, but the journey is worth it.

---

*Technical documentation by Life OS*
"""
        }
        
        template = templates.get(style, templates['engaging'])
        post = template.format(topic=topic)
        
        slug = topic.lower().replace(' ', '-').replace(',', '')[:50]
        filename = f"{datetime.now().strftime('%Y-%m-%d')}-{slug}.html"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w') as f:
            f.write(post)
        
        print(f"✅ Blog post created: {filepath}")
        return str(filepath)
    
    def list_posts(self):
        """List existing blog posts"""
        posts = list(self.output_dir.glob('*.html'))
        return sorted(posts, reverse=True)

def main():
    agent = BlogWriterAgent()
    
    parser = argparse.ArgumentParser(description='Blog Post Writer Agent')
    parser.add_argument('--topic', '-t', help='Blog post topic')
    parser.add_argument('--style', '-s', choices=['engaging', 'technical'], default='engaging')
    parser.add_argument('--list', '-l', action='store_true', list existing posts')
    
    args = parser.parse_args()
    
    print("✍️ Blog Post Writer Agent")
    print("=" * 50)
    
    if args.list:
        print("\n📝 Existing Posts:")
        for post in agent.list_posts():
            print(f"  • {post.name}")
    
    elif args.topic:
        agent.generate_post(args.topic, args.style)
    
    else:
        print("\nUsage:")
        print("  python3 blog-writer.py --topic \"Your Topic\"")
        print("  python3 blog-writer.py --topic \"Tech Guide\" --style technical")
        print("  python3 blog-writer.py --list")

if __name__ == '__main__':
    main()
