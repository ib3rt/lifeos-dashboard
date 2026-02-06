#!/bin/bash
# Activate All 15 Life OS Agents
# Assign simple tasks to each idle agent

echo "🤖 ACTIVATING ALL 15 AGENTS"
echo "============================="
echo ""

# Create tasks directory
mkdir -p ~/.openclaw/workspace/agent-tasks/$(date +%Y-%m-%d)

# Agent activation tasks
declare -A AGENT_TASKS=(
    ["oracle"]="Research the top 3 AI news stories from today and summarize key developments"
    ["diamond"]="Check current Bitcoin and Ethereum prices, note any significant movements"
    ["mechanic"]="Run system health check on Life OS infrastructure and report status"
    ["sentinel"]="Review security logs and check for any unauthorized access attempts"
    ["hype"]="Draft a Twitter thread highlighting recent Life OS achievements"
    ["ned"]="Review the Discord bot code and suggest one optimization"
    ["pablo"]="Outline a 5-minute podcast episode about AI agents in daily life"
    ["goldfinger"]="Create a simple budget summary for Life OS projects this month"
    ["legal"]="Review the terms of service for Sparkling Solutions website"
    ["bridge"]="Research current prices for Raspberry Pi 5 8GB with NVMe HAT"
    ["zen"]="Write 3 quick mindfulness tips for busy entrepreneurs"
    ["strategist"]="Draft weekly priorities list for Life OS development"
    ["butler"]="Organize the workspace/agents/ directory and list all deliverables"
    ["felix"]="Check for any error logs in the system and report issues"
    ["landlord"]="Create a maintenance checklist for Airbnb property management"
)

AGENT_NAMES=(
    "oracle:🔮 The Oracle"
    "diamond:💎 Diamond Hands"
    "mechanic:⚙️ The Mechanic"
    "sentinel:🛡️ Sentinel"
    "hype:📈 Hype Man"
    "ned:💻 Neural Net Ned"
    "pablo:🎙️ Podcast Pablo"
    "goldfinger:🏦 Goldfinger"
    "legal:⚖️ Legal Eagle"
    "bridge:🌐 The Bridge"
    "zen:☯️ Zen Master"
    "strategist:♟️ The Strategist"
    "butler:🤵 The Butler"
    "felix:🔨 Fix-It Felix"
    "landlord:🏠 The Landlord"
)

# Update agent status files
for agent_info in "${AGENT_NAMES[@]}"; do
    IFS=':' read -r key name <<< "$agent_info"
    task="${AGENT_TASKS[$key]}"
    
    echo "Activating $name..."
    
    # Create task file
    cat > ~/.openclaw/workspace/agent-tasks/$(date +%Y-%m-%d)/${key}-task.md << EOF
# Agent Task Assignment

**Agent:** $name
**Status:** ACTIVE
**Assigned:** $(date)
**Task:** $task

## Deliverable
Complete the task above and report findings.

---
Assigned by Life OS Command Center
EOF

    echo "  ✅ Task assigned: ${task:0:60}..."
done

echo ""
echo "============================="
echo "✅ ALL 15 AGENTS ACTIVATED!"
echo "============================="
echo ""
echo "Each agent has a simple task:"
echo ""
for agent_info in "${AGENT_NAMES[@]}"; do
    IFS=':' read -r key name <<< "$agent_info"
    echo "  $name"
    echo "    → ${AGENT_TASKS[$key]:0:70}..."
    echo ""
done

echo "============================="
echo "📁 Tasks saved to: agent-tasks/$(date +%Y-%m-%d)/"
echo "============================="
