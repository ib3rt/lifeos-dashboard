#!/usr/bin/env python3
"""
Create Discord Channels for Life OS
"""

import discord
import asyncio

token = open('/home/ubuntu/.openclaw/discord/bot.token').read().strip()

class ChannelCreator(discord.Client):
    async def on_ready(self):
        print(f"🎮 Connected: {self.user}\n")
        
        guild = None
        for g in self.guilds:
            if "Life" in g.name:
                guild = g
                break
        
        if not guild:
            print("❌ Server not found")
            await self.close()
            return
        
        print(f"Setting up: {guild.name}\n")
        
        # Categories to create
        categories = [
            ("📋 INFORMATION", ["welcome", "announcements", "changelog"]),
            ("🤖 AGENT HQ", ["agent-chat", "oracle-insights", "diamond-hands", "mechanic-workshop", "sentinel-alerts"]),
            ("💬 GENERAL", ["general", "showcase", "feedback"]),
            ("🔧 DEVELOPMENT", ["github-updates", "deployment", "debug"]),
            ("🎯 PROJECTS", ["local-node", "x-automation", "voice-cloning"])
        ]
        
        created = []
        
        for cat_name, channels in categories:
            # Check if category exists
            existing_cat = discord.utils.get(guild.categories, name=cat_name)
            
            if existing_cat:
                print(f"📁 Category exists: {cat_name}")
                category = existing_cat
            else:
                try:
                    category = await guild.create_category(cat_name)
                    print(f"✅ Created category: {cat_name}")
                    created.append(cat_name)
                except Exception as e:
                    print(f"❌ Failed to create {cat_name}: {e}")
                    continue
            
            # Create channels in category
            for ch_name in channels:
                existing_ch = discord.utils.get(guild.text_channels, name=ch_name)
                if existing_ch:
                    print(f"  ✓ Channel exists: #{ch_name}")
                else:
                    try:
                        await guild.create_text_channel(ch_name, category=category)
                        print(f"  ✅ Created: #{ch_name}")
                        created.append(f"#{ch_name}")
                    except Exception as e:
                        print(f"  ❌ Failed #{ch_name}: {e}")
        
        print(f"\n🎉 Setup complete!")
        print(f"   Created: {len(created)} items")
        
        # Send completion message to general
        general = discord.utils.get(guild.text_channels, name="general")
        if general:
            embed = discord.Embed(
                title="🎉 Server Setup Complete!",
                description="Life OS Command Center is fully configured with 15+ channels.",
                color=0x00ff00
            )
            embed.add_field(
                name="🤖 15 Agents Ready",
                value="Type `!agents` to see the full roster",
                inline=False
            )
            embed.add_field(
                name="📋 Channel Categories",
                value="📋 Information\n🤖 Agent HQ\n💬 General\n🔧 Development\n🎯 Projects",
                inline=False
            )
            await general.send(embed=embed)
        
        await self.close()

intents = discord.Intents.default()
client = ChannelCreator(intents=intents)
client.run(token)
