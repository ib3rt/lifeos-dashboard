#!/usr/bin/env python3
"""
Discord-Telegram Bridge with Agent Channel Responses
Posts agent replies directly to Discord channels
"""

import discord
import asyncio
import aiohttp
import json
import os
import subprocess
from datetime import datetime

DISCORD_TOKEN = open('/home/ubuntu/.openclaw/discord/bot.token').read().strip()
TELEGRAM_TOKEN = "8317783755:AAESls4iLsYWFXiBxyoyAXrwpfk0DjzActY"
CLAW_CHAT_ID = 6307161005

class BridgeWithAgentResponses(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True  # NOW ENABLED!
        super().__init__(intents=intents)
        self.telegram_token = TELEGRAM_TOKEN
        self.claw_chat_id = CLAW_CHAT_ID
        
    async def on_ready(self):
        print(f'🌉 Bridge Active: {self.user}')
        print('   Mode: FULL RELAY + AGENT CHANNEL RESPONSES')
        
        # Send startup message
        await self.send_to_telegram("🌉 **Bridge Active** - I can now reply directly in Discord channels!")
    
    async def on_message(self, message):
        if message.author == self.user:
            return
        
        # Check if message is in an agent channel
        channel_agent = self.get_channel_agent(message.channel.name)
        
        if channel_agent and not message.content.startswith('!'):
            # Generate AI response and post IN DISCORD
            await self.respond_as_agent_in_discord(message, channel_agent)
            
            # Also forward to Telegram for Claw's awareness
            await self.forward_to_telegram(message, agent=channel_agent)
            return
        
        # Handle @mentions and commands
        if self.user in message.mentions or message.content.startswith(('!ask', '!claw')):
            await self.handle_direct_message(message)
            return
        
        # Forward all other messages
        await self.forward_to_telegram(message)
    
    def get_channel_agent(self, channel_name):
        """Map channels to agents"""
        mapping = {
            'oracle-insights': 'oracle',
            'diamond-hands': 'diamond', 
            'mechanic-workshop': 'mechanic',
            'sentinel-alerts': 'sentinel',
            'agent-chat': None
        }
        return mapping.get(channel_name)
    
    async def respond_as_agent_in_discord(self, message, agent_key):
        """Generate AI response and post directly in Discord"""
        # Get agent persona
        agents = {
            'oracle': {'name': 'The Oracle', 'emoji': '🔮', 'desc': 'AI Research', 'personality': 'Mysterious and insightful'},
            'diamond': {'name': 'Diamond Hands', 'emoji': '💎', 'desc': 'Crypto/Web3', 'personality': 'Enthusiastic about crypto'},
            'mechanic': {'name': 'The Mechanic', 'emoji': '⚙️', 'desc': 'Operations', 'personality': 'Direct and efficient'},
            'sentinel': {'name': 'Sentinel', 'emoji': '🛡️', 'desc': 'Security', 'personality': 'Vigilant and protective'}
        }
        
        agent = agents.get(agent_key, agents['oracle'])
        
        # Generate AI response using Moonshot
        response = await self.generate_ai_response(agent, message.content, message.author.display_name)
        
        # Post response in Discord channel
        embed = discord.Embed(
            title=f"{agent['emoji']} {agent['name']}",
            description=response,
            color=0x00d4ff,
            timestamp=datetime.now()
        )
        embed.set_footer(text=f"AI Agent | {agent['desc']}")
        
        await message.reply(embed=embed)
        print(f"✅ {agent['name']} responded in #{message.channel.name}")
    
    async def generate_ai_response(self, agent, user_message, username):
        """Generate AI response using Moonshot API"""
        import json
        
        # Load API key
        api_key = ""
        try:
            with open('/home/ubuntu/.openclaw/agents/main/agent/auth-profiles.json') as f:
                config = json.load(f)
                api_key = config.get('profiles', {}).get('moonshot:default', {}).get('key', '')
        except:
            pass
        
        if not api_key:
            # Fallback response
            return f"{agent['emoji']} Hello {username}! I'm {agent['name']}, {agent['personality']}.\n\nYou asked about: *{user_message[:100]}*\n\nI'd love to help, but I need my full AI brain connected! Ask Claw to check my API key."
        
        # Call Moonshot API
        system_prompt = f"""You are {agent['name']} {agent['emoji']}, a specialized AI agent.

Your expertise: {agent['desc']}
Your personality: {agent['personality']}

Respond to the user's message in character. Be helpful, engaging, and concise (2-4 sentences). Stay true to your personality."""

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    'https://api.moonshot.ai/v1/chat/completions',
                    headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'},
                    json={
                        'model': 'kimi-k2.5',
                        'messages': [
                            {'role': 'system', 'content': system_prompt},
                            {'role': 'user', 'content': f"{username} says: {user_message}"}
                        ],
                        'temperature': 0.7,
                        'max_tokens': 300
                    }
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data['choices'][0]['message']['content']
        except Exception as e:
            print(f"AI error: {e}")
        
        return f"{agent['emoji']} Hey {username}! I'm {agent['name']}. {agent['personality']}\n\nI'm ready to help with: *{user_message[:100]}*"
    
    async def forward_to_telegram(self, message, agent=None):
        """Forward Discord message to Telegram"""
        agent_tag = f" | {agent.upper()} Agent" if agent else ""
        text = f"📨 Discord{agent_tag} | #{message.channel.name}\n👤 {message.author.display_name}\n💬 {message.content[:800]}"
        
        if message.attachments:
            text += f"\n📎 Images: {len(message.attachments)}"
            for att in message.attachments[:2]:
                text += f"\n  • {att.url}"
        
        await self.send_to_telegram(text)
    
    async def handle_direct_message(self, message):
        """Handle @mentions"""
        content = message.content.replace(f'<@{self.user.id}>', '').strip()
        if content.startswith('!ask ') or content.startswith('!claw '):
            content = content.split(' ', 1)[1] if ' ' in content else content
        
        # Send to Telegram
        await self.send_to_telegram(
            f"📨 **Discord DM from {message.author.display_name}**\n"
            f"📍 #{message.channel.name}\n"
            f"💬 {content}\n"
            f"\nReply: `!discord {message.channel.id} Your response`"
        )
        
        # Acknowledge in Discord
        await message.reply("🤖 **Message forwarded to Claw!** Check Telegram for the response, or wait here...")
    
    async def send_to_telegram(self, text):
        """Send to Telegram"""
        url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
        try:
            async with aiohttp.ClientSession() as session:
                await session.post(url, json={
                    'chat_id': self.claw_chat_id,
                    'text': text[:4095],
                    'parse_mode': 'Markdown'
                })
        except Exception as e:
            print(f"Telegram error: {e}")

# Run
if __name__ == '__main__':
    print("🌉 Starting Bridge with Agent Channel Responses...")
    bridge = BridgeWithAgentResponses()
    bridge.run(DISCORD_TOKEN)
