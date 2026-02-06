#!/bin/bash
# Afternoon Research Report Generator
# Runs daily at 4 PM EST
# Delivers research on topics that improve b3rt's work/life

LOG_FILE="~/.openclaw/logs/afternoon-research.log"
DATE=$(date '+%A, %B %d, %Y')
TIME=$(date '+%I:%M %p %Z')
DAY_OF_WEEK=$(date +%u)  # 1=Monday, 7=Sunday

echo "========================================" >> $LOG_FILE
echo "🕓 AFTERNOON RESEARCH - $DATE" >> $LOG_FILE
echo "========================================" >> $LOG_FILE

# Determine topic based on day of week
case $DAY_OF_WEEK in
    1)  # Monday - AI/ML
        TOPIC="AI & Machine Learning"
        SUBTOPIC="AI Agent Architectures: Building Autonomous Systems"
        INSIGHTS="• Multi-agent orchestration patterns\n• Memory management in LLM agents\n• Tool-use capabilities and function calling\n• Self-improvement loops in AI systems"
        IMPLEMENTATION="1. Review current agent architecture\n2. Implement memory persistence layer\n3. Add tool-use capabilities\n4. Test autonomous task completion"
        RESOURCES="• LangChain docs: langchain.com\n• AutoGPT architecture\n• CrewAI multi-agent patterns\n• OpenAI function calling guide"
        PREVIEW="Tuesday: Business Automation Workflows"
        ;;
    2)  # Tuesday - Business/Automation
        TOPIC="Business & Automation"
        SUBTOPIC="The $100/Hour Framework: Automating High-Value Tasks"
        INSIGHTS="• Calculate your effective hourly rate\n• Identify $10/hour vs $100/hour tasks\n• Automation ROI calculation\n• Delegation vs automation matrix"
        IMPLEMENTATION="1. Track your time for 3 days\n2. Categorize tasks by value\n3. Automate lowest-value repetitive tasks\n4. Delegate where automation isn't possible"
        RESOURCES="• Zapier automation guide\n• n8n workflow examples\n• Make.com (Integromat) tutorials\n• 'Buy Back Your Time' - Dan Martell"
        PREVIEW="Wednesday: DeFi Yield Strategies"
        ;;
    3)  # Wednesday - Crypto/Web3
        TOPIC="Crypto & Web3"
        SUBTOPIC="DeFi Yield Optimization: Current Landscape"
        INSIGHTS="• Aave v3 features and improvements\n• Lido stETH staking mechanics\n• Real yield vs inflationary rewards\n• Risk-adjusted return calculation"
        IMPLEMENTATION="1. Review current portfolio allocation\n2. Compare yields across protocols\n3. Assess risk tolerance\n4. Consider diversifying across chains"
        RESOURCES="• DeFiLlama yield dashboard\n• Aave documentation\n• Lido staking guide\n• Bankless newsletter"
        PREVIEW="Thursday: Development Tools & Workflows"
        ;;
    4)  # Thursday - Development
        TOPIC="Development & Tools"
        SUBTOPIC="NextJS 14 App Router: Patterns and Best Practices"
        INSIGHTS="• Server Components vs Client Components\n• Server Actions for mutations\n• Parallel routes and intercepting routes\n• Caching strategies and revalidation"
        IMPLEMENTATION="1. Audit current pages vs app router usage\n2. Migrate data fetching to Server Components\n3. Implement Server Actions for forms\n4. Optimize caching for your use case"
        RESOURCES="• NextJS 14 documentation\n• Vercel patterns\n• App Router migration guide\n• Server Actions deep dive"
        PREVIEW="Friday: Productivity Systems"
        ;;
    5)  # Friday - Personal Growth
        TOPIC="Personal Growth & Systems"
        SUBTOPIC="The PARA Method: Organizing Digital Life"
        INSIGHTS="• Projects vs Areas distinction\n• Resource library organization\n• Archive for completed items\n• Weekly review process"
        IMPLEMENTATION="1. Set up PARA folders (Projects, Areas, Resources, Archive)\n2. Move existing files into structure\n3. Create weekly review calendar event\n4. Practice the 2-minute rule for processing"
        RESOURCES="• Tiago Forte's Building a Second Brain\n• PARA method article\n• Notion PARA template\n• Obsidian PARA setup"
        PREVIEW="Weekend: Special Deep Dive (your choice)"
        ;;
    6|7)  # Weekend
        TOPIC="Weekend Deep Dive"
        SUBTOPIC="Recommending based on recent activity..."
        INSIGHTS="• Reviewing recent conversations\n• Identifying knowledge gaps\n• Exploring adjacent topics\n• Preparing for next week"
        IMPLEMENTATION="1. Review this week's reports\n2. Choose one concept to implement\n3. Set up any needed tools/accounts\n4. Plan Monday focus"
        RESOURCES="• This week's research links\n• Your saved bookmarks\n• Pending reading list\n• Community recommendations"
        PREVIEW="Monday: AI & Machine Learning"
        ;;
esac

cat > /tmp/afternoon-research.txt << EOF
🕓 **AFTERNOON RESEARCH REPORT**
═══════════════════════════════════════════════════

📅 **$DATE** | 🎯 **Focus: $TOPIC**

═══════════════════════════════════════════════════

📋 **$SUBTOPIC**

═══════════════════════════════════════════════════

🎯 **WHY THIS MATTERS**

This topic directly relates to your current work on Life OS, your interest in automation, and your goal of building a 1-person business empire. Understanding this concept will help you work smarter and scale your impact.

═══════════════════════════════════════════════════

💡 **KEY INSIGHTS**

$INSIGHTS

═══════════════════════════════════════════════════

🔧 **HOW TO IMPLEMENT**

$IMPLEMENTATION

═══════════════════════════════════════════════════

📚 **RESOURCES TO EXPLORE**

$RESOURCES

═══════════════════════════════════════════════════

💭 **THOUGHT STARTER**

What's one thing you learned today that you could implement before bed tonight? Small actions compound into massive results.

═══════════════════════════════════════════════════

📅 **TOMORROW'S TOPIC:** $PREVIEW

═══════════════════════════════════════════════════

*Research report generated at $TIME*
*Source: Afternoon Research Protocol v1.0*

EOF

# Save to 2nd Brain
cp /tmp/afternoon-research.txt ~/.openclaw/workspace/second-brain/concepts/$(date +%Y-%m-%d)-research-report.md

# Send full report to Discord afternoon-brief channel
export DISCORD_BOT_TOKEN=$(cat ~/.openclaw/discord/bot.token 2>/dev/null)

if [ -n "$DISCORD_BOT_TOKEN" ]; then
    python3 << 'PYDISCORD'
import discord
import os
from datetime import datetime

token = os.environ.get('DISCORD_BOT_TOKEN')
day = datetime.now().weekday()

topics = {
    0: ("AI & Machine Learning", "AI Agent Architectures", "0x3498db"),
    1: ("Business & Automation", "$100/Hour Framework", "0x2ecc71"),
    2: ("Crypto & Web3", "DeFi Yield Optimization", "0xf1c40f"),
    3: ("Development & Tools", "NextJS 14 Patterns", "0xe74c3c"),
    4: ("Personal Growth & Systems", "The PARA Method", "0x9b59b6"),
    5: ("Weekend Deep Dive", "Special Research", "0x95a5a6"),
    6: ("Weekend Deep Dive", "Special Research", "0x95a5a6"),
}

topic, subtopic, color = topics.get(day, ("Research", "Deep Dive", "0x3498db"))

class AfternoonResearch(discord.Client):
    async def on_ready(self):
        for guild in self.guilds:
            if "Life" in guild.name:
                # Post to afternoon-brief channel
                brief_ch = discord.utils.get(guild.text_channels, name="afternoon-brief")
                if brief_ch:
                    date_str = datetime.now().strftime("%A, %B %d")
                    time_str = datetime.now().strftime("%I:%M %p %Z")
                    
                    # Read the full research content
                    try:
                        with open('/tmp/afternoon-research.txt', 'r') as f:
                            research_content = f.read()
                    except:
                        research_content = "Research report content unavailable"
                    
                    # Send header embed
                    header_embed = discord.Embed(
                        title=f"🕓 AFTERNOON RESEARCH REPORT",
                        description=f"**{date_str}** | {time_str}\nFocus: {topic}",
                        color=color
                    )
                    await brief_ch.send(embed=header_embed)
                    
                    # Send full content (Discord handles long messages)
                    chunks = [research_content[i:i+1900] for i in range(0, len(research_content), 1900)]
                    for i, chunk in enumerate(chunks):
                        await brief_ch.send(f"```{chunk}```" if i == 0 else f"```...{chunk}```")
                    
                    print(f"✅ Posted research report to #{brief_ch.name}")
                break
        await self.close()

intents = discord.Intents.default()
client = AfternoonResearch(intents=intents)
client.run(token)
PYDISCORD
fi

echo "✅ Afternoon research report complete" >> $LOG_FILE
echo "📁 Saved to 2nd Brain" >> $LOG_FILE
echo "" >> $LOG_FILE

# Output for Telegram
cat /tmp/afternoon-research.txt
