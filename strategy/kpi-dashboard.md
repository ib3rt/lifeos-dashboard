# 📊 KPI Dashboard Framework

---

## KPI Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│                    NORTH STAR METRIC                          │
│                 (Single metric that drives growth)           │
└─────────────────────────┬───────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
   ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
   │  INPUT KPIs  │ │  OUTPUT KPIs │ │  HEALTH KPIs │
   │(Leading)     │ │(Lagging)     │ │(Guardrails)  │
   └──────────────┘ └──────────────┘ └──────────────┘
```

---

## Core KPI Categories

### 1. Revenue Metrics

| Metric | Formula | Target | Frequency |
|--------|---------|--------|-----------|
| **MRR** | SUM(active_subscriptions × price) | $X,XXX | Weekly |
| **ARR** | MRR × 12 | $XX,XXX | Weekly |
| **ARPU** | MRR / Active Users | $XX | Weekly |
| **LTV** | ARPU / Churn Rate | $XXX | Monthly |
| **CAC** | Total Sales Cost / New Customers | $XX | Monthly |
| **LTV:CAC** | LTV / CAC | > 3.0 | Monthly |
| **Gross Margin** | (Revenue - COGS) / Revenue | > 70% | Monthly |
| **Net Revenue Retention** | (Starting MRR + Expansion - Contraction - Churn) / Starting MRR | > 100% | Monthly |

### 2. Growth Metrics

| Metric | Formula | Target | Frequency |
|--------|---------|--------|-----------|
| **DAU/MAU** | Daily Active Users / Monthly Active Users | > 25% | Daily |
| **Conversion Rate** | New Customers / Trial Signups | > X% | Weekly |
| **Trial to Paid** | Paid / Started Trial | > X% | Weekly |
| **Virality Factor** | Referrals per User | > 1.0 | Monthly |
| **Net Promoter Score** | %Promoters - %Detractors | > 50 | Quarterly |

### 3. Engagement Metrics

| Metric | Formula | Target | Frequency |
|--------|---------|--------|-----------|
| **Session Duration** | AVG(time per session) | > X min | Daily |
| **Feature Adoption** | Users of Feature / Total Users | > X% | Weekly |
| **Return Rate** | Users returning / Total Users | > X% | Daily |
| **Time to Value** | Time to first "Aha!" moment | < X days | Weekly |
| **Support Tickets/User** | Tickets / Users | < X | Weekly |

### 4. Efficiency Metrics

| Metric | Formula | Target | Frequency |
|--------|---------|--------|-----------|
| **Burn Rate** | Monthly cash spent | $XX,XXX | Monthly |
| **Runway** | Cash / Burn Rate | > 18 months | Monthly |
| **Unit Economics** | (LTV - Service Cost) / CAC | > 1.5 | Monthly |
| **Marketing Efficiency** | New MRR / Marketing Spend | > 1.0 | Monthly |

---

## Dashboard Design

### Executive Dashboard Layout

```
┌─────────────────────────────────────────────────────────────────────────┐
│  📊 EXECUTIVE DASHBOARD                    📅 Last Updated: 2026-02-04  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐          │
│  │    $12,450      │  │    2,847        │  │    89%          │          │
│  │    MRR          │  │    Active Users │  │    Goal Progress│          │
│  │    ↑ 12% MoM    │  │    ↑ 8% MoM     │  │    🟢 On Track  │          │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘          │
│           │                     │                     │                   │
├───────────┼─────────────────────┼─────────────────────┼───────────────────┤
│           │                     │                     │                   │
│  ┌───────▼───────┐    ┌───────▼───────┐    ┌───────▼───────┐           │
│  │  📈 Revenue    │    │  👥 Users      │    │  ⚡ Engagement │           │
│  │  Trend         │    │  Growth        │    │  Metrics       │           │
│  │  [CHART]       │    │  [CHART]       │    │  [CHART]       │           │
│  └───────────────┘    └───────────────┘    └───────────────┘           │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│  🚨 Alerts                              📋 Quick Stats                  │
│  ⚠️ CAC increased 15%                   • Trial Conversion: 4.2%        │
│  ✅ LTV:CAC ratio healthy (3.2x)        • NPS Score: 52                 │
│  ℹ️ New user target reached             • Support CSAT: 4.6/5          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### KPI Alert Thresholds

```python
# tools/strategy/kpi_alerts.py

from dataclasses import dataclass
from typing import Dict, List, Callable
from enum import Enum

class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

@dataclass
class KPIThreshold:
    name: str
    warning_value: float
    critical_value: float
    direction: str  # "higher" or "lower" is better
    severity: AlertSeverity = AlertSeverity.WARNING
    
    def check(self, value: float) -> tuple[AlertSeverity, str]:
        if self.direction == "higher":
            if value <= self.critical_value:
                return (AlertSeverity.CRITICAL, 
                       f"CRITICAL: {self.name} is {value} (target: >{self.critical_value})")
            elif value <= self.warning_value:
                return (AlertSeverity.WARNING, 
                       f"WARNING: {self.name} is {value} (target: >{self.warning_value})")
        else:  # lower is better
            if value >= self.critical_value:
                return (AlertSeverity.CRITICAL, 
                       f"CRITICAL: {self.name} is {value} (target: <{self.critical_value})")
            elif value >= self.warning_value:
                return (AlertSeverity.WARNING, 
                       f"WARNING: {self.name} is {value} (target: <{self.warning_value})")
        return (AlertSeverity.INFO, f"OK: {self.name} is {value}")

class KPIAlertSystem:
    def __init__(self):
        self.thresholds: Dict[str, KPIThreshold] = {}
        self.alert_history: List[dict] = []
    
    def add_threshold(self, threshold: KPIThreshold):
        self.thresholds[threshold.name] = threshold
    
    def check_all(self, values: Dict[str, float]) -> List[dict]:
        alerts = []
        for name, value in values.items():
            if name in self.thresholds:
                severity, message = self.thresholds[name].check(value)
                if severity != AlertSeverity.INFO:
                    alerts.append({
                        "kpi": name,
                        "value": value,
                        "severity": severity.value,
                        "message": message
                    })
                    self.alert_history.append({
                        "kpi": name,
                        "value": value,
                        "severity": severity.value,
                        "timestamp": "2026-02-04T01:21:00Z"
                    })
        return alerts
```

---

## KPI Dashboard Generator

```python
# tools/strategy/dashboard_generator.py

from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime

@dataclass
class KPI:
    name: str
    category: str
    current_value: float
    target_value: float
    unit: str
    format: str = "{:,.2f}"  # number format

class DashboardGenerator:
    def __init__(self):
        self.kpis: List[KPI] = []
    
    def add_kpi(self, kpi: KPI):
        self.kpis.append(kpi)
    
    def generate_html(self) -> str:
        kpi_cards = ""
        for kpi in self.kpis:
            progress = min((kpi.current_value / kpi.target_value) * 100, 100)
            status = "🟢" if progress >= 90 else ("🟡" if progress >= 70 else "🔴")
            kpi_cards += f"""
            <div class="kpi-card">
                <h3>{kpi.name}</h3>
                <div class="value">{kpi.format.format(kpi.current_value)} {kpi.unit}</div>
                <div class="target">Target: {kpi.format.format(kpi.target_value)} {kpi.unit}</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {progress}%"></div>
                </div>
                <div class="status">{status} {progress:.0f}%</div>
            </div>
            """
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>KPI Dashboard</title>
            <style>
                .dashboard {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; padding: 20px; }}
                .kpi-card {{ background: #1a1a2e; border-radius: 10px; padding: 20px; color: white; }}
                .value {{ font-size: 2em; font-weight: bold; color: #00d9ff; }}
                .target {{ color: #888; margin: 5px 0; }}
                .progress-bar {{ background: #333; height: 8px; border-radius: 4px; margin: 10px 0; }}
                .progress-fill {{ background: #00d9ff; height: 100%; border-radius: 4px; }}
                .status {{ font-weight: bold; }}
            </style>
        </head>
        <body>
            <h1>📊 KPI Dashboard - {datetime.now().strftime('%Y-%m-%d')}</h1>
            <div class="dashboard">
                {kpi_cards}
            </div>
        </body>
        </html>
        """
    
    def generate_markdown(self) -> str:
        table_rows = []
        for kpi in self.kpis:
            progress = min((kpi.current_value / kpi.target_value) * 100, 100)
            status = "✅" if progress >= 90 else ("⚠️" if progress >= 70 else "🔴")
            table_rows.append(f"| {kpi.name} | {kpi.current_value:.2f} | {kpi.target_value:.2f} | {progress:.0f}% | {status} |")
        
        return f"""
# KPI Dashboard

| KPI | Current | Target | Progress | Status |
|-----|---------|--------|----------|--------|
{chr(10).join(table_rows)}

Generated: {datetime.now().isoformat()}
"""
```

---

## KPI Tracking Schedule

| KPI Type | Collection Frequency | Owner | Review |
|----------|---------------------|-------|--------|
| North Star | Daily | CEO | Weekly |
| Revenue | Weekly | CFO | Weekly |
| Growth | Weekly | Growth Lead | Bi-weekly |
| Engagement | Daily | Product | Weekly |
| Efficiency | Monthly | COO | Monthly |

---

## KPI Data Sources

```yaml
# tools/strategy/kpi_config.yaml

kpis:
  revenue:
    mrr:
      source: "stripe.subscriptions"
      query: "SELECT SUM(amount) WHERE status='active'"
      threshold_warning: 10000
      threshold_critical: 5000
    
  users:
    dau:
      source: "analytics.events"
      query: "COUNT(DISTINCT user_id) WHERE event='session_start'"
      threshold_warning: 500
      threshold_critical: 200
    
  engagement:
    session_duration:
      source: "analytics.events"
      query: "AVG(session_duration)"
      threshold_warning: 300  # seconds
      threshold_critical: 180

refresh_schedule:
  daily: ["00:00 UTC"]
  weekly: ["Monday 00:00 UTC"]
  monthly: ["1st of month 00:00 UTC"]
```

---

*Last Updated: 2026-02-04*
*Version: 1.0*
