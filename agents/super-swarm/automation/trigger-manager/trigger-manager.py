#!/usr/bin/env python3
"""
Trigger Manager Agent
Manages event triggers and automated responses

Usage:
    python3 trigger-manager.py --add "event" --action "command"
    python3 trigger-manager.py --list
    python3 trigger-manager.py --fire "event"
    python3 trigger-manager.py --status
"""

import json
import argparse
from datetime import datetime
from pathlib import Path

class TriggerManager:
    def __init__(self):
        self.workspace = Path('/home/ubuntu/.openclaw/workspace')
        self.triggers_file = self.workspace / 'agents/super-swarm/automation/trigger-manager/triggers.json'
        self.output_dir = self.workspace / 'agents/super-swarm/automation/trigger-manager/output'
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.triggers = self._load_triggers()
    
    def _load_triggers(self):
        """Load triggers"""
        if self.triggers_file.exists():
            with open(self.triggers_file, 'r') as f:
                return json.load(f)
        return []
    
    def _save_triggers(self):
        """Save triggers"""
        with open(self.triggers_file, 'w') as f:
            json.dump(self.triggers, f, indent=2)
    
    def add_trigger(self, event, action, condition=None):
        """Add new trigger"""
        trigger = {
            "id": len(self.triggers) + 1,
            "event": event,
            "action": action,
            "condition": condition,
            "enabled": True,
            "trigger_count": 0,
            "created": datetime.now().isoformat()
        }
        
        self.triggers.append(trigger)
        self._save_triggers()
        print(f"✅ Trigger added: {event} → {action}")
        return trigger
    
    def list_triggers(self):
        """List all triggers"""
        if not self.triggers:
            print("\n⚡ No triggers configured")
            return
        
        print(f"\n⚡ Triggers ({len(self.triggers)} total)")
        print("=" * 60)
        for t in self.triggers:
            status = "✅" if t['enabled'] else "⏸️"
            count = t['trigger_count']
            print(f"{status} [{t['event']}] → {t['action'][:40]}... ({count} fires)")
    
    def fire_trigger(self, event):
        """Fire a trigger"""
        fired = []
        for t in self.triggers:
            if t['event'] == event and t['enabled']:
                t['trigger_count'] += 1
                fired.append(t)
                print(f"⚡ Fired: {t['event']} → {t['action']}")
        
        if fired:
            self._save_triggers()
        else:
            print(f"❌ No trigger found for: {event}")
        
        return fired
    
    def get_status(self):
        """Get trigger manager status"""
        return {
            "total_triggers": len(self.triggers),
            "active_triggers": len([t for t in self.triggers if t['enabled']]),
            "total_fires": sum(t['trigger_count'] for t in self.triggers)
        }

def main():
    manager = TriggerManager()
    
    parser = argparse.ArgumentParser(description='Trigger Manager Agent')
    parser.add_argument('--add', '-a', nargs=2, metavar=('EVENT', 'ACTION'), help='Add trigger')
    parser.add_argument('--list', '-l', action='store_true', help='List triggers')
    parser.add_argument('--fire', '-f', metavar='EVENT', help='Fire trigger')
    parser.add_argument('--status', '-s', action='store_true', help='Show status')
    
    args = parser.parse_args()
    
    print("⚡ Trigger Manager Agent")
    print("=" * 60)
    
    if args.add:
        manager.add_trigger(args.add[0], args.add[1])
    elif args.list:
        manager.list_triggers()
    elif args.fire:
        manager.fire_trigger(args.fire)
    elif args.status:
        status = manager.get_status()
        print(f"\n📊 Trigger Status:")
        print(f"   Total Triggers: {status['total_triggers']}")
        print(f"   Active: {status['active_triggers']}")
        print(f"   Total Fires: {status['total_fires']}")
    else:
        print("\nUsage:")
        print("  python3 trigger-manager.py --add \"new-file\" \"process-file.sh\"")
        print("  python3 trigger-manager.py --list")
        print("  python3 trigger-manager.py --fire \"new-file\"")
        print("  python3 trigger-manager.py --status")

if __name__ == '__main__':
    main()
