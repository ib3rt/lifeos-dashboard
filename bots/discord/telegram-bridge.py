#!/usr/bin/env python3
"""
Discord-Telegram Bridge
Allows Claw to participate in Discord through Telegram
"""

import discord
import asyncio
import aiohttp
import json
import os
from datetime import datetime

# Load tokens
DISCORD_TOKEN = open('/home/ubuntu/.openclaw/discord/bot.token').read().strip()
TELEGRAM_TOKEN = open('/home/ubuntu/.openclaw/bridge/telegram.token').read().strip()
CLAW_CHAT_ID = "6307161005"  # Your Telegram ID

class DiscordTelegramBridge(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guild_messages = True
        super().__init__(intents=intents)
        self.telegram_token = TELEGRAM_TOKEN
        self.claw_chat_id = CLAW_CHAT_ID
        self.forwarded_messages = {}  # Track forwarded messages
        
    async def on_ready(self):
        print(f'🌉 Bridge Online: {self.user}')
        print(f'   Forwarding Discord → Telegram @{self.claw_chat_id}')
        
        # Send startup message to Telegram
        await self.send_to_telegram(
            "🌉 **Discord Bridge Active**\n\n"
            "I can now see Discord messages here!\n\n"
            "Reply to messages with:\n"
            "`!discord #channel Your response`\n\n"
            "Channels I'm monitoring:\n"
        )
        
        # List channels
        for guild in self.guilds:
            if "Life" in guild.name:
                channels = [f"#{ch.name}" for ch in guild.text_channels if not ch.name.startswith('_')]
                await self.send_to_telegram("\n".join(channels[:20]))
    
    async def on_message(self, message):
        # Ignore my own messages
        if message.author == self.user:
            return
        
        # Ignore bot messages to reduce noise
        if message.author.bot and message.author.name != "Bonzi":
            return
        
        # Format message for Telegram
        guild_name = message.guild.name if message.guild else "DM"
        channel_name = f"#{message.channel.name}" if hasattr(message.channel, 'name') else "DM"
        
        # Check for images/attachments
        attachments = ""
        if message.attachments:
            attachments = f"\n📎 Attachments: {len(message.attachments)}"
            for att in message.attachments:
                attachments += f"\n  - {att.filename}: {att.url}"
        
        # Format the message
        telegram_msg = (
            f"📨 **Discord | {guild_name} | {channel_name}**\n"
            f"👤 **{message.author.display_name}**\n"
            f"💬 {message.content[:500]}{'...' if len(message.content) > 500 else ''}"
            f"{attachments}\n"
            f"\n`!reply {message.channel.id} Your message here`"
        )
        
        # Send to Telegram
        await self.send_to_telegram(telegram_msg)
        
        # Store message ID for replies
        self.forwarded_messages[message.id] = {
            'channel_id': message.channel.id,
            'author': message.author.name,
            'content': message.content[:100]
        }
    
    async def send_to_telegram(self, text):
        """Send message to Claw's Telegram"""
        if not self.telegram_token:
            print(f"[TELEGRAM] {text[:100]}...")
            return
        
        url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
        try:
            async with aiohttp.ClientSession() as session:
                await session.post(url, json={
                    'chat_id': self.claw_chat_id,
                    'text': text,
                    'parse_mode': 'Markdown',
                    'disable_notification': False
                })
        except Exception as e:
            print(f"Telegram error: {e}")
    
    async def send_to_discord(self, channel_id, message):
        """Send message to Discord channel"""
        try:
            channel = self.get_channel(int(channel_id))
            if channel:
                await channel.send(f"🤖 **Claw**: {message}")
                return True
            else:
                return False
        except Exception as e:
            print(f"Discord send error: {e}")
            return False
    
    async def check_telegram_replies(self):
        """Check for Telegram replies to forward to Discord"""
        if not self.telegram_token:
            return
        
        url = f"https://api.telegram.org/bot{self.telegram_token}/getUpdates"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params={'offset': -1, 'limit': 10}) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        for update in data.get('result', []):
                            msg = update.get('message', {})
                            text = msg.get('text', '')
                            
                            # Check if it's a reply command
                            if text.startswith('!reply '):
                                parts = text.split(' ', 2)
                                if len(parts) >= 3:
                                    channel_id = parts[1]
                                    reply_text = parts[2]
                                    success = await self.send_to_discord(channel_id, reply_text)
                                    if success:
                                        await self.send_to_telegram(f"✅ Sent to Discord: {reply_text[:50]}...")
                                    else:
                                        await self.send_to_telegram(f"❌ Failed to send to channel {channel_id}")
        except Exception as e:
            print(f"Check Telegram error: {e}")

# Run bridge
if __name__ == '__main__':
    print("🌉 Starting Discord-Telegram Bridge...")
    bridge = DiscordTelegramBridge()
    bridge.run(DISCORD_TOKEN)
