#!/usr/bin/env python3
"""
Weekly Summary Bot for Discord
Posts weekly summary to #announcements every Monday
"""

import discord
import os
import subprocess
from datetime import datetime

token = open('/home/ubuntu/.openclaw/discord/bot.token').read().strip()

class WeeklySummaryBot(discord.Client):
    async def on_ready(self):
        for guild in self.guilds:
            if "Life" in guild.name:
                ann_ch = discord.utils.get(guild.text_channels, name="announcements")
                if ann_ch:
                    embed = discord.Embed(
                        title=f"📈 Weekly Summary — Week of {datetime.now().strftime('%B %d')}",
                        color=0x00ff00
                    )
                    embed.add_field(
                        name="✅ Completed This Week",
                        value="Check agent channels for completed tasks",
                        inline=False
                    )
                    embed.add_field(
                        name="🔄 In Progress",
                        value="60+ tasks across 30 agents",
                        inline=False
                    )
                    embed.add_field(
                        name="📅 This Week's Focus",
                        value="• X API activation\n• Documentation improvements\n• Agent productivity optimization",
                        inline=False
                    )
                    
                    await ann_ch.send(embed=embed)
                break
        await self.close()

intents = discord.Intents.default()
client = WeeklySummaryBot(intents=intents)
client.run(token)
