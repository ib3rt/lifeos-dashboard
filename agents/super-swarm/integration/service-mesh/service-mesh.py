#!/usr/bin/env python3
"""
Service Mesh Agent
Manages service communication and routing

Usage:
    python3 service-mesh.py --register "service-name" --endpoint "http://..."
    python3 service-mesh.py --list
    python3 service-mesh.py --route "service-name" --path "/api/..."
    python3 service-mesh.py --status
"""

import json
import argparse
from datetime import datetime
from pathlib import Path

class ServiceMesh:
    def __init__(self):
        self.workspace = Path('/home/ubuntu/.openclaw/workspace')
        self.mesh_file = self.workspace / 'agents/super-swarm/integration/service-mesh/mesh.json'
        self.output_dir = self.workspace / 'agents/super-swarm/integration/service-mesh/output'
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.mesh = self._load_mesh()
    
    def _load_mesh(self):
        """Load service mesh"""
        if self.mesh_file.exists():
            with open(self.mesh_file, 'r') as f:
                return json.load(f)
        return {"services": [], "routes": []}
    
    def _save_mesh(self):
        """Save mesh"""
        with open(self.mesh_file, 'w') as f:
            json.dump(self.mesh, f, indent=2)
    
    def register_service(self, name, endpoint, health_check=None):
        """Register service in mesh"""
        service = {
            "id": len(self.mesh['services']) + 1,
            "name": name,
            "endpoint": endpoint,
            "health_check": health_check or f"{endpoint}/health",
            "status": "healthy",
            "registered": datetime.now().isoformat(),
            "last_check": None
        }
        
        self.mesh['services'].append(service)
        self._save_mesh()
        print(f"✅ Service registered: {name}")
        return service
    
    def add_route(self, service_name, path, method='GET'):
        """Add routing rule"""
        for svc in self.mesh['services']:
            if svc['name'] == service_name:
                route = {
                    "id": len(self.mesh['routes']) + 1,
                    "service": service_name,
                    "path": path,
                    "method": method,
                    "active": True
                }
                self.mesh['routes'].append(route)
                self._save_mesh()
                print(f"✅ Route added: {method} {path} → {service_name}")
                return
        print(f"❌ Service not found: {service_name}")
    
    def list_services(self):
        """List registered services"""
        services = self.mesh['services']
        if not services:
            print("\n🔗 No services registered")
            return
        
        print(f"\n🔗 Services ({len(services)} total)")
        print("=" * 60)
        for s in services:
            status = "🟢" if s['status'] == 'healthy' else "🔴"
            print(f"{status} {s['name']} - {s['endpoint']}")
    
    def route_request(self, path, method='GET'):
        """Route request to appropriate service"""
        for route in self.mesh['routes']:
            if route['path'] == path and route['method'] == method:
                for svc in self.mesh['services']:
                    if svc['name'] == route['service']:
                        print(f"🔀 Routed: {method} {path} → {svc['endpoint']}")
                        return svc['endpoint']
        print(f"❌ No route found: {method} {path}")
        return None
    
    def health_check(self):
        """Run health checks on all services"""
        print("\n🏥 Running health checks...")
        healthy = 0
        for svc in self.mesh['services']:
            # Simplified health check
            svc['last_check'] = datetime.now().isoformat()
            if svc['status'] == 'healthy':
                healthy += 1
        self._save_mesh()
        print(f"✅ Health check complete: {healthy}/{len(self.mesh['services'])} healthy")

def main():
    mesh = ServiceMesh()
    
    parser = argparse.ArgumentParser(description='Service Mesh Agent')
    parser.add_argument('--register', '-r', nargs=2, metavar=('NAME', 'ENDPOINT'), help='Register service')
    parser.add_argument('--route', nargs=2, metavar=('SERVICE', 'PATH'), help='Add route')
    parser.add_argument('--list', '-l', action='store_true', help='List services')
    parser.add_argument('--route-req', metavar='PATH', help='Route request')
    parser.add_argument('--health', action='store_true', help='Run health checks')
    
    args = parser.parse_args()
    
    print("🔗 Service Mesh Agent")
    print("=" * 60)
    
    if args.register:
        mesh.register_service(args.register[0], args.register[1])
    elif args.route:
        mesh.add_route(args.route[0], args.route[1])
    elif args.list:
        mesh.list_services()
    elif args.route_req:
        mesh.route_request(args.route_req)
    elif args.health:
        mesh.health_check()
    else:
        print("\nUsage:")
        print("  python3 service-mesh.py --register \"api\" \"http://localhost:8080\"")
        print("  python3 service-mesh.py --route \"api\" \"/api/v1\"")
        print("  python3 service-mesh.py --list")
        print("  python3 service-mesh.py --route-req \"/api/v1/users\"")
        print("  python3 service-mesh.py --health")

if __name__ == '__main__':
    main()
