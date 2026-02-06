# 🌉 Full Discord-Telegram Bridge Setup

## What You'll Get:

### ✅ Bidirectional Messaging
- **Discord → Telegram**: All messages forwarded to you
- **Telegram → Discord**: Reply and it posts back
- **Images**: Shared both ways

### ✅ Talk to Claw in Discord
| Method | Example | Result |
|--------|---------|--------|
| @Mention | `@Bonzi What's new?` | Message sent to Claw on Telegram |
| !ask command | `!ask Help with X` | Claw sees it, responds |
| !claw command | `!claw Deploy dashboard` | Action request to Claw |

### ✅ Auto-Responses
- Clack (the Discord bot persona) acknowledges receipt
- Full response comes from Claw on Telegram
- Can reply back to Discord

---

## Setup Steps:

### Step 1: Enable MESSAGE CONTENT INTENT (REQUIRED)

**Go to:** https://discord.com/developers/applications/1467746979189882920/bot

1. Find **"Privileged Gateway Intents"**
2. Toggle **"MESSAGE CONTENT INTENT"** → **ON** ✅
3. Click **"Save Changes"**

### Step 2: Restart Bridge

Once enabled, I'll restart the bridge:
```bash
kill $(cat ~/.openclaw/bridge/bridge.pid)
python3 full-bridge.py
```

### Step 3: Test It

**In Discord:**
```
@Bonzi Hello from Discord!
```

**You'll see in Telegram:**
```
📨 Discord Question from [username]
📍 #general
💬 Hello from Discord!

Reply with: !discord 123456 Your response
```

**Reply in Telegram:**
```
!discord 123456 Hey! I see you in Discord!
```

**Appears in Discord:**
```
🤖 Claw: Hey! I see you in Discord!
```

---

## Commands in Discord:

| Command | What It Does |
|---------|--------------|
| `@Bonzi <message>` | Send message to Claw on Telegram |
| `!ask <question>` | Same as @mention |
| `!claw <request>` | Action request |
| `!status` | Show bridge status |
| `!help` | All commands |

---

## Image Support:

**Discord → Telegram:**
- Post image in Discord
- URL forwarded to Telegram
- Can view and reply

**Telegram → Discord:**
- Send image URL in reply
- Bot posts image to Discord

---

**Ready? Enable MESSAGE CONTENT INTENT now!**
