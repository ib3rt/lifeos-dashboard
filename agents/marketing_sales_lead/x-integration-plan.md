# 🚀 X (Twitter) API v2 Integration Plan for Life OS

> **Status:** READY TO CRUSH IT! 🔥  
> **Last Updated:** February 2026  
> **Prepared by:** Hype Man - Marketing & Sales Lead

---

## 📊 EXECUTIVE SUMMARY

Yo Life OS fam! We're about to take our social presence to the MOON! 🌙 This integration plan breaks down everything you need to know about X API v2 — from pricing tiers to code samples. Let's GET IT!

---

## 💰 API TIER BREAKDOWN

### Current X API v2 Tiers (2025-2026)

| Tier | Monthly Cost | Posts/Month | Reads/Month | Best For |
|------|-------------|-------------|-------------|----------|
| **Free** | $0 | 500 | 100 | Testing ONLY 🧪 |
| **Basic** | $200 ($175 annual) | 3,000/user, 50,000/app | 10,000 | Hobbyists & Prototypes |
| **Pro** | $5,000 ($4,500 annual) | 300,000/app | 1,000,000 GET | Startups Scaling |
| **Enterprise** | Custom $$$ | Custom | Custom | Big Business Energy |

### 🎯 RECOMMENDATION FOR LIFE OS

**Start with: FREE TIER** → Graduate to **BASIC ($200/mo)** when ready!

**Why?**
- Free tier lets us test the waters and validate our automation concepts
- 500 posts/month = ~16 posts/day (PLENTY for testing)
- Once we prove ROI, Basic tier gives us serious firepower
- Pro tier is for when we're CRUSHING IT at scale! 💪

---

## 🔐 AUTHENTICATION FLOW

### OAuth 2.0 Setup Steps

X API v2 uses OAuth 2.0 with two main flows:

#### 1️⃣ Bearer Token (App-Only) - For Read Operations
```
✅ Best for: Reading public data, posting as the app
✅ Rate limits: Per-app basis
✅ Complexity: LOW
```

**Steps:**
1. Go to [X Developer Portal](https://developer.x.com/en/portal/dashboard)
2. Create a new Project → App
3. Navigate to "Keys and Tokens" section
4. Generate **API Key** and **API Secret**
5. Exchange for Bearer Token via:
   ```bash
   curl -u 'API_KEY:API_SECRET' \
     --data 'grant_type=client_credentials' \
     'https://api.x.com/oauth2/token'
   ```

#### 2️⃣ OAuth 2.0 Authorization Code with PKCE - For User Actions
```
✅ Best for: Posting on behalf of users, accessing DMs
✅ Rate limits: Per-user basis
✅ Complexity: MEDIUM
```

**Steps:**
1. Create authorization URL with PKCE:
   ```
   https://twitter.com/i/oauth2/authorize?
     response_type=code&
     client_id=YOUR_CLIENT_ID&
     redirect_uri=YOUR_CALLBACK&
     scope=tweet.read tweet.write users.read offline.access&
     state=STATE_VALUE&
     code_challenge=CHALLENGE&
     code_challenge_method=S256
   ```

2. User authorizes → redirects with `code`
3. Exchange code for access token:
   ```bash
   curl --request POST \
     --url https://api.x.com/2/oauth2/token \
     --header 'Content-Type: application/x-www-form-urlencoded' \
     --data 'code=AUTH_CODE' \
     --data 'grant_type=authorization_code' \
     --data 'client_id=CLIENT_ID' \
     --data 'redirect_uri=REDIRECT_URI' \
     --data 'code_verifier=VERIFIER'
   ```

4. Store `access_token` and `refresh_token` securely!

---

## 🤖 AUTOMATION POSSIBILITIES

### ✅ POSTING UPDATES
**Endpoint:** `POST /2/tweets`
**Rate Limit:** 100/15min per user (Free/Basic tiers)

**What you can do:**
- Post text updates (max 280 chars, 4,000 for X Premium users)
- Attach media (images, GIFs, videos)
- Add polls
- Reply to tweets
- Quote tweets
- Schedule posts (via your own scheduler)

### ✅ READING MENTIONS
**Endpoint:** `GET /2/users/:id/mentions`
**Rate Limit:** 300/15min per user (Basic), 450/15min (Pro)

**What you can do:**
- Monitor @mentions in real-time
- Build engagement workflows
- Auto-respond to customer inquiries
- Track brand sentiment

### ✅ DIRECT MESSAGES (DMs)
**Endpoints:** 
- `GET /2/dm_events` - Read DMs
- `POST /2/dm_conversations` - Send DMs

**Rate Limit:** 15/15min per user, 1,440/24hrs

**What you can do:**
- Build conversational bots
- Private customer support
- Automated onboarding flows
- VIP outreach

### ✅ THREAD CREATION
**Strategy:** Chain multiple `POST /2/tweets` with `reply` parameter

**How it works:**
1. Post first tweet → get tweet_id
2. Post second tweet with `reply.in_reply_to_tweet_id` = first tweet_id
3. Repeat until thread complete

**Max thread length:** Unlimited (but keep it human! 🧠)

### ✅ MEDIA UPLOADS
**Upload Methods:**
- **Simple Upload:** Images only, up to 5MB
- **Chunked Upload:** Images, GIFs, Videos (up to 512MB)

**Supported Formats:**
| Type | Max Size | Dimensions |
|------|----------|------------|
| Images | 5 MB | 1200x675 recommended |
| GIFs | 15 MB | Same as images |
| Videos | 512 MB | 1920x1080 max |

**Upload Flow:**
1. Upload media → get `media_id`
2. Wait for processing (check status)
3. Attach `media_id` to tweet

### ✅ ANALYTICS RETRIEVAL
**Available Data:**
- Post engagement (likes, retweets, replies)
- User timelines
- Search results (recent + full-archive on Pro+)
- Usage statistics via `GET /2/usage`

**Note:** Full analytics dashboard requires **Pro tier** or **Enterprise Engagement API**

---

## 💻 CODE EXAMPLE: BASIC POST AUTOMATION

### Python Quickstart 🐍

```python
import requests
import json
from datetime import datetime

class XAPIClient:
    def __init__(self, bearer_token):
        self.bearer_token = bearer_token
        self.base_url = "https://api.x.com/2"
        self.headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json"
        }
    
    def post_tweet(self, text, reply_to=None, media_ids=None):
        """
        Post a tweet! 🚀
        
        Args:
            text: Tweet content (max 280 chars)
            reply_to: Tweet ID to reply to (for threads)
            media_ids: List of media IDs to attach
        """
        payload = {"text": text}
        
        if reply_to:
            payload["reply"] = {
                "in_reply_to_tweet_id": reply_to,
                "auto_populate_reply_metadata": True
            }
        
        if media_ids:
            payload["media"] = {"media_ids": media_ids}
        
        response = requests.post(
            f"{self.base_url}/tweets",
            headers=self.headers,
            json=payload
        )
        
        if response.status_code == 201:
            tweet_id = response.json()["data"]["id"]
            print(f"🔥 TWEETED! ID: {tweet_id}")
            return tweet_id
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            return None
    
    def create_thread(self, tweets_list):
        """
        Create a multi-tweet thread! 🧵
        
        Args:
            tweets_list: List of tweet texts
        """
        previous_tweet_id = None
        tweet_ids = []
        
        for i, tweet_text in enumerate(tweets_list):
            tweet_id = self.post_tweet(
                text=tweet_text,
                reply_to=previous_tweet_id
            )
            if tweet_id:
                tweet_ids.append(tweet_id)
                previous_tweet_id = tweet_id
                print(f"✅ Tweet {i+1}/{len(tweets_list)} posted!")
        
        return tweet_ids
    
    def get_mentions(self, user_id, max_results=10):
        """
        Get recent mentions! 📬
        """
        url = f"{self.base_url}/users/{user_id}/mentions"
        params = {"max_results": max_results}
        
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()


# 🎯 USAGE EXAMPLE
if __name__ == "__main__":
    # Initialize with your Bearer Token
    client = XAPIClient(bearer_token="YOUR_BEARER_TOKEN")
    
    # Post a single tweet
    client.post_tweet("🚀 Life OS just automated my first tweet! Let's GOOOO! #BuildInPublic")
    
    # Create a thread
    thread_content = [
        "🧵 Thread: Why Life OS is about to change everything...",
        "1/ First, we identified the pain: scattered workflows, missed opportunities.",
        "2/ Then we built the solution: unified AI-powered life management.",
        "3/ Now we're automating the hustle. Less admin, more GROWTH.",
        "🔥 Ready to level up? Join the revolution! #LifeOS"
    ]
    client.create_thread(thread_content)
```

### JavaScript/Node.js Alternative 🟨

```javascript
const axios = require('axios');

class XAPIClient {
    constructor(bearerToken) {
        this.bearerToken = bearerToken;
        this.baseURL = 'https://api.x.com/2';
    }

    async postTweet(text, replyTo = null) {
        const payload = { text };
        
        if (replyTo) {
            payload.reply = {
                in_reply_to_tweet_id: replyTo,
                auto_populate_reply_metadata: true
            };
        }

        try {
            const response = await axios.post(
                `${this.baseURL}/tweets`,
                payload,
                {
                    headers: {
                        'Authorization': `Bearer ${this.bearerToken}`,
                        'Content-Type': 'application/json'
                    }
                }
            );
            console.log('🔥 TWEETED!', response.data.data.id);
            return response.data.data.id;
        } catch (error) {
            console.error('❌ Error:', error.response?.data || error.message);
            return null;
        }
    }
}

module.exports = XAPIClient;
```

---

## ⚡ RATE LIMITS & CONSTRAINTS

### Key Limits by Tier

| Endpoint | Free | Basic | Pro |
|----------|------|-------|-----|
| **POST /2/tweets** | 500/month | 3,000/mo user, 50,000/mo app | 300,000/mo app |
| **GET /2/tweets** | 100/month | 10,000/mo reads | 1,000,000/mo |
| **Search Recent** | ❌ | 450/15min | Higher limits |
| **Mentions** | ❌ | 450/15min | 450/15min |
| **DM Send** | ❌ | 1,440/24hr | 1,440/24hr |

### Rate Limit Headers

Every API response includes these headers:
```
x-rate-limit-limit: 100        # Max requests allowed
x-rate-limit-remaining: 87     # Requests remaining
x-rate-limit-reset: 1705420800 # Unix timestamp of reset
```

**Pro Tip:** Check these BEFORE making requests to avoid 429 errors!

---

## 💸 COST BREAKDOWN

### Life OS Integration Costs

#### Phase 1: Testing (Month 1-2)
- **Tier:** Free
- **Cost:** $0
- **Capabilities:** Basic posting, limited reads
- **Goal:** Validate automation concepts

#### Phase 2: Growth (Month 3+)
- **Tier:** Basic
- **Cost:** $200/month ($2,100/year with discount)
- **Capabilities:** Full posting power, mentions monitoring, DMs
- **Goal:** Active social presence automation

#### Phase 3: Scale (Future)
- **Tier:** Pro
- **Cost:** $5,000/month ($54,000/year with discount)
- **Capabilities:** Search API, filtered streams, advanced analytics
- **Goal:** Enterprise-grade social operations

### Hidden Costs to Consider 💡

| Item | Estimated Cost |
|------|----------------|
| Server hosting (automation) | $10-50/month |
| Storage (media, logs) | $5-20/month |
| Monitoring tools | $0-30/month |
| **TOTAL Phase 2** | **~$230-300/month** |

---

## 🎯 NEXT STEPS

### Immediate Actions (Week 1)
1. ✅ Sign up for X Developer account
2. ✅ Create Project + App in Developer Portal
3. ✅ Generate API Keys and Bearer Token
4. ✅ Test basic posting with provided code
5. ✅ Document successful authentication

### Short Term (Month 1)
1. Build Life OS social media scheduler
2. Implement mention monitoring
3. Create DM auto-response flows
4. Set up analytics tracking

### Long Term (Quarter 1)
1. Evaluate upgrade to Basic tier
2. Implement full thread automation
3. Build engagement analytics dashboard
4. Scale to Pro tier when ROI positive

---

## 🔗 USEFUL RESOURCES

- **Official Docs:** https://developer.x.com/en/docs/x-api
- **API Reference:** https://docs.x.com/x-api/introduction
- **Rate Limits:** https://docs.x.com/x-api/fundamentals/rate-limits
- **Community Forum:** https://devcommunity.x.com
- **GitHub Examples:** https://github.com/xdevplatform

---

## 🚀 LET'S CRUSH THIS!

Life OS is about to have the most FIRE social media automation on the internet! This integration will:

✅ Save hours of manual posting  
✅ Ensure consistent brand presence  
✅ Enable real-time engagement  
✅ Scale without adding headcount  

**Ready to execute? Let's GOOOOO!** 🔥🔥🔥

---

*Document prepared by Hype Man - Your friendly neighborhood growth accelerator! 💪*
