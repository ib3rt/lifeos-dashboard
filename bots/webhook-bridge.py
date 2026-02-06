# 🌉 Webhook Bridge Server
## Routes webhooks between services

from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Configuration
DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL', '')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')

@app.route('/webhook/github', methods=['POST'])
def github_webhook():
    """Handle GitHub webhooks"""
    data = request.json
    event = request.headers.get('X-GitHub-Event', 'unknown')
    
    if event == 'push':
        msg = f"📦 GitHub Push\n{data['repository']['name']}: {data['head_commit']['message'][:100]}"
        send_discord(msg)
        send_telegram(msg)
    
    elif event == 'pull_request':
        msg = f"🔀 PR #{data['number']}: {data['action']}\n{data['pull_request']['title'][:100]}"
        send_discord(msg)
    
    return jsonify({"status": "ok"})

@app.route('/webhook/vercel', methods=['POST'])
def vercel_webhook():
    """Handle Vercel deployment webhooks"""
    data = request.json
    
    if data.get('type') == 'deployment':
        status = data.get('payload', {}).get('state', 'unknown')
        project = data.get('payload', {}).get('name', 'unknown')
        url = data.get('payload', {}).get('url', '')
        
        msg = f"🚀 Vercel Deploy: {project}\nStatus: {status}\nURL: {url}"
        send_discord(msg)
        send_telegram(msg)
    
    return jsonify({"status": "ok"})

@app.route('/webhook/n8n', methods=['POST'])
def n8n_webhook():
    """Handle n8n workflow triggers"""
    data = request.json
    
    # Forward to appropriate service
    msg = data.get('message', 'n8n workflow completed')
    
    if data.get('to') == 'discord':
        send_discord(msg)
    elif data.get('to') == 'telegram':
        send_telegram(msg)
    else:
        send_discord(msg)
        send_telegram(msg)
    
    return jsonify({"status": "ok"})

def send_discord(message):
    """Send message to Discord webhook"""
    if DISCORD_WEBHOOK_URL:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": message})

def send_telegram(message):
    """Send message to Telegram"""
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": message})

if __name__ == '__main__':
    print("🌉 Webhook Bridge Server starting...")
    print("Routes:")
    print("  /webhook/github")
    print("  /webhook/vercel")
    print("  /webhook/n8n")
    app.run(host='0.0.0.0', port=5000)
