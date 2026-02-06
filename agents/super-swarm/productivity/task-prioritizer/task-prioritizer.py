#!/usr/bin/env python3
"""
Task Prioritizer Agent
Organizes and prioritizes tasks based on impact and effort

Usage:
    python3 task-prioritizer.py --add "Task description"
    python3 task-prioritizer.py --list
    python3 task-prioritizer.py --prioritize
    python3 task-prioritizer.py --plan
"""

import json
import argparse
from datetime import datetime
from pathlib import Path

class TaskPrioritizer:
    def __init__(self):
        self.workspace = Path('/home/ubuntu/.openclaw/workspace')
        self.tasks_file = self.workspace / 'memory/tasks.json'
        self.output_dir = self.workspace / 'agents/super-swarm/productivity/task-prioritizer/output'
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Load existing tasks
        self.tasks = self._load_tasks()
    
    def _load_tasks(self):
        """Load tasks from file"""
        if self.tasks_file.exists():
            with open(self.tasks_file, 'r') as f:
                return json.load(f)
        return []
    
    def _save_tasks(self):
        """Save tasks to file"""
        with open(self.tasks_file, 'w') as f:
            json.dump(self.tasks, f, indent=2)
    
    def add_task(self, task, priority='medium', effort='medium'):
        """Add new task"""
        new_task = {
            'id': len(self.tasks) + 1,
            'task': task,
            'priority': priority,  # high, medium, low
            'effort': effort,  # high, medium, low
            'status': 'pending',
            'created': datetime.now().isoformat(),
            'tags': []
        }
        self.tasks.append(new_task)
        self._save_tasks()
        print(f"✅ Task added: {task}")
        return new_task
    
    def list_tasks(self):
        """List all tasks"""
        if not self.tasks:
            print("\n📋 No tasks found")
            return
        
        print(f"\n📋 Tasks ({len(self.tasks)} total)")
        print("-" * 60)
        for task in sorted(self.tasks, key=lambda x: self._priority_score(x)):
            status = "✅" if task['status'] == 'done' else "○"
            priority_emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}[task['priority']]
            print(f"{status} {priority_emoji} [{task['priority']:6}] {task['task'][:50]}")
    
    def _priority_score(self, task):
        """Calculate priority score"""
        priority_map = {'high': 3, 'medium': 2, 'low': 1}
        score = priority_map.get(task['priority'], 1)
        if task['status'] == 'done':
            score = 0
        return -score  # Descending order
    
    def prioritize(self):
        """Generate prioritized task list"""
        sorted_tasks = sorted(self.tasks, key=self._priority_score)
        
        print("\n🎯 Prioritized Tasks")
        print("=" * 60)
        
        for i, task in enumerate(sorted_tasks[:10], 1):
            if task['status'] == 'done':
                continue
            print(f"{i:2}. {task['task'][:55]}")
            print(f"    Priority: {task['priority']} | Effort: {task['effort']}")
        
        # Generate plan
        self._generate_plan(sorted_tasks)
    
    def _generate_plan(self, tasks):
        """Generate execution plan"""
        plan = {
            'generated': datetime.now().isoformat(),
            'today': [],
            'this_week': [],
            'backlog': []
        }
        
        for task in tasks:
            if task['status'] == 'done':
                continue
            
            entry = {'id': task['id'], 'task': task['task'], 'priority': task['priority']}
            
            if task['priority'] == 'high':
                plan['today'].append(entry)
            elif task['priority'] == 'medium':
                plan['this_week'].append(entry)
            else:
                plan['backlog'].append(entry)
        
        output_file = self.output_dir / f'task-plan-{datetime.now().strftime("%Y%m%d")}.json'
        with open(output_file, 'w') as f:
            json.dump(plan, f, indent=2)
        
        print(f"\n✅ Plan saved: {output_file}")
    
    def complete_task(self, task_id):
        """Mark task as complete"""
        for task in self.tasks:
            if task['id'] == task_id:
                task['status'] = 'done'
                task['completed'] = datetime.now().isoformat()
                self._save_tasks()
                print(f"✅ Task completed: {task['task']}")
                return
        print(f"❌ Task not found: {task_id}")

def main():
    prioritizer = TaskPrioritizer()
    
    parser = argparse.ArgumentParser(description='Task Prioritizer Agent')
    parser.add_argument('--add', '-a', metavar='TASK', help='Add new task')
    parser.add_argument('--list', '-l', action='store_true', help='List all tasks')
    parser.add_argument('--prioritize', '-p', action='store_true', help='Show prioritized list')
    parser.add_argument('--complete', '-c', type=int, help='Complete task by ID')
    
    args = parser.parse_args()
    
    print("🎯 Task Prioritizer Agent")
    print("=" * 50)
    
    if args.add:
        prioritizer.add_task(args.add)
    elif args.list:
        prioritizer.list_tasks()
    elif args.prioritize:
        prioritizer.prioritize()
    elif args.complete:
        prioritizer.complete_task(args.complete)
    else:
        print("\nUsage:")
        print("  python3 task-prioritizer.py --add \"Important task\"")
        print("  python3 task-prioritizer.py --list")
        print("  python3 task-prioritizer.py --prioritize")
        print("  python3 task-prioritizer.py --complete 1")

if __name__ == '__main__':
    main()
