# Business SOP Index

Life OS - Standard Operating Procedures Master Index

## Overview
This directory contains all Standard Operating Procedures for Life OS business operations. Each SOP is designed to be automated, version-controlled, and tracked for compliance.

## SOP Categories

### 1. Core Business SOPs
- **[Sales Pipeline](sales-pipeline.md)** - Lead qualification, opportunity management, deal closing
- **[Client Onboarding](client-onboarding.md)** - New client setup, kickoff meetings, deliverable tracking
- **[Content Workflow](content-workflow.md)** - Content ideation, creation, review, and publication
- **[Financial Tracking](financial-tracking.md)** - Invoicing, expense tracking, budget management
- **[Project Management](project-management.md)** - Project initiation, execution, monitoring, closure
- **[Quality Assurance](quality-assurance.md)** - Review processes, standards enforcement, feedback loops

### 2. Automation & Logic SOPs
- **[Automation Logic](automation-logic.md)** - Decision trees, workflow triggers, approval chains

## Automation Tools

| Tool | Purpose | Location |
|------|---------|----------|
| SOP Generator | Create SOPs from templates | `tools/sop-automation/generate_sop.sh` |
| Execution Tracker | Track SOP compliance | `tools/sop-automation/track_execution.py` |
| Compliance Checker | Verify SOP adherence | `tools/sop-automation/compliance_check.py` |
| Version Controller | Manage SOP versions | `tools/sop-automation/version_control.sh` |
| Team Assigner | Auto-assign tasks | `tools/sop-automation/team_assign.py` |

## Workflow Definitions

JSON workflow definitions for automation engines:
- `business/workflows/*.json` - Process automation definitions
- `business/templates/*.md` - SOP templates

## Process Diagrams

Mermaid diagrams for visual process documentation:
- Flowcharts
- Sequence diagrams
- Decision trees
- Gantt charts

## Version Control

- **Current Version**: 1.0.0
- **Last Updated**: 2024-01-01
- **Change Log**: See individual SOP files

## Compliance Status

| SOP | Status | Last Review | Next Review |
|-----|--------|-------------|-------------|
| Sales Pipeline | ✅ Active | 2024-01-01 | 2024-04-01 |
| Client Onboarding | ✅ Active | 2024-01-01 | 2024-04-01 |
| Content Workflow | ✅ Active | 2024-01-01 | 2024-04-01 |
| Financial Tracking | ✅ Active | 2024-01-01 | 2024-04-01 |
| Project Management | ✅ Active | 2024-01-01 | 2024-04-01 |
| Quality Assurance | ✅ Active | 2024-01-01 | 2024-04-01 |
| Automation Logic | ✅ Active | 2024-01-01 | 2024-04-01 |

## Getting Started

1. **For New Team Members**: Start with the [Automation Logic](automation-logic.md) to understand the decision framework
2. **For Process Owners**: Review your assigned SOPs and ensure they reflect current practices
3. **For Automation**: Use the tools in `tools/sop-automation/` to generate, track, and manage SOPs

## Support

- **SOP Administrator**: Life OS Core
- **Issue Reporting**: Create an issue in the project repository
- **Questions**: Refer to the automation tools documentation

---

*This index is auto-generated. Last sync: 2024-01-01 00:00:00 UTC*
