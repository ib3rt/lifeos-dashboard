#!/usr/bin/env python3
"""
Knowledge Curator Agent - Self-contained version
Generates article content using templates (no API required)

Usage:
    python3 knowledge-curator.py generate "Topic Name"
    python3 knowledge-curator.py generate "Topic Name" tutorial
    python3 knowledge-curator.py batch "Topic" 5
"""

import os
import re
import sys
from datetime import datetime
from pathlib import Path
from argparse import ArgumentParser

# Paths
WORKSPACE = Path('/home/ubuntu/.openclaw/workspace')
ARTICLES_DIR = WORKSPACE / 'brands/b3rt-dev' / 'content' / 'articles'

# Ensure directory
ARTICLES_DIR.mkdir(parents=True, exist_ok=True)

# Content templates
TOPIC_TEMPLATES = {
    'life-os-intro': """# {title}

*Your comprehensive guide to {topic_lower}*

## Introduction

Welcome to this in-depth exploration of **{topic}**. In today's rapidly evolving landscape of personal productivity and AI-assisted work, understanding {topic_lower} has become essential for anyone looking to optimize their workflow and achieve exceptional results.

This guide will walk you through everything you need to know, from foundational concepts to advanced strategies that you can implement immediately.

## Understanding {topic}

### The Fundamentals

Before diving into implementation, let's establish a solid understanding of {topic_lower}:

- **Core Concept**: {topic} represents a paradigm shift in how we approach [specific domain]
- **Practical Benefits**: Immediate improvements in efficiency, quality, and consistency
- **Real-World Application**: Successfully deployed by leading teams and individuals
- **Strategic Advantage**: Competitive edge in an increasingly automated world

### Historical Context

{topic} has evolved significantly over the past few years. What began as a niche technique has transformed into a fundamental practice for modern knowledge workers and AI practitioners.

## Getting Started

### Prerequisites

Before you begin implementing {topic_lower}, ensure you have:

1. **Basic Understanding**: Familiarity with core Life OS concepts
2. **Tooling**: Access to necessary platforms and APIs
3. **Time Commitment**: Dedicate 2-3 hours for initial implementation
4. **Mindset**: Openness to new approaches and methodologies

### Step-by-Step Implementation

#### Step 1: Assessment

Evaluate your current situation and identify specific areas where {topic_lower} can have the greatest impact.

#### Step 2: Planning

Develop a clear roadmap with measurable milestones and success criteria.

#### Step 3: Initial Implementation

Start with a small, focused pilot project to validate your approach.

#### Step 4: Iteration and Refinement

Based on results, continuously improve your implementation.

## Advanced Strategies

### Optimization Techniques

Once you've mastered the basics, explore these advanced approaches:

- **Automation**: Reduce manual effort through intelligent automation
- **Integration**: Connect {topic_lower} with existing systems and workflows
- **Scaling**: Expand successful patterns across your entire operation
- **Customization**: Tailor implementations to your specific needs

### Best Practices

- **Consistency**: Maintain standards across all implementations
- **Documentation**: Thoroughly document processes and decisions
- **Monitoring**: Track performance and identify improvement opportunities
- **Collaboration**: Share knowledge and learn from others

## Common Challenges

### Addressing Obstacles

Every implementation journey encounters challenges:

1. **Resistance to Change**: Overcome through education and demonstrating value
2. **Technical Complexity**: Break down into manageable components
3. **Resource Constraints**: Prioritize highest-impact improvements
4. **Knowledge Gaps**: Invest in continuous learning

### Solutions and Workarounds

Each challenge has solutions. Focus on incremental progress rather than perfect implementation.

## Measuring Success

### Key Metrics

Track these indicators to gauge progress:

- **Efficiency Gains**: Time saved on routine tasks
- **Quality Improvements**: Consistency and accuracy metrics
- **Adoption Rates**: Team and personal adoption
- **ROI**: Return on investment analysis

## Conclusion

Mastering **{topic}** is a journey, not a destination. By following the principles and practices outlined in this guide, you'll be well-equipped to leverage {topic_lower} effectively within your Life OS implementation.

Start small, iterate frequently, and continuously refine your approach based on results. The investment you make today will pay dividends in productivity and effectiveness tomorrow.

---

**Next Steps:**
1. Assess your current implementation readiness
2. Identify quick wins you can implement immediately
3. Develop a 30-day action plan
4. Connect with others on similar journeys

*Part of the Life OS Article Collection - Building the future of personal AI automation.*

**Tags:** Life OS, {topic}, Automation, AI, Guide
""",

    'technical-guide': """# {title}

*Complete technical documentation*

## Overview

This guide provides comprehensive technical documentation for implementing **{topic}** within your Life OS infrastructure.

## Prerequisites

Before beginning, ensure you have:

- **Environment**: Linux/macOS/WSL with Python 3.8+
- **Dependencies**: [List required packages]
- **Access**: API keys, credentials, permissions
- **Resources**: Minimum 2GB RAM, 500MB storage

## Installation

### Step 1: Setup Environment

```bash
# Clone repository
git clone https://github.com/your-repo/{topic_lower}.git
cd {topic_lower}

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configuration

Create your configuration file:

```bash
cp config.example.yaml config.yaml
# Edit config.yaml with your settings
```

### Step 3: Initialize

```bash
python3 init.py
```

## Usage

### Basic Usage

```python
from {topic_lower} import main

# Initialize
result = main.execute(task="your-task")
print(result)
```

### Advanced Options

- **Custom Parameters**: Fine-tune behavior with advanced options
- **Batch Processing**: Handle multiple tasks efficiently
- **Scheduling**: Automate recurring operations

## API Reference

### Methods

| Method | Description | Parameters |
|--------|-------------|------------|
| `execute()` | Main execution method | task, options |
| `validate()` | Input validation | data |
| `process()` | Data processing | input, config |

### Examples

```python
# Execute with options
result = main.execute(
    task="process",
    options={"mode": "fast", "output": "json"}
)
```

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Error X | Missing config | Run init.py |
| Error Y | Invalid input | Validate data |
| Error Z | Resource limits | Scale resources |

## Best Practices

1. **Regular Updates**: Keep dependencies current
2. **Monitoring**: Implement observability
3. **Backup**: Maintain recovery procedures
4. **Security**: Follow security guidelines

## Conclusion

This guide covers the essential aspects of implementing {topic} in your Life OS setup. For additional resources, consult the documentation and community forums.

---
*Technical documentation for Life OS practitioners.*
""",

    'tutorial': """# {title}

*Step-by-step learning guide*

## Learning Objectives

By the end of this tutorial, you will:

- Understand the fundamentals of {topic}
- Implement a complete {topic_lower} solution
- Apply best practices in real scenarios
- Extend your knowledge to advanced topics

## Estimated Time

**30-45 minutes** for complete tutorial

## Prerequisites

- Basic Life OS familiarity
- Text editor (VS Code recommended)
- Terminal access
- [Any other requirements]

## Module 1: Foundation

### Lesson 1.1: Introduction

{topic_cap} is a fundamental concept in modern productivity systems. This tutorial will guide you through every aspect.

### Lesson 1.2: Core Concepts

Understanding these building blocks is essential:

- **Concept A**: Explanation and significance
- **Concept B**: How it relates to your workflow
- **Concept C**: Practical applications

### Practice Exercise 1

Apply what you've learned: [Exercise description]

## Module 2: Implementation

### Lesson 2.1: Setup

Let's begin implementing {topic_lower}:

```bash
# Command to run
your-command --setup
```

### Lesson 2.2: Configuration

Configure your environment:

```python
# Configuration code
config = {{
    "setting": "value",
    "option": True
}}
```

### Practice Exercise 2

Build a small project incorporating {topic_lower}.

## Module 3: Advanced Topics

### Lesson 3.1: Optimization

Take your implementation to the next level:

- Performance tuning
- Resource optimization
- Scaling strategies

### Lesson 3.2: Integration

Connect {topic_lower} with other Life OS components:

```python
# Integration example
from life_os import connector
connector.connect("{topic_lower}")
```

### Practice Exercise 3

Enhance your project with advanced features.

## Module 4: Mastery

### Capstone Project

Apply everything you've learned:

1. **Planning Phase**: Design your solution
2. **Development Phase**: Build incrementally
3. **Review Phase**: Evaluate and improve

### Assessment

Test your understanding with [assessment description].

## Summary

You've completed the {topic} tutorial! You now have:

- ✅ Solid understanding of {topic_lower}
- ✅ Practical implementation skills
- ✅ Best practices knowledge
- ✅ Foundation for advanced learning

## Next Steps

1. **Practice**: Apply in real projects
2. **Explore**: Advanced tutorials in the series
3. **Connect**: Join the community

---
*Tutorial part of the Life OS Learning Path.*
"""
}

def slugify(text):
    """Convert to URL-friendly slug"""
    return re.sub(r'[^a-zA-Z0-9\s]', '', text.lower()).replace(' ', '-')

def get_template(template_type, topic):
    """Get content template with topic substituted"""
    template = TOPIC_TEMPLATES.get(template_type, TOPIC_TEMPLATES['life-os-intro'])
    
    return template.format(
        title=topic,
        topic=topic,
        topic_lower=topic.lower(),
        topic_cap=topic.capitalize()
    )

def save_article(content, topic, template_type):
    """Save markdown and generate HTML"""
    slug = slugify(topic)
    date = datetime.now().strftime('%B %d, %Y')
    words = len(content.split())
    read_time = max(1, round(words / 200))
    
    # Markdown with front matter
    md_content = f"""---
title: "{topic}"
date: "{date}"
read_time: "{read_time} min read"
category: "Life OS"
tags: ["Life OS", "Automation", "AI"]
---

{content}"""
    
    md_path = ARTICLES_DIR / f"{slug}.md"
    with open(md_path, 'w') as f:
        f.write(md_content)
    
    # Generate HTML
    generate_html(md_path, topic, read_time)
    
    return str(md_path), slug

def generate_html(md_path, title, read_time):
    """Convert markdown to HTML"""
    html_path = md_path.with_suffix('.html')
    
    # Read markdown
    with open(md_path, 'r') as f:
        content = f.read()
    
    # Remove front matter
    content = re.sub(r'^---.*?---', '', content, flags=re.DOTALL).strip()
    
    # Convert markdown to HTML (simplified)
    html_body = content
    html_body = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html_body, flags=re.MULTILINE)
    html_body = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html_body, flags=re.MULTILINE)
    html_body = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html_body, flags=re.MULTILINE)
    html_body = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_body)
    html_body = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html_body)
    html_body = re.sub(r'`(.+?)`', r'<code>\1</code>', html_body)
    html_body = re.sub(r'^- (.+)$', r'<li>\1</li>', html_body, flags=re.MULTILINE)
    
    # Convert paragraphs
    lines = html_body.split('\n\n')
    body_html = ''
    for line in lines:
        line = line.strip()
        if line and not line.startswith('<h') and not line.startswith('<li'):
            body_html += f'<p>{line}</p>\n'
        elif line:
            body_html += line + '\n'
    
    # Full HTML document
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | b3rt.dev</title>
    <link rel="stylesheet" href="/design-system.css">
</head>
<body>
    <nav class="glass-nav">
        <div class="nav-container">
            <a href="/" class="nav-logo">🦞 b3rt</a>
            <div class="nav-links">
                <a href="/articles">Articles</a>
                <a href="/templates">Templates</a>
                <a href="/journey">Journey</a>
            </div>
        </div>
    </nav>

    <main class="container">
        <a href="/articles" class="back-link">← Back to Articles</a>
        
        <article class="article-content">
            <header class="article-header">
                <span class="article-category">Life OS</span>
                <h1 class="article-title">{title}</h1>
                <div class="article-meta">
                    <span>📖 {read_time} min read</span>
                    <span>✍️ By b3rt</span>
                </div>
            </header>
            
            <div class="article-body">
{body_html}
            </div>
        </article>
    </main>

    <footer>
        <p>Built with ❤️ using Life OS</p>
    </footer>
</body>
</html>"""
    
    with open(html_path, 'w') as f:
        f.write(html_content)

def main():
    parser = ArgumentParser(description='🦞 Knowledge Curator Agent')
    parser.add_argument('command', choices=['generate', 'create', 'batch', 'help'],
                       help='Command to execute')
    parser.add_argument('topic', nargs='?', help='Topic or specification')
    parser.add_argument('--template', '-t', choices=['life-os-intro', 'technical-guide', 'tutorial'],
                       default='life-os-intro', help='Article template')
    parser.add_argument('--count', '-c', type=int, default=1, help='Number for batch')
    
    args = parser.parse_args()
    
    print(f"\n🦞 Knowledge Curator Agent")
    print(f"{'='*50}\n")
    
    if args.command == 'help':
        print("Usage:")
        print("  python3 knowledge-curator.py generate \"Topic Name\" [template]")
        print("  python3 knowledge-curator.py batch \"Topic\" [count]")
        print()
        print("Templates:")
        print("  life-os-intro    - General introductions")
        print("  technical-guide  - Developer documentation")
        print("  tutorial         - Step-by-step guides")
        print()
        print("Examples:")
        print('  knowledge-curator.py generate "AI Automation"')
        print('  knowledge-curator.py generate "API Setup" technical-guide')
        print('  knowledge-curator.py batch "Machine Learning" 5')
    
    elif args.command in ['generate', 'create']:
        topic = args.topic
        if not topic:
            print("Error: Topic required")
            sys.exit(1)
        
        print(f"📚 Curating: {topic}")
        print(f"📝 Template: {args.template}")
        
        content = get_template(args.template, topic)
        md_path, slug = save_article(content, topic, args.template)
        
        print(f"\n✅ Article created!")
        print(f"   Markdown: {md_path}")
        print(f"   HTML: {md_path.replace('.md', '.html')}")
    
    elif args.command == 'batch':
        topic = args.topic
        if not topic:
            print("Error: Topic required")
            sys.exit(1)
        
        print(f"📦 Batch generating {args.count} articles on: {topic}\n")
        
        for i in range(1, args.count + 1):
            subtopic = f"{topic} - Part {i}"
            print(f"  [{i}/{args.count}] {subtopic}")
            content = get_template('life-os-intro', subtopic)
            save_article(content, subtopic, 'life-os-intro')
        
        print(f"\n✅ Created {args.count} articles")

if __name__ == '__main__':
    main()
