#!/usr/bin/env python3
"""
Discord Terminal Bridge
Execute AWS/terminal commands via Discord
Output returned to Discord channel
"""

import os
import sys
import subprocess
import discord
from discord.ext import commands
from datetime import datetime

# Authorized Discord user IDs (add b3rt's ID)
AUTHORIZED_USERS = [
    6307161005,  # b3rt's Telegram ID (mapped to Discord if linked)
    # Add Discord user ID here when known
]

# Allowed commands (whitelist approach for safety)
# Empty list = allow all (dangerous but flexible)
# Populate with safe commands for restricted mode
ALLOWED_COMMANDS = []  # ['ls', 'cat', 'ps', 'df', 'free', 'uptime', 'pwd', 'echo', 'head', 'tail', 'grep']

# Blocked commands (blacklist - ALWAYS block these)
BLOCKED_COMMANDS = [
    'rm -rf /', 'rm -rf /*', 'dd if=/dev/zero', ':(){ :|:& };:', 
    'mkfs', 'format', 'shutdown', 'reboot', 'halt', 'poweroff',
    'su -', 'sudo su', 'passwd', 'userdel', 'deluser'
]

class TerminalBridge:
    def __init__(self, bot):
        self.bot = bot
    
    def is_authorized(self, user_id):
        """Check if user is authorized to run commands"""
        return str(user_id) in [str(u) for u in AUTHORIZED_USERS] or len(AUTHORIZED_USERS) == 0
    
    def is_safe_command(self, command):
        """Check if command is safe to execute"""
        # Check blocked commands
        for blocked in BLOCKED_COMMANDS:
            if blocked in command.lower():
                return False, f"Command blocked for security: contains '{blocked}'"
        
        # If whitelist is enabled, check against it
        if ALLOWED_COMMANDS:
            cmd_base = command.split()[0] if command.split() else ""
            if cmd_base not in ALLOWED_COMMANDS:
                return False, f"Command '{cmd_base}' not in allowed list"
        
        return True, "OK"
    
    async def execute_command(self, command, channel, user):
        """Execute command and return output to Discord"""
        
        # Security checks
        safe, reason = self.is_safe_command(command)
        if not safe:
            embed = discord.Embed(
                title="⛔ Command Blocked",
                description=reason,
                color=0xff0000
            )
            await channel.send(embed=embed)
            return
        
        # Create executing embed
        exec_embed = discord.Embed(
            title="⚙️ Executing Command",
            description=f"```{command}```",
            color=0xffa500
        )
        exec_embed.set_footer(text=f"Requested by {user} | {datetime.now().strftime('%H:%M:%S')}")
        exec_msg = await channel.send(embed=exec_embed)
        
        try:
            # Execute command with timeout
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,  # 30 second timeout
                cwd=os.path.expanduser('~/.openclaw/workspace')
            )
            
            stdout = result.stdout
            stderr = result.stderr
            returncode = result.returncode
            
            # Build output embed
            if returncode == 0:
                color = 0x00ff00  # Green for success
                status = "✅ Success"
            else:
                color = 0xffa500  # Orange for error
                status = f"⚠️ Exit Code: {returncode}"
            
            # Truncate output if too long (Discord limit ~2000 chars per field)
            max_output = 1800
            if len(stdout) > max_output:
                stdout = stdout[:max_output] + "\n... (truncated)"
            if len(stderr) > max_output:
                stderr = stderr[:max_output] + "\n... (truncated)"
            
            output_embed = discord.Embed(
                title=f"{status}",
                color=color,
                timestamp=datetime.now()
            )
            
            if stdout:
                output_embed.add_field(
                    name="📤 Output",
                    value=f"```{stdout}```",
                    inline=False
                )
            
            if stderr:
                output_embed.add_field(
                    name="⚠️ Errors",
                    value=f"```{stderr}```",
                    inline=False
                )
            
            if not stdout and not stderr:
                output_embed.add_field(
                    name="📤 Output",
                    value="*(No output)*",
                    inline=False
                )
            
            output_embed.set_footer(text=f"Command: {command[:50]}{'...' if len(command) > 50 else ''}")
            
            # Delete executing message and send result
            await exec_msg.delete()
            await channel.send(embed=output_embed)
            
        except subprocess.TimeoutExpired:
            await exec_msg.delete()
            timeout_embed = discord.Embed(
                title="⏱️ Command Timeout",
                description="Command took longer than 30 seconds and was terminated.",
                color=0xff0000
            )
            await channel.send(embed=timeout_embed)
            
        except Exception as e:
            await exec_msg.delete()
            error_embed = discord.Embed(
                title="❌ Execution Error",
                description=f"```{str(e)}```",
                color=0xff0000
            )
            await channel.send(embed=error_embed)

# Command handler to add to main bot
def setup_terminal_bridge(bot):
    """Add terminal commands to bot"""
    bridge = TerminalBridge(bot)
    
    @bot.command(name='exec', aliases=['run', 'cmd', '$'])
    async def execute(ctx, *, command: str):
        """Execute a terminal command on AWS instance"""
        
        # Check authorization
        if not bridge.is_authorized(ctx.author.id):
            embed = discord.Embed(
                title="⛔ Unauthorized",
                description="You are not authorized to execute terminal commands.",
                color=0xff0000
            )
            await ctx.send(embed=embed)
            return
        
        # Execute command
        await bridge.execute_command(command, ctx.channel, ctx.author.display_name)
    
    @bot.command(name='status')
    async def system_status(ctx):
        """Quick system status check"""
        await bridge.execute_command("uptime && df -h / && free -h", ctx.channel, ctx.author.display_name)
    
    @bot.command(name='ps')
    async def process_list(ctx):
        """Show running processes"""
        await bridge.execute_command("ps aux --sort=-%mem | head -20", ctx.channel, ctx.author.display_name)
    
    @bot.command(name='logs')
    async def view_logs(ctx, lines: int = 20):
        """View recent logs"""
        await bridge.execute_command(f"tail -n {lines} ~/.openclaw/logs/*.log 2>/dev/null | tail -{lines}", ctx.channel, ctx.author.display_name)
    
    return bridge

if __name__ == "__main__":
    print("Terminal Bridge module loaded")
    print("Add 'setup_terminal_bridge(bot)' to your main bot to enable commands")
