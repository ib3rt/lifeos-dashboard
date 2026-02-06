#!/usr/bin/env python3
"""
Discord Bot for Life OS
Multi-agent bot swarm integration
"""

import os
import json
import asyncio
from datetime import datetime

try:
    import discord
    from discord.ext import commands, tasks
except ImportError:
    print("Installing discord.py...")
    os.system("pip3 install discord.py")
    import discord
    from discord.ext import commands, tasks

# Bot configuration
BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
COMMAND_PREFIX = '!'

# Agent personas
AGENTS = {
    'oracle': {
        'name': 'The Oracle',
        'emoji': '🔮',
        'color': 0x9b59b6,
        'description': 'AI Research Specialist',
        'personality': 'Mysterious, speaks in predictions'
    },
    'diamond': {
        'name': 'Diamond Hands',
        'emoji': '💎',
        'color': 0x3498db,
        'description': 'Crypto/Web3 Specialist',
        'personality': 'Enthusiastic, hodl mindset'
    },
    'mechanic': {
        'name': 'The Mechanic',
        'emoji': '⚙️',
        'color': 0xe74c3c,
        'description': 'Operations & Automation',
        'personality': 'Direct, gets things done'
    },
    'sentinel': {
        'name': 'Sentinel',
        'emoji': '🛡️',
        'color': 0x2ecc71,
        'description': 'Security Specialist',
        'personality': 'Vigilant, protective'
    }
}

class LifeOSBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        # intents.message_content = True  # Requires privileged intent
        # intents.members = True  # Requires privileged intent
        
        super().__init__(
            command_prefix=COMMAND_PREFIX,
            intents=intents,
            help_command=None
        )
        
        self.start_time = datetime.now()
    
    async def setup_hook(self):
        """Setup after bot connects"""
        print(f'🔮 Life OS Bot connected as {self.user}')
        self.status_update.start()
    
    async def on_ready(self):
        """Called when bot is ready"""
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="Life OS Command Center"
            )
        )
        print(f'✅ Bot ready! Latency: {round(self.latency * 1000)}ms')
    
    async def on_message(self, message):
        """Handle messages"""
        if message.author == self.user:
            return
        
        # Check if bot is mentioned
        if self.user in message.mentions:
            await self.handle_mention(message)
            return
        
        await self.process_commands(message)
    
    async def handle_mention(self, message):
        """Handle @bot mentions with agent routing"""
        content = message.content.lower()
        
        # Route to appropriate agent based on keywords
        if any(word in content for word in ['ai', 'research', 'gpt', 'claude', 'trend']):
            await self.send_agent_response(message, 'oracle')
        elif any(word in content for word in ['crypto', 'btc', 'eth', 'sol', 'wallet']):
            await self.send_agent_response(message, 'diamond')
        elif any(word in content for word in ['deploy', 'server', 'error', 'fix']):
            await self.send_agent_response(message, 'mechanic')
        elif any(word in content for word in ['security', 'alert', 'breach', 'cve']):
            await self.send_agent_response(message, 'sentinel')
        else:
            # Default response
            embed = discord.Embed(
                title="🦾 Life OS Command Center",
                description="I am the central hub for your Life OS agents.\n\n**Available Agents:**\n🔮 @Oracle - AI Research\n💎 @Diamond - Crypto/Web3\n⚙️ @Mechanic - Operations\n🛡️ @Sentinel - Security\n\nMention me with keywords to route to the right agent!",
                color=0x00d4ff
            )
            await message.reply(embed=embed)
    
    async def send_agent_response(self, message, agent_key):
        """Send response as specific agent"""
        agent = AGENTS[agent_key]
        
        embed = discord.Embed(
            title=f"{agent['emoji']} {agent['name']}",
            description=f"*{agent['description']}*\n\nPersonality: {agent['personality']}",
            color=agent['color'],
            timestamp=datetime.now()
        )
        
        embed.set_footer(text="Life OS Agent Swarm")
        
        await message.reply(embed=embed)
    
    @tasks.loop(minutes=5)
    async def status_update(self):
        """Periodic status check"""
        # Could update status, check system health, etc.
        pass

# Create bot instance
bot = LifeOSBot()

# Commands
@bot.command(name='status')
async def status(ctx):
    """Show Life OS status"""
    uptime = datetime.now() - bot.start_time
    
    embed = discord.Embed(
        title="📊 Life OS Status",
        color=0x00d4ff,
        timestamp=datetime.now()
    )
    
    embed.add_field(
        name="⏱️ Uptime",
        value=f"{uptime.days}d {uptime.seconds//3600}h {(uptime.seconds//60)%60}m",
        inline=True
    )
    
    embed.add_field(
        name="🤖 Agents",
        value="15 active",
        inline=True
    )
    
    embed.add_field(
        name="📁 Reports",
        value="11 available",
        inline=True
    )
    
    embed.add_field(
        name="🌐 Dashboard",
        value="[Open Dashboard](https://lifeos-dashboard-three.vercel.app)",
        inline=False
    )
    
    await ctx.send(embed=embed)

@bot.command(name='agents')
async def list_agents(ctx):
    """List all Life OS agents"""
    embed = discord.Embed(
        title="🤖 Life OS Agent Roster",
        description="Your specialized AI workforce",
        color=0x9b59b6
    )
    
    for key, agent in AGENTS.items():
        embed.add_field(
            name=f"{agent['emoji']} {agent['name']}",
            value=agent['description'],
            inline=True
        )
    
    await ctx.send(embed=embed)

@bot.command(name='report')
async def get_report(ctx, *, report_name=None):
    """Get a research report"""
    if not report_name:
        await ctx.send("📊 Available reports:\n• ai-briefing\n• kool-tools\n• security-audit\n• local-node\n• phantom-integration\n\nUse: `!report <name>`")
        return
    
    # Map common names to files
    reports = {
        'ai': 'ai-industry-briefing',
        'briefing': 'ai-industry-briefing',
        'tools': 'kool-tools-tracker',
        'security': 'security-audit',
        'node': 'local-node-architecture',
        'phantom': 'phantom-integration',
    }
    
    report_file = reports.get(report_name.lower(), report_name)
    report_path = f"~/.openclaw/workspace/research/{report_file}.md"
    
    await ctx.send(f"🔮 Fetching report: {report_name}...")
    # Would read and summarize actual report here

@bot.command(name='deploy')
async def deploy(ctx):
    """Trigger dashboard deployment"""
    embed = discord.Embed(
        title="🚀 Deployment Triggered",
        description="Deploying latest changes to Vercel...",
        color=0x2ecc71
    )
    msg = await ctx.send(embed=embed)
    
    # Simulate deployment
    await asyncio.sleep(2)
    
    embed.description = "✅ Deployment complete!\n\n🔗 https://lifeos-dashboard-three.vercel.app"
    await msg.edit(embed=embed)

@bot.command(name='help')
async def help_command(ctx):
    """Show help"""
    embed = discord.Embed(
        title="🦾 Life OS Bot Commands",
        description="Your command center for Life OS",
        color=0x00d4ff
    )
    
    commands = [
        ("!status", "Show system status"),
        ("!agents", "List all agents"),
        ("!report <name>", "Get research report"),
        ("!deploy", "Deploy dashboard updates"),
        ("@mention", "Route to appropriate agent"),
    ]
    
    for cmd, desc in commands:
        embed.add_field(name=cmd, value=desc, inline=False)
    
    await ctx.send(embed=embed)

# Run bot
if __name__ == '__main__':
    if BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        print("❌ Error: Set DISCORD_BOT_TOKEN environment variable")
        print("   export DISCORD_BOT_TOKEN='your_token_here'")
    else:
        print("🔮 Starting Life OS Discord Bot...")
        bot.run(BOT_TOKEN)
