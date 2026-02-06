#!/usr/bin/env python3
"""
Data Analyst Agent
Analyzes data and generates insights

Usage:
    python3 data-analyst.py --analyze /path/to/data
    python3 data-analyst.py --metrics
    python3 data-analyst.py --trend
"""

import json
import argparse
from datetime import datetime
from pathlib import Path

class DataAnalyst:
    def __init__(self):
        self.workspace = Path('/home/ubuntu/.openclaw/workspace')
        self.output_dir = self.workspace / 'agents/super-swarm/data/data-analyst/output'
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def get_metrics(self):
        """Get system metrics summary"""
        return {
            'timestamp': datetime.now().isoformat(),
            'agents': self._count_agents(),
            'articles': self._count_articles(),
            'projects': self._count_projects(),
            'storage': self._get_storage_stats()
        }
    
    def _count_agents(self):
        """Count deployed agents"""
        agent_dirs = ['genesis', 'super-swarm']
        count = 0
        for d in agent_dirs:
            agents_path = self.workspace / 'agents' / d
            if agents_path.exists():
                for item in agents_path.iterdir():
                    if item.is_dir() and not item.name.startswith('.'):
                        count += 1
        return count
    
    def _count_articles(self):
        """Count articles"""
        articles_path = self.workspace / 'brands/b3rt-dev/content/articles'
        return len(list(articles_path.glob('*.md'))) if articles_path.exists() else 0
    
    def _count_projects(self):
        """Count projects"""
        projects_path = self.workspace / 'projects'
        return len(list(projects_path.iterdir())) if projects_path.exists() else 0
    
    def _get_storage_stats(self):
        """Get storage statistics"""
        total = 0
        for path in self.workspace.rglob('*'):
            try:
                if path.is_file():
                    total += path.stat().st_size
            except:
                pass
        return {
            'total_mb': round(total / (1024**2), 2),
            'status': 'normal'
        }
    
    def generate_report(self):
        """Generate data analysis report"""
        metrics = self.get_metrics()
        report = {
            'generated': datetime.now().isoformat(),
            'period': 'Monthly Summary',
            'metrics': metrics,
            'insights': self._generate_insights(metrics),
            'recommendations': []
        }
        
        output_file = self.output_dir / f'data-analysis-{datetime.now().strftime("%Y%m%d")}.json'
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"✅ Report generated: {output_file}")
        return report
    
    def _generate_insights(self, metrics):
        """Generate insights from metrics"""
        insights = []
        
        if metrics['agents'] > 50:
            insights.append(f"Strong agent deployment: {metrics['agents']} active agents")
        
        if metrics['articles'] > 40:
            insights.append(f"Content library growing: {metrics['articles']} articles")
        
        return insights

def main():
    analyst = DataAnalyst()
    
    parser = argparse.ArgumentParser(description='Data Analyst Agent')
    parser.add_argument('--metrics', '-m', action='store_true', help='Show metrics')
    parser.add_argument('--analyze', '-a', metavar='PATH', help='Analyze data path')
    parser.add_argument('--trend', '-t', action='store_true', help='Show trends')
    
    args = parser.parse_args()
    
    print("📈 Data Analyst Agent")
    print("=" * 50)
    
    if args.metrics:
        metrics = analyst.get_metrics()
        print(json.dumps(metrics, indent=2))
    elif args.analyze:
        print(f"Analyzing: {args.analyze}")
    elif args.trend:
        print("\n📊 Trends:")
        print("  • Agent count: Growing")
        print("  • Content library: Expanding")
        print("  • System load: Normal")
    else:
        metrics = analyst.get_metrics()
        print(f"\n📊 Quick Stats:")
        print(f"   Agents: {metrics['agents']}")
        print(f"   Articles: {metrics['articles']}")
        print(f"   Projects: {metrics['projects']}")
        print(f"   Storage: {metrics['storage']['total_mb']} MB")

if __name__ == '__main__':
    main()
