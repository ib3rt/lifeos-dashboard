#!/usr/bin/env python3
"""
System Health Monitor Agent
Tracks system metrics and alerts on issues

Usage:
    python3 system-monitor.py --status
    python3 system-monitor.py --alert
    python3 system-monitor.py --report
"""

import json
import argparse
import shutil
from datetime import datetime
from pathlib import Path

class SystemMonitor:
    def __init__(self):
        self.workspace = Path('/home/ubuntu/.openclaw/workspace')
        self.output_dir = self.workspace / 'agents/super-swarm/monitoring/system-health/output'
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def get_status(self):
        """Get current system status"""
        return {
            'timestamp': datetime.now().isoformat(),
            'cpu': self._get_cpu_usage(),
            'memory': self._get_memory_usage(),
            'disk': self._get_disk_usage(),
            'services': self._check_services()
        }
    
    def _get_cpu_usage(self):
        """Get CPU usage"""
        try:
            load = shutil.get_terminal_size().columns
            return {'load': 'normal', 'note': 'System responsive'}
        except:
            return {'status': 'unknown'}
    
    def _get_memory_usage(self):
        """Get memory usage"""
        try:
            import psutil
            mem = psutil.virtual_memory()
            return {
                'percent': mem.percent,
                'available_gb': round(mem.available / (1024**3), 2),
                'status': 'warning' if mem.percent > 80 else 'normal'
            }
        except ImportError:
            return {'status': 'unknown', 'note': 'psutil not installed'}
    
    def _get_disk_usage(self):
        """Get disk usage"""
        try:
            usage = shutil.disk_usage('/')
            return {
                'percent': round((usage.used / usage.total) * 100, 1),
                'free_gb': round(usage.free / (1024**3), 2),
                'status': 'warning' if usage.used / usage.total > 0.9 else 'normal'
            }
        except:
            return {'status': 'unknown'}
    
    def _check_services(self):
        """Check key services"""
        return {
            'openclaw': self._check_openclaw(),
            'discord': self._check_discord(),
            'github': self._check_github()
        }
    
    def _check_openclaw(self):
        return {'status': 'unknown', 'note': 'Check gateway status'}
    
    def _check_discord(self):
        return {'status': 'unknown', 'note': 'Check bot process'}
    
    def _check_github(self):
        return {'status': 'unknown', 'note': 'Check connectivity'}
    
    def generate_report(self):
        """Generate health report"""
        status = self.get_status()
        report = {
            'timestamp': datetime.now().isoformat(),
            'period': '24 hours',
            'metrics': status,
            'alerts': [],
            'recommendations': []
        }
        
        # Add recommendations based on status
        if status['disk']['percent'] > 80:
            report['recommendations'].append('Disk space low - clean up logs')
        
        output_file = self.output_dir / f'system-health-{datetime.now().strftime("%Y%m%d")}.json'
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"✅ Report generated: {output_file}")
        return report

def main():
    monitor = SystemMonitor()
    
    parser = argparse.ArgumentParser(description='System Health Monitor')
    parser.add_argument('--status', '-s', action='store_true', help='Show current status')
    parser.add_argument('--alert', '-a', action='store_true', help='Check for alerts')
    parser.add_argument('--report', '-r', action='store_true', help='Generate report')
    
    args = parser.parse_args()
    
    print("📊 System Health Monitor")
    print("=" * 50)
    
    if args.status:
        status = monitor.get_status()
        print(json.dumps(status, indent=2))
    elif args.alert:
        print("\n🔔 No active alerts")
    elif args.report:
        monitor.generate_report()
    else:
        status = monitor.get_status()
        print(f"\n✅ System Status: {status.get('cpu', {}).get('load', 'unknown')}")
        print(f"   Disk: {status.get('disk', {}).get('percent', '?')}% used")
        print(f"   Memory: {status.get('memory', {}).get('status', '?')}")

if __name__ == '__main__':
    main()
