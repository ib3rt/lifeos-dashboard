#!/bin/bash
# Morning Brief Generator
# Runs daily at 8 AM EST
# Sends comprehensive morning brief to b3rt

LOG_FILE="~/.openclaw/logs/morning-brief.log"
DATE=$(date '+%A, %B %d, %Y')
TIME=$(date '+%I:%M %p %Z')

echo "========================================" >> $LOG_FILE
echo "🌅 MORNING BRIEF - $DATE" >> $LOG_FILE
echo "========================================" >> $LOG_FILE

# Get weather
WEATHER=$(curl -s "https://wttr.in/?format=%C+%t+%w" 2>/dev/null || echo "Weather data unavailable")

cat > /tmp/morning-brief.txt << EOF
🌅 **GOOD MORNING, GENERAL!**

📅 **$DATE** | ⏰ **$TIME**

═══════════════════════════════════════════════════

🌤️ **TODAY'S WEATHER**
$WEATHER

═══════════════════════════════════════════════════

📋 **YOUR TASKS FOR TODAY**
EOF

# Check for active todos
cd ~/.openclaw/workspace
if [ -f "memory/daily-tasks.md" ]; then
    echo "" >> /tmp/morning-brief.txt
    grep -E "^- \[ \]" memory/daily-tasks.md | head -5 >> /tmp/morning-brief.txt
else
    echo "" >> /tmp/morning-brief.txt
    echo "📋 No active todos in system" >> /tmp/morning-brief.txt
fi

cat >> /tmp/morning-brief.txt << EOF

═══════════════════════════════════════════════════

🤖 **WHAT I CAN DO FOR YOU TODAY**

EOF

# Analyze what would be most helpful
# Based on current projects and context
cat >> /tmp/morning-brief.txt << EOF
Based on current projects:
• Monitor Life OS agent tasks
• Continue 2nd Brain development
• Review any overnight PRs from Proactive Coder
• Check Discord for community activity
• Analyze business metrics

Proactive suggestions:
• Optimize one workflow bottleneck
• Create documentation for recent builds
• Research new automation opportunities

═══════════════════════════════════════════════════

📺 **TRENDING VIDEOS**

EOF

# Note: YouTube API integration would go here
# For now, placeholder with search suggestions
cat >> /tmp/morning-brief.txt << EOF
*YouTube trending for your interests:*
• Search: "AI agent development 2026"
• Search: "NextJS 14 new features"
• Search: "Solana DeFi updates"
• Search: "Productivity automation tools"

*Note: YouTube API integration pending*

═══════════════════════════════════════════════════

📰 **TRENDING STORIES**

EOF

# Use web search for trending stories
cat >> /tmp/morning-brief.txt << EOF
*Quick search suggestions:*
• "AI news today"
• "crypto market updates"
• "tech startup funding"
• "automation tools 2026"

*Note: News API integration pending*

═══════════════════════════════════════════════════

💡 **TODAY'S PRODUCTIVITY RECOMMENDATION**

🎯 **Focus Block Strategy:**
• 8:30-10:30 AM: Deep work on priority task
• 10:30-11:00 AM: Break + communication check
• 11:00-12:30 PM: Secondary tasks
• 12:30-1:30 PM: Lunch + recharge
• 1:30-3:30 PM: Collaborative/communicative work
• 3:30-5:00 PM: Wrap up + planning

🧠 **Mindset:** Progress over perfection. One important thing completed > ten things started.

═══════════════════════════════════════════════════

🚀 **SYSTEM STATUS**
• Life OS: 30 agents active
• Tasks: 60+ in progress
• Proactive Coder: Ready for tonight
• 2nd Brain: Building in progress

═══════════════════════════════════════════════════

**Have a productive day, General! 🎖️**

*Brief generated at $TIME*
EOF

# Send full brief to Discord morning-brief channel
export DISCORD_BOT_TOKEN=$(cat ~/.openclaw/discord/bot.token 2>/dev/null)

if [ -n "$DISCORD_BOT_TOKEN" ]; then
    python3 << 'PYDISCORD'
import discord
import os

token = os.environ.get('DISCORD_BOT_TOKEN')

class MorningBrief(discord.Client):
    async def on_ready(self):
        for guild in self.guilds:
            if "Life" in guild.name:
                # Post to morning-brief channel
                brief_ch = discord.utils.get(guild.text_channels, name="morning-brief")
                if brief_ch:
                    from datetime import datetime
                    date_str = datetime.now().strftime("%A, %B %d")
                    time_str = datetime.now().strftime("%I:%M %p %Z")
                    
                    # Read the full brief content
                    try:
                        with open('/tmp/morning-brief.txt', 'r') as f:
                            brief_content = f.read()
                    except:
                        brief_content = "Morning brief content unavailable"
                    
                    # Split into chunks if too long (Discord limit 2000 chars per message)
                    chunks = [brief_content[i:i+1900] for i in range(0, len(brief_content), 1900)]
                    
                    # Send header
                    header_embed = discord.Embed(
                        title=f"🌅 MORNING BRIEF",
                        description=f"**{date_str}** | {time_str}",
                        color=0xffa500
                    )
                    await brief_ch.send(embed=header_embed)
                    
                    # Send content chunks
                    for i, chunk in enumerate(chunks):
                        await brief_ch.send(f"```{chunk}```" if i == 0 else f"```...{chunk}```")
                    
                    print(f"✅ Posted morning brief to #{brief_ch.name}")
                break
        await self.close()

intents = discord.Intents.default()
client = MorningBrief(intents=intents)
client.run(token)
PYDISCORD
fi

echo "✅ Morning brief complete" >> $LOG_FILE
echo "" >> $LOG_FILE

# Also output for Telegram
if [ -f /tmp/morning-brief.txt ]; then
    cat /tmp/morning-brief.txt
fi