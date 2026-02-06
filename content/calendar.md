# Content Calendar

## Publishing Schedule

### Daily
| Time | Platform | Content Type |
|------|----------|--------------|
| 8:00 AM | Twitter | Industry news + comment |
| 12:00 PM | LinkedIn | Educational post |
| 3:00 PM | Instagram | Tip/graphic |

### Weekly
| Day | Content | Platform |
|-----|---------|----------|
| Monday | Weekly kickoff/Goals | Blog + Newsletter |
| Wednesday | Deep-dive article | Blog + Social |
| Friday | Weekly recap | Newsletter |

### Monthly
| Week | Focus |
|------|-------|
| Week 1 | Thought leadership |
| Week 2 | How-to/Educational |
| Week 3 | Case studies |
| Week 4 | Community/Culture |

## Calendar Format

```yaml
events:
  - date: 2024-02-05
    type: blog
    title: "5 Productivity Hacks That Actually Work"
    status: draft
    platforms: [blog, twitter, linkedin]
    
  - date: 2024-02-07
    type: social
    title: "Quick tip: Time-blocking"
    status: scheduled
    platforms: [instagram, twitter]
```

## Scheduling Commands

```bash
# View calendar
python tools/content/calendar_view.py --month current

# Add content to calendar
python tools/content/calendar_add.py --date 2024-02-15 --type blog --title "New Post"

# Check upcoming content
python tools/content/upcoming.py --days 7

# Auto-schedule based on templates
python tools/content/auto_schedule.py --template weekly --start 2024-02-01
```

## Campaign Coordination

### Multi-Platform Launch
```
Day -3: Teaser posts
Day -2: Countdown + behind-the-scenes
Day -1: Preview + link in bio
Day 0: Full launch
Day +1: Testimonials
Day +3: Data/results sharing
```

## Performance Tracking

Track metrics per content piece:
- Impressions
- Engagement rate
- Click-through rate
- Conversion rate
- Time on page
