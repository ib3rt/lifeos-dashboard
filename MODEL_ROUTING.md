# Agent Model Routing

*Which models power which agents.*

---

## Model Indicators

| Emoji | Model | Location | Best For |
|-------|-------|----------|----------|
| 🌙 | Kimi K2.5 | Cloud (Moonshot) | Complex reasoning, primary tasks |
| 🏠 | Qwen3 14B | Local (Your 9070XT) | Fast, private, cost-free agent work |

---

## Default Routing

### 🌙 Cloud-First (Kimi K2.5)
**Agents:**
- 💰 Finance Director
- ⚖️ Legal & Compliance Advisor
- 🎯 Strategy & Innovation Consultant
- 🏢 Asset & Risk Manager

**Why:** High-stakes decisions need maximum capability.

---

### 🏠 Local-First (Qwen3 14B)
**Agents:**
- 📈 Marketing & Sales Lead
- ⚙️ Operations Coordinator
- 💻 IT & Tech Specialist
- 📋 Executive Support Assistant
- 🔧 Maintenance & Mechanics Expert
- ✈️ Travel & Logistics Planner

**Why:** High-volume, lower-risk tasks. Saves tokens, faster response.

---

### 🌙🏠 Hybrid (Context-Dependent)
**Agents:**
- 🧘 Health & Wellness Coach (local for routine, cloud for complex)
- 🛡️ Cybersecurity Guardian (local for monitoring, cloud for incident response)

---

## Override Commands

Force a specific model for any request:

| Command | Effect |
|---------|--------|
| `/use local` | Switch to Qwen3 14B for next task |
| `/use cloud` | Switch to Kimi K2.5 for next task |
| `/use auto` | Return to agent-based routing |

---

## Cost Tracking

| Model | Input Cost | Output Cost | Typical Use |
|-------|-----------|-------------|-------------|
| 🌙 Kimi K2.5 | Variable | Variable | Primary reasoning |
| 🏠 Qwen3 14B | $0 | $0 | Agent tasks, quick queries |

---

*Last updated: 2026-02-02*
