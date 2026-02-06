#!/usr/bin/env python3
"""
SWOT Analyzer - Automated SWOT Analysis Generator

Usage:
    python swot_analyzer.py --interactive
    python swot_analyzer.py --template
    python swot_analyzer.py --generate
"""

import argparse
import json
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class SWOTFactor:
    category: str  # S, W, O, T
    title: str
    description: str
    impact_score: float = 5.0  # 1-10
    evidence: List[str] = field(default_factory=list)
    trend: str = "stable"  # improving, stable, declining

class SWOTAnalyzer:
    def __init__(self):
        self.factors: Dict[str, List[SWOTFactor]] = {
            'S': [],  # Strengths
            'W': [],  # Weaknesses
            'O': [],  # Opportunities
            'T': []   # Threats
        }
    
    def add_factor(self, factor: SWOTFactor):
        self.factors[factor.category].append(factor)
    
    def get_strengths(self) -> List[SWOTFactor]:
        return sorted(self.factors['S'], key=lambda x: x.impact_score, reverse=True)
    
    def get_weaknesses(self) -> List[SWOTFactor]:
        return sorted(self.factors['W'], key=lambda x: x.impact_score, reverse=True)
    
    def get_opportunities(self) -> List[SWOTFactor]:
        return sorted(self.factors['O'], key=lambda x: x.impact_score, reverse=True)
    
    def get_threats(self) -> List[SWOTFactor]:
        return sorted(self.factors['T'], key=lambda x: x.impact_score, reverse=True)
    
    def generate_so_strategy(self) -> List[str]:
        """Strength-Opportunity: Leverage advantages"""
        strategies = []
        for s in self.get_strengths()[:2]:
            for o in self.get_opportunities()[:2]:
                strategies.append(
                    f"Leverage {s.title} to capture {o.title}"
                )
        return strategies[:5]
    
    def generate_wo_strategy(self) -> List[str]:
        """Weakness-Opportunity: Build capabilities"""
        strategies = []
        for w in self.get_weaknesses()[:2]:
            for o in self.get_opportunities()[:2]:
                strategies.append(
                    f"Develop {w.title} to enable {o.title}"
                )
        return strategies[:5]
    
    def generate_st_strategy(self) -> List[str]:
        """Strength-Threat: Defend position"""
        strategies = []
        for s in self.get_strengths()[:2]:
            for t in self.get_threats()[:2]:
                strategies.append(
                    f"Use {s.title} to counter {t.title}"
                )
        return strategies[:5]
    
    def generate_wt_strategy(self) -> List[str]:
        """Weakness-Threat: Mitigate risks"""
        strategies = []
        for w in self.get_weaknesses()[:2]:
            for t in self.get_threats()[:2]:
                strategies.append(
                    f"Address {w.title} to avoid {t.title}"
                )
        return strategies[:5]
    
    def generate_report(self, format: str = "markdown") -> str:
        if format == "json":
            return json.dumps({
                "strengths": [{"title": f.title, "description": f.description, "impact": f.impact_score} 
                             for f in self.get_strengths()],
                "weaknesses": [{"title": f.title, "description": f.description, "impact": f.impact_score} 
                              for f in self.get_weaknesses()],
                "opportunities": [{"title": f.title, "description": f.description, "impact": f.impact_score} 
                                for f in self.get_opportunities()],
                "threats": [{"title": f.title, "description": f.description, "impact": f.impact_score} 
                           for f in self.get_threats()],
                "strategies": {
                    "SO": self.generate_so_strategy(),
                    "WO": self.generate_wo_strategy(),
                    "ST": self.generate_st_strategy(),
                    "WT": self.generate_wt_strategy()
                }
            }, indent=2)
        
        # Markdown format
        report = f"""# SWOT Analysis Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## Strengths ({len(self.factors['S'])} items)

| # | Strength | Impact | Evidence |
|---|----------|--------|----------|
"""
        for i, f in enumerate(self.get_strengths(), 1):
            report += f"| {i} | **{f.title}** | {f.impact_score}/10 | {', '.join(f.evidence[:2])} |\n"
        
        report += """
## Weaknesses ({len(self.factors['W'])} items)

| # | Weakness | Impact | Trend |
|---|----------|--------|-------|
"""
        for i, f in enumerate(self.get_weaknesses(), 1):
            trend_emoji = "📈" if f.trend == "improving" else ("📉" if f.trend == "declining" else "➡️")
            report += f"| {i} | **{f.title}** | {f.impact_score}/10 | {trend_emoji} {f.trend} |\n"
        
        report += """
## Opportunities ({len(self.factors['O'])} items)

| # | Opportunity | Impact |
|---|-------------|--------|
"""
        for i, f in enumerate(self.get_opportunities(), 1):
            report += f"| {i} | **{f.title}** | {f.impact_score}/10 |\n"
        
        report += """
## Threats ({len(self.factors['T'])} items)

| # | Threat | Impact | Trend |
|---|--------|--------|-------|
"""
        for i, f in enumerate(self.get_threats(), 1):
            trend_emoji = "📈" if f.trend == "improving" else ("📉" if f.trend == "declining" else "➡️")
            report += f"| {i} | **{f.title}** | {f.impact_score}/10 | {trend_emoji} {f.trend} |\n"
        
        report += """
---

## Strategic Implications

### SO Strategies (Strength + Opportunity)
"""
        for i, s in enumerate(self.generate_so_strategy(), 1):
            report += f"{i}. {s}\n"
        
        report += """
### WO Strategies (Weakness + Opportunity)
"""
        for i, s in enumerate(self.generate_wo_strategy(), 1):
            report += f"{i}. {s}\n"
        
        report += """
### ST Strategies (Strength + Threat)
"""
        for i, s in enumerate(self.generate_st_strategy(), 1):
            report += f"{i}. {s}\n"
        
        report += """
### WT Strategies (Weakness + Threat)
"""
        for i, s in enumerate(self.generate_wt_strategy(), 1):
            report += f"{i}. {s}\n"
        
        report += """
---

*Generated by SWOT Analyzer*
"""
        return report


def interactive_mode() -> SWOTAnalyzer:
    """Interactive SWOT data collection"""
    analyzer = SWOTAnalyzer()
    
    print("\n🧠 SWOT Analysis - Interactive Mode")
    print("=" * 40)
    
    # Collect Strengths
    print("\n📊 STRENGTHS (internal advantages)")
    while True:
        title = input("  Strength name (or 'done'): ").strip()
        if title.lower() == 'done':
            break
        description = input("  Description: ").strip()
        impact = float(input("  Impact score (1-10): ") or "5")
        analyzer.add_factor(SWOTFactor(category='S', title=title, description=description, impact_score=impact))
    
    # Collect Weaknesses
    print("\n📉 WEAKNESSES (internal gaps)")
    while True:
        title = input("  Weakness name (or 'done'): ").strip()
        if title.lower() == 'done':
            break
        description = input("  Description: ").strip()
        impact = float(input("  Impact score (1-10): ") or "5")
        analyzer.add_factor(SWOTFactor(category='W', title=title, description=description, impact_score=impact))
    
    # Collect Opportunities
    print("\n🚀 OPPORTUNITIES (external possibilities)")
    while True:
        title = input("  Opportunity name (or 'done'): ").strip()
        if title.lower() == 'done':
            break
        description = input("  Description: ").strip()
        impact = float(input("  Impact score (1-10): ") or "5")
        analyzer.add_factor(SWOTFactor(category='O', title=title, description=description, impact_score=impact))
    
    # Collect Threats
    print("\n⚠️ THREATS (external risks)")
    while True:
        title = input("  Threat name (or 'done'): ").strip()
        if title.lower() == 'done':
            break
        description = input("  Description: ").strip()
        impact = float(input("  Impact score (1-10): ") or "5")
        analyzer.add_factor(SWOTFactor(category='T', title=title, description=description, impact_score=impact))
    
    return analyzer


def template_data() -> SWOTAnalyzer:
    """Load template SWOT data"""
    analyzer = SWOTAnalyzer()
    
    # Sample strengths
    analyzer.add_factor(SWOTFactor(category='S', title="Strong Technical Team",
                                  description="Experienced engineering team with deep expertise",
                                  impact_score=9, evidence=["Low bug rate", "Fast iterations"]))
    analyzer.add_factor(SWOTFactor(category='S', title="Product-Market Fit",
                                  description="Clear validation of customer need",
                                  impact_score=8, evidence=["High NPS", "Low churn"]))
    
    # Sample weaknesses
    analyzer.add_factor(SWOTFactor(category='W', title="Limited Marketing",
                                  description="Lack of brand awareness campaigns",
                                  impact_score=6, trend="stable"))
    analyzer.add_factor(SWOTFactor(category='W', title="Small Sales Team",
                                  description="Limited capacity for enterprise sales",
                                  impact_score=7, trend="improving"))
    
    # Sample opportunities
    analyzer.add_factor(SWOTFactor(category='O', title="New Market Segment",
                                  description="Adjacent market showing interest",
                                  impact_score=8))
    analyzer.add_factor(SWOTFactor(category='O', title="Strategic Partnership",
                                  description="Potential integration with major platform",
                                  impact_score=9))
    
    # Sample threats
    analyzer.add_factor(SWOTFactor(category='T', title="Competitor Launch",
                                  description="Well-funded competitor entering market",
                                  impact_score=7, trend="improving"))
    analyzer.add_factor(SWOTFactor(category='T', title="Regulatory Change",
                                  description="Potential privacy regulation changes",
                                  impact_score=5, trend="declining"))
    
    return analyzer


def main():
    parser = argparse.ArgumentParser(description='SWOT Analysis Tool')
    parser.add_argument('--interactive', '-i', action='store_true',
                       help='Interactive mode')
    parser.add_argument('--template', '-t', action='store_true',
                       help='Load template data')
    parser.add_argument('--generate', '-g', action='store_true',
                       help='Generate report')
    parser.add_argument('--json', '-j', action='store_true',
                       help='Output as JSON')
    parser.add_argument('--output', '-o', type=str,
                       help='Output file path')
    
    args = parser.parse_args()
    
    if args.interactive:
        analyzer = interactive_mode()
    elif args.template:
        analyzer = template_data()
    else:
        # Default: load template
        analyzer = template_data()
    
    if args.json:
        output = analyzer.generate_report(format="json")
    else:
        output = analyzer.generate_report()
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Report saved to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
