# LLM Cost Tracker Methodology

## Overview

This document outlines the comprehensive methodology for tracking LLM and AI agent costs across multiple providers. It includes pricing references, budget thresholds, alert configurations, and tracking best practices.

## Cost Tracking Methodology

### Data Collection

#### API Usage Logging
Every LLM API call is logged with the following attributes:
- **Timestamp**: Exact time of the request (ISO 8601 format)
- **Provider**: LLM service provider (OpenAI, Anthropic, etc.)
- **Model**: Specific model version used
- **Endpoint**: API endpoint called
- **Request ID**: Unique identifier for the request
- **Input Tokens**: Number of tokens in the prompt
- **Output Tokens**: Number of tokens in the response
- **Cached Tokens**: Tokens served from cache (if applicable)
- **Duration**: Request processing time in milliseconds
- **Status**: Success, error, or rate limit
- **Cost**: Calculated cost for this request
- **Agent**: Name of the agent that initiated the request
- **Task**: Task type or description
- **Session ID**: User or session identifier

#### Log Storage Structure
```
logs/
├── costs/
│   ├── provider=openai/
│   │   ├── year=2024/
│   │   │   ├── month=01/
│   │   │   │   ├── day=15/
│   │   │   │   └── day=16/
│   │   │   └── month=02/
│   │   └── year=2025/
│   └── provider=anthropic/
├── aggregated/
│   ├── daily/
│   │   └── 2024-01-15.parquet
│   └── monthly/
│       └── 2024-01.parquet
└── alerts/
    └── 2024-01-15.json
```

### Cost Calculation

#### Base Formula
```
Total Cost = (Input Tokens × Input Price) + (Output Tokens × Output Price)
```

#### Cached Token Discount
If cached tokens are available:
```
Effective Input Cost = ((Input Tokens - Cached Tokens) × Input Price) + (Cached Tokens × Cached Price)
```
Note: Many providers offer discounts for cached tokens (typically 50-90% off input price).

#### Token Counting
- **Input Tokens**: System prompt + user prompt + context
- **Output Tokens**: Generated response tokens
- **Total Tokens**: Input + Output

### Provider Pricing Reference

#### OpenAI
| Model | Context | Input ($/1M tokens) | Output ($/1M tokens) | Cache Discount |
|-------|---------|---------------------|----------------------|----------------|
| GPT-4o | 128K | $2.50 | $10.00 | 75% |
| GPT-4o-mini | 128K | $0.15 | $0.60 | 75% |
| GPT-4 Turbo | 128K | $10.00 | $30.00 | 75% |
| GPT-4 | 8K | $30.00 | $60.00 | N/A |
| GPT-3.5-Turbo | 16K | $0.50 | $1.50 | 50% |

#### Anthropic
| Model | Context | Input ($/1M tokens) | Output ($/1M tokens) | Cache Discount |
|-------|---------|---------------------|----------------------|----------------|
| Claude-3.5-Sonnet | 200K | $3.00 | $15.00 | 90% |
| Claude-3-Opus | 200K | $15.00 | $75.00 | 90% |
| Claude-3-Haiku | 200K | $0.25 | $1.25 | 90% |

#### Moonshot (Kimi)
| Model | Context | Input ($/1M tokens) | Output ($/1M tokens) | Cache Discount |
|-------|---------|---------------------|----------------------|----------------|
| Kimi-2.5-Pro | 1M | $5.00 | $15.00 | 50% |
| Kimi-2.5-Turbo | 200K | $2.00 | $6.00 | 50% |
| Kimi-2.5-Apex | 1M | $12.00 | $36.00 | 50% |

#### MiniMax
| Model | Context | Input ($/1M tokens) | Output ($/1M tokens) | Cache Discount |
|-------|---------|---------------------|----------------------|----------------|
| MiniMax-2.1-Reasoning | 200K | $1.00 | $4.00 | 50% |
| MiniMax-2.1-Standard | 200K | $2.00 | $6.00 | 50% |
| MiniMax-2.1-Flash | 200K | $0.50 | $2.00 | 50% |

#### DeepSeek
| Model | Context | Input ($/1M tokens) | Output ($/1M tokens) | Cache Discount |
|-------|---------|---------------------|----------------------|----------------|
| DeepSeek-V2.5 | 128K | $0.14 | $0.28 | 50% |
| DeepSeek-Coder-V2.5 | 128K | $0.14 | $0.28 | 50% |
| DeepSeek-V2 | 128K | $0.27 | $0.55 | 50% |

#### Google Gemini
| Model | Context | Input ($/1M tokens) | Output ($/1M tokens) | Cache Discount |
|-------|---------|---------------------|----------------------|----------------|
| Gemini-1.5-Pro | 2M | $1.25 | $5.00 | 75% |
| Gemini-1.5-Flash | 1M | $0.075 | $0.30 | 75% |
| Gemini-1.0-Pro | 32K | $0.50 | $1.50 | N/A |

### Budget Thresholds

#### Default Budget Configuration
```yaml
budgets:
  daily:
    soft_limit: $50.00
    hard_limit: $75.00
    warning_percentage: 0.80  # 80% of soft limit
    critical_percentage: 0.95  # 95% of soft limit
  
  weekly:
    soft_limit: $300.00
    hard_limit: $450.00
    warning_percentage: 0.80
    critical_percentage: 0.95
  
  monthly:
    soft_limit: $1200.00
    hard_limit: $1800.00
    warning_percentage: 0.80
    critical_percentage: 0.95

  per_agent:
    default: $20.00
    research_agent: $50.00
    coding_agent: $100.00
    chat_agent: $10.00

  per_model:
    gpt-4: $30.00
    claude-3-opus: $30.00
    default: $50.00
```

#### Budget Tracking Rules
1. **Soft Limit**: Warning issued when approaching
2. **Hard Limit**: Block non-critical requests
3. **Percentage Calculation**: Based on soft limit
4. **Time Windows**:滚动 24-hour, 7-day, and 30-day windows

### Alert Configurations

#### Alert Types
| Alert Type | Severity | Trigger | Action |
|------------|----------|---------|--------|
| Budget Warning | Medium | >80% of daily budget | Informational |
| Budget Critical | High | >95% of daily budget | Immediate attention |
| Budget Exceeded | Critical | >100% of daily budget | Block non-critical |
| Cost Anomaly | High | >3σ from baseline | Investigate |
| Usage Spike | Medium | >200% of average | Monitor |
| Model Mismatch | Low | Non-optimal model used | Suggest optimization |
| API Error | High | Error rate >5% | Check provider status |
| Rate Limit | Medium | Approaching rate limit | Backoff recommendations |

#### Alert Channels and Priority
```yaml
alerts:
  budget_warning:
    channels:
      - telegram
      - discord
    priority: medium
    escalation: none

  budget_critical:
    channels:
      - telegram
      - discord
      - email
    priority: high
    escalation: budget_exceeded after 1 hour

  cost_anomaly:
    channels:
      - telegram
      - discord
    priority: high
    escalation: none

  api_error:
    channels:
      - telegram
      - discord
    priority: high
    escalation: pager after 30 minutes
```

### Anomaly Detection

#### Statistical Methods
- **Z-Score Detection**: Flag values >3 standard deviations from mean
- **Percentile Analysis**: Monitor tail distributions (P95, P99)
- **Moving Average**: Compare against 7-day rolling average
- **Seasonal Decomposition**: Account for time-of-day and day-of-week patterns

#### Thresholds
```yaml
anomaly_detection:
  z_score_threshold: 3.0
  percentage_change_threshold: 200  # 2x baseline
  absolute_change_threshold: $50.00  # Absolute dollar amount
  min_data_points: 7  # Minimum days for baseline
```

### Cost Attribution

#### Agent-Level Tracking
Each cost is attributed to:
1. **Primary Agent**: The agent that initiated the request
2. **Task Category**: Type of task (coding, research, chat, etc.)
3. **User/Project**: Project or user identifier
4. **Session**: Conversation or session ID

#### Aggregation Levels
- Per Agent
- Per Task Type
- Per Model
- Per Provider
- Per User/Project
- Per Day/Week/Month

### Reporting Metrics

#### Key Performance Indicators
| Metric | Formula | Target |
|--------|---------|--------|
| Cost per 1K tokens | (Total Cost / Total Tokens) × 1000 | Provider-specific |
| Cost per request | Total Cost / Total Requests | Model-specific |
| Token efficiency | (Useful Tokens / Total Tokens) × 100 | >70% |
| Cache hit rate | (Cached Tokens / Total Tokens) × 100 | >30% |
| Error cost ratio | (Error Cost / Total Cost) × 100 | <5% |
| Budget utilization | (Actual Cost / Budget) × 100 | <100% |

#### Efficiency Metrics
- **Tokens per dollar**: Measure of cost efficiency
- **Response quality score**: Quality-adjusted cost metric
- **Task completion cost**: Cost per successfully completed task
- **Idle time cost**: Cost of requests that timed out or were cancelled

### Data Retention

| Data Type | Retention Period | Archive Location |
|-----------|-----------------|-------------------|
| Raw API logs | 30 days | S3/Glacier |
| Aggregated daily | 1 year | S3/Standard |
| Aggregated monthly | 7 years | S3/Archive |
| Alert history | 2 years | Database |
| Reports | Permanent | Version control |

### API Integration

#### Supported Providers
1. OpenAI API
2. Anthropic API
3. Moonshot AI (Kimi)
4. MiniMax API
5. DeepSeek API
6. Google Gemini API
7. Azure OpenAI
8. AWS Bedrock
9. Custom endpoints (configurable)

#### Authentication Methods
- API Key (most providers)
- OAuth 2.0 (Google, Azure)
- AWS Signature v4 (Bedrock)

### Quality Assurance

#### Cost Verification
1. **Daily Reconciliation**: Compare tracked costs against provider invoices
2. **Spot Checks**: Random verification of sample requests
3. **Rate Limit Verification**: Ensure costs align with rate limit usage
4. **Cross-Provider Validation**: Verify aggregate costs across all providers

#### Accuracy Targets
- **Per-request accuracy**: ±1% of actual cost
- **Daily aggregate accuracy**: ±0.5% of actual cost
- **Monthly reconciliation**: 100% match with invoices

### Troubleshooting

#### Common Issues
1. **Missing logs**: Check network connectivity and API timeout settings
2. **Cost discrepancies**: Verify pricing table is up-to-date
3. **Alert fatigue**: Adjust sensitivity thresholds
4. **Storage issues**: Monitor disk space and implement rotation

#### Debug Commands
```bash
# Check recent logs
tail -f logs/costs/today.log

# Reconcile daily costs
python tools/cost-consultant/tracker.py --reconcile --date 2024-01-15

# Test alert delivery
python tools/cost-consultant/tracker.py --test-alerts

# Generate cost audit
python tools/cost-consultant/tracker.py --audit --provider openai
```

---

**Document Version**: 1.0
**Last Updated**: 2024-01-15
**Next Review**: 2024-04-15
