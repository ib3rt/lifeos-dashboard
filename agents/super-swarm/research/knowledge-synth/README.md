# Knowledge Curator Agent

**Status:** ✅ OPERATIONAL  
**Version:** 2.0.0  
**Last Updated:** 2026-02-05

Generates world-class article content for Life OS. Can create introductions, technical guides, and tutorials on any topic.

## Quick Start

```bash
# Generate one article
./knowledge-curator.py generate "Your Topic Here"

# With specific template
./knowledge-curator.py generate "Docker Guide" --template technical-guide

# Batch generate multiple articles
./knowledge-curator.py generate "Machine Learning" --count 5

# Via launcher
../tools/generate-article.sh "AI Automation"
```

## Templates

| Template | Description | Use For |
|----------|-------------|---------|
| `life-os-intro` | General introductions | Getting started, overviews |
| `technical-guide` | Developer documentation | API docs, setup guides |
| `tutorial` | Step-by-step learning | How-to guides, lessons |

## Output

Articles are saved to:
- **Markdown:** `brands/b3rt-dev/content/articles/{slug}.md`
- **HTML:** `brands/b3rt-dev/content/articles/{slug}.html`

Both formats are automatically generated and ready for deployment.

## Features

- ✅ Self-contained (works without API keys)
- ✅ Professional writing quality
- ✅ Consistent formatting
- ✅ HTML generation included
- ✅ Batch mode for multiple articles
- ✅ URL-friendly slugs
- ✅ Read time estimation
- ✅ Proper front matter

## Testing

```bash
# Test with tutorial template
./knowledge-curator.py generate "Understanding Neural Networks" --template tutorial

# Verify output
cat ../brands/b3rt-dev/content/articles/understanding-neural-networks.md
```

## Integration

**Part of:** Super Swarm Research Team  
**Reports to:** Research Lead  
**Coordinates with:** Content Team, Blog Writer

## Example Output

```
🦞 Knowledge Curator Agent
==================================================

📚 Curating: Understanding Machine Learning
📝 Template: tutorial

✅ Article created!
   Markdown: .../content/articles/understanding-machine-learning.md
   HTML: .../content/articles/understanding-machine-learning.html
```

---

*Ready for production use. Generate unlimited articles on any topic.*
