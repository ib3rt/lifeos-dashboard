#!/usr/bin/env python3
"""
LLM API Cost Tracker

Tracks LLM API usage across multiple providers, monitors token usage,
generates daily reports, and detects cost anomalies.
"""

import json
import yaml
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Pricing configuration
PROVIDER_PRICING = {
    "openai": {
        "gpt-4o": {"input_per_m": 2.50, "output_per_m": 10.00, "cache_discount": 0.75},
        "gpt-4o-mini": {"input_per_m": 0.15, "output_per_m": 0.60, "cache_discount": 0.75},
        "gpt-4-turbo": {"input_per_m": 10.00, "output_per_m": 30.00, "cache_discount": 0.75},
        "gpt-4": {"input_per_m": 30.00, "output_per_m": 60.00, "cache_discount": 0.0},
        "gpt-3.5-turbo": {"input_per_m": 0.50, "output_per_m": 1.50, "cache_discount": 0.50},
    },
    "anthropic": {
        "claude-3-5-sonnet": {"input_per_m": 3.00, "output_per_m": 15.00, "cache_discount": 0.90},
        "claude-3-opus": {"input_per_m": 15.00, "output_per_m": 75.00, "cache_discount": 0.90},
        "claude-3-haiku": {"input_per_m": 0.25, "output_per_m": 1.25, "cache_discount": 0.90},
    },
    "moonshot": {
        "kimi-2.5-pro": {"input_per_m": 5.00, "output_per_m": 15.00, "cache_discount": 0.50},
        "kimi-2.5-turbo": {"input_per_m": 2.00, "output_per_m": 6.00, "cache_discount": 0.50},
        "kimi-2.5-apex": {"input_per_m": 12.00, "output_per_m": 36.00, "cache_discount": 0.50},
    },
    "minimax": {
        "minimax-2.1-reasoning": {"input_per_m": 1.00, "output_per_m": 4.00, "cache_discount": 0.50},
        "minimax-2.1-standard": {"input_per_m": 2.00, "output_per_m": 6.00, "cache_discount": 0.50},
        "minimax-2.1-flash": {"input_per_m": 0.50, "output_per_m": 2.00, "cache_discount": 0.50},
    },
    "deepseek": {
        "deepseek-v2.5": {"input_per_m": 0.14, "output_per_m": 0.28, "cache_discount": 0.50},
        "deepseek-coder-v2.5": {"input_per_m": 0.14, "output_per_m": 0.28, "cache_discount": 0.50},
        "deepseek-v2": {"input_per_m": 0.27, "output_per_m": 0.55, "cache_discount": 0.50},
    },
    "google": {
        "gemini-1.5-pro": {"input_per_m": 1.25, "output_per_m": 5.00, "cache_discount": 0.75},
        "gemini-1.5-flash": {"input_per_m": 0.075, "output_per_m": 0.30, "cache_discount": 0.75},
        "gemini-1.0-pro": {"input_per_m": 0.50, "output_per_m": 1.50, "cache_discount": 0.0},
    },
}


@dataclass
class CostEntry:
    """Represents a single cost entry."""
    timestamp: str
    provider: str
    model: str
    agent: str
    task: str
    input_tokens: int
    output_tokens: int
    cached_tokens: int
    duration_ms: int
    status: str
    cost: float
    request_id: str
    session_id: str


class CostTracker:
    """Main cost tracking class."""
    
    def __init__(self, db_path: str = "costs.db", config_path: str = None):
        """Initialize the cost tracker."""
        self.db_path = db_path
        self.config_path = config_path or self._find_config()
        self.config = self._load_config()
        self._init_database()
    
    def _find_config(self) -> str:
        """Find configuration file."""
        possible_paths = [
            "config.yaml",
            "tools/cost-consultant/config.yaml",
            "/home/ubuntu/.openclaw/workspace/tools/cost-consultant/config.yaml",
        ]
        for path in possible_paths:
            if Path(path).exists():
                return path
        return "tools/cost-consultant/config.yaml"
    
    def _load_config(self) -> Dict:
        """Load configuration from YAML file."""
        default_config = {
            "budgets": {
                "daily": {"soft_limit": 50.00, "hard_limit": 75.00},
                "weekly": {"soft_limit": 300.00, "hard_limit": 450.00},
                "monthly": {"soft_limit": 1200.00, "hard_limit": 1800.00},
            },
            "alert_thresholds": {
                "warning_percentage": 0.80,
                "critical_percentage": 0.95,
            },
        }
        
        if Path(self.config_path).exists():
            with open(self.config_path) as f:
                user_config = yaml.safe_load(f)
                if user_config:
                    default_config.update(user_config)
        
        return default_config
    
    def _init_database(self):
        """Initialize SQLite database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cost_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                provider TEXT NOT NULL,
                model TEXT NOT NULL,
                agent TEXT NOT NULL,
                task TEXT NOT NULL,
                input_tokens INTEGER DEFAULT 0,
                output_tokens INTEGER DEFAULT 0,
                cached_tokens INTEGER DEFAULT 0,
                duration_ms INTEGER DEFAULT 0,
                status TEXT DEFAULT 'success',
                cost REAL DEFAULT 0.0,
                request_id TEXT UNIQUE,
                session_id TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_summary (
                date TEXT PRIMARY KEY,
                total_cost REAL,
                total_tokens INTEGER,
                total_requests INTEGER,
                providers TEXT,
                models TEXT,
                agents TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                alert_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                message TEXT,
                acknowledged INTEGER DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info(f"Database initialized at {self.db_path}")
    
    def calculate_cost(
        self,
        provider: str,
        model: str,
        input_tokens: int,
        output_tokens: int,
        cached_tokens: int = 0
    ) -> float:
        """Calculate the cost of an API call."""
        provider = provider.lower()
        model = model.lower().replace("-", "-").replace("_", "-")
        
        if provider not in PROVIDER_PRICING:
            logger.warning(f"Unknown provider: {provider}, using default pricing")
            provider = "openai"
        
        pricing = PROVIDER_PRICING.get(provider, {})
        model_pricing = pricing.get(model, {"input_per_m": 1.0, "output_per_m": 2.0, "cache_discount": 0.0})
        
        input_cost = (input_tokens / 1_000_000) * model_pricing["input_per_m"]
        output_cost = (output_tokens / 1_000_000) * model_pricing["output_per_m"]
        
        # Apply cached token discount
        if cached_tokens > 0:
            discount = model_pricing["cache_discount"]
            uncached_input = input_tokens - cached_tokens
            cached_cost = (cached_tokens / 1_000_000) * model_pricing["input_per_m"] * (1 - discount)
            uncached_cost = (uncached_input / 1_000_000) * model_pricing["input_per_m"]
            input_cost = uncached_cost + cached_cost
        
        return round(input_cost + output_cost, 6)
    
    def track_usage(
        self,
        provider: str,
        model: str,
        agent: str,
        task: str,
        input_tokens: int,
        output_tokens: int,
        duration_ms: int,
        status: str = "success",
        cached_tokens: int = 0,
        request_id: Optional[str] = None,
        session_id: Optional[str] = None,
    ) -> CostEntry:
        """Track an LLM API usage."""
        cost = self.calculate_cost(provider, model, input_tokens, output_tokens, cached_tokens)
        
        timestamp = datetime.now().isoformat()
        if request_id is None:
            request_id = f"{provider}-{int(datetime.now().timestamp())}"
        
        entry = CostEntry(
            timestamp=timestamp,
            provider=provider,
            model=model,
            agent=agent,
            task=task,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cached_tokens=cached_tokens,
            duration_ms=duration_ms,
            status=status,
            cost=cost,
            request_id=request_id,
            session_id=session_id or "",
        )
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO cost_entries (
                    timestamp, provider, model, agent, task,
                    input_tokens, output_tokens, cached_tokens,
                    duration_ms, status, cost, request_id, session_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                entry.timestamp, entry.provider, entry.model, entry.agent, entry.task,
                entry.input_tokens, entry.output_tokens, entry.cached_tokens,
                entry.duration_ms, entry.status, entry.cost, entry.request_id, entry.session_id
            ))
            
            conn.commit()
            logger.info(f"Tracked usage: {provider}/{model} - ${cost:.6f}")
            
        except sqlite3.IntegrityError:
            logger.warning(f"Duplicate request ID: {request_id}")
        
        conn.close()
        
        # Check for budget alerts
        self._check_budget_alerts()
        
        return entry
    
    def _check_budget_alerts(self):
        """Check if budget thresholds have been breached."""
        today = datetime.now().strftime("%Y-%m-%d")
        daily_cost = self.get_daily_cost(today)
        
        daily_budget = self.config["budgets"]["daily"]["soft_limit"]
        warning_threshold = daily_budget * self.config["alert_thresholds"]["warning_percentage"]
        critical_threshold = daily_budget * self.config["alert_thresholds"]["critical_percentage"]
        
        if daily_cost >= critical_threshold:
            self.create_alert(
                "budget_critical",
                "critical",
                f"Daily cost ${daily_cost:.2f} exceeds 95% of budget ${daily_budget:.2f}"
            )
        elif daily_cost >= warning_threshold:
            self.create_alert(
                "budget_warning",
                "medium",
                f"Daily cost ${daily_cost:.2f} exceeds 80% of budget ${daily_budget:.2f}"
            )
    
    def create_alert(
        self,
        alert_type: str,
        severity: str,
        message: str
    ) -> int:
        """Create an alert in the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO alerts (timestamp, alert_type, severity, message)
            VALUES (?, ?, ?, ?)
        ''', (datetime.now().isoformat(), alert_type, severity, message))
        
        alert_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        logger.warning(f"Alert created: {alert_type} - {message}")
        return alert_id
    
    def get_daily_cost(self, date: str) -> float:
        """Get total cost for a specific date."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COALESCE(SUM(cost), 0) FROM cost_entries
            WHERE timestamp LIKE ?
        ''', (f"{date}%",))
        
        total = cursor.fetchone()[0]
        conn.close()
        return float(total)
    
    def get_daily_summary(self, date: str) -> Dict:
        """Generate daily summary for a specific date."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total cost and metrics
        cursor.execute('''
            SELECT 
                COUNT(*) as requests,
                COALESCE(SUM(cost), 0) as total_cost,
                COALESCE(SUM(input_tokens), 0) as input_tokens,
                COALESCE(SUM(output_tokens), 0) as output_tokens,
                COALESCE(SUM(cached_tokens), 0) as cached_tokens,
                COALESCE(AVG(duration_ms), 0) as avg_duration
            FROM cost_entries
            WHERE timestamp LIKE ?
        ''', (f"{date}%",))
        
        row = cursor.fetchone()
        
        # Provider breakdown
        cursor.execute('''
            SELECT provider, COUNT(*), SUM(cost), SUM(input_tokens + output_tokens)
            FROM cost_entries
            WHERE timestamp LIKE ?
            GROUP BY provider
            ORDER BY SUM(cost) DESC
        ''', (f"{date}%",))
        
        provider_breakdown = [
            {"provider": r[0], "requests": r[1], "cost": r[2], "tokens": r[3]}
            for r in cursor.fetchall()
        ]
        
        # Model breakdown
        cursor.execute('''
            SELECT model, provider, COUNT(*), SUM(cost), SUM(input_tokens + output_tokens)
            FROM cost_entries
            WHERE timestamp LIKE ?
            GROUP BY model
            ORDER BY SUM(cost) DESC
        ''', (f"{date}%",))
        
        model_breakdown = [
            {"model": r[0], "provider": r[1], "requests": r[2], "cost": r[3], "tokens": r[4]}
            for r in cursor.fetchall()
        ]
        
        # Agent breakdown
        cursor.execute('''
            SELECT agent, COUNT(*), SUM(cost)
            FROM cost_entries
            WHERE timestamp LIKE ?
            GROUP BY agent
            ORDER BY SUM(cost) DESC
        ''', (f"{date}%",))
        
        agent_breakdown = [
            {"agent": r[0], "requests": r[1], "cost": r[2]}
            for r in cursor.fetchall()
        ]
        
        conn.close()
        
        total_tokens = (row[2] or 0) + (row[3] or 0)
        avg_cost_per_token = (row[1] or 0) / total_tokens if total_tokens > 0 else 0
        
        return {
            "date": date,
            "requests": row[0] or 0,
            "total_cost": row[1] or 0,
            "input_tokens": row[2] or 0,
            "output_tokens": row[3] or 0,
            "cached_tokens": row[4] or 0,
            "total_tokens": total_tokens,
            "avg_cost_per_token": avg_cost_per_token,
            "avg_duration_ms": row[5] or 0,
            "by_provider": provider_breakdown,
            "by_model": model_breakdown,
            "by_agent": agent_breakdown,
        }
    
    def detect_anomalies(self, date: str) -> List[Dict]:
        """Detect cost anomalies for a specific date."""
        anomalies = []
        summary = self.get_daily_summary(date)
        
        # Get baseline (last 7 days average)
        baseline = self._get_baseline()
        
        if not baseline:
            return anomalies
        
        # Check total cost anomaly
        cost_zscore = self._calculate_zscore(
            summary["total_cost"],
            baseline["avg_daily_cost"],
            baseline["std_daily_cost"]
        )
        
        if abs(cost_zscore) > 3:
            anomalies.append({
                "type": "cost_anomaly",
                "severity": "high",
                "metric": "total_cost",
                "value": summary["total_cost"],
                "expected": baseline["avg_daily_cost"],
                "zscore": cost_zscore,
                "message": f"Daily cost ${summary['total_cost']:.2f} is {cost_zscore:.1f}σ from average"
            })
        
        # Check per-model anomalies
        for model in summary["by_model"]:
            model_baseline = self._get_model_baseline(model["model"])
            if model_baseline:
                model_zscore = self._calculate_zscore(
                    model["cost"],
                    model_baseline["avg_cost"],
                    model_baseline["std_cost"]
                )
                
                if abs(model_zscore) > 3:
                    anomalies.append({
                        "type": "model_cost_anomaly",
                        "severity": "high",
                        "model": model["model"],
                        "value": model["cost"],
                        "expected": model_baseline["avg_cost"],
                        "zscore": model_zscore,
                        "message": f"Model {model['model']} cost ${model['cost']:.2f} is {model_zscore:.1f}σ from average"
                    })
        
        return anomalies
    
    def _get_baseline(self) -> Optional[Dict]:
        """Calculate baseline from last 7 days."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        dates = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(1, 8)]
        
        cursor.execute('''
            SELECT 
                AVG(daily_cost) as avg_daily_cost,
                AVG(daily_tokens) as avg_daily_tokens,
                AVG(daily_requests) as avg_daily_requests
            FROM (
                SELECT DATE(timestamp) as date,
                    SUM(cost) as daily_cost,
                    SUM(input_tokens + output_tokens) as daily_tokens,
                    COUNT(*) as daily_requests
                FROM cost_entries
                WHERE DATE(timestamp) IN ({})
                GROUP BY DATE(timestamp)
            )
        '''.format(",".join("?" * len(dates))), dates)
        
        row = cursor.fetchone()
        conn.close()
        
        if row and row[0]:
            return {
                "avg_daily_cost": row[0],
                "std_daily_cost": row[0] * 0.2 if row[0] > 0 else 1,
                "avg_daily_tokens": row[1],
                "avg_daily_requests": row[2],
            }
        
        return None
    
    def _get_model_baseline(self, model: str) -> Optional[Dict]:
        """Calculate baseline for a specific model."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        dates = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(1, 8)]
        
        cursor.execute('''
            SELECT AVG(daily_cost), NULL
            FROM (
                SELECT DATE(timestamp) as date, SUM(cost) as daily_cost
                FROM cost_entries
                WHERE model = ? AND DATE(timestamp) IN ({})
                GROUP BY DATE(timestamp)
            )
        '''.format(",".join("?" * len(dates))), [model] + dates)
        
        row = cursor.fetchone()
        conn.close()
        
        if row and row[0]:
            return {
                "avg_cost": row[0],
                "std_cost": row[0] * 0.2 if row[0] > 0 else 1,
            }
        
        return None
    
    def _calculate_zscore(self, value: float, mean: float, std: float) -> float:
        """Calculate z-score."""
        if std == 0:
            return 0
        return (value - mean) / std
    
    def get_weekly_trend(self) -> List[Dict]:
        """Get cost trend for the last 7 days."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        dates = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7, -1, -1)]
        
        cursor.execute('''
            SELECT DATE(timestamp) as date,
                SUM(cost) as total_cost,
                SUM(input_tokens + output_tokens) as total_tokens,
                COUNT(*) as requests
            FROM cost_entries
            WHERE DATE(timestamp) IN ({})
            GROUP BY DATE(timestamp)
            ORDER BY date ASC
        '''.format(",".join("?" * len(dates))), dates)
        
        trend = [
            {"date": r[0], "cost": r[1], "tokens": r[2], "requests": r[3]}
            for r in cursor.fetchall()
        ]
        
        conn.close()
        return trend
    
    def export_daily_report(self, date: str) -> Dict:
        """Generate a complete daily report."""
        summary = self.get_daily_summary(date)
        anomalies = self.detect_anomalies(date)
        
        # Get yesterday for comparison
        yesterday = (datetime.strptime(date, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
        yesterday_cost = self.get_daily_cost(yesterday)
        
        cost_change_pct = 0
        if yesterday_cost > 0:
            cost_change_pct = ((summary["total_cost"] - yesterday_cost) / yesterday_cost) * 100
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "report_date": date,
            "summary": {
                "total_cost": summary["total_cost"],
                "total_tokens": summary["total_tokens"],
                "avg_cost_per_token": summary["avg_cost_per_token"],
                "cost_change_vs_yesterday": round(cost_change_pct, 2),
            },
            "usage_by_model": [
                {
                    "model": m["model"],
                    "requests": m["requests"],
                    "tokens": m["tokens"],
                    "cost": round(m["cost"], 2),
                    "percentage": round((m["cost"] / summary["total_cost"] * 100) if summary["total_cost"] > 0 else 0, 1)
                }
                for m in summary["by_model"]
            ],
            "usage_by_provider": [
                {
                    "provider": p["provider"],
                    "requests": p["requests"],
                    "cost": round(p["cost"], 2),
                    "percentage": round((p["cost"] / summary["total_cost"] * 100) if summary["total_cost"] > 0 else 0, 1)
                }
                for p in summary["by_provider"]
            ],
            "usage_by_agent": [
                {
                    "agent": a["agent"],
                    "requests": a["requests"],
                    "cost": round(a["cost"], 2),
                }
                for a in summary["by_agent"]
            ],
            "alerts": anomalies,
        }
        
        return report


def main():
    """Main entry point for CLI usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="LLM Cost Tracker")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Track command
    track_parser = subparsers.add_parser("track", help="Track an API usage")
    track_parser.add_argument("--provider", required=True)
    track_parser.add_argument("--model", required=True)
    track_parser.add_argument("--agent", required=True)
    track_parser.add_argument("--task", required=True)
    track_parser.add_argument("--input-tokens", type=int, required=True)
    track_parser.add_argument("--output-tokens", type=int, required=True)
    track_parser.add_argument("--duration", type=int, required=True)
    track_parser.add_argument("--cached-tokens", type=int, default=0)
    
    # Summary command
    subparsers.add_parser("summary", help="Get daily summary")
    subparsers.add_parser("trend", help="Get weekly trend")
    
    # Report command
    report_parser = subparsers.add_parser("report", help="Generate daily report")
    report_parser.add_argument("--date", help="Date (YYYY-MM-DD, defaults to today)")
    
    # Reconcile command
    reconcile_parser = subparsers.add_parser("reconcile", help="Reconcile costs")
    reconcile_parser.add_argument("--date", help="Date to reconcile")
    
    args = parser.parse_args()
    
    tracker = CostTracker()
    
    if args.command == "track":
        tracker.track_usage(
            provider=args.provider,
            model=args.model,
            agent=args.agent,
            task=args.task,
            input_tokens=args.input_tokens,
            output_tokens=args.output_tokens,
            duration_ms=args.duration,
            cached_tokens=args.cached_tokens,
        )
    
    elif args.command == "summary":
        today = datetime.now().strftime("%Y-%m-%d")
        summary = tracker.get_daily_summary(today)
        print(json.dumps(summary, indent=2))
    
    elif args.command == "trend":
        trend = tracker.get_weekly_trend()
        print(json.dumps(trend, indent=2))
    
    elif args.command == "report":
        date = args.date or datetime.now().strftime("%Y-%m-%d")
        report = tracker.export_daily_report(date)
        print(json.dumps(report, indent=2))
    
    elif args.command == "reconcile":
        date = args.date or datetime.now().strftime("%Y-%m-%d")
        summary = tracker.get_daily_summary(date)
        anomalies = tracker.detect_anomalies(date)
        print(f"Daily Summary for {date}:")
        print(f"  Total Cost: ${summary['total_cost']:.2f}")
        print(f"  Total Tokens: {summary['total_tokens']:,}")
        print(f"  Requests: {summary['requests']}")
        if anomalies:
            print(f"  Anomalies: {len(anomalies)}")
            for a in anomalies:
                print(f"    - {a['message']}")
        else:
            print("  Anomalies: None detected")


if __name__ == "__main__":
    main()
