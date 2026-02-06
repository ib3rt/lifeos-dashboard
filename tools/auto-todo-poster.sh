#!/bin/bash
# Auto-Todo Discord Poster
# Posts new tasks to Discord #master-todo channel

TASK="$1"
PRIORITY="${2:-medium}"
SOURCE="${3:-conversation}"

echo "📤 Posting new task to Discord: $TASK"

export DISCORD_BOT_TOKEN=$(cat ~/.openclaw/discord/bot.token 2>/dev/null)

if [ -n "$DISCORD_BOT_TOKEN" ]; then
    python3 << PYDISCORD
import discord

token = """$DISCORD_BOT_TOKEN"""
task = """$TASK"""
priority = """$PRIORITY"""
source = """$SOURCE"""

# Color based on priority
colors = {
    "high": 0xe74c3c,    # Red
    "medium": 0xf39c12,   # Orange
    "low": 0x2ecc71,      # Green
}
color = colors.get(priority.lower(), 0x95a5a6)

class TodoPoster(discord.Client):
    async def on_ready(self):
        for guild in self.guilds:
            if "Life" in guild.name:
                todo_ch = discord.utils.get(guild.text_channels, name="master-todo")
                if todo_ch:
                    embed = discord.Embed(
                        title="📝 NEW TASK ADDED",
                        description=f"```{task}```",
                        color=color
                    )
                    
                    embed.add_field(
                        name="Priority",
                        value=priority.upper(),
                        inline=True
                    )
                    
                    embed.add_field(
                        name="Source",
                        value=source,
                        inline=True
                    )
                    
                    embed.set_footer(text="Auto-captured from conversation")
                    
                    await todo_ch.send(embed=embed)
                    print(f"✅ Posted task to #{todo_ch.name}")
                break
        await self.close()

intents = discord.Intents.default()
client = TodoPoster(intents=intents)
client.run(token)
PYDISCORD
fi