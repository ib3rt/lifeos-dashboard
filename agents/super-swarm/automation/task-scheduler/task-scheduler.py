#!/usr/bin/env python3
"""
Task Scheduler Agent
Schedules and manages recurring tasks

Usage:
    python3 task-scheduler.py --add "task" --daily
    python3 task-scheduler.py --add "task" --weekly
    python3 task-scheduler.py --list
    python3 task-scheduler.py --run-now "task"
"""

import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path

class TaskScheduler:
    def __init__(self):
        self.workspace = Path('/home/ubuntu/.openclaw/workspace')
        self.schedule_file = self.workspace / 'agents/super-swarm/automation/task-scheduler/schedule.json'
        self.output_dir = self.workspace / 'agents/super-swarm/automation/task-scheduler/output'
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.schedule = self._load_schedule()
    
    def _load_schedule(self):
        """Load scheduled tasks"""
        if self.schedule_file.exists():
            with open(self.schedule_file, 'r') as f:
                return json.load(f)
        return {"tasks": []}
    
    def _save_schedule(self):
        """Save schedule"""
        with open(self.schedule_file, 'w') as f:
            json.dump(self.schedule, f, indent=2)
    
    def add_task(self, task, frequency='daily', time='06:00'):
        """Add task to schedule"""
        new_task = {
            "id": len(self.schedule['tasks']) + 1,
            "task": task,
            "frequency": frequency,  # daily, weekly, monthly
            "time": time,
            "enabled": True,
            "created": datetime.now().isoformat(),
            "last_run": None,
            "next_run": self._calculate_next_run(frequency, time)
        }
        
        self.schedule['tasks'].append(new_task)
        self._save_schedule()
        print(f"✅ Task scheduled: {task} ({frequency} at {time})")
        return new_task
    
    def _calculate_next_run(self, frequency, time):
        """Calculate next run time"""
        now = datetime.now()
        hour, minute = map(int, time.split(':'))
        
        next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        if frequency == 'weekly':
            next_run += timedelta(days=7)
        elif frequency == 'monthly':
            next_run += timedelta(days=30)
        else:  # daily
            if next_run <= now:
                next_run += timedelta(days=1)
        
        return next_run.isoformat()
    
    def list_tasks(self):
        """List scheduled tasks"""
        tasks = self.schedule['tasks']
        if not tasks:
            print("\n📅 No scheduled tasks")
            return
        
        print(f"\n📅 Scheduled Tasks ({len(tasks)} total)")
        print("=" * 60)
        for task in tasks:
            status = "✅" if task['enabled'] else "⏸️"
            freq = task['frequency'][:3].upper()
            print(f"{status} [{freq}] {task['task']} @ {task['time']}")
    
    def run_task(self, task_id):
        """Mark task as run"""
        for task in self.schedule['tasks']:
            if task['id'] == task_id:
                task['last_run'] = datetime.now().isoformat()
                task['next_run'] = self._calculate_next_run(task['frequency'], task['time'])
                self._save_schedule()
                print(f"✅ Task completed: {task['task']}")
                return
        print(f"❌ Task not found: {task_id}")

def main():
    scheduler = TaskScheduler()
    
    parser = argparse.ArgumentParser(description='Task Scheduler Agent')
    parser.add_argument('--add', '-a', metavar='TASK', help='Add task to schedule')
    parser.add_argument('--daily', action='store_true', help='Daily frequency')
    parser.add_argument('--weekly', action='store_true', help='Weekly frequency')
    parser.add_argument('--time', '-t', default='06:00', help='Time (HH:MM)')
    parser.add_argument('--list', '-l', action='store_true', help='List scheduled tasks')
    parser.add_argument('--run', '-r', type=int, help='Run task by ID')
    
    args = parser.parse_args()
    
    print("📅 Task Scheduler Agent")
    print("=" * 60)
    
    if args.add:
        freq = 'weekly' if args.weekly else 'daily'
        scheduler.add_task(args.add, freq, args.time)
    elif args.list:
        scheduler.list_tasks()
    elif args.run:
        scheduler.run_task(args.run)
    else:
        print("\nUsage:")
        print("  python3 task-scheduler.py --add \"Generate Report\" --daily")
        print("  python3 task-scheduler.py --add \"Backup Data\" --weekly --time 02:00")
        print("  python3 task-scheduler.py --list")
        print("  python3 task-scheduler.py --run 1")

if __name__ == '__main__':
    main()
