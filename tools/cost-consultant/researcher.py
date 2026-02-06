#!/usr/bin/env python3
"""
LLM Cost Researcher

Handles market research on LLM pricing, identifies alternative models,
analyzes optimization opportunities, and monitors technology trends.
"""

import json
import yaml
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Make httpx optional - only used for HTTP requests
try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False
    logger.info("httpx not available - HTTP features disabled")


@dataclass
class ModelComparison:
    """Comparison between two models."""
    current_model: str
    candidate_model: str
    current_cost: float
    candidate_cost: float
    savings_potential: float
    suitability_score: float
    recommendation: str
    notes: str


@dataclass
class OptimizationOpportunity:
    """An optimization opportunity."""
    id: str
    title: str
    description: str
    category: str
    priority: str  # high, medium, low
    estimated_savings: float
    implementation_effort: str  # easy, medium, hard
    affected_models: List[str]
    affected_tasks: List[str]
    recommendation: str


class CostResearcher:
    """Research and optimization analysis class."""
    
    def __init__(self, config_path: str = None):
        """Initialize the researcher."""
        self.config_path = config_path or self._find_config()
        self.config = self._load_config()
        self._init_cache()
    
    def _find_config(self) -> str:
        """Find configuration file."""
        possible_paths = [
            "tools/cost-consultant/config.yaml",
            "/home/ubuntu/.openclaw/workspace/tools/cost-consultant/config.yaml",
        ]
        for path in possible_paths:
            if Path(path).exists():
                return path
        return "tools/cost-consultant/config.yaml"
    
    def _load_config(self) -> Dict:
        """Load configuration."""
        default_config = {
            "min_savings_threshold": 0.10,  # 10% minimum savings to recommend
            "max_switch_overhead": 0.05,  # 5% max quality degradation allowed
            "cache_ttl_hours": 24,
            "research_interval_hours": 6,
            "model_replacements": {
                "gpt-4": ["claude-3-5-sonnet", "gemini-1.5-pro"],
                "gpt-3.5-turbo": ["claude-3-haiku", "minimax-2.1-flash"],
                "claude-3-opus": ["gpt-4o", "claude-3-5-sonnet"],
                "kimi-2.5-pro": ["minimax-2.1-standard", "deepseek-v2.5"],
            },
            "task_routing": {
                "code_generation": ["deepseek-coder", "claude-3-5-sonnet"],
                "reasoning": ["claude-3-opus", "gpt-4o"],
                "simple_chat": ["claude-3-haiku", "minimax-2.1-flash"],
                "summarization": ["claude-3-sonnet", "gpt-4o-mini"],
                "analysis": ["claude-3-5-sonnet", "gpt-4o"],
            },
        }
        
        if Path(self.config_path).exists():
            with open(self.config_path) as f:
                user_config = yaml.safe_load(f)
                if user_config:
                    default_config.update(user_config)
        
        return default_config
    
    def _init_cache(self):
        """Initialize research cache."""
        self.cache_file = Path("research_cache.json")
        self.cache = {}
        
        if self.cache_file.exists():
            try:
                with open(self.cache_file) as f:
                    self.cache = json.load(f)
                logger.info(f"Loaded research cache with {len(self.cache)} entries")
            except Exception as e:
                logger.warning(f"Failed to load cache: {e}")
                self.cache = {}
    
    def _save_cache(self):
        """Save research cache."""
        with open(self.cache_file, "w") as f:
            json.dump(self.cache, f, indent=2)
        logger.info(f"Saved research cache with {len(self.cache)} entries")
    
    async def fetch_pricing(self, provider: str) -> Dict:
        """Fetch current pricing for a provider."""
        cache_key = f"pricing_{provider}"
        
        if cache_key in self.cache:
            cached = self.cache[cache_key]
            if (datetime.now() - datetime.fromisoformat(cached["timestamp"])).hours < self.config["cache_ttl_hours"]:
                logger.info(f"Using cached pricing for {provider}")
                return cached["data"]
        
        # In production, this would call actual provider APIs
        # For now, we return hardcoded current pricing
        pricing_data = {
            "openai": {
                "gpt-4o": {"input_per_m": 2.50, "output_per_m": 10.00, "updated": datetime.now().isoformat()},
                "gpt-4o-mini": {"input_per_m": 0.15, "output_per_m": 0.60, "updated": datetime.now().isoformat()},
            },
            "anthropic": {
                "claude-3-5-sonnet": {"input_per_m": 3.00, "output_per_m": 15.00, "updated": datetime.now().isoformat()},
                "claude-3-opus": {"input_per_m": 15.00, "output_per_m": 75.00, "updated": datetime.now().isoformat()},
            },
        }
        
        self.cache[cache_key] = {
            "timestamp": datetime.now().isoformat(),
            "data": pricing_data.get(provider, {}),
        }
        
        self._save_cache()
        return pricing_data.get(provider, {})
    
    async def research_pricing_trends(self) -> Dict:
        """Research recent pricing changes and trends."""
        # In production, this would analyze market data
        return {
            "last_updated": datetime.now().isoformat(),
            "trends": [
                {
                    "provider": "OpenAI",
                    "change": "gpt-4o-mini introduced",
                    "impact": "New low-cost option for simple tasks",
                    "date": "2024-07-18",
                },
                {
                    "provider": "Anthropic",
                    "change": "Claude 3.5 Sonnet pricing reduced",
                    "impact": "50% price reduction for intermediate tasks",
                    "date": "2024-06-21",
                },
                {
                    "provider": "Google",
                    "change": "Gemini 1.5 Flash launched",
                    "impact": "Ultra-low cost option ($0.075/1M input)",
                    "date": "2024-05-24",
                },
            ],
            "recommendations": [
                "Consider migrating simple chat tasks to gpt-4o-mini or Gemini 1.5 Flash",
                "Claude 3.5 Sonnet offers good value for reasoning tasks",
                "DeepSeek models provide excellent cost-performance for coding",
            ],
        }
    
    async def find_model_alternatives(
        self,
        current_model: str,
        use_case: str = "general",
        min_quality_threshold: float = 0.8,
    ) -> List[ModelComparison]:
        """Find alternative models for a given use case."""
        alternatives = []
        
        # Get known replacements from config
        replacements = self.config.get("model_replacements", {})
        candidates = replacements.get(current_model, [])
        
        # Also get task-specific recommendations
        task_routing = self.config.get("task_routing", {})
        task_alternatives = task_routing.get(use_case, [])
        
        # Combine and deduplicate
        all_candidates = list(set(candidates + task_alternatives))
        
        # Pricing reference (simplified)
        pricing = {
            "gpt-4o": {"input": 2.50, "output": 10.00, "quality": 0.95},
            "gpt-4o-mini": {"input": 0.15, "output": 0.60, "quality": 0.85},
            "claude-3-5-sonnet": {"input": 3.00, "output": 15.00, "quality": 0.93},
            "claude-3-opus": {"input": 15.00, "output": 75.00, "quality": 0.98},
            "claude-3-haiku": {"input": 0.25, "output": 1.25, "quality": 0.82},
            "gemini-1.5-pro": {"input": 1.25, "output": 5.00, "quality": 0.90},
            "gemini-1.5-flash": {"input": 0.075, "output": 0.30, "quality": 0.80},
            "minimax-2.1-standard": {"input": 2.00, "output": 6.00, "quality": 0.85},
            "minimax-2.1-flash": {"input": 0.50, "output": 2.00, "quality": 0.78},
            "deepseek-v2.5": {"input": 0.14, "output": 0.28, "quality": 0.82},
            "deepseek-coder-v2.5": {"input": 0.14, "output": 0.28, "quality": 0.88},
        }
        
        current_pricing = pricing.get(current_model, {"input": 10.00, "output": 30.00, "quality": 0.90})
        current_cost_per_1k = (current_pricing["input"] + current_pricing["output"]) / 2
        
        for candidate in all_candidates:
            if candidate == current_model or candidate not in pricing:
                continue
            
            cand_pricing = pricing[candidate]
            cand_cost_per_1k = (cand_pricing["input"] + cand_pricing["output"]) / 2
            
            # Calculate savings potential
            savings_pct = ((current_cost_per_1k - cand_cost_per_1k) / current_cost_per_1k) * 100
            quality_ratio = cand_pricing["quality"] / current_pricing["quality"]
            
            # Suitability score combines savings and quality
            suitability = min(quality_ratio, 1.0) * (1 + savings_pct / 100) if savings_pct > 0 else quality_ratio
            
            # Generate recommendation
            if savings_pct > 50 and quality_ratio > 0.9:
                recommendation = "Strongly recommended - significant savings with minimal quality loss"
            elif savings_pct > 20:
                recommendation = "Recommended - good savings opportunity"
            elif savings_pct > 0:
                recommendation = "Consider for specific use cases"
            else:
                recommendation = "Not recommended - higher cost than current model"
            
            notes = ""
            if quality_ratio < min_quality_threshold:
                notes = "Quality may be below threshold - test first"
            if savings_pct < 0:
                notes = "This model is more expensive - consider only if quality improves significantly"
            
            alternatives.append(ModelComparison(
                current_model=current_model,
                candidate_model=candidate,
                current_cost=current_cost_per_1k,
                candidate_cost=cand_cost_per_1k,
                savings_potential=round(savings_pct, 2),
                suitability_score=round(suitability, 3),
                recommendation=recommendation,
                notes=notes,
            ))
        
        # Sort by suitability
        alternatives.sort(key=lambda x: x.suitability_score, reverse=True)
        
        return [asdict(a) for a in alternatives]
    
    def analyze_caching_opportunities(
        self,
        recent_requests: List[Dict],
        similarity_threshold: float = 0.85,
    ) -> List[OptimizationOpportunity]:
        """Identify opportunities for response caching."""
        opportunities = []
        
        # Group similar requests
        request_groups = {}
        
        for req in recent_requests:
            key = req.get("task_type", "general")
            if key not in request_groups:
                request_groups[key] = []
            request_groups[key].append(req)
        
        # Analyze each group for caching opportunities
        for task_type, requests in request_groups.items():
            if len(requests) < 10:
                continue
            
            # Check for repeated patterns
            unique_prompts = len(set(r.get("prompt_hash", "") for r in requests))
            repeat_rate = 1 - (unique_prompts / len(requests))
            
            if repeat_rate > 0.3:  # 30% repetition
                savings_estimate = sum(r.get("cost", 0) for r in requests) * repeat_rate * 0.5
                
                opportunities.append(OptimizationOpportunity(
                    id=f"cache-{task_type}",
                    title=f"Cache responses for {task_type} queries",
                    description=f"Found {int(repeat_rate * 100)}% repeat rate in {task_type} queries. "
                               f"Implementing semantic caching could reduce costs.",
                    category="caching",
                    priority="medium" if savings_estimate > 10 else "low",
                    estimated_savings=round(savings_estimate, 2),
                    implementation_effort="medium",
                    affected_models=["all"],
                    affected_tasks=[task_type],
                    recommendation="Implement semantic cache with embeddings for similar queries",
                ))
        
        return [asdict(o) for o in opportunities]
    
    def analyze_batching_opportunities(
        self,
        recent_requests: List[Dict],
        time_window_minutes: int = 5,
    ) -> List[OptimizationOpportunity]:
        """Identify opportunities for request batching."""
        opportunities = []
        
        # Group requests by time window
        time_buckets = {}
        
        for req in recent_requests:
            timestamp = req.get("timestamp", "")
            try:
                dt = datetime.fromisoformat(timestamp)
                bucket = dt.strftime("%Y-%m-%d %H:%M")
                if bucket not in time_buckets:
                    time_buckets[bucket] = []
                time_buckets[bucket].append(req)
            except Exception:
                continue
        
        # Find consecutive small requests
        small_request_count = 0
        total_small_cost = 0
        
        for bucket, requests in sorted(time_buckets.items()):
            for req in requests:
                cost = req.get("cost", 0)
                if cost < 0.01:  # Less than 1 cent
                    small_request_count += 1
                    total_small_cost += cost
        
        if small_request_count > 100 and total_small_cost > 0.50:
            opportunities.append(OptimizationOpportunity(
                id="batch-small-requests",
                title="Batch small API requests",
                description=f"Found {small_request_count} small requests (<$0.01) totaling ${total_small_cost:.2f}. "
                           "Batching could reduce overhead.",
                category="batching",
                priority="low",
                estimated_savings=round(total_small_cost * 0.2, 2),  # 20% savings estimate
                implementation_effort="easy",
                affected_models=["gpt-4o", "claude-3-5-sonnet"],
                affected_tasks=["general"],
                recommendation="Use batch API endpoints for non-urgent small requests",
            ))
        
        return [asdict(o) for o in opportunities]
    
    def identify_optimization_opportunities(
        self,
        usage_data: Dict,
    ) -> List[OptimizationOpportunity]:
        """Identify all optimization opportunities from usage data."""
        opportunities = []
        
        # Analyze by model
        model_usage = usage_data.get("by_model", [])
        
        for model_data in model_usage:
            model = model_data.get("model", "")
            cost = model_data.get("cost", 0)
            requests = model_data.get("requests", 0)
            
            # Check for expensive models that could be downscaled
            expensive_models = ["gpt-4", "claude-3-opus", "kimi-2.5-apex"]
            
            if any(exp in model.lower() for exp in expensive_models):
                if cost > 20:  # Significant spend
                    alternatives = self.find_model_alternatives(model)
                    if alternatives:
                        best_alt = alternatives[0]
                        if best_alt.get("savings_potential", 0) > 20:
                            opportunities.append(OptimizationOpportunity(
                                id=f"downscale-{model}",
                                title=f"Downscale {model} to cheaper alternative",
                                description=f"Current spend: ${cost:.2f}. "
                                           f"Consider {best_alt['candidate_model']} for potential savings.",
                                category="model-selection",
                                priority="high" if cost > 50 else "medium",
                                estimated_savings=round(cost * best_alt["savings_potential"] / 100, 2),
                                implementation_effort="medium",
                                affected_models=[model],
                                affected_tasks=["general"],
                                recommendation=best_alt["recommendation"],
                            ))
        
        # Analyze by task
        task_usage = usage_data.get("by_agent", [])
        
        for task_data in task_usage:
            agent = task_data.get("agent", "")
            cost = task_data.get("cost", 0)
            requests = task_data.get("requests", 0)
            
            avg_cost_per_request = cost / requests if requests > 0 else 0
            
            if avg_cost_per_request > 0.10:  # More than 10 cents per request
                opportunities.append(OptimizationOpportunity(
                    id=f"optimize-{agent}",
                    title=f"Optimize {agent} task efficiency",
                    description=f"Average cost per request: ${avg_cost_per_request:.4f}. "
                               "Consider prompt optimization or model downscaling.",
                    category="efficiency",
                    priority="medium",
                    estimated_savings=round(cost * 0.15, 2),  # 15% savings estimate
                    implementation_effort="easy",
                    affected_models=["all"],
                    affected_tasks=[agent],
                    recommendation="Review prompts for unnecessary verbosity and optimize context length",
                ))
        
        return [asdict(o) for o in opportunities]
    
    async def generate_market_report(self) -> Dict:
        """Generate a comprehensive market research report."""
        pricing_trends = await self.research_pricing_trends()
        
        # Find all replacement opportunities
        all_opportunities = []
        for current_model in ["gpt-4", "gpt-3.5-turbo", "claude-3-opus"]:
            alternatives = await self.find_model_alternatives(current_model)
            all_opportunities.extend(alternatives)
        
        # Get latest pricing
        all_pricing = {}
        for provider in ["openai", "anthropic"]:
            all_pricing[provider] = await self.fetch_pricing(provider)
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "pricing_trends": pricing_trends,
            "model_alternatives": all_opportunities[:10],  # Top 10
            "current_pricing": all_pricing,
            "market_insights": [
                {
                    "insight": "Flash/Lite models gaining popularity",
                    "detail": "Google Gemini 1.5 Flash and OpenAI GPT-4o-mini offer 90%+ cost reduction",
                    "action": "Migrate simple tasks to flash models",
                },
                {
                    "insight": "DeepSeek disrupting coding market",
                    "detail": "DeepSeek Coder V2 offers competitive pricing at $0.14/1M tokens",
                    "action": "Consider for code generation tasks",
                },
                {
                    "insight": "Anthropic cache discounts",
                    "detail": "Claude 3 models offer 90% discount on cached tokens",
                    "action": "Implement caching for repeated contexts",
                },
            ],
            "recommendations": [
                "Review current model usage and identify migration candidates",
                "Implement semantic caching to leverage 90% Anthropic discount",
                "Use batch APIs for non-time-sensitive requests",
                "Consider DeepSeek for coding tasks to reduce costs by 80%+",
            ],
        }
        
        return report
    
    async def monitor_technology_trends(self) -> Dict:
        """Monitor LLM technology trends and announcements."""
        # In production, this would scrape news and announcements
        return {
            "last_updated": datetime.now().isoformat(),
            "emerging_trends": [
                {
                    "trend": "Small Language Models (SLMs)",
                    "description": "Models like Phi-3, Gemma 2B showing impressive capabilities at lower cost",
                    "impact_on_costs": "Could reduce simple task costs by 90%+",
                    "adoption_timeline": "6-12 months",
                },
                {
                    "trend": "Mixture of Experts (MoE)",
                    "description": "Sparse MoE models like Mixtral offering better cost-quality tradeoffs",
                    "impact_on_costs": "40-60% cost reduction for equivalent quality",
                    "adoption_timeline": "3-6 months",
                },
                {
                    "trend": "Model Distillation",
                    "description": "Using large models to train smaller, cheaper models",
                    "impact_on_costs": "Significant long-term savings potential",
                    "adoption_timeline": "12+ months",
                },
            ],
            "upcoming_releases": [
                {
                    "provider": "OpenAI",
                    "model": "GPT-5",
                    "expected": "Q2 2025",
                    "expected_pricing": "Similar to GPT-4 or lower",
                },
                {
                    "provider": "Anthropic",
                    "model": "Claude 4",
                    "expected": "Q3 2025",
                    "expected_pricing": "TBD",
                },
            ],
            "provider_news": [
                {
                    "provider": "OpenAI",
                    "news": "Expanded fine-tuning capabilities",
                    "date": "2024-07-15",
                },
                {
                    "provider": "Google",
                    "news": "2M context window now available on Gemini 1.5 Pro",
                    "date": "2024-07-01",
                },
            ],
        }


async def main():
    """Main entry point for CLI usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="LLM Cost Researcher")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Alternatives command
    alt_parser = subparsers.add_parser("alternatives", help="Find model alternatives")
    alt_parser.add_argument("--model", required=True)
    alt_parser.add_argument("--use-case", default="general")
    
    # Market report command
    subparsers.add_parser("market", help="Generate market research report")
    
    # Trends command
    subparsers.add_parser("trends", help="Monitor technology trends")
    
    # Optimize command
    opt_parser = subparsers.add_parser("optimize", help="Identify optimizations")
    opt_parser.add_argument("--usage-file", help="JSON file with usage data")
    
    args = parser.parse_args()
    
    researcher = CostResearcher()
    
    if args.command == "alternatives":
        alternatives = await researcher.find_model_alternatives(
            args.model,
            args.use_case,
        )
        print(json.dumps(alternatives, indent=2))
    
    elif args.command == "market":
        report = await researcher.generate_market_report()
        print(json.dumps(report, indent=2))
    
    elif args.command == "trends":
        trends = await researcher.monitor_technology_trends()
        print(json.dumps(trends, indent=2))
    
    elif args.command == "optimize":
        if args.usage_file:
            with open(args.usage_file) as f:
                usage_data = json.load(f)
        else:
            usage_data = {"by_model": [], "by_agent": []}
        
        opportunities = researcher.identify_optimization_opportunities(usage_data)
        print(json.dumps(opportunities, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
