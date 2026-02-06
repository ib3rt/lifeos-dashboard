#!/usr/bin/env python3
"""
Code Review Agent
Automated code quality and security analysis

Usage:
    python3 code-review-agent.py --path /path/to/code
    python3 code-review-agent.py --git-diff
    python3 code-review-agent.py --check security
"""

import json
import argparse
import subprocess
from datetime import datetime
from pathlib import Path

class CodeReviewAgent:
    def __init__(self):
        self.workspace = Path('/home/ubuntu/.openclaw/workspace')
        self.output_dir = self.workspace / 'agents/super-swarm/developer/code-reviewer/output'
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def review_code(self, code_path, checks=None):
        """Review code for quality and security"""
        if checks is None:
            checks = ['security', 'style', 'performance', 'bugs']
        
        path = Path(code_path)
        findings = []
        
        # Check if path exists
        if not path.exists():
            return {"error": f"Path does not exist: {code_path}"}
        
        # Run security checks
        if 'security' in checks:
            findings.extend(self._check_security(path))
        
        # Run style checks  
        if 'style' in checks:
            findings.extend(self._check_style(path))
        
        # Run performance checks
        if 'performance' in checks:
            findings.extend(self._check_performance(path))
        
        # Generate report
        report = self._generate_report(path, findings, checks)
        
        output_file = self.output_dir / f'code-review-{datetime.now().strftime("%Y%m%d-%H%M%S")}.json'
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"✅ Review complete: {output_file}")
        return report
    
    def _check_security(self, path):
        """Security-focused checks"""
        findings = []
        
        # Check for secrets
        secret_patterns = ['api_key', 'password', 'secret', 'token']
        
        if path.is_file():
            if path.suffix in ['.py', '.js', '.ts', '.json']:
                with open(path, 'r') as f:
                    content = f.read()
                    for pattern in secret_patterns:
                        if pattern in content.lower():
                            findings.append({
                                'type': 'security',
                                'severity': 'high',
                                'message': f'Potential secret found: {pattern}',
                                'file': str(path)
                            })
        
        return findings
    
    def _check_style(self, path):
        """Code style checks"""
        findings = []
        
        if path.is_file() and path.suffix == '.py':
            with open(path, 'r') as f:
                content = f.read()
                
            # Check line length
            for i, line in enumerate(content.split('\n'), 1):
                if len(line) > 120:
                    findings.append({
                        'type': 'style',
                        'severity': 'low',
                        'message': f'Line exceeds 120 characters',
                        'line': i,
                        'file': str(path)
                    })
        
        return findings
    
    def _check_performance(self, path):
        """Performance checks"""
        findings = []
        
        # Placeholder for actual performance analysis
        findings.append({
            'type': 'performance',
            'severity': 'info',
            'message': 'Performance checks placeholder - implement specific rules',
            'file': str(path)
        })
        
        return findings
    
    def _generate_report(self, path, findings, checks):
        """Generate review report"""
        high = len([f for f in findings if f.get('severity') == 'high'])
        medium = len([f for f in findings if f.get('severity') == 'medium'])
        low = len([f for f in findings if f.get('severity') == 'low'])
        
        return {
            'path': str(path),
            'timestamp': datetime.now().isoformat(),
            'checks_performed': checks,
            'summary': {
                'total': len(findings),
                'high': high,
                'medium': medium,
                'low': low
            },
            'findings': findings,
            'recommendation': 'Critical issues found - review required' if high > 0 else 'No critical issues'
        }
    
    def get_git_diff(self):
        """Review staged changes"""
        try:
            result = subprocess.run(['git', 'diff', '--staged', '--name-only'], 
                                  capture_output=True, text=True)
            files = result.stdout.strip().split('\n') if result.stdout.strip() else []
            return {'staged_files': files}
        except Exception as e:
            return {'error': str(e)}

def main():
    agent = CodeReviewAgent()
    
    parser = argparse.ArgumentParser(description='Code Review Agent')
    parser.add_argument('--path', '-p', help='Path to code to review')
    parser.add_argument('--git-diff', '-g', action='store_true', help='Review staged changes')
    parser.add_argument('--check', '-c', action='append', choices=['security', 'style', 'performance'],
                       help='Specific checks to run')
    
    args = parser.parse_args()
    
    print("🔍 Code Review Agent")
    print("=" * 50)
    
    if args.git_diff:
        diff = agent.get_git_diff()
        print(f"\n📝 Staged files: {diff.get('staged_files', [])}")
    
    elif args.path:
        agent.review_code(args.path, args.check)
    
    else:
        print("\nUsage:")
        print("  python3 code-review-agent.py --path /path/to/code")
        print("  python3 code-review-agent.py --path /path/to/code --check security --check style")
        print("  python3 code-review-agent.py --git-diff")

if __name__ == '__main__':
    main()
