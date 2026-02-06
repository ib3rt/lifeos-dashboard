# Cross-System Triggers - Life OS Automation Platform

## Overview

This document defines the event triggers that enable communication and coordination between the three core automation swarms in the Super Swarm system.

## Trigger Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                      CROSS-SYSTEM TRIGGER BUS                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   SOP SWARM ◄────► TRIGGER BUS ◄────► STRATEGY SWARM                │
│                     ▲                                              │
│                     │                                              │
│                     ▼                                              │
│                 CONTENT SWARM                                       │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Trigger Categories

### 1. Task Completion Triggers

| Trigger Name | Source | Target | Description |
|--------------|--------|--------|-------------|
| `sop.completed` | SOP Agent | All | Standard operating procedure finished |
| `strategy.completed` | Strategy Agent | All | Strategic planning task finished |
| `content.completed` | Content Agent | All | Content creation task finished |

**Payload Structure:**
```json
{
  "trigger": "task.completed",
  "source": "sop-agent",
  "task_id": "uuid-string",
  "task_type": "sop|strategy|content",
  "result": {
    "status": "success",
    "output_path": "/path/to/output",
    "metrics": {}
  },
  "timestamp": "ISO8601",
  "correlation_id": "uuid-for-tracing"
}
```

### 2. Resource Triggers

| Trigger Name | Source | Target | Description |
|--------------|--------|--------|-------------|
| `resource.request` | Any Agent | Coordinator | Request additional resources |
| `resource.allocated` | Coordinator | Requesting Agent | Resources have been allocated |
| `resource.release` | Any Agent | All | Resources released for other use |

### 3. Dependency Triggers

| Trigger Name | Source | Target | Description |
|--------------|--------|--------|-------------|
| `dependency.ready` | Source Agent | Dependent Agent | Required dependency is available |
| `dependency.blocked` | Dependent Agent | Coordinator | Task blocked by unmet dependency |
| `dependency.resolved` | Coordinator | Dependent Agent | Blocked task can now proceed |

### 4. Error Triggers

| Trigger Name | Source | Target | Description |
|--------------|--------|--------|-------------|
| `error.occurred` | Any Agent | All | Error condition detected |
| `error.recovered` | Erring Agent | All | Error condition resolved |
| `error.escalated` | Any Agent | Coordinator | Error requires human intervention |

### 5. Sync Triggers

| Trigger Name | Source | Target | Description |
|--------------|--------|--------|-------------|
| `sync.request` | Any Agent | All | Request synchronization point |
| `sync.ack` | All Agents | Requester | All agents ready to sync |
| `sync.complete` | Synced System | All | Synchronization finished |

## Swarm-Specific Triggers

### SOP Automation Triggers

| Trigger | Direction | Description |
|---------|-----------|-------------|
| `sop.workflow.start` | Internal | Workflow execution began |
| `sop.workflow.complete` | Internal → Coordinator | Workflow finished |
| `sop.template.apply` | Internal | New template being applied |
| `sop.compliance.check` | Internal → Strategy | Compliance verification needed |

### Strategy Automation Triggers

| Trigger | Direction | Description |
|---------|-----------|-------------|
| `strategy.goal.set` | Internal | New strategic goal defined |
| `strategy.goal.achieved` | Internal → Content | Goal reached, content opportunity |
| `strategy.roadmap.update` | Internal → SOP | Roadmap changes affect SOPs |
| `strategy.kpi.update` | Internal | KPI measurement completed |

### Content Automation Triggers

| Trigger | Direction | Description |
|---------|-----------|-------------|
| `content.pipeline.start` | Internal | Content pipeline initiated |
| `content.published` | Internal → All | Content published to platform |
| `content.analytics` | Internal → Strategy | Content performance data |
| `content.approved` | Strategy → Content | Strategic approval received |

## Trigger Handlers

### Default Handler Mappings

```yaml
handlers:
  # SOP Handlers
  - trigger: "sop.*"
    handlers:
      - "log_event"
      - "update_metrics"
      - "notify_coordinator"
  
  # Strategy Handlers
  - trigger: "strategy.*"
    handlers:
      - "log_event"
      - "update_metrics"
      - "trigger_content_pipeline"
  
  # Content Handlers
  - trigger: "content.*"
    handlers:
      - "log_event"
      - "update_analytics"
      - "notify_stakeholders"

  # Cross-System Handlers
  - trigger: "*.completed"
    handlers:
      - "check_dependencies"
      - "update_dashboard"
      - "trigger_next_task"
```

## Trigger Configuration

### Enabling/Disabling Triggers

```bash
# List all triggers
bash tools/super-swarm-coordinator.sh --triggers --list

# Enable specific trigger
bash tools/super-swarm-coordinator.sh --triggers --enable "content.published"

# Disable specific trigger
bash tools/super-swarm-coordinator.sh --triggers --disable "error.*"
```

### Trigger Rate Limiting

| Trigger Type | Max Rate | Burst |
|--------------|----------|-------|
| `error.*` | 100/min | 10 |
| `*.completed` | 1000/min | 50 |
| `content.published` | 100/min | 10 |
| `sync.*` | 50/min | 5 |

## Integration with External Systems

### Webhook Integration

```yaml
webhooks:
  - trigger: "*.completed"
    url: "https://api.example.com/webhooks/life-os"
    method: "POST"
    headers:
      "Authorization": "Bearer ${WEBHOOK_TOKEN}"
  
  - trigger: "content.published"
    url: "https://api.slack.com/webhooks/..."
    method: "POST"
```

### Email Notifications

```yaml
notifications:
  - trigger: "error.escalated"
    type: "email"
    to: "admin@example.com"
    subject: "Life OS Error Escalation"
  
  - trigger: "strategy.goal.achieved"
    type: "email"
    to: "team@example.com"
    subject: "Strategic Goal Achieved! 🎉"
```

## Monitoring & Debugging

### Trigger Logs

Logs are stored in `${WORKSPACE_DIR}/logs/triggers/`

```
triggers/
├── 2026-02-04/
│   ├── sop.completed_001.log
│   ├── content.published_002.log
│   └── error.occurred_001.log
└── trigger-audit.log
```

### Debug Commands

```bash
# View recent triggers
tail -100 logs/triggers/trigger-audit.log

# Filter by trigger type
grep "content.published" logs/triggers/trigger-audit.log

# Count trigger occurrences
wc -l logs/triggers/*/*.log
```

## Example Trigger Flows

### Content → Strategy Feedback Loop

```
1. content.published
   └─► Strategy Engine receives engagement data
2. strategy.kpi.update
   └─► KPIs recalculated with new content metrics
3. strategy.goal.achieved (if applicable)
   └─► Notify all systems of goal completion
4. sync.request
   └─► Coordinate next phase
```

### SOP → Strategy Alignment

```
1. sop.completed (compliance check)
   └─► Strategy Engine evaluates risk
2. strategy.roadmap.update
   └─► Adjust timelines based on compliance findings
3. sop.workflow.update
   └─► Update SOPs with new requirements
```

---

*Trigger Definitions v1.0.0 - 2026-02-04*
