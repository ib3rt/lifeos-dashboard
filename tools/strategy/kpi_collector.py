#!/usr/bin/env python3
"""
KPI Collector - Automated Collection KPI and Alert System

Usage:
    python kpi_collector.py --config kpi_config.yaml
    python kpi_collector.py --check-all
    python kpi_collector.py --alert
"""

import argparse
import json
import yaml
from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum
import sys

class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

@dataclass
class KPIThreshold:
    name: str
    warning_value: float
    critical_value: float
    direction: str = "higher"  # "higher" or "lower" is better
    
    def check(self, value: float) -> tuple[AlertSeverity, str]:
        if self.direction == "higher":
            if value <= self.critical_value:
                return (AlertSeverity.CRITICAL, 
                       f"CRITICAL: {self.name} is {value} (target: >{self.critical_value})")
            elif value <= self.warning_value:
                return (AlertSeverity.WARNING, 
                       f"WARNING: {self.name} is {value} (target: >{self.warning_value})")
        else:
            if value >= self.critical_value:
                return (AlertSeverity.CRITICAL, 
                       f"CRITICAL: {self.name} is {value} (target: <{self.critical_value})")
            elif value >= self.warning_value:
                return (AlertSeverity.WARNING, 
                       f"WARNING: {self.name} is {value} (target: <{self.warning_value})")
        return (AlertSeverity.INFO, f"OK: {self.name} is {value}")

@dataclass
class KPI:
    name: str
    category: str
    value: float
    target: float
    unit: str = ""
    source: str = ""

class KPICollector:
    def __init__(self, config_file: str = None):
        self.kpis: Dict[str, KPI] = {}
        self.thresholds: Dict[str, KPIThreshold] = {}
        self.alert_history: List[dict] = []
        self.last_check: datetime = None
        
        if config_file:
            self.load_config(config_file)
    
    def load_config(self, config_file: str):
        """Load KPI configuration from YAML file"""
        try:
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)
                
            # Load thresholds
            for kpi_name, kpi_config in config.get('kpis', {}).items():
                self.add_threshold(KPIThreshold(
                    name=kpi_name,
                    warning_value=kpi_config.get('threshold_warning', 0),
                    critical_value=kpi_config.get('threshold_critical', 0),
                    direction=kpi_config.get('direction', 'higher')
                ))
        except FileNotFoundError:
            print(f"Config file {config_file} not found")
        except Exception as e:
            print(f"Error loading config: {e}")
    
    def add_threshold(self, threshold: KPIThreshold):
        self.thresholds[threshold.name] = threshold
    
    def add_kpi(self, kpi: KPI):
        self.kpis[kpi.name] = kpi
    
    def check_all(self) -> List[dict]:
        """Check all KPIs against thresholds"""
        alerts = []
        for name, kpi in self.kpis.items():
            if name in self.thresholds:
                severity, message = self.thresholds[name].check(kpi.value)
                if severity != AlertSeverity.INFO:
                    alert = {
                        "kpi": name,
                        "value": kpi.value,
                        "severity": severity.value,
                        "message": message,
                        "timestamp": datetime.now().isoformat()
                    }
                    alerts.append(alert)
                    self.alert_history.append(alert)
        self.last_check = datetime.now()
        return alerts
    
    def generate_report(self) -> str:
        """Generate KPI status report"""
        report = f"# KPI Report - {datetime.now().strftime('%Y-%m-%d')}\n\n"
        
        # Group by category
        by_category = {}
        for kpi in self.kpis.values():
            if kpi.category not in by_category:
                by_category[kpi.category] = []
            by_category[kpi.category].append(kpi)
        
        for category, kpi_list in by_category.items():
            report += f"## {category.upper()}\n\n"
            report += "| KPI | Current | Target | Progress | Status |\n"
            report += "|-----|---------|--------|----------|--------|\n"
            
            for kpi in kpi_list:
                progress = min((kpi.value / kpi.target) * 100, 100) if kpi.target > 0 else 0
                status = "✅" if progress >= 90 else ("⚠️" if progress >= 70 else "🔴")
                report += f"| {kpi.name} | {kpi.value:.2f} | {kpi.target:.2f} | {progress:.0f}% | {status} |\n"
            report += "\n"
        
        # Add alerts
        alerts = self.check_all()
        if alerts:
            report += f"## Active Alerts ({len(alerts)})\n\n"
            for alert in alerts:
                emoji = "🚨" if alert['severity'] == 'critical' else ("⚠️" if alert['severity'] == 'warning' else "ℹ️")
                report += f"{emoji} {alert['message']}\n"
        else:
            report += "## Status\n\n✅ All KPIs are within healthy thresholds.\n"
        
        return report
    
    def export_json(self) -> str:
        """Export KPI data as JSON"""
        data = {
            "timestamp": datetime.now().isoformat(),
            "kpis": {
                name: {
                    "value": kpi.value,
                    "target": kpi.target,
                    "category": kpi.category,
                    "unit": kpi.unit
                }
                for name, kpi in self.kpis.items()
            },
            "alerts": self.check_all()
        }
        return json.dumps(data, indent=2)


def main():
    parser = argparse.ArgumentParser(description='KPI Collector and Alert System')
    parser.add_argument('--config', '-c', default='kpi_config.yaml', help='Config file path')
    parser.add_argument('--check-all', action='store_true', help='Check all configured KPIs')
    parser.add_argument('--report', '-r', action='store_true', help='Generate markdown report')
    parser.add_argument('--json', '-j', action='store_true', help='Export as JSON')
    parser.add_argument('--add-kpi', nargs=4, metavar=('NAME', 'VALUE', 'TARGET', 'CATEGORY'),
                       help='Add a KPI manually')
    
    args = parser.parse_args()
    
    collector = KPICollector(args.config)
    
    if args.add_kpi:
        name, value, target, category = args.add_kpi
        collector.add_kpi(KPI(
            name=name,
            value=float(value),
            target=float(target),
            category=category
        ))
    
    if args.report:
        print(collector.generate_report())
    elif args.json:
        print(collector.export_json())
    elif args.check_all:
        alerts = collector.check_all()
        if alerts:
            print(f"Found {len(alerts)} alerts:")
            for alert in alerts:
                print(f"  [{alert['severity'].upper()}] {alert['message']}")
        else:
            print("No alerts - all KPIs healthy")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
