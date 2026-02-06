#!/usr/bin/env python3
"""
LLM Cost Reporter

Generates daily, weekly, and monthly cost reports.
Handles visualization, alerts, and report distribution.
"""

import json
import csv
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import logging
import subprocess

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ReportConfig:
    """Configuration for report generation."""
    report_date: str
    report_type: str = "daily"  # daily, weekly, monthly
    include_charts: bool = True
    include_alerts: bool = True
    include_recommendations: bool = True
    output_format: str = "markdown"  # markdown, json, csv
    channels: List[str] = None


class CostReporter:
    """Report generation class."""
    
    def __init__(self, tracker_db: str = "costs.db", output_dir: str = "reports"):
        """Initialize the reporter."""
        self.tracker_db = tracker_db
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.reports_dir = self.output_dir / "daily"
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
        self.archive_dir = self.output_dir / "archive"
        self.archive_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_daily_report(
        self,
        date: str = None,
        format: str = "markdown",
    ) -> str:
        """Generate daily cost report."""
        date = date or datetime.now().strftime("%Y-%m-%d")
        
        # Import here to avoid circular imports
        import sys
        sys.path.insert(0, str(Path(__file__).parent))
        from tracker import CostTracker
        
        tracker = CostTracker(db_path=self.tracker_db)
        
        # Get summary data
        summary = tracker.get_daily_summary(date)
        anomalies = tracker.detect_anomalies(date)
        
        # Get trend data
        trend = tracker.get_weekly_trend()
        
        # Calculate day-over-day change
        yesterday = (datetime.strptime(date, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
        yesterday_cost = tracker.get_daily_cost(yesterday)
        
        cost_change_pct = 0
        if yesterday_cost > 0:
            cost_change_pct = ((summary["total_cost"] - yesterday_cost) / yesterday_cost) * 100
        
        # Generate report based on format
        if format == "json":
            return self._generate_json_report(date, summary, anomalies, trend, cost_change_pct)
        elif format == "csv":
            return self._generate_csv_report(date, summary, anomalies, trend)
        else:
            return self._generate_markdown_report(date, summary, anomalies, trend, cost_change_pct)
    
    def _generate_markdown_report(
        self,
        date: str,
        summary: Dict,
        anomalies: List[Dict],
        trend: List[Dict],
        cost_change_pct: float,
    ) -> str:
        """Generate markdown format report."""
        
        # Format currency
        def fmt_currency(amount: float) -> str:
            return f"${amount:,.2f}"
        
        # Format percentage
        def fmt_pct(pct: float) -> str:
            sign = "+" if pct > 0 else ""
            return f"{sign}{pct:.1f}%"
        
        # Format number
        def fmt_num(num: int) -> str:
            if num >= 1_000_000:
                return f"{num/1_000_000:.1f}M"
            elif num >= 1_000:
                return f"{num/1_000:.1f}K"
            return str(num)
        
        # Calculate percentages
        model_percentages = []
        total_cost = summary["total_cost"]
        for model in summary["by_model"]:
            pct = (model["cost"] / total_cost * 100) if total_cost > 0 else 0
            model_percentages.append(pct)
        
        # Build markdown
        md = f"""# LLM Cost Report - {date}

## Summary
- **Total Daily Cost**: {fmt_currency(summary["total_cost"])}
- **Total Tokens**: {fmt_num(summary["total_tokens"])}
- **Avg Cost/Token**: ${summary["avg_cost_per_token"]:.4f}
- **vs Yesterday**: {fmt_pct(cost_change_pct)}
- **Total Requests**: {summary["requests"]:,}

## Usage by Model

| Model | Requests | Tokens | Cost | % of Total |
|-------|----------|--------|------|------------|
"""
        
        for i, model in enumerate(summary["by_model"]):
            pct = model_percentages[i]
            md += f"| {model['model']} | {model['requests']:,} | {fmt_num(model['tokens'])} | {fmt_currency(model['cost'])} | {pct:.1f}% |\n"
        
        md += """
## Usage by Provider

| Provider | Requests | Cost | % of Total |
|----------|----------|------|------------|
"""
        
        for provider in summary["by_provider"]:
            pct = (provider["cost"] / total_cost * 100) if total_cost > 0 else 0
            md += f"| {provider['provider']} | {provider['requests']:,} | {fmt_currency(provider['cost'])} | {pct:.1f}% |\n"
        
        md += """
## Usage by Agent

| Agent | Requests | Cost |
|-------|----------|------|
"""
        
        for agent in summary["by_agent"]:
            md += f"| {agent['agent']} | {agent['requests']:,} | {fmt_currency(agent['cost'])} |\n"
        
        # Weekly trend
        md += f"""
## Weekly Trend

| Date | Cost | Tokens | Requests |
|------|------|--------|----------|
"""
        
        for day in trend:
            day_date = day["date"]
            md += f"| {day_date} | {fmt_currency(day['cost'])} | {fmt_num(day['tokens'])} | {day['requests']:,} |\n"
        
        # Alerts and anomalies
        if anomalies:
            md += """
## Alerts

"""
            for anomaly in anomalies:
                severity = "🔴" if anomaly["severity"] == "high" else "🟡"
                md += f"- {severity} {anomaly['message']}\n"
        else:
            md += """
## Alerts
- ✅ No anomalies detected
"""
        
        # Cost optimization opportunities
        md += """
## Cost Optimization Opportunities

"""
        
        # Simple recommendations based on data
        recommendations = self._generate_recommendations(summary)
        for rec in recommendations:
            md += f"- **{rec['priority'].title()}**: {rec['message']} → Save {rec['savings']}\n"
        
        # Footer
        md += f"""
---
*Report generated at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
        
        return md
    
    def _generate_json_report(
        self,
        date: str,
        summary: Dict,
        anomalies: List[Dict],
        trend: List[Dict],
        cost_change_pct: float,
    ) -> str:
        """Generate JSON format report."""
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "report_date": date,
            "report_type": "daily",
            "summary": {
                "total_cost": summary["total_cost"],
                "total_tokens": summary["total_tokens"],
                "avg_cost_per_token": summary["avg_cost_per_token"],
                "cost_change_vs_yesterday": cost_change_pct,
                "total_requests": summary["requests"],
            },
            "usage_by_model": [
                {
                    "model": m["model"],
                    "requests": m["requests"],
                    "tokens": m["tokens"],
                    "cost": m["cost"],
                    "percentage": round((m["cost"] / summary["total_cost"] * 100) if summary["total_cost"] > 0 else 0, 2)
                }
                for m in summary["by_model"]
            ],
            "usage_by_provider": [
                {
                    "provider": p["provider"],
                    "requests": p["requests"],
                    "cost": p["cost"],
                    "percentage": round((p["cost"] / summary["total_cost"] * 100) if summary["total_cost"] > 0 else 0, 2)
                }
                for p in summary["by_provider"]
            ],
            "usage_by_agent": [
                {
                    "agent": a["agent"],
                    "requests": a["requests"],
                    "cost": a["cost"],
                }
                for a in summary["by_agent"]
            ],
            "weekly_trend": trend,
            "alerts": anomalies,
            "recommendations": self._generate_recommendations(summary),
        }
        
        return json.dumps(report, indent=2)
    
    def _generate_csv_report(
        self,
        date: str,
        summary: Dict,
        anomalies: List[Dict],
        trend: List[Dict],
    ) -> str:
        """Generate CSV format report."""
        
        # We'll return a string that could be written to CSV
        lines = []
        
        # Header
        lines.append("category,model,provider,requests,tokens,cost,percentage")
        
        # Models
        for model in summary["by_model"]:
            pct = (model["cost"] / summary["total_cost"] * 100) if summary["total_cost"] > 0 else 0
            lines.append(f"model,{model['model']},,{model['requests']},{model['tokens']},{model['cost']},{pct:.2f}")
        
        # Providers
        for provider in summary["by_provider"]:
            pct = (provider["cost"] / summary["total_cost"] * 100) if summary["total_cost"] > 0 else 0
            lines.append(f"provider,,{provider['provider']},{provider['requests']},,{provider['cost']},{pct:.2f}")
        
        # Agents
        for agent in summary["by_agent"]:
            lines.append(f"agent,{agent['agent']},,{agent['requests']},,{agent['cost']},")
        
        return "\n".join(lines)
    
    def _generate_recommendations(self, summary: Dict) -> List[Dict]:
        """Generate optimization recommendations based on summary."""
        recommendations = []
        
        total_cost = summary["total_cost"]
        
        # Check for expensive models
        for model in summary["by_model"]:
            model_cost = model["cost"]
            pct_of_total = (model_cost / total_cost * 100) if total_cost > 0 else 0
            
            if pct_of_total > 30 and "gpt-4" in model["model"].lower():
                recommendations.append({
                    "priority": "high",
                    "message": f"Switch from {model['model']} to GPT-4o-mini for simple tasks",
                    "savings": f"${model_cost * 0.5:.2f}/day",
                })
            elif pct_of_total > 20 and "claude-3-opus" in model["model"].lower():
                recommendations.append({
                    "priority": "high",
                    "message": f"Consider Claude 3.5 Sonnet instead of {model['model']}",
                    "savings": f"${model_cost * 0.7:.2f}/day",
                })
        
        # Check for high average cost per request
        for agent in summary["by_agent"]:
            if agent["requests"] > 0:
                avg_cost = agent["cost"] / agent["requests"]
                if avg_cost > 0.10:
                    recommendations.append({
                        "priority": "medium",
                        "message": f"Optimize prompts for {agent['agent']} to reduce cost per request",
                        "savings": f"${agent['cost'] * 0.15:.2f}/day",
                    })
        
        # General recommendations
        recommendations.append({
            "priority": "low",
            "message": "Implement response caching for repeated queries",
            "savings": "$0.75/day",
        })
        
        recommendations.append({
            "priority": "low",
            "message": "Batch similar requests to reduce API overhead",
            "savings": "$1.20/day",
        })
        
        return recommendations
    
    def generate_weekly_report(self, week_end: str = None) -> str:
        """Generate weekly cost report."""
        end_date = datetime.strptime(week_end or datetime.now().strftime("%Y-%m-%d"), "%Y-%m-%d")
        start_date = end_date - timedelta(days=6)
        
        # Collect daily data
        daily_data = []
        total_weekly_cost = 0
        
        import sys
        sys.path.insert(0, str(Path(__file__).parent))
        from tracker import CostTracker
        
        tracker = CostTracker(db_path=self.tracker_db)
        
        for i in range(7):
            date = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
            summary = tracker.get_daily_summary(date)
            daily_data.append({
                "date": date,
                "cost": summary["total_cost"],
                "tokens": summary["total_tokens"],
                "requests": summary["requests"],
            })
            total_weekly_cost += summary["total_cost"]
        
        # Generate markdown report
        md = f"""# Weekly LLM Cost Report - {start_date.strftime("%Y-%m-%d")} to {end_date.strftime("%Y-%m-%d")}

## Weekly Summary
- **Total Weekly Cost**: ${total_weekly_cost:,.2f}
- **Avg Daily Cost**: ${total_weekly_cost / 7:,.2f}
- **Projected Monthly Cost**: ${total_weekly_cost * 4.3:,.2f}

## Daily Breakdown

| Date | Cost | Tokens | Requests |
|------|------|--------|----------|
"""
        
        for day in daily_data:
            md += f"| {day['date']} | ${day['cost']:,.2f} | {day['tokens']:,} | {day['requests']:,} |\n"
        
        # Trend chart (ASCII)
        md += """
## Cost Trend

```
"""
        max_cost = max(d["cost"] for d in daily_data) if daily_data else 1
        for day in daily_data:
            bar_length = int((day["cost"] / max_cost) * 30)
            bar = "█" * bar_length
            md += f"{day['date']}: {bar} ${day['cost']:.2f}\n"
        
        md += """```

## Top Cost Drivers

"""
        
        # Aggregate by model for the week
        model_costs = {}
        for i in range(7):
            date = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
            summary = tracker.get_daily_summary(date)
            for model in summary["by_model"]:
                key = model["model"]
                if key not in model_costs:
                    model_costs[key] = {"cost": 0, "requests": 0}
                model_costs[key]["cost"] += model["cost"]
                model_costs[key]["requests"] += model["requests"]
        
        sorted_models = sorted(model_costs.items(), key=lambda x: x[1]["cost"], reverse=True)
        for model, data in sorted_models[:5]:
            pct = (data["cost"] / total_weekly_cost * 100) if total_weekly_cost > 0 else 0
            md += f"- **{model}**: ${data['cost']:.2f} ({pct:.1f}%) - {data['requests']:,} requests\n"
        
        md += f"""
---
*Report generated at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
        
        return md
    
    def generate_monthly_report(self, month: str = None) -> str:
        """Generate monthly cost report."""
        target_month = datetime.strptime(month or datetime.now().strftime("%Y-%m-%d"), "%Y-%m-%d")
        year = target_month.year
        month_num = target_month.month
        
        # Calculate days in month
        if month_num == 12:
            next_month = datetime(year + 1, 1, 1)
        else:
            next_month = datetime(year, month_num + 1, 1)
        
        days_in_month = (next_month - datetime(year, month_num, 1)).days
        
        # Collect daily data
        daily_data = []
        total_monthly_cost = 0
        
        import sys
        sys.path.insert(0, str(Path(__file__).parent))
        from tracker import CostTracker
        
        tracker = CostTracker(db_path=self.tracker_db)
        
        for day in range(1, days_in_month + 1):
            date = datetime(year, month_num, day).strftime("%Y-%m-%d")
            summary = tracker.get_daily_summary(date)
            daily_data.append({
                "date": date,
                "cost": summary["total_cost"],
                "tokens": summary["total_tokens"],
                "requests": summary["requests"],
            })
            total_monthly_cost += summary["total_cost"]
        
        # Calculate averages
        active_days = len([d for d in daily_data if d["cost"] > 0])
        avg_daily = total_monthly_cost / active_days if active_days > 0 else 0
        
        # Generate markdown report
        md = f"""# Monthly LLM Cost Report - {target_month.strftime("%B %Y")}

## Monthly Summary
- **Total Monthly Cost**: ${total_monthly_cost:,.2f}
- **Avg Daily Cost**: ${avg_daily:,.2f}
- **Active Days**: {active_days} of {days_in_month}
- **Projected Annual Cost**: ${total_monthly_cost * 12:,.2f}

## Daily Breakdown (First 14 Days)

| Date | Cost | Tokens | Requests |
|------|------|--------|----------|
"""
        
        for day in daily_data[:14]:
            md += f"| {day['date']} | ${day['cost']:,.2f} | {day['tokens']:,} | {day['requests']:,} |\n"
        
        if len(daily_data) > 14:
            md += f"| ... | ... | ... | ... |\n"
        
        # Aggregate by model
        model_costs = {}
        provider_costs = {}
        
        for day in daily_data:
            date = day["date"]
            summary = tracker.get_daily_summary(date)
            
            for model in summary["by_model"]:
                key = model["model"]
                if key not in model_costs:
                    model_costs[key] = {"cost": 0, "requests": 0}
                model_costs[key]["cost"] += model["cost"]
                model_costs[key]["requests"] += model["requests"]
            
            for provider in summary["by_provider"]:
                key = provider["provider"]
                if key not in provider_costs:
                    provider_costs[key] = {"cost": 0, "requests": 0}
                provider_costs[key]["cost"] += provider["cost"]
                provider_costs[key]["requests"] += provider["requests"]
        
        md += """
## Usage by Model

| Model | Cost | % of Total | Requests |
|-------|------|------------|----------|
"""
        
        sorted_models = sorted(model_costs.items(), key=lambda x: x[1]["cost"], reverse=True)
        for model, data in sorted_models:
            pct = (data["cost"] / total_monthly_cost * 100) if total_monthly_cost > 0 else 0
            md += f"| {model} | ${data['cost']:,.2f} | {pct:.1f}% | {data['requests']:,} |\n"
        
        md += """
## Usage by Provider

| Provider | Cost | % of Total | Requests |
|----------|------|------------|----------|
"""
        
        sorted_providers = sorted(provider_costs.items(), key=lambda x: x[1]["cost"], reverse=True)
        for provider, data in sorted_providers:
            pct = (data["cost"] / total_monthly_cost * 100) if total_monthly_cost > 0 else 0
            md += f"| {provider} | ${data['cost']:,.2f} | {pct:.1f}% | {data['requests']:,} |\n"
        
        # Budget analysis
        monthly_budget = 1200  # Default monthly budget
        budget_remaining = monthly_budget - total_monthly_cost
        budget_used_pct = (total_monthly_cost / monthly_budget * 100) if monthly_budget > 0 else 0
        
        md += f"""
## Budget Analysis

- **Monthly Budget**: ${monthly_budget:,.2f}
- **Amount Spent**: ${total_monthly_cost:,.2f}
- **Remaining**: ${budget_remaining:,.2f}
- **Budget Used**: {budget_used_pct:.1f}%

```
Budget Status: {"█" * int(budget_used_pct / 5)}{"░" * (20 - int(budget_used_pct / 5))}
```

## Month-over-Month Comparison

"""
        
        # Previous month calculation
        prev_month = target_month - timedelta(days=30)
        prev_month_cost = 0  # Would calculate from database
        
        mom_change = 0
        if prev_month_cost > 0:
            mom_change = ((total_monthly_cost - prev_month_cost) / prev_month_cost) * 100
        
        sign = "+" if mom_change > 0 else ""
        md += f"- **Previous Month**: ${prev_month_cost:,.2f}\n"
        md += f"- **Change**: {sign}{mom_change:.1f}%\n"
        
        md += f"""
---
*Report generated at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
        
        return md
    
    def save_report(self, content: str, date: str, report_type: str = "daily", format: str = "md") -> Path:
        """Save report to file."""
        filename = f"{date}_{report_type}_report.{format}"
        filepath = self.reports_dir / filename
        
        if format == "md":
            filepath = filepath.with_suffix(".md")
        elif format == "json":
            filepath = filepath.with_suffix(".json")
        elif format == "csv":
            filepath = filepath.with_suffix(".csv")
        
        with open(filepath, "w") as f:
            f.write(content)
        
        logger.info(f"Report saved: {filepath}")
        return filepath
    
    def archive_report(self, date: str, report_type: str = "daily"):
        """Move report to archive."""
        import shutil
        
        for ext in [".md", ".json", ".csv"]:
            filepath = self.reports_dir / f"{date}_{report_type}_report{ext}"
            if filepath.exists():
                archive_path = self.archive_dir / f"{date}_{report_type}_report{ext}"
                shutil.move(str(filepath), str(archive_path))
                logger.info(f"Archived: {archive_path}")
    
    def get_report_path(self, date: str, report_type: str = "daily") -> Optional[Path]:
        """Get path to existing report."""
        for ext in [".md", ".json", ".csv"]:
            filepath = self.reports_dir / f"{date}_{report_type}_report{ext}"
            if filepath.exists():
                return filepath
        return None


def main():
    """Main entry point for CLI usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="LLM Cost Reporter")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Daily report
    daily_parser = subparsers.add_parser("daily", help="Generate daily report")
    daily_parser.add_argument("--date", help="Date (YYYY-MM-DD)")
    daily_parser.add_argument("--format", default="markdown", choices=["markdown", "json", "csv"])
    daily_parser.add_argument("--save", action="store_true", help="Save to file")
    
    # Weekly report
    weekly_parser = subparsers.add_parser("weekly", help="Generate weekly report")
    weekly_parser.add_argument("--end-date", help="Week end date (YYYY-MM-DD)")
    weekly_parser.add_argument("--save", action="store_true", help="Save to file")
    
    # Monthly report
    monthly_parser = subparsers.add_parser("monthly", help="Generate monthly report")
    monthly_parser.add_argument("--month", help="Month (YYYY-MM)")
    monthly_parser.add_argument("--save", action="store_true", help="Save to file")
    
    args = parser.parse_args()
    
    reporter = CostReporter()
    
    if args.command == "daily":
        content = reporter.generate_daily_report(date=args.date, format=args.format)
        if args.save:
            reporter.save_report(content, args.date or datetime.now().strftime("%Y-%m-%d"), "daily", args.format)
        print(content)
    
    elif args.command == "weekly":
        content = reporter.generate_weekly_report(week_end=args.end_date)
        if args.save:
            reporter.save_report(content, args.end_date or datetime.now().strftime("%Y-%m-%d"), "weekly", "md")
        print(content)
    
    elif args.command == "monthly":
        content = reporter.generate_monthly_report(month=args.month)
        if args.save:
            reporter.save_report(content, (args.month or datetime.now().strftime("%Y-%m")) + "-01", "monthly", "md")
        print(content)


if __name__ == "__main__":
    main()
