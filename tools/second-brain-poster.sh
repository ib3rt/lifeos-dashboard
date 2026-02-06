#!/bin/bash
# 2nd Brain Auto-Poster
# Watches the 2nd Brain content folder and posts new documents to Discord
# Runs via cron or can be triggered after document creation

LOG_FILE="~/.openclaw/logs/second-brain-poster.log"
DATE=$(date '+%Y-%m-%d %H:%M %Z')

echo "========================================" >> $LOG_FILE
echo "🧠 2ND BRAIN POSTER - $DATE" >> $LOG_FILE
echo "========================================" >> $LOG_FILE

# Configuration
CONTENT_DIR="$HOME/.openclaw/workspace/second-brain/content"
LAST_POSTED_FILE="$HOME/.openclaw/workspace/memory/last-second-brain-post.txt"

# Create last posted tracker if doesn't exist
touch "$LAST_POSTED_FILE"

# Function to post document to Discord
post_to_discord() {
    local file="$1"
    local category="$2"
    local filename=$(basename "$file")
    
    echo "📤 Posting: $filename ($category)" >> $LOG_FILE
    
    # Read content (limit to reasonable size)
    content=$(head -c 8000 "$file" 2>/dev/null || echo "Content unavailable")
    
    # Get title from first line or filename
    title=$(head -1 "$file" | sed 's/^# //' | sed 's/^\*\*//' | sed 's/\*\*$//' | tr -d '#*')
    if [ -z "$title" ] || [ "$title" = "" ]; then
        title="$filename"
    fi
    
    # Determine emoji based on category
    case "$category" in
        journal) emoji="📓" ;;
        concepts) emoji="💡" ;;
        projects) emoji="📁" ;;
        reference) emoji="📚" ;;
        *) emoji="📝" ;;
    esac
    
    export DISCORD_BOT_TOKEN=$(cat ~/.openclaw/discord/bot.token 2>/dev/null)
    
    if [ -n "$DISCORD_BOT_TOKEN" ]; then
        python3 << PYDISCORD
import discord
import os

token = os.environ.get('DISCORD_BOT_TOKEN')
file_path = "$file"
file_name = "$filename"
title = """$title"""
content = """$content"""
emoji = "$emoji"
category = "$category"

class SecondBrainPoster(discord.Client):
    async def on_ready(self):
        for guild in self.guilds:
            if "Life" in guild.name:
                brain_ch = discord.utils.get(guild.text_channels, name="second-brain")
                if brain_ch:
                    # Create embed
                    embed = discord.Embed(
                        title=f"{emoji} {title}",
                        description=f"Category: {category.capitalize()} | Auto-generated from 2nd Brain",
                        color=0x9b59b6
                    )
                    
                    # Add content preview (first 1000 chars)
                    preview = content[:1000]
                    if len(content) > 1000:
                        preview += "...\n\n*[Content truncated - full document in 2nd Brain app]*"
                    
                    embed.add_field(
                        name="Content",
                        value=f"```{preview}```",
                        inline=False
                    )
                    
                    embed.set_footer(text=f"2nd Brain | {file_name}")
                    
                    await brain_ch.send(embed=embed)
                    print(f"✅ Posted {file_name} to #{brain_ch.name}")
                break
        await self.close()

intents = discord.Intents.default()
client = SecondBrainPoster(intents=intents)
client.run(token)
PYDISCORD
    fi
}

# Check each category folder
for category in journal concepts projects reference; do
    category_dir="$CONTENT_DIR/$category"
    
    if [ -d "$category_dir" ]; then
        # Find files modified in last 24 hours
        find "$category_dir" -name "*.md" -mtime -1 -type f | while read -r file; do
            # Check if already posted
            if ! grep -q "$file" "$LAST_POSTED_FILE" 2>/dev/null; then
                post_to_discord "$file" "$category"
                echo "$file" >> "$LAST_POSTED_FILE"
                echo "  ✅ Posted: $(basename "$file")" >> $LOG_FILE
            else
                echo "  ⏭️ Already posted: $(basename "$file")" >> $LOG_FILE
            fi
        done
    fi
done

echo "✅ 2nd Brain poster complete" >> $LOG_FILE
echo "" >> $LOG_FILE
