# Strategy Tools

Automated strategic planning and decision-making tools.

## Tools Overview

| Tool | Purpose | Usage |
|------|---------|-------|
| `kpi_collector.py` | Collect and monitor KPIs | `python kpi_collector.py --check-all` |
| `swot_analyzer.py` | SWOT analysis automation | `python swot_analyzer.py --template` |
| `risk_matrix.py` | Risk assessment tracking | `python risk_matrix.py --report` |
| `roi_calculator.py` | Investment ROI analysis | `python roi_calculator.py --compare` |
| `growth_model.py` | Growth trajectory projection | `python growth_model.py --compare` |
| `generate_report.sh` | Generate strategic reports | `./generate_report.sh all` |

## Quick Start

### Generate All Reports
```bash
./generate_report.sh all
```

### KPI Management
```bash
# Check all KPIs
python3 kpi_collector.py --check-all

# Generate KPI report
python3 kpi_collector.py --report
```

### SWOT Analysis
```bash
# Interactive mode
python3 swot_analyzer.py --interactive

# Template mode
python3 swot_analyzer.py --template
```

### Risk Assessment
```bash
# Add new risk
python3 risk_matrix.py --add "New Risk" --probability medium --impact high

# Generate report
python3 risk_matrix.py --report
```

### ROI Calculation
```bash
# Single investment
python3 roi_calculator.py --cost 50000 --return 80000 --months 12

# Compare investments
python3 roi_calculator.py --compare
```

### Growth Modeling
```bash
# Project 24 months
python3 growth_model.py --project 24

# Compare scenarios
python3 growth_model.py --compare
```

## Configuration

### KPI Config (`kpi_config.yaml`)
```yaml
kpis:
  mrr:
    source: "stripe.subscriptions"
    threshold_warning: 10000
    threshold_critical: 5000
    direction: higher
```

### Investment List (`investments.json`)
```json
[
  {
    "name": "Marketing Campaign",
    "initial_cost": 20000,
    "expected_return": 35000,
    "timeline_months": 6
  }
]
```

## Output

Reports are saved to `../reports/` directory:
- `kpi_report_YYYY-MM-DD.md`
- `swot_report_YYYY-MM-DD.md`
- `risk_report_YYYY-MM-DD.md`
- `strategic_report_YYYY-MM-DD.md`
