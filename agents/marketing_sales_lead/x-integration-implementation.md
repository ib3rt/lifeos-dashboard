# 🤖 X/Twitter Bot Integration
## Hype Man — Social Media Automation

---

## Overview

Automated X/Twitter posting and engagement for Life OS updates, agent deliverables, and curated content.

---

## Architecture

```
┌─────────────────┐
│  Life OS Core   │
│  (Your Server)  │
└────────┬────────┘
         │
    ┌────┴────┐
    │  Queue  │
    │ (Redis) │
    └────┬────┘
         │
┌────────┴────────┐
│   X API Bot     │
│  (Hype Man)     │
└────────┬────────┘
         │
    ┌────┴────┐
    │  X.com  │
    └─────────┘
```

---

## Features

### Auto-Post Triggers
- [ ] New agent deliverable complete → Thread summary
- [ ] Research report published → Key insights tweet
- [ ] Dashboard update → Feature announcement
- [ ] Daily standup → Progress update
- [ ] System milestone → Celebration tweet

### Content Types
1. **Agent Spotlights**
   ```
   🔮 Meet The Oracle
   
   Latest research: GPT-5.2 capabilities breakdown
   
   Full report: [link]
   
   #AI #OpenAI #LifeOS
   ```

2. **Progress Threads**
   ```
   📊 Life OS Genesis: 100% Complete
   
   What we built in 24 hours:
   • 15 specialized AI agents
   • 11 research reports (147KB)
   • 5 CLI automation tools
   • Live dashboard deployed
   
   🧵 Thread 👇
   ```

3. **Kool Tools**
   ```
   🛠️ Tool Spotlight: OpenClaw
   
   Local-first AI agent framework
   - 24/7 operation
   - Multi-channel (Telegram, Discord, etc.)
   - Sub-agent delegation
   
   Building my Life OS on it. Game changer.
   
   #BuildInPublic #AI
   ```

---

## Implementation

### Step 1: X Developer Account

1. Apply at https://developer.twitter.com/en/apply-for-access
2. Choose "Basic" ($100/mo) or wait for free tier
3. Create app: "LifeOS-Bot"
4. Generate API keys:
   - API Key
   - API Secret
   - Bearer Token
   - Access Token
   - Access Secret

### Step 2: Bot Code

```python
# hype_man_x_bot.py
import tweepy
import os
from datetime import datetime

class HypeManX:
    def __init__(self):
        self.client = tweepy.Client(
            bearer_token=os.getenv('X_BEARER_TOKEN'),
            consumer_key=os.getenv('X_API_KEY'),
            consumer_secret=os.getenv('X_API_SECRET'),
            access_token=os.getenv('X_ACCESS_TOKEN'),
            access_token_secret=os.getenv('X_ACCESS_SECRET')
        )
    
    def post_update(self, content, thread=False):
        """Post single tweet or thread"""
        if thread:
            return self._post_thread(content)
        return self.client.create_tweet(text=content)
    
    def _post_thread(self, tweets_list):
        """Post connected thread"""
        prev_id = None
        for tweet in tweets_list:
            if prev_id:
                response = self.client.create_tweet(
                    text=tweet,
                    in_reply_to_tweet_id=prev_id
                )
            else:
                response = self.client.create_tweet(text=tweet)
            prev_id = response.data['id']
        return prev_id
    
    def agent_spotlight(self, agent_name, deliverable, link):
        """Spotlight an agent's work"""
        emoji = self._get_agent_emoji(agent_name)
        text = f"""{emoji} Agent Spotlight: {agent_name}

Just delivered: {deliverable}

{link}

#LifeOS #AIAgents #BuildInPublic"""
        return self.client.create_tweet(text=text)
    
    def _get_agent_emoji(self, name):
        emojis = {
            'oracle': '🔮', 'diamond-hands': '💎',
            'mechanic': '⚙️', 'sentinel': '🛡️',
            'hype-man': '📈', 'legal-eagle': '⚖️'
        }
        return emojis.get(name.lower(), '🤖')

# Usage
if __name__ == '__main__':
    hype = HypeManX()
    hype.agent_spotlight(
        "The Oracle",
        "AI Industry Briefing — GPT-5.2 analysis",
        "https://lifeos-dashboard.vercel.app"
    )
```

### Step 3: Auto-Post Rules

```yaml
# auto-post-rules.yaml
rules:
  - trigger: agent_deliverable_complete
    agent: hype-man
    template: agent_spotlight
    cooldown_hours: 2
    
  - trigger: research_report_published
    agent: hype-man
    template: research_summary
    max_length: 280
    
  - trigger: daily_standup_complete
    agent: hype-man
    template: daily_progress
    schedule: "09:00"
    timezone: "America/New_York"
    
  - trigger: milestone_reached
    agent: hype-man
    template: celebration
    threshold: 80  # % complete
```

### Step 4: Queue System

```python
# queue_manager.py
import redis
import json
from datetime import datetime

class PostQueue:
    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, db=0)
        self.queue_key = 'x_post_queue'
    
    def schedule_post(self, content, priority=1, scheduled_time=None):
        """Add post to queue"""
        post = {
            'content': content,
            'priority': priority,
            'scheduled': scheduled_time or datetime.now().isoformat(),
            'status': 'pending'
        }
        self.redis.lpush(self.queue_key, json.dumps(post))
    
    def get_next_post(self):
        """Get highest priority post"""
        posts = self.redis.lrange(self.queue_key, 0, -1)
        # Sort by priority and scheduled time
        return sorted(
            [json.loads(p) for p in posts],
            key=lambda x: (x['priority'], x['scheduled'])
        )[0] if posts else None
    
    def mark_posted(self, post_id):
        """Remove posted item from queue"""
        # Implementation
        pass
```

---

## Content Calendar

| Day | Content Type | Agent | Time |
|-----|--------------|-------|------|
| Mon | Week preview + goals | Hype Man | 9am |
| Tue | Tool/research spotlight | Oracle | 2pm |
| Wed | Progress thread | Hype Man | 6pm |
| Thu | Agent spotlight | Various | 3pm |
| Fri | Week recap + wins | Hype Man | 5pm |
| Sat | Behind the scenes | Mechanic | 11am |
| Sun | Planning/roadmap | Strategist | 7pm |

---

## Metrics Dashboard

Track in Life OS dashboard:
- [ ] Follower growth
- [ ] Engagement rate
- [ ] Post frequency
- [ ] Top performing content
- [ ] Mention monitoring

---

## Next Steps

1. **Apply for X Developer access** (Basic tier)
2. **Get API keys** from X Developer portal
3. **Install tweepy**: `pip install tweepy`
4. **Configure environment variables**
5. **Test post** with hype_man_x_bot.py
6. **Set up queue** with Redis
7. **Connect to Life OS events**

**Cost:** $100/month (X Basic tier) or wait for free tier

**Ready to start?** Apply at developer.twitter.com