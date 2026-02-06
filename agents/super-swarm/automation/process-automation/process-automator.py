#!/usr/bin/env python3
"""
Process Automation Agent
Automates business processes and workflows

Usage:
    python3 process-automator.py --create "Process Name"
    python3 process-automator.py --run "Process Name"
    python3 process-automator.py --list
    python3 process-automator.py --status
"""

import json
import argparse
from datetime import datetime
from pathlib import Path

class ProcessAutomator:
    def __init__(self):
        self.workspace = Path('/home/ubuntu/.openclaw/workspace')
        self.processes_dir = self.workspace / 'agents/super-swarm/automation/process-automation'
        self.output_dir = self.workspace / 'agents/super-swarm/automation/process-automation/output'
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.processes = self._load_processes()
    
    def _load_processes(self):
        """Load processes"""
        processes_file = self.processes_dir / 'processes.json'
        if processes_file.exists():
            with open(processes_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_processes(self):
        """Save processes"""
        processes_file = self.processes_dir / 'processes.json'
        with open(processes_file, 'w') as f:
            json.dump(self.processes, f, indent=2)
    
    def create_process(self, name, steps=None):
        """Create business process"""
        if steps is None:
            steps = [
                {"name": "Start", "type": "manual", "description": "Initiate process"},
                {"name": "Validate", "type": "automated", "action": "validate_inputs"},
                {"name": "Process", "type": "automated", "action": "execute_main_task"},
                {"name": "Notify", "type": "automated", "action": "send_notification"},
                {"name": "Complete", "type": "manual", "description": "Review and complete"}
            ]
        
        process_id = name.lower().replace(' ', '-')
        self.processes[process_id] = {
            "id": process_id,
            "name": name,
            "steps": steps,
            "status": "ready",
            "created": datetime.now().isoformat(),
            "last_run": None,
            "run_count": 0
        }
        
        self._save_processes()
        print(f"✅ Process created: {name}")
        return self.processes[process_id]
    
    def list_processes(self):
        """List all processes"""
        if not self.processes:
            print("\n🔄 No processes configured")
            return
        
        print(f"\n🔄 Business Processes ({len(self.processes)} total)")
        print("=" * 60)
        for p_id, p in self.processes.items():
            status = {"ready": "🟢", "running": "🟡", "completed": "🔵", "failed": "🔴"}.get(p['status'], "⚪")
            print(f"{status} {p['name']} - {p['run_count']} runs")
    
    def run_process(self, process_id):
        """Execute a business process"""
        if process_id not in self.processes:
            print(f"❌ Process not found: {process_id}")
            return
        
        p = self.processes[process_id]
        print(f"\n🔄 Running process: {p['name']}")
        print("=" * 60)
        
        for i, step in enumerate(p['steps'], 1):
            step_type = step.get('type', 'manual')
            step_icon = "🤖" if step_type == 'automated' else "👤"
            print(f"  {step_icon} [{i}/{len(p['steps'])}] {step['name']}")
        
        p['last_run'] = datetime.now().isoformat()
        p['run_count'] += 1
        p['status'] = 'completed'
        self._save_processes()
        
        print(f"\n✅ Process completed: {p['name']}")
    
    def get_status(self):
        """Get automation status"""
        return {
            "total_processes": len(self.processes),
            "ready_processes": len([p for p in self.processes.values() if p['status'] == 'ready']),
            "total_runs": sum(p['run_count'] for p in self.processes.values())
        }

def main():
    automator = ProcessAutomator()
    
    parser = argparse.ArgumentParser(description='Process Automation Agent')
    parser.add_argument('--create', '-c', metavar='NAME', help='Create new process')
    parser.add_argument('--list', '-l', action='store_true', help='List processes')
    parser.add_argument('--run', '-r', metavar='ID', help='Run process')
    parser.add_argument('--status', '-s', action='store_true', help='Show status')
    
    args = parser.parse_args()
    
    print("🔄 Process Automation Agent")
    print("=" * 60)
    
    if args.create:
        automator.create_process(args.create)
    elif args.list:
        automator.list_processes()
    elif args.run:
        automator.run_process(args.run)
    elif args.status:
        status = automator.get_status()
        print(f"\n📊 Process Status:")
        print(f"   Total Processes: {status['total_processes']}")
        print(f"   Ready: {status['ready_processes']}")
        print(f"   Total Runs: {status['total_runs']}")
    else:
        print("\nUsage:")
        print("  python3 process-automator.py --create \"Onboarding\"")
        print("  python3 process-automator.py --list")
        print("  python3 process-automator.py --run \"onboarding\"")
        print("  python3 process-automator.py --status")

if __name__ == '__main__':
    main()
