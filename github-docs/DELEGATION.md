# Delegation Patterns

*Standard operating procedures for deploying sub-agents.*

---

## When to Delegate

| Scenario | Action |
|----------|--------|
| Task > 5 minutes | Spawn sub-agent, report back on completion |
| Multi-step research | Delegate with clear scope, deliverables, sources |
| Parallel work | Spawn multiple agents, aggregate results |
| Specialized domain | Route to appropriate specialist agent |
| Error recovery | Delegate retry with exponential backoff |

---

## Standard Spawn Template

```javascript
sessions_spawn({
  task: `Detailed description including:
    - Goal: what to accomplish
    - Scope: boundaries and constraints
    - Tools: which to use or avoid
    - Deliverables: expected output format
    - Escalation: when to loop back`,
  runTimeoutSeconds: 300,  // 5 min default, adjust per task
  cleanup: "delete",       // or "keep" for complex workflows
  label: "descriptive-tag" // for tracking
})
```

---

## Role-Based Routing

| Need | Delegate To |
|------|-------------|
| Investment analysis | FINANCE_DIRECTOR |
| Tax strategy questions | FINANCE_DIRECTOR |
| Crypto portfolio review | FINANCE_DIRECTOR |
| Brand/campaign ideas | MARKETING_SALES_LEAD |
| SEO audit | MARKETING_SALES_LEAD |
| Contract review | LEGAL_COMPLIANCE_ADVISOR |
| IP/trademark questions | LEGAL_COMPLIANCE_ADVISOR |
| Process optimization | OPERATIONS_PROJECT_COORDINATOR |
| Supply chain issues | OPERATIONS_PROJECT_COORDINATOR |
| Automation setup | IT_TECH_SPECIALIST |
| Security concerns | CYBERSECURITY_GUARDIAN |
| Fitness/nutrition plan | HEALTH_WELLNESS_COACH |
| Long-term strategy | STRATEGY_INNOVATION_CONSULTANT |
| Scheduling conflicts | EXECUTIVE_SUPPORT_ASSISTANT |
| Equipment maintenance | MAINTENANCE_MECHANICS_EXPERT |
| Property/insurance review | ASSET_RISK_MANAGER |
| Travel planning | TRAVEL_LOGISTICS_PLANNER |

---

## Escalation Triggers

**Always escalate (loop back to user) when:**
- Cost estimate > $0.50
- Financial transactions involved
- Legal liability or contracts to sign
- Security incidents confirmed
- Medical/health decisions
- Irreversible operations

**Decide autonomously when:**
- Within documented preferences
- Similar past decisions exist
- Error recovery follows known pattern
- Cost < $0.10 and low risk

---

## Multi-Agent Coordination

For complex tasks requiring multiple specialists:

1. **Coordinator agent** (Executive Support or Operations)
   - Receives high-level request
   - Breaks into subtasks
   - Spawns appropriate specialists

2. **Parallel execution**
   - Multiple agents work simultaneously
   - Each reports to coordinator

3. **Aggregation & synthesis**
   - Coordinator compiles outputs
   - Resolves conflicts
   - Delivers unified response

---

## Retry & Error Handling

```javascript
// Failed operation retry pattern
if (error.includes("temporarily overloaded")) {
  // Queue for health check retry
  heartbeatState.queuedOperations.push({
    task: originalTask,
    retryCount: currentRetry + 1,
    maxRetries: 5,
    backoffMs: 30000 * (2 ** currentRetry)  // exponential
  });
}
```

---

## Communication Protocol

**From sub-agent to user (via me):**
- Concise summary
- Key findings or outputs
- Decisions made (with rationale)
- Items requiring approval
- Next steps recommended

**From me to sub-agent:**
- Clear task boundaries
- Relevant context from memory
- Expected output format
- Authority limits
- Timeout constraints

---

## Tracking & Observability

All delegations logged to:
- `memory/delegation-log.jsonl` — timestamp, task, agent, result
- Sub-agent labels for quick lookup
- State in heartbeat for queued operations

---

*Update this file as new patterns emerge.*
