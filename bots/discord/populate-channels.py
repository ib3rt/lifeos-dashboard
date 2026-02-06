#!/usr/bin/env python3
"""
Populate Discord channels with content and resources
"""

import discord
import asyncio
import json

token = open('/home/ubuntu/.openclaw/discord/bot.token').read().strip()

class ChannelPopulator(discord.Client):
    async def on_ready(self):
        print(f"🎮 Connected: {self.user}\n")
        
        # Find server
        guild = None
        for g in self.guilds:
            if "Life" in g.name:
                guild = g
                break
        
        if not guild:
            print("❌ Server not found")
            await self.close()
            return
        
        print(f"Populating: {guild.name}\n")
        
        # Channel content to post
        channel_content = {
            "welcome": {
                "title": "🦾 Welcome to Life OS Command Center",
                "description": "Your centralized hub for 15 AI agents, automation, and project management.",
                "fields": [
                    ("🤖 Getting Started", "Type `!agents` to see all available agents\nUse `!help` for commands\nMention @Bonzi for assistance"),
                    ("🌐 Quick Links", "[Dashboard](https://lifeos-dashboard-three.vercel.app)\n[Sparkling Solutions](https://sparkling-solutions.vercel.app)\n[BE Repaired](https://be-repaired.vercel.app)"),
                    ("📁 Resources", "All project files in `~/workspace/`\nAgent deliverables in `~/workspace/agents/`\nResearch in `~/workspace/research/`")
                ]
            },
            "announcements": {
                "title": "📢 Life OS Announcements",
                "description": "Latest updates and milestones.",
                "fields": [
                    ("✅ Recently Completed", "• 15 AI agents deployed\n• 3 business websites live\n• Discord server fully configured\n• n8n automation running"),
                    ("🚀 In Progress", "• X/Twitter bot development\n• Local node hardware planning\n• Voice cloning setup"),
                    ("📅 Coming Soon", "• Custom domain setup\n• Multi-bot Telegram swarm\n• Advanced workflow automations")
                ]
            },
            "oracle-insights": {
                "title": "🔮 The Oracle - AI Research Hub",
                "description": "Latest AI industry intelligence, tool reviews, and trend analysis.",
                "fields": [
                    ("📊 Latest Research", "• GPT-5.2 deployment analysis\n• Claude 4.5 coding capabilities\n• DeepSeek R1 cost comparison"),
                    ("🛠️ Kool Tools", "• Claude Code - Terminal AI\n• Perplexity Comet - AI browser\n• n8n - Workflow automation"),
                    ("📚 Resources", "[AI Briefing](https://lifeos-dashboard-three.vercel.app)\n[Tool Tracker](https://lifeos-dashboard-three.vercel.app)\nDashboard > Reports tab")
                ]
            },
            "diamond-hands": {
                "title": "💎 Diamond Hands - Crypto Command Center",
                "description": "Web3, DeFi, and crypto asset management.",
                "fields": [
                    ("📈 Market Focus", "• Portfolio tracking\n• DeFi yield strategies\n• NFT market analysis"),
                    ("🔐 Wallet Setup", "• Phantom integration ready\n• Web3.js configured\n• Multi-chain support planned"),
                    ("📚 Resources", "[Phantom Guide](https://lifeos-dashboard-three.vercel.app)\nDashboard > Reports > Phantom Integration")
                ]
            },
            "mechanic-workshop": {
                "title": "⚙️ The Mechanic - Operations Hub",
                "description": "Automation, deployments, and system management.",
                "fields": [
                    ("🚀 Active Deployments", "• Dashboard: Vercel\n• Business sites: 3 live\n• n8n: Port 5678"),
                    ("🛠️ CLI Tools", "• `!status` - System health\n• `!deploy` - Trigger builds\n• `!agents` - Agent roster"),
                    ("📚 Resources", "Tools in `~/workspace/tools/`\nn8n: http://54.147.20.162:5678")
                ]
            },
            "sentinel-alerts": {
                "title": "🛡️ Sentinel - Security Operations",
                "description": "Security alerts, audits, and hardening guides.",
                "fields": [
                    ("🔒 Active Monitoring", "• API key rotation\n• Token expiration tracking\n• Backup verification"),
                    ("⚠️ Recent Alerts", "• GitHub token rotated\n• Vercel token updated\n• Discord bot token refreshed"),
                    ("📚 Resources", "Security docs in workspace\nRemediation checklist available")
                ]
            },
            "local-node": {
                "title": "🖥️ Local Node Project",
                "description": "Self-hosted Life OS infrastructure.",
                "fields": [
                    ("📋 Project Plan", "• Hardware: Pi 5 / NUC\n• Stack: Ollama, n8n, Grafana\n• VPN: Tailscale mesh"),
                    ("💰 Budget Options", "• Pi 5 + NVMe: ~$200\n• Intel NUC 13: ~$600\n• Custom build: ~$1000"),
                    ("📚 Resources", "[Architecture Guide](https://lifeos-dashboard-three.vercel.app)\n30KB detailed specs in dashboard")
                ]
            },
            "x-automation": {
                "title": "🐦 X/Twitter Bot Project",
                "description": "Social media automation with Hype Man.",
                "fields": [
                    ("📋 Status", "• Code: Ready\n• API access: Pending\n• Cost: $100/mo (X Basic)"),
                    ("✨ Features", "• Agent spotlights\n• Progress threads\n• Auto-posting workflows"),
                    ("📚 Resources", "[Integration Plan](https://lifeos-dashboard-three.vercel.app)\n13KB implementation guide")
                ]
            },
            "voice-cloning": {
                "title": "🎙️ AI Voice Clone Project",
                "description": "Personal voice for podcast and automation.",
                "fields": [
                    ("📋 Status", "• Guide: Ready\n• Recording: Pending\n• Options: ElevenLabs / XTTS"),
                    ("🎤 Recording Setup", "• 10-30 min sample\n• Clean audio\n• Varied sentences"),
                    ("📚 Resources", "[Voice Setup Guide](https://lifeos-dashboard-three.vercel.app)\n17KB documentation")
                ]
            },
            "github-updates": {
                "title": "🔀 GitHub Activity",
                "description": "Repository updates and deployment notifications.",
                "fields": [
                    ("📁 Repositories", "• lifeos-dashboard\n• workspace (private)"),
                    ("🚀 Recent Deploys", "• Dashboard v2.3\n• Business sites live\n• Discord bot updated"),
                    ("🔗 Links", "[GitHub](https://github.com/ib3rt)\n[Dashboard Repo](https://github.com/ib3rt/lifeos-dashboard)")
                ]
            }
        }
        
        # Post content to each channel
        for channel_name, content in channel_content.items():
            channel = discord.utils.get(guild.text_channels, name=channel_name)
            if channel:
                try:
                    embed = discord.Embed(
                        title=content["title"],
                        description=content["description"],
                        color=0x00d4ff
                    )
                    for name, value in content["fields"]:
                        embed.add_field(name=name, value=value, inline=False)
                    
                    await channel.send(embed=embed)
                    print(f"✅ Posted to #{channel_name}")
                except Exception as e:
                    print(f"❌ Failed #{channel_name}: {e}")
            else:
                print(f"⚠️ Channel not found: #{channel_name}")
        
        print("\n🎉 Channel population complete!")
        await self.close()

intents = discord.Intents.default()
client = ChannelPopulator(intents=intents)
client.run(token)
