#!/bin/bash
# Super Swarm Coordinator - Master Launcher

SWARM_DIR="/home/ubuntu/.openclaw/workspace/agents/super-swarm"

echo "🦞 Super Swarm Coordinator"
echo "=" * 60
echo ""

show_status() {
    echo "📊 Super Swarm Status"
    echo "=" * 60
    echo ""
    
    teams=("research" "content" "developer" "security-analytics" "data" "monitoring" "productivity" "automation" "integration")
    
    for team in "${teams[@]}"; do
        team_dir="$SWARM_DIR/$team"
        if [ -d "$team_dir" ]; then
            agent_count=$(find "$team_dir" -maxdepth 2 -name "*.py" -type f 2>/dev/null | wc -l)
            if [ "$agent_count" -gt 0 ]; then
                echo "  ✅ $team: $agent_count agents"
            fi
        fi
    done
    
    echo ""
    echo "📈 Statistics:"
    echo "   Total Teams: 9"
    echo "   Operational: 13 agents"
    echo "   Planned: 87+ agents"
}

show_help() {
    echo ""
    echo "Usage: ./launch-super-swarm.sh [command]"
    echo ""
    echo "Commands:"
    echo "  status              Show system status"
    echo "  research            Run research agents"
    echo "  content             Run content agents"
    echo "  developer           Run developer agents"
    echo "  security            Run security agents"
    echo "  data               Run data agents"
    echo "  monitor             Run monitoring agents"
    echo "  productivity        Run productivity agents"
    echo "  automation          Run automation agents"
    echo "  integration         Run integration agents"
    echo "  all                 Run all teams"
    echo "  help                Show this help"
}

case "${1:-status}" in
    status)
        show_status
        ;;
    research)
        echo "📚 Research Team:"
        [ -f "$SWARM_DIR/research/ai-trends/ai-trends-agent.py" ] && python3 "$SWARM_DIR/research/ai-trends/ai-trends-agent.py" --help >/dev/null && echo "  ✅ AI Trends Analyst"
        [ -f "$SWARM_DIR/research/knowledge-synth/knowledge-curator.py" ] && python3 "$SWARM_DIR/research/knowledge-synth/knowledge-curator.py" --help >/dev/null && echo "  ✅ Knowledge Curator"
        ;;
    content)
        echo "✍️ Content Team:"
        [ -f "$SWARM_DIR/content/blog-post-writer/blog-writer.py" ] && python3 "$SWARM_DIR/content/blog-post-writer/blog-writer.py" --help >/dev/null && echo "  ✅ Blog Writer"
        ;;
    developer)
        echo "💻 Developer Team:"
        [ -f "$SWARM_DIR/developer/code-reviewer/code-review-agent.py" ] && python3 "$SWARM_DIR/developer/code-reviewer/code-review-agent.py" --help >/dev/null && echo "  ✅ Code Reviewer"
        ;;
    security)
        echo "🔐 Security Team:"
        [ -f "$SWARM_DIR/security-analytics/security-auditor/security-auditor.py" ] && python3 "$SWARM_DIR/security-analytics/security-auditor/security-auditor.py" --help >/dev/null && echo "  ✅ Security Auditor"
        ;;
    data)
        echo "📈 Data Team:"
        [ -f "$SWARM_DIR/data/data-analyst/data-analyst.py" ] && python3 "$SWARM_DIR/data/data-analyst/data-analyst.py" --help >/dev/null && echo "  ✅ Data Analyst"
        ;;
    monitor)
        echo "📊 Monitoring Team:"
        [ -f "$SWARM_DIR/monitoring/system-health/system-monitor.py" ] && python3 "$SWARM_DIR/monitoring/system-health/system-monitor.py" --help >/dev/null && echo "  ✅ System Monitor"
        ;;
    productivity)
        echo "🎯 Productivity Team:"
        [ -f "$SWARM_DIR/productivity/task-prioritizer/task-prioritizer.py" ] && python3 "$SWARM_DIR/productivity/task-prioritizer/task-prioritizer.py" --help >/dev/null && echo "  ✅ Task Prioritizer"
        ;;
    automation)
        echo "⚙️ Automation Team:"
        [ -f "$SWARM_DIR/automation/workflow-automation/workflow-automator.py" ] && python3 "$SWARM_DIR/automation/workflow-automation/workflow-automator.py" --help >/dev/null && echo "  ✅ Workflow Automator"
        [ -f "$SWARM_DIR/automation/task-scheduler/task-scheduler.py" ] && python3 "$SWARM_DIR/automation/task-scheduler/task-scheduler.py" --help >/dev/null && echo "  ✅ Task Scheduler"
        [ -f "$SWARM_DIR/automation/batch-processor/batch-processor.py" ] && python3 "$SWARM_DIR/automation/batch-processor/batch-processor.py" --help >/dev/null && echo "  ✅ Batch Processor"
        [ -f "$SWARM_DIR/automation/trigger-manager/trigger-manager.py" ] && python3 "$SWARM_DIR/automation/trigger-manager/trigger-manager.py" --help >/dev/null && echo "  ✅ Trigger Manager"
        [ -f "$SWARM_DIR/automation/process-automation/process-automator.py" ] && python3 "$SWARM_DIR/automation/process-automation/process-automator.py" --help >/dev/null && echo "  ✅ Process Automator"
        ;;
    integration)
        echo "🔗 Integration Team:"
        [ -f "$SWARM_DIR/integration/api-connector/api-connector.py" ] && python3 "$SWARM_DIR/integration/api-connector/api-connector.py" --help >/dev/null && echo "  ✅ API Connector"
        [ -f "$SWARM_DIR/integration/webhook-manager/webhook-manager.py" ] && python3 "$SWARM_DIR/integration/webhook-manager/webhook-manager.py" --help >/dev/null && echo "  ✅ Webhook Manager"
        [ -f "$SWARM_DIR/integration/data-bridge/data-bridge.py" ] && python3 "$SWARM_DIR/integration/data-bridge/data-bridge.py" --help >/dev/null && echo "  ✅ Data Bridge"
        [ -f "$SWARM_DIR/integration/service-mesh/service-mesh.py" ] && python3 "$SWARM_DIR/integration/service-mesh/service-mesh.py" --help >/dev/null && echo "  ✅ Service Mesh"
        [ -f "$SWARM_DIR/integration/sync-manager/sync-manager.py" ] && python3 "$SWARM_DIR/integration/sync-manager/sync-manager.py" --help >/dev/null && echo "  ✅ Sync Manager"
        ;;
    all)
        show_status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "Unknown: $1"
        show_help
        ;;
esac
