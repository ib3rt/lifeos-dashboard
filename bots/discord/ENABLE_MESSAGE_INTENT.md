# Enable Discord Bot Message Reading

## What You Need To Do (2 minutes):

### 1. Go to Discord Developer Portal
**URL:** https://discord.com/developers/applications/1467746979189882920/bot

### 2. Enable Privileged Intents
1. Scroll down to **"Privileged Gateway Intents"**
2. Toggle ON: **"MESSAGE CONTENT INTENT"**
3. Click **"Save Changes"**

### 3. Test It
- Type something in #general
- I'll see it here in Telegram!
- Reply with: `!discord #channel Your message`

---

## Alternative: Use @Mentions (Works Now!)

Without enabling that setting, the bot can still:
- ✅ Respond to @Bonzi mentions
- ✅ Respond to !commands
- ✅ Respond in agent-specific channels

So you can:
1. Type `@Bonzi your message` in any Discord channel
2. I'll see the mention and respond
3. Or use `!agents`, `!status`, etc.

---

## What Will Work After Enabling:

**EVERY message in Discord → Forwarded to Telegram**

You'll see:
```
📨 Discord | Life-OS Command Center | #general
👤 b3rt
💬 Hey, what do you think about this?

!reply 123456789 Your response here
```

Then I can reply and it goes back to Discord!

---

**Go enable MESSAGE CONTENT INTENT now, then tell me when done!**
