# Content Automation Tools

## Shell Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `generate_ideas.sh` | Generate content ideas | `./generate_ideas.sh --topic "productivity" --count 10` |
| `create_blog.sh` | Create blog posts | `./create_blog.sh --title "Blog Title" --keyword "seo keyword"` |
| `schedule_social.sh` | Schedule social posts | `./schedule_social.sh --calendar content/calendar.md` |
| `publish_all.sh` | Publish to all platforms | `./publish_all.sh --drafts` |
| `run_pipeline.sh` | Manage pipeline | `./run_pipeline.sh --status` |

## Python Scripts

| Script | Purpose |
|--------|---------|
| `generate_ideas.py` | AI-powered idea generation |
| `create_blog.py` | Blog post creation with templates |
| `schedule_social.py` | Multi-platform social scheduling |
| `pipeline_status.py` | Track pipeline stages |
| `optimize_seo.py` | SEO analysis and optimization |
| `track_performance.py` | Performance metrics tracking |

## Quick Start

```bash
# Generate ideas
./tools/content/generate_ideas.sh --topic "productivity" --count 10

# Create a blog post
./tools/content/create_blog.sh --title "10 Ways to Boost Productivity"

# Check pipeline status
./tools/content/run_pipeline.sh --status

# Schedule social posts
./tools/content/schedule_social.sh --calendar content/calendar.md
```

## Configuration

Set environment variables:
```bash
export AI_MODEL="gpt-4"
export PLATFORM_API_KEYS='{"twitter": "key1", "linkedin": "key2"}'
```
