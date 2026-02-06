#!/usr/bin/env python3
"""
ROI Calculator - Investment Return Analysis

Usage:
    python roi_calculator.py --cost 50000 --return 80000 --months 12
    python roi_calculator.py --file investments.json --compare
"""

import argparse
import json
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class Investment:
    name: str
    initial_cost: float
    expected_return: float
    timeline_months: int
    operating_cost_monthly: float = 0
    risk_adjustment: float = 0.1  # 10% risk discount
    category: str = "general"
    
    def __hash__(self):
        return hash(self.name)


class ROICalculator:
    def __init__(self, discount_rate: float = 0.1):
        self.discount_rate = discount_rate
    
    def calculate_roi(self, inv: Investment) -> Dict:
        """Calculate ROI metrics for an investment"""
        total_operating = inv.operating_cost_monthly * inv.timeline_months
        gross_return = inv.expected_return
        net_return = gross_return - inv.initial_cost - total_operating
        
        # Basic ROI
        roi = (net_return / inv.initial_cost) * 100 if inv.initial_cost > 0 else 0
        
        # Risk-adjusted ROI
        risk_discount = inv.risk_adjustment
        adjusted_return = gross_return * (1 - risk_discount)
        adjusted_net = adjusted_return - inv.initial_cost - total_operating
        risk_adjusted_roi = (adjusted_net / inv.initial_cost) * 100 if inv.initial_cost > 0 else 0
        
        # Payback period
        monthly_net = (inv.expected_return / inv.timeline_months) - inv.operating_cost_monthly
        payback = inv.initial_cost / monthly_net if monthly_net > 0 else float('inf')
        
        # NPV (Net Present Value)
        npv = self._calculate_npv(inv)
        
        # IRR (Internal Rate of Return) - simplified approximation
        irr = self._approximate_irr(inv)
        
        return {
            "name": inv.name,
            "roi_percent": round(roi, 2),
            "risk_adjusted_roi": round(risk_adjusted_roi, 2),
            "payback_months": round(payback, 1) if payback < float('inf') else None,
            "npv": round(npv, 2),
            "irr_percent": round(irr, 2) if irr else None,
            "net_return": round(net_return, 2),
            "total_investment": round(inv.initial_cost, 2),
            "total_operating_cost": round(total_operating, 2),
            "gross_return": round(gross_return, 2),
            "recommendation": self._recommend(roi, risk_adjusted_roi)
        }
    
    def _calculate_npv(self, inv: Investment) -> float:
        """Calculate NPV using discount rate"""
        npv = -inv.initial_cost
        monthly_return = inv.expected_return / inv.timeline_months
        
        for month in range(1, inv.timeline_months + 1):
            cash_flow = monthly_return - inv.operating_cost_monthly
            # Discount factor: 1 / (1 + r)^n
            discount_factor = 1 / ((1 + self.discount_rate) ** (month / 12))
            npv += cash_flow * discount_factor
        
        return npv
    
    def _approximate_irr(self, inv: Investment) -> Optional[float]:
        """Approximate IRR using simple method"""
        if inv.initial_cost == 0:
            return None
        
        # Initial investment is negative
        cash_flows = [-inv.initial_cost]
        monthly_return = inv.expected_return / inv.timeline_months
        for _ in range(inv.timeline_months):
            cash_flows.append(monthly_return - inv.operating_cost_monthly)
        
        # Simple IRR approximation
        total_cash_in = sum(cf for cf in cash_flows if cf > 0)
        total_cash_out = abs(sum(cf for cf in cash_flows if cf < 0))
        
        if total_cash_out == 0:
            return None
        
        # Annualized return
        annual_gain = (total_cash_in - total_cash_out) / total_cash_out
        years = inv.timeline_months / 12
        annualized = ((1 + annual_gain) ** (1 / years) - 1) * 100 if years > 0 else 0
        
        return annualized
    
    def _recommend(self, roi: float, risk_roi: float) -> str:
        if risk_roi > 50:
            return "✅ Strong investment - prioritize"
        elif risk_roi > 30:
            return "✅ Good investment - proceed"
        elif risk_roi > 15:
            return "⚠️ Moderate return - consider with alternatives"
        elif risk_roi > 0:
            return "⚠️ Low return - proceed with caution"
        return "❌ Negative return - do not proceed"
    
    def compare_investments(self, investments: List[Investment]) -> str:
        """Compare multiple investments"""
        results = []
        for inv in investments:
            results.append(self.calculate_roi(inv))
        
        # Sort by risk-adjusted ROI
        sorted_results = sorted(results, key=lambda x: x['risk_adjusted_roi'], reverse=True)
        
        table = f"""# Investment Comparison Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Ranked by Risk-Adjusted ROI

| Rank | Investment | ROI | Risk-Adj ROI | NPV | Payback | Recommendation |
|------|------------|-----|--------------|-----|---------|----------------|
"""
        for i, r in enumerate(sorted_results, 1):
            payback = f"{r['payback_months']} mo" if r['payback_months'] else "N/A"
            table += f"| {i} | {r['name']} | {r['roi_percent']}% | {r['risk_adjusted_roi']}% | ${r['npv']:,.0f} | {payback} | {r['recommendation'][:20]} |\n"
        
        table += """
## Analysis Summary

"""
        best = sorted_results[0] if sorted_results else None
        if best:
            table += f"**Top Investment:** {best['name']} with {best['risk_adjusted_roi']}% risk-adjusted ROI\n\n"
        
        total_investment = sum(inv.initial_cost for inv in investments)
        table += f"**Total Investment Required:** ${total_investment:,.0f}\n"
        
        # Category breakdown
        by_category = {}
        for inv in investments:
            if inv.category not in by_category:
                by_category[inv.category] = []
            by_category[inv.category].append(self.calculate_roi(inv))
        
        table += "\n### By Category\n"
        for cat, cat_results in by_category.items():
            avg_roi = sum(r['risk_adjusted_roi'] for r in cat_results) / len(cat_results)
            table += f"- **{cat}:** {len(cat_results)} investments, avg {avg_roi:.1f}% ROI\n"
        
        return table


def main():
    parser = argparse.ArgumentParser(description='ROI Calculator')
    parser.add_argument('--cost', '-c', type=float, help='Initial investment cost')
    parser.add_argument('--return', '-r', dest='return_val', type=float, help='Expected return')
    parser.add_argument('--months', '-m', type=int, default=12, help='Timeline in months')
    parser.add_argument('--operating', '-o', type=float, default=0, help='Monthly operating cost')
    parser.add_argument('--name', '-n', default='Investment', help='Investment name')
    parser.add_argument('--risk', type=float, default=0.1, help='Risk adjustment (0-1)')
    parser.add_argument('--category', default='general', help='Investment category')
    parser.add_argument('--compare', action='store_true', help='Compare multiple')
    parser.add_argument('--file', '-f', help='Input JSON file')
    parser.add_argument('--output', type=str, help='Output file')
    
    args = parser.parse_args()
    
    calculator = ROICalculator()
    
    if args.compare or args.file:
        # Load from file or use defaults
        if args.file:
            with open(args.file) as f:
                data = json.load(f)
                investments = [Investment(**inv) for inv in data]
        else:
            # Default examples
            investments = [
                Investment(name="Marketing Campaign", initial_cost=20000, 
                          expected_return=35000, timeline_months=6,
                          operating_cost_monthly=500, category="marketing"),
                Investment(name="New Feature", initial_cost=30000,
                          expected_return=50000, timeline_months=12,
                          operating_cost_monthly=1000, category="product"),
                Investment(name="Infrastructure", initial_cost=15000,
                          expected_return=20000, timeline_months=12,
                          operating_cost_monthly=200, category="infrastructure")
            ]
        
        output = calculator.compare_investments(investments)
    else:
        if not args.cost or not args.return_val:
            parser.error("--cost and --return are required for single investment")
        
        inv = Investment(
            name=args.name,
            initial_cost=args.cost,
            expected_return=args.return_val,
            timeline_months=args.months,
            operating_cost_monthly=args.operating,
            risk_adjustment=args.risk,
            category=args.category
        )
        
        result = calculator.calculate_roi(inv)
        
        output = f"""# ROI Analysis: {inv.name}

## Investment Details
- **Initial Cost:** ${inv.initial_cost:,.2f}
- **Expected Return:** ${inv.expected_return:,.2f}
- **Timeline:** {inv.timeline_months} months
- **Monthly Operating Cost:** ${inv.operating_cost_monthly:,.2f}
- **Risk Adjustment:** {inv.risk_adjustment * 100}%

## Results

| Metric | Value |
|--------|-------|
| **ROI** | {result['roi_percent']}% |
| **Risk-Adjusted ROI** | {result['risk_adjusted_roi']}% |
| **Net Present Value (NPV)** | ${result['npv']:,.2f} |
| **Internal Rate of Return (IRR)** | {result['irr_percent']}% |
| **Payback Period** | {result['payback_months']} months |
| **Net Return** | ${result['net_return']:,.2f} |

## Recommendation

{result['recommendation']}

---
"""
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Report saved to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
