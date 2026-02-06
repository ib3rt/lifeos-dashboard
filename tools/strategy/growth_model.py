#!/usr/bin/env python3
"""
Growth Model - Project growth trajectories and model scenarios

Usage:
    python growth_model.py --project 24
    python growth_model.py --scenario aggressive
    python growth_model.py --compare
"""

import argparse
import json
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class GrowthInputs:
    initial_users: float = 1000
    monthly_growth_rate: float = 0.05  # 5% MoM
    conversion_rate: float = 0.03     # 3% to paid
    avg_revenue_per_user: float = 29.0
    churn_rate: float = 0.02           # 2% monthly
    referral_rate: float = 0.1         # 10% refer others
    expansion_rate: float = 0.02      # 2% upsell

@dataclass
class GrowthScenario:
    name: str
    inputs: GrowthInputs

class GrowthModel:
    def __init__(self, inputs: GrowthInputs):
        self.inputs = inputs
    
    def project(self, months: int = 24) -> Dict:
        """Project growth over N months"""
        projections = []
        users = self.inputs.initial_users
        
        for month in range(1, months + 1):
            # Organic growth
            new_users = users * self.inputs.monthly_growth_rate
            
            # Referral growth
            referred_users = users * self.inputs.referral_rate
            
            # Total additions
            total_users = users + new_users + referred_users
            
            # Churn
            churned = total_users * self.inputs.churn_rate
            active_users = total_users - churned
            
            # Revenue
            paying_users = active_users * self.inputs.conversion_rate
            revenue = paying_users * self.inputs.avg_revenue_per_user
            
            # Expansion revenue
            expansion_revenue = revenue * self.inputs.expansion_rate
            
            projections.append({
                "month": month,
                "total_users": round(total_users, 0),
                "active_users": round(active_users, 0),
                "paying_users": round(paying_users, 0),
                "mrr": round(revenue + expansion_revenue, 2),
                "new_users": round(new_users, 0),
                "churned": round(churned, 0)
            })
            
            users = active_users
        
        return {
            "projections": projections,
            "summary": self._summarize(projections),
            "inputs": {
                "initial_users": self.inputs.initial_users,
                "growth_rate": self.inputs.monthly_growth_rate,
                "conversion_rate": self.inputs.conversion_rate,
                "churn_rate": self.inputs.churn_rate
            }
        }
    
    def _summarize(self, projections: List[Dict]) -> Dict:
        final = projections[-1]
        return {
            "final_month": len(projections),
            "final_users": final["active_users"],
            "final_mrr": final["mrr"],
            "total_new_users": sum(p["new_users"] for p in projections),
            "total_revenue": sum(p["mrr"] for p in projections),
            "cagr": self._calculate_cagr(
                self.inputs.initial_users,
                final["active_users"],
                len(projections)
            )
        }
    
    def _calculate_cagr(self, start: float, end: float, months: int) -> float:
        if start == 0:
            return 0
        years = months / 12
        return ((end / start) ** (1 / years) - 1) * 100 if years > 0 else 0
    
    def doubling_time(self) -> float:
        """Calculate months to double users"""
        return 72 / (self.inputs.monthly_growth_rate * 100)
    
    def runway_analysis(self, target_mrr: float) -> int:
        """Find months to reach target MRR"""
        users = self.inputs.initial_users
        month = 0
        while month < 120:  # Cap at 10 years
            users *= (1 + self.inputs.monthly_growth_rate - self.inputs.churn_rate)
            paying = users * self.inputs.conversion_rate
            mrr = paying * self.inputs.avg_revenue_per_user
            if mrr >= target_mrr:
                return month
            month += 1
        return 120


class ScenarioComparer:
    def __init__(self):
        self.scenarios: Dict[str, GrowthScenario] = {}
    
    def add_scenario(self, scenario: GrowthScenario):
        self.scenarios[scenario.name] = scenario
    
    def compare(self, months: int = 24) -> str:
        results = {}
        for name, scenario in self.scenarios.items():
            model = GrowthModel(scenario.inputs)
            results[name] = model.project(months)
        
        # Generate comparison table
        table = "# Growth Scenario Comparison\n\n"
        table += f"| Metric | {' | '.join(results.keys())} |\n"
        table += f"|---|{'---|' * len(results)}\n"
        
        metrics = [
            ("Final Users", lambda r: f"{r['summary']['final_users']:,.0f}"),
            ("Final MRR", lambda r: f"${r['summary']['final_mrr']:,.0f}"),
            ("Total Revenue", lambda r: f"${r['summary']['total_revenue']:,.0f}"),
            ("CAGR", lambda r: f"{r['summary']['cagr']:.1f}%")
        ]
        
        for metric_name, formatter in metrics:
            row = f"| {metric_name} | "
            row += " | ".join(formatter(results[name]) for name in self.scenarios.keys())
            table += row + " |\n"
        
        return table


def main():
    parser = argparse.ArgumentParser(description='Growth Model Projector')
    parser.add_argument('--project', '-p', type=int, default=24, 
                       help='Number of months to project')
    parser.add_argument('--inputs', '-i', type=str,
                       help='Input JSON file with growth parameters')
    parser.add_argument('--scenario', '-s', default='conservative',
                       choices=['conservative', 'moderate', 'aggressive'],
                       help='Predefined scenario')
    parser.add_argument('--compare', '-c', action='store_true',
                       help='Compare all scenarios')
    parser.add_argument('--output', '-o', type=str,
                       help='Output JSON file')
    
    args = parser.parse_args()
    
    # Define scenarios
    scenarios = {
        'conservative': GrowthInputs(
            initial_users=1000,
            monthly_growth_rate=0.03,
            conversion_rate=0.02,
            churn_rate=0.03,
            referral_rate=0.05
        ),
        'moderate': GrowthInputs(
            initial_users=1000,
            monthly_growth_rate=0.05,
            conversion_rate=0.03,
            churn_rate=0.02,
            referral_rate=0.10
        ),
        'aggressive': GrowthInputs(
            initial_users=1000,
            monthly_growth_rate=0.08,
            conversion_rate=0.04,
            churn_rate=0.015,
            referral_rate=0.15
        )
    }
    
    if args.compare:
        comparer = ScenarioComparer()
        for name, inputs in scenarios.items():
            comparer.add_scenario(GrowthScenario(name, inputs))
        print(comparer.compare(args.project))
    else:
        inputs = scenarios[args.scenario]
        if args.inputs:
            with open(args.inputs) as f:
                data = json.load(f)
                inputs = GrowthInputs(**data)
        
        model = GrowthModel(inputs)
        result = model.project(args.project)
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"Results saved to {args.output}")
        else:
            print(json.dumps(result, indent=2))
        
        print(f"\n📊 {args.scenario.title()} Scenario Summary:")
        print(f"  Final Users: {result['summary']['final_users']:,.0f}")
        print(f"  Final MRR: ${result['summary']['final_mrr']:,.0f}")
        print(f"  Doubling Time: {model.doubling_time():.1f} months")


if __name__ == "__main__":
    main()
