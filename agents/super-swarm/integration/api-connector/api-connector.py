#!/usr/bin/env python3
"""
API Connector Agent
Connects to external APIs and manages integrations

Usage:
    python3 api-connector.py --connect "API Name" --url "https://api.example.com"
    python3 api-connector.py --list
    python3 api-connector.py --test "API Name"
    python3 api-connector.py --status
"""

import json
import argparse
import requests
from datetime import datetime
from pathlib import Path

class APIConnector:
    def __init__(self):
        self.workspace = Path('/home/ubuntu/.openclaw/workspace')
        self.connections_file = self.workspace / 'agents/super-swarm/integration/api-connector/connections.json'
        self.output_dir = self.workspace / 'agents/super-swarm/integration/api-connector/output'
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.connections = self._load_connections()
    
    def _load_connections(self):
        """Load existing connections"""
        if self.connections_file.exists():
            with open(self.connections_file, 'r') as f:
                return json.load(f)
        return {"apis": []}
    
    def _save_connections(self):
        """Save connections"""
        with open(self.connections_file, 'w') as f:
            json.dump(self.connections, f, indent=2)
    
    def connect(self, name, url, api_key=None, auth_type='none'):
        """Add new API connection"""
        connection = {
            "id": len(self.connections['apis']) + 1,
            "name": name,
            "url": url,
            "api_key": api_key,
            "auth_type": auth_type,
            "status": "connected",
            "last_check": datetime.now().isoformat(),
            "created": datetime.now().isoformat()
        }
        
        self.connections['apis'].append(connection)
        self._save_connections()
        print(f"✅ API connected: {name}")
        return connection
    
    def list_connections(self):
        """List all API connections"""
        apis = self.connections['apis']
        if not apis:
            print("\n🔗 No API connections")
            return
        
        print(f"\n🔗 API Connections ({len(apis)} total)")
        print("=" * 60)
        for api in apis:
            status = "✅" if api['status'] == 'connected' else "❌"
            print(f"{status} {api['name']} - {api['url'][:50]}...")
    
    def test_connection(self, name):
        """Test API connection"""
        for api in self.connections['apis']:
            if api['name'] == name:
                print(f"🔍 Testing: {name}")
                try:
                    response = requests.get(api['url'], timeout=5)
                    if response.status_code == 200:
                        api['status'] = 'connected'
                        api['last_check'] = datetime.now().isoformat()
                        self._save_connections()
                        print(f"✅ Connection successful: {name}")
                    else:
                        print(f"❌ Connection failed: {response.status_code}")
                except Exception as e:
                    api['status'] = 'error'
                    print(f"❌ Connection error: {str(e)[:50]}")
                return
        print(f"❌ API not found: {name}")
    
    def get_status(self):
        """Get connector status"""
        apis = self.connections['apis']
        return {
            "total_apis": len(apis),
            "connected": len([a for a in apis if a['status'] == 'connected']),
            "errors": len([a for a in apis if a['status'] == 'error'])
        }

def main():
    connector = APIConnector()
    
    parser = argparse.ArgumentParser(description='API Connector Agent')
    parser.add_argument('--connect', '-c', nargs=2, metavar=('NAME', 'URL'), help='Add API connection')
    parser.add_argument('--list', '-l', action='store_true', help='List connections')
    parser.add_argument('--test', '-t', metavar='NAME', help='Test connection')
    parser.add_argument('--status', '-s', action='store_true', help='Show status')
    
    args = parser.parse_args()
    
    print("🔗 API Connector Agent")
    print("=" * 60)
    
    if args.connect:
        connector.connect(args.connect[0], args.connect[1])
    elif args.list:
        connector.list_connections()
    elif args.test:
        connector.test_connection(args.test)
    elif args.status:
        status = connector.get_status()
        print(f"\n📊 API Status:")
        print(f"   Total APIs: {status['total_apis']}")
        print(f"   Connected: {status['connected']}")
        print(f"   Errors: {status['errors']}")
    else:
        print("\nUsage:")
        print("  python3 api-connector.py --connect \"Weather\" \"https://api.weather.com\"")
        print("  python3 api-connector.py --list")
        print("  python3 api-connector.py --test \"Weather\"")
        print("  python3 api-connector.py --status")

if __name__ == '__main__':
    main()
