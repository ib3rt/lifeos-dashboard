# 🏦 Life OS Expense Tracker

> *"Watch the pennies and the dollars will watch themselves."* — Goldfinger's Second Law

---

## 📊 Executive Dashboard

```
┌─────────────────────────────────────────────────────────────────┐
│  LIFE OS FINANCIAL HEALTH          Status: 🟢 HEALTHY           │
├─────────────────────────────────────────────────────────────────┤
│  Current Monthly Burn:    $116/mo                               │
│  Projected (6 months):    $245/mo                               │
│  Annual Run Rate:         $1,392 → $2,940                       │
│  Risk Level:              LOW                                   │
│  Optimization Potential:  $60-85/mo savings identified          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 💰 Current Monthly Expenses (February 2026)

### 🖥️ Infrastructure & Hosting

| Service | Monthly Cost | Billing Type | Purpose | Provider |
|---------|-------------|--------------|---------|----------|
| **AWS EC2** | $50.00 | On-demand | Primary compute (t3.medium) | AWS |
| **AWS S3** | $5.00 | Usage-based | Backups, static assets | AWS |
| **AWS Data Transfer** | $10.00 | Usage-based | Egress fees | AWS |
| **Vercel Pro** | $20.00 | Fixed | Hosting for dashboard & sites | Vercel |
| **AWS Route 53** | $0.50 | Fixed | DNS management | AWS |
| **Subtotal Infrastructure** | **$85.50** | | | |

### 🤖 APIs & AI Services

| Service | Monthly Cost | Billing Type | Purpose | Provider |
|---------|-------------|--------------|---------|----------|
| **Moonshot AI (Kimi)** | $30.00 | Usage-based | Primary LLM for agents | Moonshot |
| **OpenClaw Gateway** | $0.00 | Self-hosted | Agent orchestration | Self |
| **Telegram Bot API** | $0.00 | Free tier | Messaging interface | Telegram |
| **Brave Search API** | $0.00 | ❌ Not configured | Web search capability | Brave |
| **Anthropic Claude** | $0.00 | On-demand | Fallback LLM option | Anthropic |
| **Subtotal AI/APIs** | **$30.00** | | | |

### 🌐 Domains & SSL

| Service | Monthly Cost | Billing Type | Purpose | Provider |
|---------|-------------|--------------|---------|----------|
| **Domain Registration** | $1.00 | Annual/12 | lifeos.b3rt.dev (pending) | Namecheap/Cloudflare |
| **SSL Certificates** | $0.00 | Free | HTTPS via Let's Encrypt | Let's Encrypt |
| **Subtotal Domains** | **$1.00** | | | |

### 🛠️ Development & Productivity Tools

| Service | Monthly Cost | Billing Type | Purpose | Status |
|---------|-------------|--------------|---------|--------|
| **GitHub** | $0.00 | Free tier | Code repositories | ✅ Active |
| **n8n** | $0.00 | Self-hosted | Workflow automation | 🟡 Testing |
| **Subtotal Dev Tools** | **$0.00** | | | |

### 📈 Planned/Projected Services

| Service | Est. Monthly | Purpose | Timeline | Status |
|---------|-------------|---------|----------|--------|
| **Riverside.fm** | $15.00 | Podcast recording | Month 2 | 📋 Planned |
| **Buzzsprout** | $12.00 | Podcast hosting | Month 2 | 📋 Planned |
| **Descript** | $15.00 | Audio/video editing | Month 2 | 📋 Planned |
| **OpusClip** | $15.00 | Video clip extraction | Month 3 | 📋 Planned |
| **Discord Nitro** | $10.00 | Community server boosts | Month 2 | 📋 Planned |
| **Subtotal Planned** | **$67.00** | | | |

---

## 📂 Expense Categorization

### By Category (Current)

```
Infrastructure & Hosting  ████████████████████████████████  $85.50  (73.7%)
APIs & AI Services        ████████████                       $30.00  (25.9%)
Domains & SSL             █                                   $1.00   (0.9%)
Development Tools         ░                                   $0.00   (0.0%)
                          ─────────────────────────────────────────
TOTAL CURRENT                                                 $116.50
```

### By Provider (Current)

```
AWS (EC2 + S3 + Transfer + Route 53)  ████████████████████████  $65.50  (56.2%)
Moonshot AI (Kimi)                    ████████████              $30.00  (25.8%)
Vercel                                ████████                  $20.00  (17.2%)
Domain Registrar                      ░                          $1.00   (0.9%)
                                      ─────────────────────────────────────
TOTAL                                                              $116.50
```

---

## 📈 6-Month Cost Projections

### Month-by-Month Forecast

| Month | Infrastructure | AI/APIs | Marketing | Domains | Other | **Total** | Growth |
|-------|---------------|---------|-----------|---------|-------|-----------|--------|
| **Feb** | $85.50 | $30.00 | $0.00 | $1.00 | $0.00 | **$116.50** | — |
| **Mar** | $95.00 | $45.00 | $37.00 | $1.00 | $10.00 | **$188.00** | +61% |
| **Apr** | $100.00 | $50.00 | $42.00 | $1.00 | $10.00 | **$203.00** | +8% |
| **May** | $105.00 | $55.00 | $42.00 | $1.00 | $15.00 | **$218.00** | +7% |
| **Jun** | $110.00 | $60.00 | $47.00 | $1.00 | $15.00 | **$233.00** | +7% |
| **Jul** | $115.00 | $65.00 | $47.00 | $1.00 | $20.00 | **$248.00** | +6% |
| **Aug** | $120.00 | $70.00 | $52.00 | $1.00 | $20.00 | **$263.00** | +6% |

### Scenario Planning

#### 🟢 Conservative Scenario (Status Quo + Podcast)
- **Assumes:** Current services + podcast launch (Riverside, Buzzsprout, basic editing)
- **6-month projection:** $165-200/mo average
- **Annual:** ~$2,100

#### 🟡 Moderate Growth Scenario (+New Tools & Scaling)
- **Assumes:** Above + X API integration, Discord bots, increased AI usage
- **6-month projection:** $200-280/mo average
- **Annual:** ~$2,800

#### 🔴 Aggressive Scenario (Full Marketing Stack)
- **Assumes:** Above + premium tools, sponsored content, multiple channels
- **6-month projection:** $280-400/mo average
- **Annual:** ~$3,600-4,800

---

## 🎯 Cost Optimization Playbook

### 🔥 Immediate Actions (This Week) — Potential Savings: $25-40/mo

| Action | Effort | Savings/mo | Impact |
|--------|--------|-----------|--------|
| **Right-size EC2 to t3.small** | Low | ~$25 | High |
| **Configure Brave Search API** | Low | $0 | Medium (enables capability) |
| **Set AWS cost alerts** | Low | $0 | High (prevention) |
| **Enable S3 lifecycle policies** | Low | ~$5 | Medium |

### 💡 Short-Term (This Month) — Potential Savings: $15-25/mo

| Action | Effort | Savings/mo | Impact |
|--------|--------|-----------|--------|
| **Implement LLM usage quotas** | Medium | Variable | High (prevents overages) |
| **Enable Vercel Analytics** | Low | $0 | Medium (visibility) |
| **Batch LLM requests** | Medium | ~$10-15 | Medium |
| **Review data transfer costs** | Medium | ~$5-10 | Low |

### 🌱 Long-Term (Next Quarter) — Potential Savings: $30-50/mo

| Action | Effort | Savings/mo | Impact |
|--------|--------|-----------|--------|
| **AWS Reserved Instance (1-year)** | Medium | ~$15-20 | High |
| **Evaluate Cloudflare R2 vs S3** | High | ~$10 | Medium |
| **Consider Savings Plans** | Medium | Variable | Medium |
| **Optimize AI model routing** | High | ~$10-20 | Medium |

### 💰 Free Money Opportunities

| Opportunity | Value | Eligibility | Action |
|-------------|-------|-------------|--------|
| **AWS Free Tier** | $750 credit | New accounts | Already using |
| **GitHub Student Pack** | Various | Student status | Check eligibility |
| **Vercel Hobby Plan** | $0/mo | Personal projects | Consider downgrade |
| **OpenAI credits** | $5-18 | New accounts | Already used |
| **Startup programs** | $1,000s | Incorporated startup | Research apply |

---

## 📋 Expense Tracking Template

### Monthly Reconciliation Checklist

```
□ Review AWS bill (check for anomalies)
□ Check Vercel usage vs. plan limits
□ Verify Moonshot API usage and costs
□ Update actual vs. projected expenses
□ Review optimization opportunities
□ Update this tracker with new services
□ Flag any >20% variance from projections
□ Document one-time vs. recurring costs
```

### New Service Evaluation Rubric

Before adding any new service:

| Criteria | Weight | Score (1-5) | Weighted |
|----------|--------|-------------|----------|
| **Monthly Cost** | 30% | ___ | ___ |
| **ROI Potential** | 25% | ___ | ___ |
| **Integration Effort** | 20% | ___ | ___ |
| **Vendor Lock-in Risk** | 15% | ___ | ___ |
| **Cancellation Flexibility** | 10% | ___ | ___ |
| **TOTAL** | 100% | | **___/5** |

**Approval Threshold:** Score ≥ 3.5 for costs >$10/mo

---

## 🚨 Cost Alert Thresholds

| Tier | Monthly Spend | Action |
|------|--------------|--------|
| 🟢 **Normal** | <$150 | Monitor as usual |
| 🟡 **Warning** | $150-200 | Review usage, check for anomalies |
| 🟠 **Elevated** | $200-300 | Immediate audit, pause non-critical services |
| 🔴 **Critical** | >$300 | Emergency review, implement hard limits |

---

## 📊 Growth Cost Modeling

### Cost Per Agent (Estimated)

| Agent Type | LLM Calls/mo | Compute | Storage | **Est. Cost/mo** |
|------------|-------------|---------|---------|-----------------|
| Light (scheduled tasks) | ~100 | Minimal | <1GB | ~$2-5 |
| Medium (interactive) | ~1,000 | Low | <5GB | ~$8-15 |
| Heavy (research/analysis) | ~5,000+ | Medium | >10GB | ~$25-50 |

### Scaling Projections

| # of Active Agents | Infrastructure | AI Usage | Other | **Total/mo** |
|-------------------|----------------|----------|-------|-------------|
| **10 agents** | $85 | $30 | $10 | ~$125 |
| **25 agents** | $100 | $75 | $25 | ~$200 |
| **50 agents** | $150 | $150 | $50 | ~$350 |
| **100 agents** | $250 | $300 | $100 | ~$650 |

---

## 🏦 Financial Summary

### Current State (Feb 2026)

```
╔══════════════════════════════════════════════════════════════════╗
║  MONTHLY BURN RATE                    $116.50                    ║
║  ├─ Infrastructure (73.7%)            $85.50                     ║
║  ├─ AI/APIs (25.9%)                   $30.00                     ║
║  └─ Domains & Misc (0.9%)             $1.00                      ║
║                                                                  ║
║  ANNUAL PROJECTION (Current)          $1,398                     ║
║  ANNUAL PROJECTION (With Growth)      $2,100-2,940               ║
║                                                                  ║
║  IDENTIFIED SAVINGS                   $60-85/mo                  ║
║  OPTIMIZED MONTHLY (Potential)        $35-55/mo                  ║
╚══════════════════════════════════════════════════════════════════╝
```

### Key Metrics

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Cost per agent | ~$8 | <$5 | 🟡 Optimizing |
| Infrastructure efficiency | 73.7% | <60% | 🔴 Review |
| AI cost ratio | 25.9% | <35% | 🟢 Healthy |
| Monthly growth rate | — | <15% | 🟢 On track |

---

## 📝 Changelog

| Date | Event | Impact |
|------|-------|--------|
| 2026-02-03 | Initial expense tracker created | Baseline established |
| 2026-02-03 | Life OS Genesis launch | $116/mo baseline |

---

## 🔗 Related Documents

- [Goldfinger's Budget Report](../agent-tasks/2026-02-03/goldfinger-report.md)
- [Command Requirements](../COMMAND_REQUIREMENTS.md) (pending spend approvals)
- [90-Day Roadmap](../strategy/90-day-roadmap.md)
- [Podcast Plan](../research/podcast-plan.md)

---

*Last updated: 2026-02-03 by 🏦 Goldfinger*  
*Next review: 2026-03-03*

---

> 💡 **Pro Tip:** Bookmark this file and check it monthly. Costs creep up silently—stay vigilant!
