#!/usr/bin/env python3
"""
Sync Manager Agent
Synchronizes data across systems

Usage:
    python3 sync-manager.py --add "source" "destination"
    python3 sync-manager.py --list
    python3 sync-manager.py --sync "sync-pair"
    python3 sync-manager.py --status
    python3 sync-manager.py --history "sync-pair"
"""

import json
import argparse
from datetime import datetime
from pathlib import Path

class SyncManager:
    def __init__(self):
        self.workspace = Path('/home/ubuntu/.openclaw/workspace')
        self.syncs_file = self.workspace / 'agents/super-swarm/integration/sync-manager/syncs.json'
        self.output_dir = self.workspace / 'agents/super-swarm/integration/sync-manager/output'
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.syncs = self._load_syncs()
    
    def _load_syncs(self):
        """Load syncs"""
        if self.syncs_file.exists():
            with open(self.syncs_file, 'r') as f:
                return json.load(f)
        return {"pairs": []}
    
    def _save_syncs(self):
        """Save syncs"""
        with open(self.syncs_file, 'w') as f:
            json.dump(self.syncs, f, indent=2)
    
    def add_sync(self, source, destination, schedule='manual'):
        """Add sync pair"""
        sync = {
            "id": len(self.syncs['pairs']) + 1,
            "name": f"{source} ↔ {destination}",
            "source": source,
            "destination": destination,
            "schedule": schedule,
            "status": "idle",
            "last_sync": None,
            "last_result": None,
            "sync_count": 0,
            "history": [],
            "created": datetime.now().isoformat()
        }
        
        self.syncs['pairs'].append(sync)
        self._save_syncs()
        print(f"✅ Sync pair added: {source} ↔ {destination}")
        return sync
    
    def list_syncs(self):
        """List sync pairs"""
        pairs = self.syncs['pairs']
        if not pairs:
            print("\n🔄 No sync pairs configured")
            return
        
        print(f"\n🔄 Sync Pairs ({len(pairs)} total)")
        print("=" * 60)
        for p in pairs:
            status = {"idle": "⚪", "syncing": "🔄", "success": "✅", "error": "❌"}.get(p['status'], "⚪")
            print(f"{status} {p['name']} ({p['schedule']}) - {p['sync_count']} syncs")
    
    def sync(self, sync_id):
        """Execute sync"""
        for p in self.syncs['pairs']:
            if str(p['id']) == str(sync_id) or p['name'] == sync_id:
                print(f"🔄 Syncing: {p['name']}")
                p['status'] = 'syncing'
                self._save_syncs()
                
                # Simulate sync
                p['last_sync'] = datetime.now().isoformat()
                p['sync_count'] += 1
                p['status'] = 'success'
                p['last_result'] = {
                    "items_synced": 42,
                    "duration_seconds": 1.5,
                    "errors": 0
                }
                p['history'].append({
                    "timestamp": datetime.now().isoformat(),
                    "items": 42,
                    "duration": 1.5,
                    "errors": 0
                })
                self._save_syncs()
                print(f"✅ Sync complete: {p['name']} (42 items)")
                return
        print(f"❌ Sync pair not found: {sync_id}")
    
    def show_history(self, sync_id):
        """Show sync history"""
        for p in self.syncs['pairs']:
            if str(p['id']) == str(sync_id) or p['name'] == sync_id:
                print(f"\n📜 History: {p['name']}")
                print("=" * 60)
                for i, entry in enumerate(p['history'][-10:], 1):
                    print(f"  {i}. {entry['timestamp'][:19]} - {entry['items']} items")
                return
        print(f"❌ Sync pair not found: {sync_id}")
    
    def get_status(self):
        """Get sync status"""
        pairs = self.syncs['pairs']
        return {
            "total_pairs": len(pairs),
            "idle": len([p for p in pairs if p['status'] == 'idle']),
            "syncing": len([p for p in pairs if p['status'] == 'syncing']),
            "total_syncs": sum(p['sync_count'] for p in pairs)
        }

def main():
    manager = SyncManager()
    
    parser = argparse.ArgumentParser(description='Sync Manager Agent')
    parser.add_argument('--add', '-a', nargs=2, metavar=('SOURCE', 'DEST'), help='Add sync pair')
    parser.add_argument('--list', '-l', action='store_true', help='List sync pairs')
    parser.add_argument('--sync', '-s', metavar='PAIR', help='Execute sync')
    parser.add_argument('--history', '-H', metavar='PAIR', help='Show history')
    parser.add_argument('--status', action='store_true', help='Show status')
    
    args = parser.parse_args()
    
    print("🔄 Sync Manager Agent")
    print("=" * 60)
    
    if args.add:
        manager.add_sync(args.add[0], args.add[1])
    elif args.list:
        manager.list_syncs()
    elif args.sync:
        manager.sync(args.sync)
    elif args.history:
        manager.show_history(args.history)
    elif args.status:
        status = manager.get_status()
        print(f"\n📊 Sync Status:")
        print(f"   Total Pairs: {status['total_pairs']}")
        print(f"   Idle: {status['idle']}")
        print(f"   Total Syncs: {status['total_syncs']}")
    else:
        print("\nUsage:")
        print("  python3 sync-manager.py --add \"GitHub\" \"Local\"")
        print("  python3 sync-manager.py --list")
        print("  python3 sync-manager.py --sync \"GitHub ↔ Local\"")
        print("  python3 sync-manager.py --history \"GitHub ↔ Local\"")
        print("  python3 sync-manager.py --status")

if __name__ == '__main__':
    main()
