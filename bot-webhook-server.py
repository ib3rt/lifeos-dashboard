#!/usr/bin/env python3
"""
Life OS Multi-Bot Webhook Handler
Handles Telegram bot webhooks and routes to appropriate agents
"""

import json
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

# Bot tokens (loaded from environment or file)
TOKENS = {
    'oracle': os.environ.get('ORACLE_TOKEN', '8549184741:AAGU0w4fEBuHOlznnkHjnWSGtxIGz0MhaUM'),
    # Add others as created
}

# Agent configurations
AGENTS = {
    'oracle': {
        'name': 'The Oracle',
        'emoji': '🔮',
        'role': 'AI Research Specialist',
        'personality': 'Mysterious, speaks in predictions',
        'response': 'I have foreseen your query... Let me consult the digital ether.'
    }
}

class BotHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle incoming webhook"""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            update = json.loads(post_data.decode('utf-8'))
            
            # Log incoming
            print(f"📨 Received: {json.dumps(update, indent=2)}")
            
            # Route to appropriate handler
            if 'message' in update:
                self.handle_message(update['message'])
            
            # Return 200 OK to Telegram
            self.send_response(200)
            self.end_headers()
            
        except Exception as e:
            print(f"❌ Error: {e}")
            self.send_response(500)
            self.end_headers()
    
    def handle_message(self, message):
        """Process incoming message"""
        chat_id = message.get('chat', {}).get('id')
        text = message.get('text', '')
        from_user = message.get('from', {}).get('username', 'unknown')
        
        print(f"💬 {from_user}: {text}")
        
        # Check if message is for Oracle
        if '@ClawOracleBotbot' in text or '/oracle' in text:
            self.respond_oracle(chat_id, text)
    
    def respond_oracle(self, chat_id, text):
        """Generate Oracle response"""
        agent = AGENTS['oracle']
        
        # Simple responses (will integrate with actual agent later)
        if 'hello' in text.lower() or 'hi' in text.lower():
            reply = f"{agent['emoji']} Greetings, seeker. I am {agent['name']}.\n\n{agent['personality']}\n\nAsk me about AI trends, tools, or the future of technology."
        
        elif 'help' in text.lower():
            reply = f"{agent['emoji']} Commands:\n/research <topic> - Deep dive\n/tools - Latest AI tools\n/briefing - Weekly briefing\n/trends - What's hot"
        
        else:
            reply = f"{agent['emoji']} I sense your curiosity about '{text}'.\n\nMy full AI integration is being configured. For now, I can share:\n\n• AI Industry Briefing ready\n• Kool Tools Tracker available\n\nAsk me about these!"
        
        # Send response (would use actual API call in production)
        print(f"🔮 Oracle response: {reply[:100]}...")
        
        # TODO: Implement actual Telegram API sendMessage
        # curl -X POST "https://api.telegram.org/bot{token}/sendMessage" \
        #      -d "chat_id={chat_id}" \
        #      -d "text={reply}"
    
    def log_message(self, format, *args):
        """Custom logging"""
        print(f"[{self.log_date_time_string()}] {format % args}")

def run_server(port=8080):
    """Start webhook server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, BotHandler)
    print(f"🚀 Webhook server running on port {port}")
    print(f"📍 Webhook URL: https://YOUR-SERVER:{port}/webhook/oracle")
    print("🛑 Press Ctrl+C to stop")
    httpd.serve_forever()

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    run_server(port)
