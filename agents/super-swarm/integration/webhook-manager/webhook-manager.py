#!/usr/bin/env python3
"""
Webhook Manager Agent
Manages incoming and outgoing webhooks

Usage:
    python3 webhook-manager.py --add "webhook-name" --url "https://..."
    python3 webhook-manager.py --list
    python3 webhook-manager.py --send "webhook-name" --data '{"key": "value"}'
    python3 webhook-manager.py --status
"""

import json
import argparse
import requests
from datetime import datetime
from pathlib import Path

class WebhookManager:
    def __init__(self):
        self.workspace = Path('/home/ubuntu/.openclaw/workspace')
        self.webhooks_file = self.workspace / 'agents/super-swarm/integration/webhook-manager/webhooks.json'
        self.output_dir = self.workspace / 'agents/super-swarm/integration/webhook-manager/output'
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.webhooks = self._load_webhooks()
    
    def _load_webhooks(self):
        """Load webhooks"""
        if self.webhooks_file.exists():
            with open(self.webhooks_file, 'r') as f:
                return json.load(f)
        return {"incoming": [], "outgoing": []}
    
    def _save_webhooks(self):
        """Save webhooks"""
        with open(self.webhooks_file, 'w') as f:
            json.dump(self.webhooks, f, indent=2)
    
    def add_webhook(self, name, url, webhook_type='outgoing', secret=None):
        """Add new webhook"""
        webhook = {
            "id": len(self.webhooks[webhook_type]) + 1,
            "name": name,
            "url": url,
            "secret": secret,
            "type": webhook_type,
            "status": "active",
            "events": ["all"],
            "created": datetime.now().isoformat(),
            "last_triggered": None
        }
        
        self.webhooks[webhook_type].append(webhook)
        self._save_webhooks()
        print(f"✅ Webhook added: {name} ({webhook_type})")
        return webhook
    
    def list_webhooks(self):
        """List all webhooks"""
        incoming = self.webhooks['incoming']
        outgoing = self.webhooks['outgoing']
        
        print(f"\n🔔 Webhooks")
        print("=" * 60)
        print(f"Incoming ({len(incoming)}):")
        for wh in incoming:
            print(f"  👂 {wh['name']} - {wh.get('url', 'configured')}")
        
        print(f"\nOutgoing ({len(outgoing)}):")
        for wh in outgoing:
            status = "✅" if wh['status'] == 'active' else "⏸️"
            print(f"  📤 {status} {wh['name']} - {wh['url'][:50]}...")
    
    def send_webhook(self, name, data=None):
        """Send outgoing webhook"""
        for wh in self.webhooks['outgoing']:
            if wh['name'] == name:
                print(f"📤 Sending webhook: {name}")
                try:
                    response = requests.post(wh['url'], json=data or {}, timeout=10)
                    wh['last_triggered'] = datetime.now().isoformat()
                    wh['last_status'] = response.status_code
                    self._save_webhooks()
                    print(f"✅ Webhook sent: {name} ({response.status_code})")
                except Exception as e:
                    print(f"❌ Webhook failed: {str(e)[:50]}")
                return
        print(f"❌ Webhook not found: {name}")
    
    def receive_webhook(self, name, payload):
        """Process incoming webhook"""
        for wh in self.webhooks['incoming']:
            if wh['name'] == name:
                wh['last_triggered'] = datetime.now().isoformat()
                wh['last_payload'] = payload
                self._save_webhooks()
                print(f"👂 Received webhook: {name}")
                return True
        return False
    
    def get_status(self):
        """Get webhook status"""
        return {
            "incoming": len(self.webhooks['incoming']),
            "outgoing": len(self.webhooks['outgoing']),
            "active": len([w for w in self.webhooks['outgoing'] if w['status'] == 'active'])
        }

def main():
    manager = WebhookManager()
    
    parser = argparse.ArgumentParser(description='Webhook Manager Agent')
    parser.add_argument('--add', '-a', nargs=2, metavar=('NAME', 'URL'), help='Add webhook')
    parser.add_argument('--type', metavar='TYPE', choices=['incoming', 'outgoing'], default='outgoing')
    parser.add_argument('--list', '-l', action='store_true', help='List webhooks')
    parser.add_argument('--send', '-s', metavar='NAME', help='Send webhook')
    parser.add_argument('--data', '-d', help='Webhook payload (JSON)')
    parser.add_argument('--status', action='store_true', help='Show status')
    
    args = parser.parse_args()
    
    print("🔔 Webhook Manager Agent")
    print("=" * 60)
    
    if args.add:
        manager.add_webhook(args.add[0], args.add[1], args.type)
    elif args.list:
        manager.list_webhooks()
    elif args.send:
        data = json.loads(args.data) if args.data else None
        manager.send_webhook(args.send, data)
    elif args.status:
        status = manager.get_status()
        print(f"\n📊 Webhook Status:")
        print(f"   Incoming: {status['incoming']}")
        print(f"   Outgoing: {status['outgoing']}")
        print(f"   Active: {status['active']}")
    else:
        print("\nUsage:")
        print("  python3 webhook-manager.py --add \"slack\" \"https://hooks.slack.com/...\"")
        print("  python3 webhook-manager.py --list")
        print("  python3 webhook-manager.py --send \"slack\" --data '{\"text\":\"Hello\"}'")
        print("  python3 webhook-manager.py --status")

if __name__ == '__main__':
    main()
