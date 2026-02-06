#!/usr/bin/env python3
"""
Risk Matrix - Automated Risk Assessment and Tracking

Usage:
    python risk_matrix.py --add "Risk Name" --probability high --impact medium
    python risk_matrix.py --report
    python risk_matrix.py --heatmap
"""

import argparse
import json
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime

class Probability(Enum):
    VERY_LOW = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    VERY_HIGH = 5

class Impact(Enum):
    MINOR = 1
    MODERATE = 2
    SIGNIFICANT = 3
    MAJOR = 4
    CRITICAL = 5

class Status(Enum):
    ACTIVE = "active"
    MITIGATED = "mitigated"
    CLOSED = "closed"
    ACCEPTED = "accepted"

@dataclass
class Risk:
    id: str
    title: str
    description: str
    probability: Probability
    impact: Impact
    mitigation: str
    owner: str
    status: Status = Status.ACTIVE
    created_date: str = ""
    updated_date: str = ""
    
    @property
    def score(self) -> int:
        return self.probability.value * self.impact.value
    
    @property
    def priority(self) -> str:
        s = self.score
        if s >= 16:
            return "CRITICAL"
        elif s >= 12:
            return "HIGH"
        elif s >= 8:
            return "MEDIUM"
        return "LOW"

@dataclass
class RiskThreshold:
    critical: int = 16
    high: int = 12
    medium: int = 8


class RiskMatrix:
    def __init__(self, thresholds: RiskThreshold = None):
        self.risks: List[Risk] = []
        self.thresholds = thresholds or RiskThreshold()
        self.id_counter = 1
    
    def add_risk(self, risk: Risk):
        if not risk.id:
            risk.id = f"R{self.id_counter:03d}"
            self.id_counter += 1
        if not risk.created_date:
            risk.created_date = datetime.now().isoformat()
        risk.updated_date = datetime.now().isoformat()
        self.risks.append(risk)
    
    def update_risk(self, risk_id: str, **kwargs):
        for risk in self.risks:
            if risk.id == risk_id:
                for key, value in kwargs.items():
                    setattr(risk, key, value)
                risk.updated_date = datetime.now().isoformat()
                return True
        return False
    
    def get_risk(self, risk_id: str) -> Optional[Risk]:
        for risk in self.risks:
            if risk.id == risk_id:
                return risk
        return None
    
    def get_by_priority(self, priority: str) -> List[Risk]:
        return sorted([r for r in self.risks if r.priority == priority],
                      key=lambda r: r.score, reverse=True)
    
    def get_top_risks(self, n: int = 5) -> List[Risk]:
        return sorted(self.risks, key=lambda r: r.score, reverse=True)[:n]
    
    def get_critical_risks(self) -> List[Risk]:
        return self.get_by_priority("CRITICAL")
    
    def get_high_risks(self) -> List[Risk]:
        return self.get_by_priority("HIGH")
    
    def risk_breakdown(self) -> Dict:
        return {
            "CRITICAL": len([r for r in self.risks if r.priority == "CRITICAL"]),
            "HIGH": len([r for r in self.risks if r.priority == "HIGH"]),
            "MEDIUM": len([r for r in self.risks if r.priority == "MEDIUM"]),
            "LOW": len([r for r in self.risks if r.priority == "LOW"]),
            "ACTIVE": len([r for r in self.risks if r.status.value == "active"]),
            "MITIGATED": len([r for r in self.risks if r.status.value == "mitigated"]),
            "CLOSED": len([r for r in self.risks if r.status.value == "closed"])
        }
    
    def generate_heatmap_data(self) -> str:
        """Generate ASCII heatmap"""
        heatmap = """
         IMPACT
         1    2    3    4    5
       ┌────┬────┬────┬────┬────┐
   5   │  L  │  M  │  M  │  H  │  C  │ ← P
       ├────┼────┼────┼────┼────┤     R
   4   │  L  │  L  │  M  │  H  │  C  │     O
       ├────┼────┼────┼────┼────┤     B
   3   │  L  │  L  │  M  │  M  │  H  │     A
       ├────┼────┼────┼────┼────┤     B
   2   │  L  │  L  │  L  │  M  │  M  │     I
       ├────┼────┼────┼────┼────┤     L
   1   │  L  │  L  │  L  │  L  │  M  │     I
       └────┴────┴────┴────┴────┘     T
         1    2    3    4    5   Y
              Probability
              
L = Low Risk    M = Medium Risk    H = High Risk    C = Critical
"""
        
        # Add risk counts
        breakdown = self.risk_breakdown()
        heatmap += f"\nRisk Distribution:\n"
        heatmap += f"  Critical: {breakdown['CRITICAL']}\n"
        heatmap += f"  High: {breakdown['HIGH']}\n"
        heatmap += f"  Medium: {breakdown['MEDIUM']}\n"
        heatmap += f"  Low: {breakdown['LOW']}\n"
        
        return heatmap
    
    def generate_report(self, format: str = "markdown") -> str:
        if format == "json":
            return json.dumps({
                "risks": [
                    {
                        "id": r.id,
                        "title": r.title,
                        "score": r.score,
                        "priority": r.priority,
                        "status": r.status.value
                    }
                    for r in self.risks
                ],
                "breakdown": self.risk_breakdown(),
                "critical_count": len(self.get_critical_risks())
            }, indent=2)
        
        # Markdown format
        report = f"""# Risk Assessment Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Risk Heatmap

{self.generate_heatmap_data()}

## Risk Summary

| Priority | Count |
|----------|-------|
| 🔴 CRITICAL | {self.risk_breakdown()['CRITICAL']} |
| 🟠 HIGH | {self.risk_breakdown()['HIGH']} |
| 🟡 MEDIUM | {self.risk_breakdown()['MEDIUM']} |
| 🟢 LOW | {self.risk_breakdown()['LOW']} |

## Critical Risks (Requiring Immediate Attention)

"""
        critical = self.get_critical_risks()
        if critical:
            for r in critical:
                report += f"""### {r.id}: {r.title}
- **Score:** {r.score} (CRITICAL)
- **Probability:** {r.probability.name}
- **Impact:** {r.impact.name}
- **Mitigation:** {r.mitigation}
- **Owner:** {r.owner}
- **Status:** {r.status.value}

"""
        else:
            report += "No critical risks identified.\n\n"
        
        report += """## All Active Risks

| ID | Risk | Score | Priority | Prob | Impact | Owner | Status |
|----|------|-------|----------|------|--------|-------|--------|
"""
        for r in sorted(self.risks, key=lambda x: x.score, reverse=True):
            if r.status.value != "closed":
                emoji = "🔴" if r.priority == "CRITICAL" else ("🟠" if r.priority == "HIGH" else ("🟡" if r.priority == "MEDIUM" else "🟢"))
                report += f"| {r.id} | {r.title[:30]} | {r.score} | {emoji} {r.priority} | {r.probability.name} | {r.impact.name} | {r.owner} | {r.status.value} |\n"
        
        report += """
---

*Generated by Risk Matrix*
"""
        return report


def risk_from_args(args) -> Risk:
    prob_map = {
        'very_low': Probability.VERY_LOW,
        'low': Probability.LOW,
        'medium': Probability.MEDIUM,
        'high': Probability.HIGH,
        'very_high': Probability.VERY_HIGH
    }
    impact_map = {
        'minor': Impact.MINOR,
        'moderate': Impact.MODERATE,
        'significant': Impact.SIGNIFICANT,
        'major': Impact.MAJOR,
        'critical': Impact.CRITICAL
    }
    return Risk(
        id="",
        title=args.title,
        description=args.description,
        probability=prob_map.get(args.probability, Probability.MEDIUM),
        impact=impact_map.get(args.impact, Impact.MODERATE),
        mitigation=args.mitigation,
        owner=args.owner,
        status=Status(args.status) if args.status else Status.ACTIVE
    )


def main():
    parser = argparse.ArgumentParser(description='Risk Matrix Management')
    parser.add_argument('--add', dest='title', help='Add a new risk')
    parser.add_argument('--description', help='Risk description')
    parser.add_argument('--probability', '-p', choices=['very_low', 'low', 'medium', 'high', 'very_high'],
                       default='medium', help='Probability level')
    parser.add_argument('--impact', '-i', choices=['minor', 'moderate', 'significant', 'major', 'critical'],
                       default='moderate', help='Impact level')
    parser.add_argument('--mitigation', '-m', help='Mitigation strategy')
    parser.add_argument('--owner', '-o', default='Unassigned', help='Risk owner')
    parser.add_argument('--status', choices=['active', 'mitigated', 'closed', 'accepted'],
                       help='Risk status')
    parser.add_argument('--report', '-r', action='store_true', help='Generate report')
    parser.add_argument('--heatmap', action='store_true', help='Show risk heatmap')
    parser.add_argument('--json', '-j', action='store_true', help='Output as JSON')
    parser.add_argument('--output', type=str, help='Output file')
    
    args = parser.parse_args()
    
    # Initialize risk matrix (in production, load from file/db)
    matrix = RiskMatrix()
    
    if args.add:
        risk = risk_from_args(args)
        matrix.add_risk(risk)
        print(f"Added risk: {risk.id} - {risk.title}")
    
    if args.report:
        if args.json:
            output = matrix.generate_report(format="json")
        else:
            output = matrix.generate_report()
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"Report saved to {args.output}")
        else:
            print(output)
    
    elif args.heatmap:
        print(matrix.generate_heatmap_data())


if __name__ == "__main__":
    main()
