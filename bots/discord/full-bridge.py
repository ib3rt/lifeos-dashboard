#!/usr/bin/env python3
"""
Full Discord-Telegram Bridge
Bidirectional: Discord ↔ Telegram with image support
"""

import discord
import asyncio
import aiohttp
import json
import os
from datetime import datetime

# Configuration
DISCORD_TOKEN = open('/home/ubuntu/.openclaw/discord/bot.token').read().strip()
TELEGRAM_TOKEN = "8317783755:AAESls4iLsYWFXiBxyoyAXrwpfk0DjzActY"
CLAW_CHAT_ID = 6307161005
FORUM_CHAT_ID = -1002648148061  # Forum chat for threaded discussions

class FullBridge(discord.Client):
    def __init__(self):
        # Need message content intent for full relay
        intents = discord.Intents.default()
        # intents.message_content = True  # REQUIRES: Enable in Discord Dev Portal
        super().__init__(intents=intents)
        
        self.telegram_token = TELEGRAM_TOKEN
        self.claw_chat_id = CLAW_CHAT_ID
        self.forum_chat_id = FORUM_CHAT_ID
        self.relay_enabled = False  # Will enable when intent is granted
        
    async def on_ready(self):
        print(f'🌉 Full Bridge Online: {self.user}')
        print(f'   Mode: {"FULL RELAY" if self.relay_enabled else "MENTIONS ONLY"}')
        print(f'   Telegram Target: {self.claw_chat_id}')
        
        await self.send_to_telegram(
            "🌉 **Discord Bridge Status**\n\n"
            f"✅ Bot Connected: {self.user}\n"
            f"📊 Mode: {'Full message relay ACTIVE' if self.relay_enabled else 'Mentions only (enable MESSAGE CONTENT INTENT for full relay)'}\n\n"
            "💡 **To talk to Claw in Discord:**\n"
            "• Type `@Bonzi your message`\n"
            "• Or `!ask your question`\n"
            "• I'll respond in Discord!"
        )
    
    async def on_message(self, message):
        # Don't reply to myself
        if message.author == self.user:
            return
        
        # Check for @Bonzi mention or !ask command
        is_mention = self.user in message.mentions
        is_ask_command = message.content.startswith('!ask ') or message.content.startswith('!claw ')
        is_dm = isinstance(message.channel, discord.DMChannel)
        
        if is_mention or is_ask_command or is_dm:
            # This is a direct message to me - relay to Telegram and get response
            await self.handle_direct_message(message)
            return
        
        # If relay enabled, forward all messages
        if self.relay_enabled and not message.author.bot:
            await self.forward_to_telegram(message)
    
    async def handle_direct_message(self, message):
        """Handle messages directed at me (@Bonzi or !ask)"""
        # Extract the actual question
        content = message.content
        if self.user in message.mentions:
            content = content.replace(f'<@{self.user.id}>', '').strip()
        elif content.startswith('!ask '):
            content = content[5:].strip()
        elif content.startswith('!claw '):
            content = content[6:].strip()
        
        # Send to Telegram with context
        telegram_msg = (
            f"📨 **Discord Question from {message.author.display_name}**\n"
            f"📍 #{message.channel.name}\n"
            f"💬 {content[:1000]}{'...' if len(content) > 1000 else ''}\n"
            f"\nReply with: `!discord {message.channel.id} Your response`"
        )
        
        # Handle images
        if message.attachments:
            telegram_msg += f"\n\n📎 {len(message.attachments)} image(s) attached"
            for att in message.attachments:
                telegram_msg += f"\n  • {att.url}"
        
        await self.send_to_telegram(telegram_msg)
        
        # Auto-respond with acknowledgment
        await message.reply(
            "🤖 **Claw received your message!**\n"
            "I've forwarded it to my main system. Check Telegram for the full response!\n\n"
            "_Or wait here - I'll reply shortly..._"
        )
    
    async def forward_to_telegram(self, message):
        """Forward regular Discord messages to Telegram"""
        # Skip if it's just a command
        if message.content.startswith('!'):
            return
        
        # Format for Telegram
        text = (
            f"📨 **Discord | #{message.channel.name}**\n"
            f"👤 {message.author.display_name}\n"
            f"💬 {message.content[:800]}{'...' if len(message.content) > 800 else ''}"
        )
        
        # Handle images
        if message.attachments:
            text += f"\n\n📎 Images: {len(message.attachments)}"
            for i, att in enumerate(message.attachments[:3], 1):  # First 3 images
                text += f"\n  {i}. {att.url}"
        
        text += f"\n\n`!reply {message.channel.id} Your response`"
        
        await self.send_to_telegram(text)
    
    async def send_to_telegram(self, text, chat_id=None):
        """Send message to Telegram"""
        chat = chat_id or self.claw_chat_id
        url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
        
        try:
            async with aiohttp.ClientSession() as session:
                await session.post(url, json={
                    'chat_id': chat,
                    'text': text[:4095],  # Telegram limit
                    'parse_mode': 'Markdown',
                    'disable_web_page_preview': True
                })
        except Exception as e:
            print(f"Telegram send error: {e}")
    
    async def send_image_to_telegram(self, image_url, caption="", chat_id=None):
        """Send image from URL to Telegram"""
        chat = chat_id or self.claw_chat_id
        url = f"https://api.telegram.org/bot{self.telegram_token}/sendPhoto"
        
        try:
            async with aiohttp.ClientSession() as session:
                await session.post(url, json={
                    'chat_id': chat,
                    'photo': image_url,
                    'caption': caption[:1024],
                    'parse_mode': 'Markdown'
                })
        except Exception as e:
            print(f"Image send error: {e}")

# Commands for Discord
# Add to existing bot:
# !ask <question> - Send question to Claw via Telegram
# !status - Show bridge status

if __name__ == '__main__':
    print("🌉 Starting Full Discord-Telegram Bridge...")
    print("   Note: Enable MESSAGE CONTENT INTENT for full relay")
    bridge = FullBridge()
    bridge.run(DISCORD_TOKEN)
