# 🧠 Decision Engine

## Automated Decision Framework System

---

## SWOT Analysis Automation

### SWOT Matrix Generator

```
┌─────────────────────────────────────────────────────────────┐
│                      INTERNAL                               │
│                Strengths      │      Weaknesses             │
│                                    │                         │
│   ┌──────────────────────────────┼─────────────────────────┐ │
│   │  S1: [Advantage]           │  W1: [Gap]              │ │
│   │  S2: [Capability]          │  W2: [Limitation]       │ │
│   │  S3: [Resource]            │  W3: [Vulnerability]    │ │
│   │  S4: [Network]             │  W4: [Debt]             │ │
│   ├──────────────────────────────┼─────────────────────────┤ │
│   │  O1: [Opportunity]         │  T1: [Threat]           │ │
│   │  O2: [Trend to leverage]   │  T2: [Competition]      │ │
│   │  O3: [Market gap]          │  T3: [Risk factor]      │ │
│   │  O4: [Adjacency]           │  T4: [Disruption]       │ │
│   └──────────────────────────────┴─────────────────────────┘ │
│                      EXTERNAL                               │
└─────────────────────────────────────────────────────────────┘
```

### Automated SWOT Generator (Python)

```python
# tools/strategy/swot_analyzer.py

from dataclasses import dataclass
from typing import List, Dict
import json

@dataclass
class SWOTFactor:
    category: str  # S, W, O, T
    title: str
    description: str
    impact_score: float  # 1-10
    evidence: List[str]
    trend: str  # improving, stable, declining

class SWOTAnalyzer:
    def __init__(self):
        self.factors: Dict[str, List[SWOTFactor]] = {
            'S': [], 'W': [], 'O': [], 'T': []
        }
    
    def add_factor(self, factor: SWOTFactor):
        self.factors[factor.category].append(factor)
    
    def generate_so_strategy(self) -> List[str]:
        """Strength-Opportunity: Leverage advantages"""
        return [f"Use {f.title} to capture {f.description}" 
                for f in self.factors['S'][:3]]
    
    def generate_wo_strategy(self) -> List[str]:
        """Weakness-Opportunity: Build capabilities"""
        return [f"Develop {f.title} to enable {f.description}"
                for f in self.factors['W'][:3]]
    
    def generate_st_strategy(self) -> List[str]:
        """Strength-Threat: Defend position"""
        return [f"Leverage {f.title} to counter {f.description}"
                for f in self.factors['S'][:3]]
    
    def generate_wt_strategy(self) -> List[str]:
        """Weakness-Threat: Mitigate risks"""
        return [f"Address {f.title} to avoid {f.description}"
                for f in self.factors['W'][:3]]
    
    def generate_report(self) -> str:
        return f"""
# SWOT Analysis Report

## Strengths ({len(self.factors['S'])} items)
{[f"- {f.title}: {f.description}" for f in self.factors['S']]}

## Weaknesses ({len(self.factors['W'])} items)
{[f"- {f.title}: {f.description}" for f in self.factors['W']]}

## Opportunities ({len(self.factors['O'])} items)
{[f"- {f.title}: {f.description}" for f in self.factors['O']]}

## Threats ({len(self.factors['T'])} items)
{[f"- {f.title}: {f.description}" for f in self.factors['T']]}

## Strategic Priorities
1. SO: {self.generate_so_strategy()}
2. WO: {self.generate_wo_strategy()}
3. ST: {self.generate_st_strategy()}
4. WT: {self.generate_wt_strategy()}
"""
```

---

## Risk Assessment Matrix

### Risk Matrix Template

| Risk ID | Risk Description | Probability | Impact | Score | Mitigation | Owner | Status |
|---------|------------------|-------------|--------|-------|------------|-------|--------|
| R001 | [Risk description] | H/M/L | H/M/L | P×I | [Strategy] | [Owner] | Active |

### Automated Risk Tracker

```python
# tools/strategy/risk_matrix.py

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

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

@dataclass
class Risk:
    id: str
    description: str
    probability: Probability
    impact: Impact
    mitigation: str
    owner: str
    status: str = "active"  # active, mitigated, closed
    
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

class RiskMatrix:
    def __init__(self):
        self.risks: List[Risk] = []
    
    def add_risk(self, risk: Risk):
        self.risks.append(risk)
    
    def get_top_risks(self, n: int = 5) -> List[Risk]:
        return sorted(self.risks, key=lambda r: r.score, reverse=True)[:n]
    
    def export_matrix(self) -> str:
        header = "| ID | Risk | Prob | Impact | Score | Priority | Mitigation |\n"
        separator = "|----|------|------|--------|-------|----------|------------|\n"
        rows = []
        for r in sorted(self.risks, key=lambda x: x.score, reverse=True):
            rows.append(f"| {r.id} | {r.description[:30]} | {r.probability.name} | {r.impact.name} | {r.score} | {r.priority} | {r.mitigation[:25]} |")
        return header + separator + "\n".join(rows)
```

### Risk Heat Map

```
         IMPACT
         1    2    3    4    5
       ┌────┬────┬────┬────┬────┐
   5   │ M  │ H  │ H  │ C  │ C  │ ← Probability
       ├────┼────┼────┼────┼────┤
   4   │ L  │ M  │ H  │ H  │ C  │
       ├────┼────┼────┼────┼────┤
P  3   │ L  │ L  │ M  │ H  │ H  │ ←
R      ├────┼────┼────┼────┼────┤
O  2   │ L  │ L  │ L  │ M  │ H  │
B      ├────┼────┼────┼────┼────┤
A  1   │ L  │ L  │ L  │ L  │ M  │
B      └────┴────┴────┴────┴────┘
         1    2    3    4    5
    
    L=Low Risk, M=Medium, H=High, C=Critical
```

---

## ROI Calculator

### Investment ROI Framework

```
ROI = (Net Return / Investment Cost) × 100

Net Return = Gross Return - Investment Cost - Operating Costs

Payback Period = Investment Cost / (Monthly Return - Monthly Cost)
```

### Automated ROI Calculator

```python
# tools/strategy/roi_calculator.py

from dataclasses import dataclass
from typing import List
from datetime import datetime, timedelta

@dataclass
class Investment:
    name: str
    initial_cost: float
    expected_return: float
    timeline_months: int
    operating_cost_monthly: float = 0
    risk_adjustment: float = 0.1  # 10% risk discount

class ROICalculator:
    def calculate_roi(self, inv: Investment) -> dict:
        net_return = inv.expected_return - inv.initial_cost - (inv.operating_cost_monthly * inv.timeline_months)
        roi = (net_return / inv.initial_cost) * 100
        
        # Risk-adjusted ROI
        risk_adjusted_return = inv.expected_return * (1 - inv.risk_adjustment)
        risk_net = risk_adjusted_return - inv.initial_cost - (inv.operating_cost_monthly * inv.timeline_months)
        risk_roi = (risk_net / inv.initial_cost) * 100
        
        # Payback period
        monthly_net = (inv.expected_return / inv.timeline_months) - inv.operating_cost_monthly
        payback = inv.initial_cost / monthly_net if monthly_net > 0 else float('inf')
        
        return {
            "name": inv.name,
            "roi_percent": round(roi, 2),
            "risk_adjusted_roi": round(risk_roi, 2),
            "payback_months": round(payback, 1),
            "npv": self._calculate_npv(inv),
            "recommendation": self._recommend(roi, risk_roi)
        }
    
    def _calculate_npv(self, inv: Investment, discount_rate: float = 0.1) -> float:
        npv = -inv.initial_cost
        monthly_return = inv.expected_return / inv.timeline_months
        for month in range(1, inv.timeline_months + 1):
            cash_flow = monthly_return - inv.operating_cost_monthly
            npv += cash_flow / ((1 + discount_rate) ** month)
        return round(npv, 2)
    
    def _recommend(self, roi: float, risk_roi: float) -> str:
        if risk_roi > 30:
            return "✅ Strong investment - proceed"
        elif risk_roi > 10:
            return "⚠️ Moderate return - proceed with monitoring"
        elif risk_roi > 0:
            return "⚠️ Low return - consider alternatives"
        return "❌ Negative return - do not proceed"

# Usage
calc = ROICalculator()
result = calc.calculate_roi(Investment(
    name="New Feature Development",
    initial_cost=50000,
    expected_return=80000,
    timeline_months=12,
    operating_cost_monthly=2000
))
```

---

## Competitive Analysis

### Competitive Intelligence Framework

```
┌─────────────────────────────────────────────────────────────┐
│ COMPETITIVE ANALYSIS MATRIX                                 │
├─────────────┬──────────┬──────────┬──────────┬────────────┤
│ Dimension   │ [Us]     │ [Comp A] │ [Comp B] │ [Comp C]   │
├─────────────┼──────────┼──────────┼──────────┼────────────┤
│ Pricing     │ $XX      │ $XX      │ $XX      │ $XX        │
├─────────────┼──────────┼──────────┼──────────┼────────────┤
│ Features    │ X/Y/Z    │ X/Y/Z    │ X/Y/Z    │ X/Y/Z      │
├─────────────┼──────────┼──────────┼──────────┼────────────┤
│ UX Score    │ 8/10     │ 7/10     │ 9/10     │ 6/10       │
├─────────────┼──────────┼──────────┼──────────┼────────────┤
│ Market Share│ XX%      │ XX%      │ XX%      │ XX%        │
├─────────────┼──────────┼──────────┼──────────┼────────────┤
│ Strength    │ [X]      │ [Y]      │ [Z]      │ [W]        │
├─────────────┼──────────┼──────────┼──────────┼────────────┤
│ Weakness    │ [A]      │ [B]      │ [C]      │ [D]        │
└─────────────┴──────────┴──────────┴──────────┴────────────┘
```

### Competitive Radar Chart Dimensions

1. **Product Features** - Breadth/depth of features
2. **UX/Design** - User experience quality
3. **Pricing** - Cost competitiveness
4. **Brand** - Recognition and trust
5. **Support** - Customer service quality
6. **Innovation** - Speed of new features
7. **Reliability** - Uptime/performance
8. **Scalability** - Growth capacity

---

## Market Positioning Logic

### Positioning Statement Template

```
For [target customer] who [need],
[Product] provides [key benefit] unlike [competitor]
because [reason to believe].
```

### Positioning Matrix

```
                    High Price
                         │
          Premium        │        Luxury
    ┌────────────────────┼────────────────────┐
    │                    │                    │
    │   [OUR PRODUCT]    │   Competitor A     │
    │                    │                    │
Low │                    │                    │ High
 ───┼────────────────────┼────────────────────┼─── Value
    │                    │                    │
    │   Competitor C     │   Competitor B     │
    │                    │                    │
    └────────────────────┼────────────────────┘
                         │
                    Economy
                    Low Price
```

### Blue Ocean vs Red Ocean Strategy

| Red Ocean | Blue Ocean |
|-----------|------------|
| Compete in existing market | Create new market space |
| Beat competitors | Make competition irrelevant |
| Exploit existing demand | Create new demand |
| Focus on cost vs value | Unlock new value & cost |

---

## Decision Framework Summary

| Tool | When to Use | Output |
|------|-------------|--------|
| **SWOT** | Strategic planning, capability assessment | Strategy options |
| **Risk Matrix** | Project planning, investment decisions | Risk register |
| **ROI Calculator** | Budget allocation, investment justification | Investment scorecard |
| **Competitive Analysis** | Product positioning, go-to-market | Competitive advantage |
| **Positioning Matrix** | Brand strategy, messaging | Positioning statement |

---

*Last Updated: 2026-02-04*
*Version: 1.0*
