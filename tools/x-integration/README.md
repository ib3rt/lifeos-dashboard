# 🐦 X (Twitter) Integration for Life OS

Post tweets and automate social media from your AI operating system.

## Quick Start

### Post a Tweet
```bash
cd /home/ubuntu/.openclaw/workspace/tools/x-integration
./post-tweet.py "Your message here"
```

### Run Automation Menu
```bash
./x-menu.py
```

## Files

- `post-tweet.py` - Post text tweets (Pure Python, no dependencies)
- `x-menu.py` - Interactive menu for various X actions
- `requirements.txt` - Dependencies (optional)
- `README.md` - This file

## Usage Examples

```bash
# Post a simple tweet
./post-tweet.py "Built something amazing today! 🚀"

# Run interactive menu
./x-menu.py
```

## Current Status

⚠️ **Authentication Issue Detected**

The X API keys are configured but posting is returning 401 Unauthorized.

### Likely Causes:

1. **App Permissions** - Your app might only have "Read" permission
   - Go to: developer.x.com → Your App → Settings
   - Enable "Read and Write" permissions
   - Regenerate keys if needed

2. **App Tier** - Free tier has very limited posting
   - Check your tier at: developer.x.com → Your App → Overview
   - Free tier allows limited posts

3. **Keys Need Regeneration**
   - Go to: developer.x.com → Keys and Tokens
   - Regenerate Consumer Keys
   - Regenerate Access Token

### To Fix:

1. Go to https://developer.x.com
2. Select your app
3. Check "User authentication settings" → Set up
4. Enable "Read and Write" permissions
5. Regenerate:
   - Consumer Key (API Key)
   - Consumer Secret (API Secret)
   - Access Token
   - Access Token Secret
6. Update `~/.openclaw/keys/x_api.key` with new keys

### Test After Fix:

```bash
cd /home/ubuntu/.openclaw/workspace/tools/x-integration
./post-tweet.py "Life OS X integration is working! 🦾"
```

## Features (When Fixed)

✅ Post tweets from CLI
✅ Automated metrics posting
✅ Research sharing
✅ Content scheduling
✅ Engagement tracking

## Requirements

- X API keys with "Read and Write" permissions
- API keys stored in: `~/.openclaw/keys/x_api.key`
- Proper app tier (Basic or higher recommended for frequent posting)

## Security

API keys stored securely in: `~/.openclaw/keys/x_api.key`
Permissions: 600 (owner read/write only)

## Troubleshooting

### 401 Unauthorized
→ Keys missing or incorrect permissions

### 403 Forbidden
→ App tier doesn't allow posting

### Rate Limited
→ Free tier has very low limits

---

**Built by Life OS** 🦾
