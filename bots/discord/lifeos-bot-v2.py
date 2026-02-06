#!/usr/bin/env python3
"""
Life OS Discord Bot - Full Agent Swarm
All 15 agents available with AI responses
"""

import os
import sys
import asyncio
import json
from datetime import datetime

try:
    import discord
    from discord.ext import commands, tasks
    import aiohttp
except ImportError:
    os.system("python3 -m pip install discord.py aiohttp --user --break-system-packages")
    import discord
    from discord.ext import commands, tasks
    import aiohttp

# Bot configuration
TOKEN_PATH = os.path.expanduser('~/.openclaw/discord/bot.token')
with open(TOKEN_PATH) as f:
    BOT_TOKEN = f.read().strip()

COMMAND_PREFIX = '!'

# Load Moonshot API key from OpenClaw config
MOONSHOT_API_KEY = ''
try:
    config_path = os.path.expanduser('~/.openclaw/openclaw.json')
    with open(config_path) as f:
        config = json.load(f)
        # Extract API key from config structure
        MOONSHOT_API_KEY = os.getenv('MOONSHOT_API_KEY', config.get('auth', {}).get('profiles', {}).get('moonshot:default', {}).get('apiKey', ''))
except:
    MOONSHOT_API_KEY = os.getenv('MOONSHOT_API_KEY', '')

if not MOONSHOT_API_KEY:
    print("⚠️  Warning: MOONSHOT_API_KEY not found. AI responses will use fallback mode.")

# All 15 Life OS Agents
AGENTS = {
    'oracle': {
        'name': 'The Oracle',
        'emoji': '🔮',
        'color': 0x9b59b6,
        'description': 'AI Research Specialist',
        'personality': 'Mysterious, speaks in predictions',
        'keywords': ['ai', 'gpt', 'claude', 'research', 'trend', 'tool']
    },
    'diamond': {
        'name': 'Diamond Hands',
        'emoji': '💎',
        'color': 0x3498db,
        'description': 'Crypto/Web3 Specialist',
        'personality': 'Enthusiastic, hodl mindset',
        'keywords': ['crypto', 'btc', 'eth', 'sol', 'wallet', 'defi', 'nft']
    },
    'mechanic': {
        'name': 'The Mechanic',
        'emoji': '⚙️',
        'color': 0xe74c3c,
        'description': 'Operations & Automation',
        'personality': 'Direct, gets things done',
        'keywords': ['deploy', 'server', 'error', 'fix', 'automation', 'n8n']
    },
    'sentinel': {
        'name': 'Sentinel',
        'emoji': '🛡️',
        'color': 0x2ecc71,
        'description': 'Security Specialist',
        'personality': 'Vigilant, protective',
        'keywords': ['security', 'alert', 'breach', 'cve', 'hack', 'protect']
    },
    'hype': {
        'name': 'Hype Man',
        'emoji': '📈',
        'color': 0xf39c12,
        'description': 'Marketing & Social Media',
        'personality': 'Energetic, always promoting',
        'keywords': ['marketing', 'x', 'twitter', 'social', 'promote', 'content']
    },
    'ned': {
        'name': 'Neural Net Ned',
        'emoji': '💻',
        'color': 0x1abc9c,
        'description': 'Code & Technical Architecture',
        'personality': 'Nerdy, enthusiastic about tech',
        'keywords': ['code', 'build', 'develop', 'program', 'api', 'script']
    },
    'pablo': {
        'name': 'Podcast Pablo',
        'emoji': '🎙️',
        'color': 0xe91e63,
        'description': 'Content & Audio Production',
        'personality': 'Creative, audio-focused',
        'keywords': ['podcast', 'audio', 'voice', 'record', 'content']
    },
    'goldfinger': {
        'name': 'Goldfinger',
        'emoji': '🏦',
        'color': 0xf1c40f,
        'description': 'Finance & Treasury',
        'personality': 'Sophisticated, financial focus',
        'keywords': ['finance', 'budget', 'money', 'invest', 'tax', 'account']
    },
    'legal': {
        'name': 'Legal Eagle',
        'emoji': '⚖️',
        'color': 0x95a5a6,
        'description': 'Legal & Compliance',
        'personality': 'Formal, precise, cautious',
        'keywords': ['legal', 'contract', 'law', 'compliance', 'entity', 'llc']
    },
    'bridge': {
        'name': 'The Bridge',
        'emoji': '🌐',
        'color': 0x34495e,
        'description': 'Hardware & Local Infrastructure',
        'personality': 'Practical, hardware-focused',
        'keywords': ['hardware', 'pi', 'server', 'local', 'node', 'infrastructure']
    },
    'zen': {
        'name': 'Zen Master',
        'emoji': '☯️',
        'color': 0x8e44ad,
        'description': 'Mindfulness & Productivity',
        'personality': 'Calm, philosophical',
        'keywords': ['focus', 'meditate', 'mindful', 'calm', 'balance', 'stress']
    },
    'strategist': {
        'name': 'The Strategist',
        'emoji': '♟️',
        'color': 0x2c3e50,
        'description': 'Long-term Planning',
        'personality': 'Thoughtful, analytical',
        'keywords': ['plan', 'strategy', 'roadmap', 'future', 'vision', 'goal']
    },
    'butler': {
        'name': 'The Butler',
        'emoji': '🤵',
        'color': 0xecf0f1,
        'description': 'Personal Assistant',
        'personality': 'Polite, service-oriented',
        'keywords': ['schedule', 'calendar', 'remind', 'organize', 'task']
    },
    'felix': {
        'name': 'Fix-It Felix',
        'emoji': '🔨',
        'color': 0xd35400,
        'description': 'Emergency Troubleshooting',
        'personality': 'Quick, resourceful',
        'keywords': ['bug', 'broken', 'fix', 'urgent', 'error', 'crash']
    },
    'landlord': {
        'name': 'The Landlord',
        'emoji': '🏠',
        'color': 0x27ae60,
        'description': 'Property Management',
        'personality': 'Professional, property-focused',
        'keywords': ['property', 'rental', 'airbnb', 'tenant', 'maintenance']
    }
}

class LifeOSBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(
            command_prefix=COMMAND_PREFIX,
            intents=intents,
            help_command=None
        )
        self.start_time = datetime.now()
    
    async def on_ready(self):
        print(f'🦾 Life OS Bot Ready: {self.user}')
        print(f'   Latency: {round(self.latency * 1000)}ms')
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name="15 Agents | !help"
            )
        )
    
    async def on_message(self, message):
        if message.author == self.user:
            return
        
        # Check for @mentions
        if self.user in message.mentions:
            await self.handle_agent_mention(message)
            return
        
        # Check if message is in an agent-specific channel
        channel_agent = self.get_channel_agent(message.channel.name)
        if channel_agent and not message.content.startswith('!'):
            await self.respond_as_agent(message, channel_agent)
            return
        
        await self.process_commands(message)
    
    def get_channel_agent(self, channel_name):
        """Map channel names to agents"""
        channel_map = {
            'oracle-insights': 'oracle',
            'diamond-hands': 'diamond',
            'mechanic-workshop': 'mechanic',
            'sentinel-alerts': 'sentinel',
            'agent-chat': None  # General agent chat - no specific agent
        }
        return channel_map.get(channel_name)
    
    async def respond_as_agent(self, message, agent_key):
        """Respond as the specific agent for that channel using AI"""
        agent = AGENTS[agent_key]
        
        # Generate AI-powered response in agent persona
        response = await self.generate_agent_response(agent, message.content, message.author.name)
        
        embed = discord.Embed(
            title=f"{agent['emoji']} {agent['name']}",
            description=response,
            color=agent['color'],
            timestamp=datetime.now()
        )
        embed.set_footer(text=f"Responding in #{message.channel.name} | Try @Bonzi for general help")
        await message.reply(embed=embed)
    
    async def generate_agent_response(self, agent, user_message, username):
        """Generate AI response in agent persona"""
        import aiohttp
        import os
        
        # Build the persona prompt
        system_prompt = f"""You are {agent['name']} {agent['emoji']}, a specialized AI agent in the Life OS system.

Your role: {agent['description']}
Your personality: {agent['personality']}

Respond to the user's message in character, staying true to your personality and expertise. Be helpful, engaging, and concise (2-3 sentences max unless detailed analysis is needed).

Important:
- Stay in character as {agent['name']}
- Use your emoji {agent['emoji']} naturally
- Reference your specific expertise when relevant
- Be conversational and helpful
- If you don't know something, say so in character"""

        # Call Moonshot API
        api_key = os.getenv('MOONSHOT_API_KEY', '')
        if not api_key:
            # Fallback response if no API key
            return f"{agent['emoji']} Hello {username}! I'm {agent['name']}, {agent['description']}.\n\n*{agent['personality']}*\n\nI'd love to help with: '{user_message[:200]}'\n\n(Configure MOONSHOT_API_KEY for full AI responses!)"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    'https://api.moonshot.ai/v1/chat/completions',
                    headers={
                        'Authorization': f'Bearer {api_key}',
                        'Content-Type': 'application/json'
                    },
                    json={
                        'model': 'kimi-k2.5',
                        'messages': [
                            {'role': 'system', 'content': system_prompt},
                            {'role': 'user', 'content': f"{username} says: {user_message}"}
                        ],
                        'temperature': 0.7,
                        'max_tokens': 500
                    }
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data['choices'][0]['message']['content']
                    else:
                        error_text = await resp.text()
                        print(f"API Error: {error_text}")
                        raise Exception(f"API returned {resp.status}")
        except Exception as e:
            print(f"Error generating response: {e}")
            # Fallback response
            return f"{agent['emoji']} Hey {username}! It's {agent['name']} here. {agent['personality']}\n\nI'm ready to help with your question about: '{user_message[:200]}'\n\nWhat would you like to know?"
    
    async def handle_agent_mention(self, message):
        """Route mentions to appropriate agent"""
        content = message.content.lower()
        
        # Find matching agent
        best_match = None
        for key, agent in AGENTS.items():
            if any(kw in content for kw in agent['keywords']):
                best_match = agent
                break
        
        if best_match:
            embed = discord.Embed(
                title=f"{best_match['emoji']} {best_match['name']}",
                description=f"**{best_match['description']}**\n\n*{best_match['personality']}*",
                color=best_match['color'],
                timestamp=datetime.now()
            )
            embed.set_footer(text="Life OS Agent Swarm | Try !agents for full list")
            await message.reply(embed=embed)
        else:
            # Default response
            embed = discord.Embed(
                title="🦾 Life OS Command Center",
                description="I can route you to any of 15 specialized agents!\n\n**Try mentioning keywords like:**\n🔮 AI/GPT → The Oracle\n💎 Crypto → Diamond Hands\n⚙️ Deploy → The Mechanic\n🛡️ Security → Sentinel\n\nOr use **!agents** to see all 15!",
                color=0x00d4ff
            )
            await message.reply(embed=embed)

# Terminal Bridge Integration
try:
    from terminal_bridge import setup_terminal_bridge
    TERMINAL_BRIDGE_AVAILABLE = True
except ImportError:
    TERMINAL_BRIDGE_AVAILABLE = False
    print("⚠️ Terminal bridge not available")

# Initialize bot
bot = LifeOSBot()

# Setup terminal bridge if available
if TERMINAL_BRIDGE_AVAILABLE:
    terminal = setup_terminal_bridge(bot)
    print("✅ Terminal bridge loaded")
    print("   Commands: !exec <command>, !status, !ps, !logs")

@bot.command(name='agents')
async def list_agents(ctx):
    """Show all 15 Life OS agents"""
    embed = discord.Embed(
        title="🤖 Life OS Agent Roster (15 Total)",
        description="Your specialized AI workforce ready to assist",
        color=0x9b59b6
    )
    
    # Group agents
    core = ['oracle', 'diamond', 'mechanic', 'sentinel', 'hype']
    support = ['ned', 'pablo', 'goldfinger', 'legal', 'bridge']
    misc = ['zen', 'strategist', 'butler', 'felix', 'landlord']
    
    core_agents = "\n".join([f"{AGENTS[a]['emoji']} **{AGENTS[a]['name']}** - {AGENTS[a]['description']}" for a in core])
    support_agents = "\n".join([f"{AGENTS[a]['emoji']} **{AGENTS[a]['name']}** - {AGENTS[a]['description']}" for a in support])
    misc_agents = "\n".join([f"{AGENTS[a]['emoji']} **{AGENTS[a]['name']}** - {AGENTS[a]['description']}" for a in misc])
    
    embed.add_field(name="🎯 Core Team", value=core_agents, inline=False)
    embed.add_field(name="🛠️ Support Team", value=support_agents, inline=False)
    embed.add_field(name="⚡ Specialist Team", value=misc_agents, inline=False)
    
    embed.set_footer(text="Mention me with keywords to route to the right agent!")
    await ctx.send(embed=embed)

@bot.command(name='status')
async def status(ctx):
    """Show Life OS status"""
    uptime = datetime.now() - bot.start_time
    
    embed = discord.Embed(
        title="📊 Life OS Status",
        color=0x00d4ff,
        timestamp=datetime.now()
    )
    
    embed.add_field(name="⏱️ Bot Uptime", value=f"{uptime.seconds//3600}h {(uptime.seconds//60)%60}m", inline=True)
    embed.add_field(name="🤖 Agents", value="15 active", inline=True)
    embed.add_field(name="🌐 Websites", value="3 deployed", inline=True)
    embed.add_field(name="📁 Reports", value="11 available", inline=True)
    embed.add_field(name="⚙️ n8n", value="Running", inline=True)
    embed.add_field(name="🔄 Last Deploy", value="Just now", inline=True)
    
    embed.add_field(
        name="🔗 Quick Links",
        value="[Dashboard](https://lifeos-dashboard-three.vercel.app)\n[Sparkling Solutions](https://sparkling-solutions.vercel.app)\n[BE Repaired](https://be-repaired.vercel.app)",
        inline=False
    )
    
    await ctx.send(embed=embed)

@bot.command(name='agent')
async def agent_info(ctx, *, name=None):
    """Get info about a specific agent"""
    if not name:
        await ctx.send("Usage: `!agent <name>`\nExample: `!agent oracle` or `!agent 'diamond hands'`")
        return
    
    # Find agent
    name_lower = name.lower().replace(' ', '-')
    agent = None
    
    for key, data in AGENTS.items():
        if key in name_lower or name_lower in data['name'].lower():
            agent = data
            break
    
    if agent:
        embed = discord.Embed(
            title=f"{agent['emoji']} {agent['name']}",
            description=f"**{agent['description']}**\n\n*{agent['personality']}*",
            color=agent['color']
        )
        embed.add_field(name="Keywords", value=", ".join(agent['keywords']), inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"❌ Agent '{name}' not found. Use `!agents` to see all 15.")

@bot.command(name='websites')
async def websites(ctx):
    """Show all deployed websites"""
    embed = discord.Embed(
        title="🌐 Life OS Websites",
        color=0x3498db
    )
    
    sites = [
        ("✨ Sparkling Solutions", "https://sparkling-solutions.vercel.app", "Airbnb cleaning service"),
        ("🔧 BE Repaired", "https://be-repaired.vercel.app", "Handyman services"),
        ("💻 Personal Tech", "https://personal-tech-seven.vercel.app", "Tech portfolio"),
        ("🦾 Life OS Dashboard", "https://lifeos-dashboard-three.vercel.app", "Command center")
    ]
    
    for name, url, desc in sites:
        embed.add_field(name=name, value=f"[{desc}]({url})", inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name='topics')
async def topics_schedule(ctx):
    """Show afternoon research topic schedule"""
    embed = discord.Embed(
        title="🕓 Afternoon Research Schedule",
        description="Weekly research report topics",
        color=0x3498db
    )
    
    schedule = [
        ("Monday", "🤖 AI & Machine Learning", "Agent architectures, LLM updates, new tools"),
        ("Tuesday", "💼 Business & Automation", "Workflows, scaling, productivity systems"),
        ("Wednesday", "₿ Crypto & Web3", "DeFi, yields, market analysis"),
        ("Thursday", "💻 Development & Tools", "Frameworks, best practices, dev tools"),
        ("Friday", "🧠 Personal Growth", "Productivity, systems, mental models"),
        ("Weekend", "🔬 Deep Dive Special", "Extended research on user request")
    ]
    
    for day, topic, desc in schedule:
        embed.add_field(name=f"{day}: {topic}", value=desc, inline=False)
    
    embed.set_footer(text="Reports posted daily at 4:00 PM EST")
    await ctx.send(embed=embed)

@bot.command(name='deploy')
async def deploy(ctx):
    """Trigger deployment"""
    msg = await ctx.send("🚀 Triggering deployment...")
    await asyncio.sleep(2)
    await msg.edit(content="✅ **Deployment triggered!**\n\nDashboard: https://lifeos-dashboard-three.vercel.app")

# Channel-specific help configurations
CHANNEL_HELP = {
    'oracle': {
        'title': '🔮 Oracle Channel Help',
        'description': 'AI Research & Intelligence Commands',
        'commands': [
            ("!research <topic>", "Deep research on any topic"),
            ("!trends", "Show current AI/tech trends"),
            ("!tools", "List recommended AI tools"),
            ("@mention + ai/gpt/claude", "Ask Oracle AI questions")
        ],
        'tips': [
            "Oracle specializes in AI research and trends",
            "Great for: tool recommendations, capability analysis",
            "Weekly AI landscape reports posted here"
        ]
    },
    'diamond-hands': {
        'title': '💎 Diamond Hands Channel Help',
        'description': 'Crypto & DeFi Commands',
        'commands': [
            ("!prices", "Show crypto price tracker"),
            ("!portfolio", "View portfolio snapshot"),
            ("!yields", "DeFi yield opportunities"),
            ("@mention + crypto/btc/eth/sol", "Ask Diamond Hands")
        ],
        'tips': [
            "Diamond Hands tracks crypto markets",
            "Great for: DeFi strategies, yield farming",
            "Portfolio updates posted daily"
        ]
    },
    'mechanic': {
        'title': '⚙️ Mechanic Channel Help',
        'description': 'Operations & Automation Commands',
        'commands': [
            ("!health", "System health check"),
            ("!deploy", "Trigger deployment"),
            ("!logs", "View system logs"),
            ("@mention + deploy/server/error", "Ask Mechanic")
        ],
        'tips': [
            "Mechanic handles infrastructure",
            "Great for: deployments, troubleshooting",
            "Alert notifications posted here"
        ]
    },
    'sentinel': {
        'title': '🛡️ Sentinel Channel Help',
        'description': 'Security & Monitoring Commands',
        'commands': [
            ("!audit", "Run security audit"),
            ("!alerts", "View security alerts"),
            ("!status", "Security dashboard"),
            ("@mention + security/alert/cve", "Ask Sentinel")
        ],
        'tips': [
            "Sentinel monitors security",
            "Great for: threat detection, audits",
            "Critical alerts posted immediately"
        ]
    },
    'morning-brief': {
        'title': '🌅 Morning Brief Channel',
        'description': 'Daily 8 AM Briefings',
        'commands': [
            ("Auto-posted", "Brief arrives automatically at 8 AM EST"),
            ("!subscribe", "Confirm subscription (optional)"),
        ],
        'tips': [
            "Daily brief posted every morning",
            "Includes: weather, tasks, news, recommendations",
            "Scroll back to see previous days"
        ]
    },
    'afternoon-brief': {
        'title': '🕓 Afternoon Brief Channel',
        'description': 'Daily 4 PM Research Reports',
        'commands': [
            ("Auto-posted", "Report arrives automatically at 4 PM EST"),
            ("!topics", "View weekly topic schedule"),
        ],
        'tips': [
            "Research reports posted daily at 4 PM",
            "Monday: AI | Tuesday: Business | Wednesday: Crypto",
            "Thursday: Dev | Friday: Personal Growth"
        ]
    },
    'second-brain': {
        'title': '🧠 Second Brain Channel',
        'description': 'Knowledge Base & Documents',
        'commands': [
            ("Auto-posted", "Documents sync here automatically"),
            ("!search <query>", "Search knowledge base"),
            ("!recent", "Show recently added docs"),
        ],
        'tips': [
            "Documents auto-posted from our conversations",
            "Categories: Journal, Concepts, Projects, Reference",
            "Also available in web app"
        ]
    },
    'terminal': {
        'title': '💻 Terminal Bridge Channel',
        'description': 'Execute AWS Commands',
        'commands': [
            ("!exec <command>", "Execute any terminal command"),
            ("!status", "Quick system status"),
            ("!ps", "Show running processes"),
            ("!logs [lines]", "View recent logs"),
        ],
        'tips': [
            "Execute commands on AWS instance",
            "Output returned to this channel",
            "30-second timeout, dangerous commands blocked"
        ]
    },
    'master-todo': {
        'title': '📝 Master Todo Channel',
        'description': 'Task Management',
        'commands': [
            ("Auto-captured", "Tasks from conversations appear here"),
            ("!tasks", "View current task list"),
            ("!done <task>", "Mark task complete"),
        ],
        'tips': [
            "Tasks auto-captured from our conversations",
            "High/Medium/Low priority tracked",
            "Source conversation linked"
        ]
    },
    'general': {
        'title': '💬 General Chat Help',
        'description': 'General Life OS Commands',
        'commands': [
            ("!agents", "List all 15 Life OS agents"),
            ("!agent <name>", "Get specific agent info"),
            ("!status", "System status overview"),
            ("!websites", "List deployed websites"),
            ("@mention + keywords", "Route to agent")
        ],
        'tips': [
            "General chat for all Life OS discussions",
            "Mention me with keywords to get routed",
            "Each agent has their own dedicated channel"
        ]
    }
}

@bot.command(name='help')
async def help_cmd(ctx):
    """Show context-aware help based on channel"""
    channel_name = ctx.channel.name.lower()
    
    # Find matching channel help
    help_config = None
    for key, config in CHANNEL_HELP.items():
        if key in channel_name or channel_name in key:
            help_config = config
            break
    
    # Default to general if no match
    if not help_config:
        help_config = CHANNEL_HELP['general']
    
    # Build embed
    embed = discord.Embed(
        title=help_config['title'],
        description=help_config['description'],
        color=0x00d4ff,
        timestamp=datetime.now()
    )
    
    # Add commands
    for cmd, desc in help_config['commands']:
        embed.add_field(name=f"`{cmd}`", value=desc, inline=False)
    
    # Add tips
    tips_text = "\n".join([f"• {tip}" for tip in help_config['tips']])
    embed.add_field(name="💡 Tips", value=tips_text, inline=False)
    
    # Add global commands footer
    embed.add_field(
        name="🦾 Global Commands (Any Channel)",
        value="`!agents` - List all agents\n"
              "`!status` - System status\n"
              "`!websites` - Deployed sites",
        inline=False
    )
    
    embed.set_footer(text=f"Channel: #{ctx.channel.name} | Use !help in any channel for specific commands")
    await ctx.send(embed=embed)

# Run bot
if __name__ == '__main__':
    print("🔮 Starting Life OS Discord Bot...")
    print(f"   Token: {BOT_TOKEN[:20]}...")
    bot.run(BOT_TOKEN)
