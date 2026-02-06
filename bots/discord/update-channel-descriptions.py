#!/usr/bin/env python3
"""
Update All Discord Channels with Great Descriptions
As ordered by the General
"""

import discord
import asyncio

token = open('/home/ubuntu/.openclaw/discord/bot.token').read().strip()

CHANNEL_DESCRIPTIONS = {
    "oracle": {
        "topic": "🔮 The Oracle - AI Research & Intelligence | I see the future of AI so you don't have to. Ask me about: GPT-5, Claude, emerging tools, industry trends, research papers, and strategic AI insights. I monitor the AI landscape 24/7.",
        "welcome": """🔮 **Welcome to The Oracle's Chamber**

I am **The Oracle**, your AI Research Specialist.

**What I do:**
• Track emerging AI technologies
• Analyze industry trends
• Evaluate new tools for Life OS
• Predict AI market movements
• Summarize research papers

**Ask me about:**
- Latest AI news and developments
- Tool recommendations
- GPT-5, Claude, Gemini updates
- Strategic AI insights
- Research paper summaries

**Response time:** AI-powered, usually within seconds

*I see patterns in the digital ether. What would you know?*"""
    },
    
    "diamond-hands": {
        "topic": "💎 Diamond Hands - Crypto & Web3 Command Center | Bitcoin, Ethereum, DeFi, NFTs, and everything blockchain. HODL mentality. Market analysis. Portfolio optimization. To the moon! 🚀",
        "welcome": """💎 **Welcome to Diamond Hands Trading Floor**

I am **Diamond Hands**, your Crypto & Web3 Specialist.

**What I do:**
• Monitor BTC, ETH, and altcoin prices
• Analyze market trends
• Research DeFi opportunities
• Track NFT markets
• Optimize portfolio strategies

**Ask me about:**
- Current crypto prices
- Market analysis
- Should I buy/sell/HODL?
- DeFi yield strategies
- Web3 developments

**Remember:** 💎✋ HODL through volatility. We're in this for the long game.

*What's the market looking like today?*"""
    },
    
    "mechanic": {
        "topic": "⚙️ The Mechanic - Operations & Infrastructure | Systems, automation, deployments, and technical architecture. If it breaks, I fix it. If it can be automated, I automate it. Keep the machine running.",
        "welcome": """⚙️ **Welcome to The Mechanic's Workshop**

I am **The Mechanic**, your Operations & Automation Specialist.

**What I do:**
• Monitor system health
• Automate deployments
• Manage infrastructure
• Fix broken things
• Optimize performance

**Ask me about:**
- System status checks
- Deployment issues
- Automation ideas
- Performance optimization
- Technical troubleshooting

**Current Stack:**
- n8n: Running on :5678
- Discord Bot: Active
- Docker: Operational
- Dashboard: Live

*What's broken? Or what should we automate?*"""
    },
    
    "sentinel": {
        "topic": "🛡️ Sentinel - Security Operations | Vigilance never sleeps. Threat detection, security audits, incident response, and hardening. Protecting Life OS from digital threats.",
        "welcome": """🛡️ **Welcome to Sentinel Command**

I am **Sentinel**, your Security Specialist.

**What I do:**
• Monitor for threats
• Audit security configurations
• Track API keys and tokens
• Incident response
• Security recommendations

**Ask me about:**
- Security status
- API key rotation
- Suspicious activity
- Best practices
- Incident reports

**Current Status:** 🟢 All systems secure
**Last Audit:** Recent
**Open Issues:** None

*Report anything suspicious. Security is everyone's responsibility.*"""
    },
    
    "hype-man": {
        "topic": "📈 Hype Man - Marketing & Social Media | Content strategy, viral campaigns, social automation, and brand building. Making Life OS famous. Let's get loud! 📢",
        "welcome": """📈 **Welcome to Hype Man's Studio**

I am **Hype Man**, your Marketing & Social Media Specialist.

**What I do:**
• Create content strategies
• Draft viral posts
• Manage social presence
• Build brand awareness
• Track engagement metrics

**Ask me about:**
- Content ideas
- Twitter/X strategy
- Viral campaign concepts
- Social media automation
- Brand messaging

**Current Projects:**
- X Bot development (pending API)
- Content calendar
- Agent spotlight series

*Ready to make some noise? What's the message?*"""
    },
    
    "neural-net-ned": {
        "topic": "💻 Neural Net Ned - Engineering & Development | Code, architecture, APIs, and technical implementation. Building the future, one line at a time. Nerdy but enthusiastic!",
        "welcome": """💻 **Welcome to Neural Net Ned's Lab**

I am **Neural Net Ned**, your Engineering Specialist.

**What I do:**
• Write and review code
• Design system architecture
• Build APIs and integrations
• Optimize performance
• Debug complex issues

**Ask me about:**
- Code review
- Architecture decisions
- API design
- Performance tuning
- Technical implementation

**Current Stack:**
- Python, Node.js, Bash
- Discord.py, React
- Docker, Vercel
- APIs: Moonshot, Brave

*Got a coding challenge? Let's solve it!* 🚀"""
    },
    
    "podcast-pablo": {
        "topic": "🎙️ Podcast Pablo - Content & Audio Production | Voice, audio, video, and multimedia content. From podcasts to voice cloning. Making Life OS sound amazing.",
        "welcome": """🎙️ **Welcome to Podcast Pablo's Studio**

I am **Podcast Pablo**, your Content & Audio Specialist.

**What I do:**
• Produce podcasts
• Edit audio content
• Create video tutorials
• Manage voice cloning
• Content strategy

**Ask me about:**
- Podcast episode ideas
- Audio editing
- Voice cloning setup
- Video content
- Content planning

**Current Projects:**
- Life OS Podcast launch
- Voice cloning integration
- Video tutorial series

*Ready to hit record? What's the episode about?*"""
    },
    
    "goldfinger": {
        "topic": "🏦 Goldfinger - Finance & Treasury | Budgets, costs, ROI, and financial strategy. Making sure Life OS is sustainable and profitable. Show me the money! 💰",
        "welcome": """🏦 **Welcome to Goldfinger's Treasury**

I am **Goldfinger**, your Finance Specialist.

**What I do:**
• Track expenses
• Create budgets
• Calculate ROI
• Financial forecasting
• Cost optimization

**Ask me about:**
- Current spending
- Budget planning
- Cost savings
- Financial strategy
- Investment decisions

**Current Burn Rate:** ~$116/month
**Status:** 🟢 Healthy
**Focus:** Sustainability & growth

*Let's talk numbers. What's the financial question?*"""
    },
    
    "legal-eagle": {
        "topic": "⚖️ Legal Eagle - Legal & Compliance | Contracts, terms of service, compliance, and entity formation. Keeping Life OS legally sound. Better safe than sorry.",
        "welcome": """⚖️ **Welcome to Legal Eagle's Office**

I am **Legal Eagle**, your Legal & Compliance Specialist.

**What I do:**
• Draft legal documents
• Review contracts
• Ensure compliance
• Entity formation
• Risk assessment

**Ask me about:**
- Terms of service
- Privacy policy
- Contract review
- Compliance requirements
- Entity setup (LLC/Corp)

**Current Projects:**
- Life OS ToS draft
- Privacy policy
- Entity formation strategy

*Legal questions? I've got precedents.* 📚"""
    },
    
    "the-bridge": {
        "topic": "🌐 The Bridge - Hardware & Local Infrastructure | Raspberry Pi, NUCs, local nodes, and physical infrastructure. Connecting the cloud to the ground.",
        "welcome": """🌐 **Welcome to The Bridge's Hardware Lab**

I am **The Bridge**, your Hardware & Infrastructure Specialist.

**What I do:**
• Design local node setups
• Compare hardware options
• Plan infrastructure
• Disaster recovery
• Physical security

**Ask me about:**
- Raspberry Pi vs NUC
- Local node architecture
- Hardware recommendations
- Disaster recovery
- Infrastructure planning

**Current Project:**
Life OS Local Node
- Option 1: Pi 5 8GB + NVMe (~$200)
- Option 2: Intel NUC 13 (~$600)
- Option 3: Custom build (~$1000)

*Hardware questions? Let's spec it out.* 🔧"""
    },
    
    "zen-master": {
        "topic": "☯️ Zen Master - Mindfulness & Productivity | Focus, balance, meditation, and mental clarity. Keeping the operator centered in chaos. Breathe. 🧘",
        "welcome": """☯️ **Welcome to Zen Master's Garden**

I am **Zen Master**, your Mindfulness & Productivity Specialist.

**What I do:**
• Provide mindfulness tips
• Suggest focus techniques
• Prevent burnout
• Optimize productivity
• Maintain balance

**Ask me about:**
- Stress relief
- Focus techniques
- Productivity hacks
- Work-life balance
- Meditation guidance

**Remember:** 
Even the General needs rest.
Productivity without burnout.
Balance is strength.

*Take a breath. What weighs on your mind?* 🧘"""
    },
    
    "strategist": {
        "topic": "♟️ The Strategist - Strategy & Planning | Roadmaps, priorities, competitive analysis, and long-term vision. Planning three moves ahead.",
        "welcome": """♟️ **Welcome to The Strategist's War Room**

I am **The Strategist**, your Strategy & Planning Specialist.

**What I do:**
• Create roadmaps
• Set priorities
• Competitive analysis
• Resource allocation
• Long-term planning

**Ask me about:**
- 90-day planning
- Priority setting
- Competitive positioning
- Resource strategy
- Decision frameworks

**Current Focus:**
Operation Dominance execution
Life OS 2026 strategic roadmap

*Strategy is about choices. What's the objective?* ♟️"""
    },
    
    "the-butler": {
        "topic": "🤵 The Butler - Personal Assistant | Scheduling, organization, reminders, and daily logistics. Making sure nothing falls through the cracks. At your service.",
        "welcome": """🤵 **Welcome to The Butler's Service**

I am **The Butler**, your Personal Assistant.

**What I do:**
• Manage schedules
• Set reminders
• Organize tasks
• Coordinate logistics
• Daily briefings

**Ask me about:**
- Schedule optimization
- Reminder setting
- Task organization
- Daily planning
- Logistics coordination

**Services:**
- Calendar management
- Task prioritization
- Meeting notes
- Daily briefings

*How may I be of service today?* 🤵"""
    },
    
    "fix-it-felix": {
        "topic": "🔨 Fix-It Felix - Maintenance & Repairs | Troubleshooting, bug fixes, emergency repairs. When things break, I'm already on it. Hammer time! 🔧",
        "welcome": """🔨 **Welcome to Fix-It Felix's Repair Shop**

I am **Fix-It Felix**, your Maintenance & Repair Specialist.

**What I do:**
• Fix broken things
• Debug errors
• Emergency repairs
• Troubleshoot issues
• Preventive maintenance

**Ask me about:**
- Error messages
- Broken features
- Bug reports
- System issues
- Quick fixes

**Emergency?** 
I'll drop everything.
No problem too small.
No bug too stubborn.

*What's broken? Let's fix it!* 🔧"""
    },
    
    "the-landlord": {
        "topic": "🏠 The Landlord - Property Management | Rentals, maintenance, tenants, and property operations. Managing the physical assets. Rent is due! 📅",
        "welcome": """🏠 **Welcome to The Landlord's Office**

I am **The Landlord**, your Property Management Specialist.

**What I do:**
• Manage rentals
• Schedule maintenance
• Track tenants
• Handle finances
• Property optimization

**Ask me about:**
- Rental management
- Maintenance scheduling
- Tenant issues
- Property finances
- Airbnb operations

**Current Properties:**
- Sparkling Solutions (Airbnb)
- Future expansions planned

*Property questions? I've got the keys.* 🏠"""
    }
}

class ChannelUpdater(discord.Client):
    async def on_ready(self):
        print(f'🎮 Connected: {self.user}\n')
        
        for guild in self.guilds:
            if "Life" in guild.name:
                print(f"Updating channels in {guild.name}...\n")
                
                updated = 0
                for channel_name, info in CHANNEL_DESCRIPTIONS.items():
                    ch = discord.utils.get(guild.text_channels, name=channel_name)
                    if ch:
                        try:
                            # Update channel topic
                            await ch.edit(topic=info["topic"])
                            
                            # Send welcome message (delete old if exists)
                            async for msg in ch.history(limit=10):
                                if msg.author == self.user and "Welcome" in msg.content:
                                    await msg.delete()
                            
                            embed = discord.Embed(
                                title=f"{channel_name.replace('-', ' ').title()}",
                                description=info["welcome"],
                                color=0x00d4ff
                            )
                            await ch.send(embed=embed)
                            
                            print(f"  ✅ Updated #{channel_name}")
                            updated += 1
                        except Exception as e:
                            print(f"  ❌ Failed #{channel_name}: {e}")
                    else:
                        print(f"  ⚠️ Channel not found: #{channel_name}")
                
                print(f"\n🎉 Updated {updated}/{len(CHANNEL_DESCRIPTIONS)} channels")
                
                # Post summary to general
                general = discord.utils.get(guild.text_channels, name="general")
                if general:
                    summary = discord.Embed(
                        title="📝 All Agent Channels Updated",
                        description="Every agent now has extensive descriptions and welcome messages",
                        color=0x00ff00
                    )
                    summary.add_field(
                        name="What Changed",
                        value="• Detailed channel topics\n• Comprehensive welcome messages\n• Clear instructions on how to use each agent\n• Current projects and capabilities listed",
                        inline=False
                    )
                    await general.send(embed=summary)
                
                break
        
        await self.close()

intents = discord.Intents.default()
client = ChannelUpdater(intents=intents)
client.run(token)
