#!/usr/bin/env python3
"""
Security Auditor Agent
Monitors system security and compliance

Usage:
    python3 security-auditor.py --audit
    python3 security-auditor.py --check keys
    python3 security-auditor.py --report
"""

import json
import argparse
from datetime import datetime
from pathlib import Path

class SecurityAuditor:
    def __init__(self):
        self.workspace = Path('/home/ubuntu/.openclaw/workspace')
        self.output_dir = self.workspace / 'agents/super-swarm/security-analytics/security-auditor/output'
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def run_audit(self):
        """Complete security audit"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'checks': {}
        }
        
        # Check for exposed secrets
        results['checks']['secrets'] = self._check_secrets()
        
        # Check file permissions
        results['checks']['permissions'] = self._check_permissions()
        
        # Check dependency security
        results['checks']['dependencies'] = self._check_dependencies()
        
        # Generate summary
        results['summary'] = self._summarize(results['checks'])
        
        # Save report
        output_file = self.output_dir / f'security-audit-{datetime.now().strftime("%Y%m%d")}.json'
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"✅ Audit complete: {output_file}")
        return results
    
    def _check_secrets(self):
        """Check for exposed secrets in code"""
        findings = []
        secret_patterns = ['ghp_', 'sk_live', 'api_key', 'password', 'secret']
        
        for py_file in self.workspace.rglob('*.py'):
            with open(py_file, 'r') as f:
                content = f.read()
                for pattern in secret_patterns:
                    if pattern in content:
                        findings.append({
                            'file': str(py_file),
                            'pattern': pattern,
                            'severity': 'critical'
                        })
        
        return {'status': 'warning' if findings else 'clean', 'findings': findings}
    
    def _check_permissions(self):
        """Check file permissions"""
        issues = []
        for py_file in self.workspace.rglob('*.py'):
            stat = py_file.stat()
            if stat.st_mode & 0o077:  # Group/other has access
                issues.append({'file': str(py_file), 'issue': 'World-readable'})
        
        return {'status': 'warning' if issues else 'clean', 'issues': issues}
    
    def _check_dependencies(self):
        """Check dependency security"""
        return {'status': 'unknown', 'note': 'Implement npm/pip audit'}
    
    def _summarize(self, checks):
        """Generate summary"""
        critical = len(checks.get('secrets', {}).get('findings', []))
        warnings = len(checks.get('permissions', {}).get('issues', []))
        
        return {
            'critical': critical,
            'warnings': warnings,
            'overall': 'FAIL' if critical > 0 else ('WARNING' if warnings > 0 else 'PASS')
        }
    
    def check_keys(self):
        """Check for compromised API keys"""
        print("\n🔐 API Key Check:")
        print("  • Review .env files for exposed keys")
        print("  • Check git history for accidental commits")
        print("  • Use GitHub secret scanning")
        print("  • Rotate any potentially exposed keys")

def main():
    auditor = SecurityAuditor()
    
    parser = argparse.ArgumentParser(description='Security Auditor Agent')
    parser.add_argument('--audit', '-a', action='store_true', help='Run full audit')
    parser.add_argument('--check', '-c', choices=['keys'], help='Specific check')
    parser.add_argument('--report', '-r', action='store_true', help='Generate report')
    
    args = parser.parse_args()
    
    print("🔐 Security Auditor Agent")
    print("=" * 50)
    
    if args.audit:
        auditor.run_audit()
    elif args.check == 'keys':
        auditor.check_keys()
    else:
        print("\nUsage:")
        print("  python3 security-auditor.py --audit")
        print("  python3 security-auditor.py --check keys")
        print("  python3 security-auditor.py --report")

if __name__ == '__main__':
    main()
