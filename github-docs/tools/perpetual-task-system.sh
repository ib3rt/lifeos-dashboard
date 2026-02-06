#!/bin/bash
# 🎖️ PERPETUAL TASK SYSTEM
# Agents always have 3 ongoing tasks
# As ordered by the General

echo "🎖️ INITIALIZING PERPETUAL TASK SYSTEM"
echo "======================================"
echo ""

# Task database - categorized by agent expertise
declare -A TASK_DATABASE=(
    # ORACLE - AI/Research Tasks
    ["oracle_1"]="Research emerging AI model and evaluate for Life OS integration"
    ["oracle_2"]="Compile weekly AI trends report with actionable insights"
    ["oracle_3"]="Benchmark current LLM options (GPT-4, Claude, Gemini, local models)"
    ["oracle_4"]="Analyze competitor AI frameworks and identify differentiators"
    ["oracle_5"]="Document AI tool recommendations with pros/cons/pricing"
    ["oracle_6"]="Create AI capability roadmap for next 6 months"
    
    # DIAMOND - Crypto/Finance Tasks  
    ["diamond_1"]="Monitor crypto markets and alert on significant movements"
    ["diamond_2"]="Research DeFi yield opportunities for passive income"
    ["diamond_3"]="Build automated portfolio tracking dashboard"
    ["diamond_4"]="Analyze on-chain data for market sentiment"
    ["diamond_5"]="Create crypto tax reporting automation"
    ["diamond_6"]="Research Web3 integration opportunities for Life OS"
    
    # MECHANIC - Operations/Infra Tasks
    ["mechanic_1"]="Implement automated health checks for all services"
    ["mechanic_2"]="Create one-click deployment scripts for new environments"
    ["mechanic_3"]="Build system monitoring dashboard with alerts"
    ["mechanic_4"]="Optimize Docker containers for faster builds"
    ["mechanic_5"]="Document disaster recovery procedures"
    ["mechanic_6"]="Automate backup verification and testing"
    
    # SENTINEL - Security Tasks
    ["sentinel_1"]="Run security audit on all API keys and tokens"
    ["sentinel_2"]="Create automated vulnerability scanning schedule"
    ["sentinel_3"]="Document incident response playbook"
    ["sentinel_4"]="Implement IP-based access controls"
    ["sentinel_5"]="Set up automated security report generation"
    ["sentinel_6"]="Review and harden Discord server permissions"
    
    # HYPE - Marketing/Content Tasks
    ["hype_1"]="Create 7-day content calendar for Life OS marketing"
    ["hype_2"]="Design viral Twitter thread template"
    ["hype_3"]="Build social media automation workflow in n8n"
    ["hype_4"]="Create agent spotlight video script series"
    ["hype_5"]="Design infographic showing Life OS capabilities"
    ["hype_6"]="Write compelling case study of current implementation"
    
    # NED - Engineering Tasks
    ["ned_1"]="Refactor Discord bot for improved performance"
    ["ned_2"]="Create comprehensive CLI toolkit installer"
    ["ned_3"]="Build automated testing framework for all tools"
    ["ned_4"]="Implement CI/CD pipeline for automatic deployments"
    ["ned_5"]="Create API documentation generator"
    ["ned_6"]="Build developer onboarding documentation"
    
    # PABLO - Content/Audio Tasks
    ["pablo_1"]="Record and edit Life OS podcast episode 1"
    ["pablo_2"]="Create voice cloning samples for agent narration"
    ["pablo_3"]="Produce video tutorial for dashboard features"
    ["pablo_4"]="Design audio branding package for Life OS"
    ["pablo_5"]="Create podcast guest outreach list"
    ["pablo_6"]="Build video content calendar for YouTube"
    
    # GOLDFINGER - Finance Tasks
    ["goldfinger_1"]="Track and categorize all Life OS expenses"
    ["goldfinger_2"]="Create monthly budget variance analysis"
    ["goldfinger_3"]="Build ROI calculator for each agent's value"
    ["goldfinger_4"]="Research funding options (grants, VC, bootstrap)"
    ["goldfinger_5"]="Design automated expense reporting system"
    ["goldfinger_6"]="Create financial projections for 12 months"
    
    # LEGAL - Compliance Tasks
    ["legal_1"]="Draft comprehensive Terms of Service document"
    ["legal_2"]="Create Privacy Policy compliant with GDPR/CCPA"
    ["legal_3"]="Research entity formation options (LLC vs Corp)"
    ["legal_4"]="Document data handling procedures"
    ["legal_5"]="Create contract templates for partnerships"
    ["legal_6"]="Research trademark requirements for Life OS"
    
    # BRIDGE - Infrastructure Tasks
    ["bridge_1"]="Create one-command local node installation script"
    ["bridge_2"]="Compare cloud vs local cost analysis for 12 months"
    ["bridge_3"]="Design network architecture for multi-node setup"
    ["bridge_4"]="Document hardware procurement guidelines"
    ["bridge_5"]="Create VPN mesh configuration for secure access"
    ["bridge_6"]="Build automated hardware health monitoring"
    
    # ZEN - Wellness Tasks
    ["zen_1"]="Create daily mindfulness reminder system"
    ["zen_2"]="Design 'focus mode' for deep work sessions"
    ["zen_3"]="Build stress detection and mitigation workflow"
    ["zen_4"]="Create work-life balance tracking dashboard"
    ["zen_5"]="Design periodic break reminder system"
    ["zen_6"]="Build meditation guide for operators"
    
    # STRATEGIST - Planning Tasks
    ["strategist_1"]="Update 90-day roadmap with current progress"
    ["strategist_2"]="Analyze competitive landscape quarterly"
    ["strategist_3"]="Create decision matrix for feature prioritization"
    ["strategist_4"]="Design OKR framework for Life OS goals"
    ["strategist_5"]="Build scenario planning for different growth paths"
    ["strategist_6"]="Create resource allocation optimization plan"
    
    # BUTLER - Assistant Tasks
    ["butler_1"]="Implement smart daily briefing generation"
    ["butler_2"]="Create automated meeting notes system"
    ["butler_3"]="Design task prioritization algorithm"
    ["butler_4"]="Build calendar optimization suggestions"
    ["butler_5"]="Create automated follow-up reminders"
    ["butler_6"]="Design weekly review automation"
    
    # FELIX - Maintenance Tasks
    ["felix_1"]="Create troubleshooting database for common issues"
    ["felix_2"]="Build automated bug detection system"
    ["felix_3"]="Document quick fixes for known problems"
    ["felix_4"]="Create system repair automation scripts"
    ["felix_5"]="Design preventive maintenance schedule"
    ["felix_6"]="Build emergency recovery procedures"
    
    # LANDLORD - Property Tasks
    ["landlord_1"]="Create property management automation system"
    ["landlord_2"]="Build maintenance request tracking workflow"
    ["landlord_3"]="Design tenant communication automation"
    ["landlord_4"]="Create rental income tracking dashboard"
    ["landlord_5"]="Build vendor management system"
    ["landlord_6"]="Document property maintenance checklists"
)

# Function to assign 3 tasks to each agent
assign_perpetual_tasks() {
    local agent=$1
    local agent_name=$2
    local emoji=$3
    
    echo "Assigning perpetual tasks to ${emoji} ${agent_name}..."
    
    # Get 3 random tasks from database for this agent
    local task1="${TASK_DATABASE["${agent}_1"]}"
    local task2="${TASK_DATABASE["${agent}_2"]}"
    local task3="${TASK_DATABASE["${agent}_3"]}"
    
    # Create task file
    mkdir -p ~/.openclaw/workspace/perpetual-tasks/${agent}
    cat > ~/.openclaw/workspace/perpetual-tasks/${agent}/active-tasks.md << EOF
# 🎖️ PERPETUAL TASKS - ${emoji} ${agent_name}

**Status:** ACTIVE
**System:** Perpetual Task Engine
**Last Updated:** $(date)

---

## 🎯 CURRENT MISSIONS (Always 3 Active)

### TASK 1: ${task1}
**Status:** 🔴 ACTIVE
**Priority:** HIGH
**Started:** $(date)

**Acceptance Criteria:**
- [ ] Task completed to specification
- [ ] Documentation written
- [ ] Results posted to Discord
- [ ] General notified of completion

---

### TASK 2: ${task2}
**Status:** 🔴 ACTIVE
**Priority:** HIGH
**Started:** $(date)

**Acceptance Criteria:**
- [ ] Task completed to specification
- [ ] Documentation written
- [ ] Results posted to Discord
- [ ] General notified of completion

---

### TASK 3: ${task3}
**Status:** 🔴 ACTIVE
**Priority:** HIGH
**Started:** $(date)

**Acceptance Criteria:**
- [ ] Task completed to specification
- [ ] Documentation written
- [ ] Results posted to Discord
- [ ] General notified of completion

---

## 🔄 PERPETUAL PROTOCOL

**When you complete a task:**
1. Mark it complete in this file
2. Report completion to Discord channel
3. Claw will immediately assign a new Task 4
4. You ALWAYS have 3 active missions

**Never idle. Always improving. Perpetual motion.**

---

*As ordered by the General | Executed by Claw*
EOF

    echo "  ✅ 3 perpetual tasks assigned"
}

# Assign to all 15 agents
echo "Deploying perpetual tasks to all 15 agents..."
echo ""

assign_perpetual_tasks "oracle" "The Oracle" "🔮"
assign_perpetual_tasks "diamond" "Diamond Hands" "💎"
assign_perpetual_tasks "mechanic" "The Mechanic" "⚙️"
assign_perpetual_tasks "sentinel" "Sentinel" "🛡️"
assign_perpetual_tasks "hype" "Hype Man" "📈"
assign_perpetual_tasks "ned" "Neural Net Ned" "💻"
assign_perpetual_tasks "pablo" "Podcast Pablo" "🎙️"
assign_perpetual_tasks "goldfinger" "Goldfinger" "🏦"
assign_perpetual_tasks "legal" "Legal Eagle" "⚖️"
assign_perpetual_tasks "bridge" "The Bridge" "🌐"
assign_perpetual_tasks "zen" "Zen Master" "☯️"
assign_perpetual_tasks "strategist" "The Strategist" "♟️"
assign_perpetual_tasks "butler" "The Butler" "🤵"
assign_perpetual_tasks "felix" "Fix-It Felix" "🔨"
assign_perpetual_tasks "landlord" "The Landlord" "🏠"

echo ""
echo "======================================"
echo "✅ PERPETUAL TASK SYSTEM DEPLOYED"
echo "======================================"
echo ""
echo "🎖️ Each agent now has 3 active tasks"
echo "🔄 When one completes, another begins"
echo "⚡ Never idle. Always improving."
echo ""
echo "📁 Task files: perpetual-tasks/[agent]/"
echo ""
echo "🚀 Life OS ARMY is in perpetual motion!"
