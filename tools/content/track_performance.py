#!/usr/bin/env python3
"""
Content Performance Tracker
Tracks and analyzes content performance across platforms.
"""

import json
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class ContentMetrics:
    content_id: str
    platform: str
    impressions: int = 0
    clicks: int = 0
    shares: int = 0
    comments: int = 0
    likes: int = 0
    conversions: int = 0
    engagement_rate: float = 0.0
    ctr: float = 0.0
    recorded_at: str = ""
    
    def calculate_rates(self):
        """Calculate derived metrics."""
        if self.impressions > 0:
            self.ctr = (self.clicks / self.impressions) * 100
            self.engagement_rate = ((self.likes + self.comments + self.shares) / self.impressions) * 100


class PerformanceTracker:
    """Track content performance across platforms."""
    
    def __init__(self):
        self.metrics: List[ContentMetrics] = []
        self.history_file = "content/metrics_history.json"
    
    def record_metrics(self, metrics: ContentMetrics):
        """Record new metrics."""
        metrics.recorded_at = datetime.now().isoformat()
        metrics.calculate_rates()
        self.metrics.append(metrics)
    
    def get_top_performing(self, metric: str = "engagement_rate", limit: int = 10) -> List[ContentMetrics]:
        """Get top performing content by metric."""
        return sorted(self.metrics, key=lambda x: getattr(x, metric, 0), reverse=True)[:limit]
    
    def get_platform_summary(self) -> Dict[str, dict]:
        """Get summary statistics by platform."""
        summary = {}
        
        for m in self.metrics:
            if m.platform not in summary:
                summary[m.platform] = {
                    "total_impressions": 0,
                    "total_clicks": 0,
                    "avg_engagement": 0,
                    "count": 0
                }
            
            platform = summary[m.platform]
            platform["total_impressions"] += m.impressions
            platform["total_clicks"] += m.clicks
            platform["count"] += 1
        
        # Calculate averages
        for platform in summary:
            data = summary[platform]
            data["avg_engagement"] = data["total_clicks"] / max(1, data["total_impressions"]) * 100
        
        return summary
    
    def generate_report(self) -> dict:
        """Generate performance report."""
        top_engagement = self.get_top_performing("engagement_rate", 5)
        top_ctr = self.get_top_performing("ctr", 5)
        platform_summary = self.get_platform_summary()
        
        return {
            "report_date": datetime.now().isoformat(),
            "total_content_tracked": len(self.metrics),
            "top_engagement": [
                {"content_id": m.content_id, "rate": m.engagement_rate}
                for m in top_engagement
            ],
            "top_ctr": [
                {"content_id": m.content_id, "rate": m.ctr}
                for m in top_ctr
            ],
            "platform_summary": platform_summary
        }
    
    def save_history(self):
        """Save metrics to history file."""
        data = {
            "last_updated": datetime.now().isoformat(),
            "metrics": [
                {
                    "content_id": m.content_id,
                    "platform": m.platform,
                    "impressions": m.impressions,
                    "clicks": m.clicks,
                    "engagement_rate": m.engagement_rate,
                    "ctr": m.ctr
                }
                for m in self.metrics
            ]
        }
        
        with open(self.history_file, 'w') as f:
            json.dump(data, f, indent=2)


def main():
    # Example usage
    tracker = PerformanceTracker()
    
    # Record sample metrics
    tracker.record_metrics(ContentMetrics(
        content_id="blog-001",
        platform="blog",
        impressions=1000,
        clicks=50,
        shares=20,
        comments=10
    ))
    
    tracker.record_metrics(ContentMetrics(
        content_id="social-001",
        platform="twitter",
        impressions=5000,
        clicks=200,
        shares=100,
        comments=50
    ))
    
    # Generate report
    report = tracker.generate_report()
    print(json.dumps(report, indent=2))
    
    tracker.save_history()


if __name__ == "__main__":
    main()
