#!/usr/bin/env python3
"""
Discord Server Setup Script
Creates channel structure for Life OS Command Center
"""

import discord
import asyncio
import sys

token = open('/home/ubuntu/.openclaw/discord/bot.token').read().strip()

class SetupClient(discord.Client):
    async def on_ready(self):
        print(f"✅ Connected as {self.user}")
        
        # Find the Life OS server
        target_server = None
        for guild in self.guilds:
            if "Life" in guild.name or "OS" in guild.name:
                target_server = guild
                break
        
        if not target_server:
            print("❌ Life OS server not found!")
            print(f"   Available servers: {[g.name for g in self.guilds]}")
            await self.close()
            return
        
        print(f"\n🎮 Found server: {target_server.name}")
        print(f"   Current channels: {len(target_server.channels)}")
        
        # Check permissions
        me = target_server.me
        if not me.guild_permissions.manage_channels:
            print("\n⚠️  Bot needs 'Manage Channels' permission!")
            print("   Please enable in Server Settings > Roles > Life OS Bot")
        else:
            print("\n✅ Bot has channel management permissions")
            print("\n📋 Recommended Channel Structure:")
            print("""
📋 INFORMATION
├── #welcome
├── #announcements
└── #changelog

🤖 AGENT HQ
├── #agent-chat
├── #oracle-insights
├── #diamond-hands
├── #mechanic-workshop
└── #sentinel-alerts

💬 GENERAL
├── #general
├── #showcase
└── #feedback

🔧 DEVELOPMENT
├── #github-updates
├── #deployment
└── #debug

🎯 PROJECTS
├── #local-node
├── #x-automation
└── #voice-cloning
            """)
            
            # Send welcome message to general
            general = discord.utils.get(target_server.text_channels, name="general")
            if general:
                try:
                    embed = discord.Embed(
                        title="🦾 Life OS Bot is Online!",
                        description="Your 15-agent command center is ready.",
                        color=0x00d4ff
                    )
                    embed.add_field(
                        name="Available Commands",
                        value="`!agents` - List all 15 agents\n`!status` - System status\n`!help` - All commands",
                        inline=False
                    )
                    embed.set_footer(text="Try mentioning me with keywords!")
                    await general.send(embed=embed)
                    print("\n✅ Welcome message sent to #general")
                except Exception as e:
                    print(f"\n⚠️  Couldn't send welcome: {e}")
        
        await self.close()

intents = discord.Intents.default()
client = SetupClient(intents=intents)
client.run(token)
