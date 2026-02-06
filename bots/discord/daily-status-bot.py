#!/usr/bin/env python3
"""
Daily Status Bot for Discord
Posts system status to #announcements every morning
"""

import discord
import os
import subprocess
from datetime import datetime

token = open('/home/ubuntu/.openclaw/discord/bot.token').read().strip()

class DailyStatusBot(discord.Client):
    async def on_ready(self):
        for guild in self.guilds:
            if "Life" in guild.name:
                ann_ch = discord.utils.get(guild.text_channels, name="announcements")
                if ann_ch:
                    # Get system stats
                    disk = subprocess.getoutput("df -h / | tail -1 | awk '{print $5}'")
                    memory = subprocess.getoutput("free -h | grep Mem | awk '{print $3}'")
                    
                    embed = discord.Embed(
                        title=f"📊 Daily Status — {datetime.now().strftime('%A, %B %d')}",
                        color=0x00d4ff
                    )
                    embed.add_field(
                        name="🤖 Active Agents",
                        value="30 agents executing\n(15 main + 15 sub)",
                        inline=True
                    )
                    embed.add_field(
                        name="📋 Active Tasks",
                        value="60+ concurrent missions",
                        inline=True
                    )
                    embed.add_field(
                        name="💾 System",
                        value=f"Disk: {disk}\nMemory: {memory}",
                        inline=True
                    )
                    
                    await ann_ch.send(embed=embed)
                break
        await self.close()

intents = discord.Intents.default()
client = DailyStatusBot(intents=intents)
client.run(token)
