# 🌐 Local Node Architecture Guide
## *The Bridge Between Cloud and Local*

> **PERSONA MODE:** Split personality — cloud side optimistic, local side paranoid. This document bridges both worlds.

---

## Executive Summary

**☁️ Cloud Side Says:** "Local hardware is having a renaissance! The tools have never been better, cheaper, or more accessible. You can run serious AI at home now!"

**🏠 Local Side Says:** "Trust no one. Your data stays HERE. On YOUR silicon. Behind YOUR firewall. Every byte that leaves this house is a byte you don't control."

**🌉 The Bridge Says:** Both are right. The modern local node isn't an either/or proposition—it's a carefully architected hybrid that keeps sensitive operations local while leveraging cloud scale when appropriate.

---

## Part 1: Hardware Options Deep Dive

### 1.1 Raspberry Pi 5

#### Specs
| Attribute | Specification |
|-----------|---------------|
| **CPU** | Broadcom BCM2712, Quad-core Cortex-A76 @ 2.4GHz |
| **RAM** | 4GB / 8GB / 16GB LPDDR4X |
| **GPU** | VideoCore VII (800MHz) |
| **Storage** | MicroSD + PCIe 2.0 x1 (for M.2 NVMe via HAT) |
| **I/O** | 2× USB 3.0, 2× USB 2.0, Gigabit Ethernet |
| **Power** | 5V/5A USB-C (27W max) |
| **Price** | $60 (4GB) / $80 (8GB) / $120 (16GB) |

#### ☁️ Cloud Side Perspective
The Pi 5 is **genuinely impressive**. It's 2-4× faster than Pi 4, supports up to 16GB RAM, and can boot from NVMe SSD. For lightweight inference (sub-3B parameter models), home automation, file serving, and edge sensor aggregation—it's a marvel of cost engineering.

- Runs Ollama with `qwen2.5:0.5b`, `smollm2`, `gemma:2b`
- Can handle Home Assistant with 50+ devices
- Perfect for offloading low-priority tasks from your cloud bill

#### 🏠 Local Side Perspective
It's a **brittle single-board computer**. SD cards fail. The PCIe lane is shared and bottlenecked. 16GB is still limiting. No ECC RAM means bit rot is real. And the USB power delivery is a point of failure.

- SD card = ticking time bomb (use NVMe boot if possible)
- Single Ethernet = single point of failure
- Consumer-grade everything
- No hardware encryption acceleration worth mentioning

#### Verdict
**Best for:** Home automation hub, lightweight inference, secondary node, learning/experimentation  
**Avoid for:** Primary storage, mission-critical services, models >7B parameters

---

### 1.2 Intel NUC / Mini PCs

#### Specs (Intel NUC 13 Pro as reference)
| Attribute | Specification |
|-----------|---------------|
| **CPU** | Intel Core i5-1340P / i7-1360P (12-16 cores) |
| **RAM** | Up to 64GB DDR4/DDR5 SO-DIMM |
| **GPU** | Intel Iris Xe (96 EU) |
| **Storage** | 2× M.2 2280 NVMe (PCIe 4.0) |
| **I/O** | 2× Thunderbolt 4, 3× USB-A, 2.5GbE |
| **Power** | 65W-90W adapter |
| **Price** | $400-$800 barebone; $600-$1200 configured |

#### Comparable Mini PC Alternatives
| Device | CPU | RAM Max | GPU | Price |
|--------|-----|---------|-----|-------|
| Beelink SER7 | AMD Ryzen 7 7840HS | 64GB | AMD 780M (12CU) | $500-700 |
| Minisforum UM790 Pro | Ryzen 9 7940HS | 64GB | AMD 780M | $600-800 |
| ASUS NUC 14 Pro | Core Ultra 5/7 | 96GB | Intel Arc (8 Xe) | $600-900 |
| Geekom A8 | Ryzen 9 8945HS | 64GB | AMD 780M | $550-750 |

#### ☁️ Cloud Side Perspective
This is the **sweet spot for most users**. You get desktop-class compute in a 0.5L chassis. The AMD 780M iGPU can even run small LLMs via ROCm/Ollama. Up to 96GB RAM means you can load 70B quantized models (slowly). Dual NVMe slots = fast RAID options.

- Ollama with 7B-13B models at usable speeds
- Proxmox/Vmware ESXi virtualization host
- Full Linux/Windows capability
- Silent operation (most models)

#### 🏠 Local Side Perspective
**It's still a consumer device.** No ECC RAM in most models. Single power supply. Limited expansion. The "Pro" in NUC Pro is marketing—this isn't server-grade hardware. BIOS updates can brick. Intel has exited the NUC business (ASUS now manufactures).

- No IPMI = no out-of-band management
- Single NIC on most models (bonding is hacky)
- Thermal throttling under sustained load
- Proprietary power bricks

#### Verdict
**Best for:** Primary local node, virtualization host, 7B-13B model inference, development workstation  
**Avoid for:** Production workloads requiring HA, GPU-intensive training

---

### 1.3 NAS Options

#### Synology DS923+ / DS1821+
| Attribute | DS923+ | DS1821+ |
|-----------|--------|---------|
| **CPU** | AMD Ryzen R1600 (2C/4T) | AMD Ryzen V1500B (4C/4T) |
| **RAM** | 4GB base, 32GB max | 4GB base, 32GB max |
| **Bays** | 4× 3.5" + 2× M.2 (cache) | 8× 3.5" + 2× M.2 |
| **Network** | 2× 1GbE (no 10GbE option) | 2× 1GbE + 1× PCIe (10GbE add-on) |
| **Virtualization** | VMM (lightweight VMs) | VMM + Docker |
| **Price** | $600 (diskless) | $900 (diskless) |

#### TrueNAS Scale (Self-Build)
| Attribute | Entry Build | Performance Build |
|-----------|-------------|-------------------|
| **CPU** | Intel i3-12100 / AMD Ryzen 5 5600G | Xeon E-2300 / Ryzen 7 7700 |
| **RAM** | 32GB ECC DDR4 | 64-128GB ECC DDR4/DDR5 |
| **Bays** | 4-6× 3.5" | 8-12× 3.5" + NVMe |
| **Network** | 2.5GbE onboard | 10GbE + 2.5GbE |
| **Power** | 150W PicoPSU | 400W 80+ Platinum |
| **Price** | $400-600 | $800-1500 |

#### ☁️ Cloud Side Perspective
Synology is **foolproof**. DSM is polished, apps are one-click, and it just works. For users who value time over tinkering, it's unbeatable. TrueNAS Scale gives you ZFS (the gold standard), containers, and VMs on open-source software you actually control.

- Synology: Zero-config RAID, excellent mobile apps, surveillance station
- TrueNAS: ZFS snapshots, jails/containers, no vendor lock-in

#### 🏠 Local Side Perspective
Synology is a **black box**. You're dependent on their update cycle, their app ecosystem, and their pricing. The DS923+ removed hardware transcoding (a deliberate downgrade). TrueNAS has a learning cliff, but you own your data completely.

- Synology: Closed source, forced updates, discontinued models lose support
- TrueNAS: Community support only, steep learning curve, hardware compatibility lists

#### Verdict
- **Synology:** Best for users prioritizing ease-of-use over control
- **TrueNAS:** Best for data hoarders, ZFS enthusiasts, and the paranoid

---

### 1.4 GPU Options for Local LLMs

#### VRAM Requirements by Model Size (Q4_K_M Quantization)
| Model Size | VRAM Required | Example Models |
|------------|---------------|----------------|
| 1B-3B | 2-4GB | `qwen2.5:1.5b`, `smollm2`, `gemma:2b` |
| 7B-8B | 6-8GB | `llama3.1:8b`, `mistral:7b`, `deepseek-r1:7b` |
| 14B-13B | 10-12GB | `qwen2.5:14b`, `deepseek-r1:14b` |
| 30B-32B | 20-24GB | `qwen2.5:32b`, `mistral-large` |
| 70B | 40-48GB | `llama3.3:70b`, `deepseek-r1:70b` |
| 405B+ | 200GB+ | Cloud only (for mere mortals) |

#### GPU Recommendations

| GPU | VRAM | Price | Best For |
|-----|------|-------|----------|
| **RTX 4060** | 8GB | $300 | Entry-level 7B models, coding assistants |
| **RTX 4060 Ti 16GB** | 16GB | $450 | 13B models, comfortable 7B inference |
| **RTX 4070 Super** | 12GB | $600 | Balanced performance for 7B-13B |
| **RTX 4070 Ti Super** | 16GB | $800 | Sweet spot for local LLMs |
| **RTX 4090** | 24GB | $1600 | Maximum local performance, 70B models |
| **RTX 3090** | 24GB | $800 (used) | Budget 24GB option (high power draw) |
| **AMD RX 7900 XTX** | 24GB | $950 | ROCm alternative ( Linux only, less mature) |

#### ☁️ Cloud Side Perspective
Even an **RTX 4060 can run 7B models at 40+ tokens/sec** with the right quantization. That's faster than many cloud APIs! The RTX 4070 Ti Super (16GB) is the current sweet spot—enough VRAM for 13B models with room for context. For serious local work, the RTX 4090 is unmatched.

#### 🏠 Local Side Perspective
**NVIDIA owns you.** Proprietary CUDA, proprietary drivers, closed-source everything. AMD ROCm exists but is an afterthought. Intel Arc is interesting but forget about it for LLMs. You're locked into NVIDIA's ecosystem the moment you optimize for CUDA.

- Power consumption is real: 4090 = 450W under load
- Used crypto cards are a gamble
- No ECC on consumer GPUs = silent corruption possible

---

## Part 2: Architecture Design

### 2.1 Network Topology (Text Diagram)

```
                                    INTERNET
                                        │
                                        ▼
                              ┌─────────────────────┐
                              │   Cloud VPS/Host    │
                              │  (OpenClaw Cloud)   │
                              │  - Public-facing    │
                              │  - Orchestration    │
                              │  - Fallback agent   │
                              └──────────┬──────────┘
                                         │
                         ┌───────────────┼───────────────┐
                         │               │               │
                         ▼               ▼               ▼
                  ┌──────────┐   ┌──────────┐   ┌──────────┐
                  │Telegram  │   │  Brave   │   │ Calendar │
                  │  Bot     │   │  Search  │   │   API    │
                  └──────────┘   └──────────┘   └──────────┘
                         │               │               │
                         └───────────────┼───────────────┘
                                         │
                    ═════════════════════╪═════════════════════
                                         │  TAILSCALE MESH VPN
                    ═════════════════════╪═════════════════════
                                         │
                                         ▼
                              ┌─────────────────────┐
                              │   Local Node (Pi/   │
                              │   NUC/Mini PC)      │
                              │  ┌───────────────┐  │
                              │  │   Ollama      │  │
                              │  │  (LLM Host)   │  │
                              │  └───────────────┘  │
                              │  ┌───────────────┐  │
                              │  │   Docker      │  │
                              │  │  (Services)   │  │
                              │  └───────────────┘  │
                              │  ┌───────────────┐  │
                              │  │  Home Assistant│  │
                              │  │  (Automation) │  │
                              │  └───────────────┘  │
                              └──────────┬──────────┘
                                         │
                    ┌────────────────────┼────────────────────┐
                    │                    │                    │
                    ▼                    ▼                    ▼
            ┌──────────┐        ┌──────────┐        ┌──────────┐
            │   NAS    │        │  Smart   │        │ Sensors/ │
            │ (TrueNAS │        │  Devices │        │ IoT Hub  │
            │Synology) │        │ (Zigbee) │        │          │
            └──────────┘        └──────────┘        └──────────┘
```

### 2.2 Communication Patterns

#### Cloud ↔ Local Connection Options

| Method | Pros | Cons | Best For |
|--------|------|------|----------|
| **Tailscale** | Zero-config mesh, NAT traversal, open source | Relies on coordination server | Most users |
| **WireGuard** | Kernel-level, fast, minimal | Manual config, no NAT traversal helpers | Advanced users |
| **Cloudflare Tunnel** | No inbound ports, DDoS protection | Dependency on Cloudflare | Public services |
| **Reverse SSH** | Simple, works anywhere | Single point of failure, manual | Temporary/debug |
| **frp/ngrok** | Easy tunneling | Third-party dependency, rate limits | Development |

**🌉 Bridge Recommendation:** Tailscale for 95% of users. It's "magic" in the best way—works through CGNAT, requires zero firewall config, and gives you a stable 100.x.y.z IP for every device. Self-host the coordination server (Headscale) if you're truly paranoid.

### 2.3 What Runs Where: Workload Distribution

#### ☁️ Cloud Agents (Always Remote)
| Workload | Reason |
|----------|--------|
| Public-facing entry points | Security isolation |
| External API calls (search, calendar) | Rate limits, credentials |
| Large model inference (70B+) | VRAM requirements |
| Backup coordination | Geographic redundancy |
| Alerting/monitoring | Needs 24/7 uptime |

#### 🏠 Local Agents (Always On-Premise)
| Workload | Reason |
|----------|--------|
| Small/medium LLM inference (≤13B) | Privacy, latency, cost |
| File storage | Data sovereignty |
| Home automation | Local control essential |
| Personal knowledge base | Sensitive data |
| Biometric data | Legal/privacy compliance |

#### 🌉 Hybrid (Context-Dependent)
| Workload | Distribution Logic |
|----------|-------------------|
| Image analysis | Local for sensitive, cloud for complex |
| Code generation | Local for private repos, cloud for frontier |
| Document processing | Local for financial/medical, cloud for generic |
| Transcription | Local for sensitive calls, cloud for speed |

### 2.4 Data Sync Strategy

#### Sync Patterns
```
┌─────────────────────────────────────────────────────────────┐
│                    DATA CLASSIFICATION                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  TIER 1: LOCAL ONLY (Never leaves)                          │
│  ├── Financial records                                      │
│  ├── Medical data                                           │
│  ├── Biometric data                                         │
│  ├── Encryption keys                                        │
│  └── Password databases                                     │
│  SYNC: None. Air-gapped backup only.                        │
│                                                             │
│  TIER 2: LOCAL PRIMARY (Cloud encrypted backup)             │
│  ├── Personal documents                                     │
│  ├── Photos (originals)                                     │
│  ├── Code repositories                                      │
│  └── Notes/Knowledge base                                   │
│  SYNC: rclone → encrypted S3/B2 + local ZFS snapshots       │
│                                                             │
│  TIER 3: CLOUD PRIMARY (Local cache)                        │
│  ├── Shared documents                                       │
│  ├── Media library (streaming)                              │
│  └── Software packages                                      │
│  SYNC: Read-cache locally, authoritative in cloud           │
│                                                             │
│  TIER 4: EPHEMERAL (No persistence needed)                  │
│  ├── Chat history (transient)                               │
│  ├── Search results                                         │
│  └── API responses                                          │
│  SYNC: None. TTL-based eviction.                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### Recommended Sync Tools
| Tool | Use Case | Notes |
|------|----------|-------|
| **Syncthing** | Real-time folder sync | P2P, no central server |
| **rclone** | Cloud backup/sync | Universal, encrypts |
| **restic** | Versioned backups | Deduplication, encryption |
| **ZFS send/recv** | Block-level replication | Fast, efficient |
| **Nextcloud** | Self-hosted Dropbox | Heavy, but complete |

### 2.5 Security Considerations

#### ☁️ Cloud Side: "Assume breach, minimize blast radius"
- Agent tokens scoped to minimum required permissions
- Cloud resources ephemeral (cattle, not pets)
- Secrets in cloud provider KMS / HashiCorp Vault
- All access via VPN (no public SSH/RDP)

#### 🏠 Local Side: "Defense in depth, trust no one"
- Local node isolated in VLAN
- No inbound ports (outbound Tailscale only)
- Full disk encryption (LUKS/ZFS native)
- Physical security (locked rack/cabinet)
- Network segmentation (IoT on isolated VLAN)

#### 🌉 Bridge: "Verify, then trust"
```yaml
Security Layers:
  Perimeter:
    - Cloudflare Magic Firewall (if using Cloudflare Tunnel)
    - Tailscale ACLs (device-to-device rules)
    - Home firewall (OPNsense/pfSense recommended)
  
  Transport:
    - WireGuard/Tailscale encryption (WireGuard protocol)
    - Certificate pinning for agent communication
    - mTLS between cloud and local agents
  
  Application:
    - Local API authentication (API keys, not passwords)
    - Rate limiting on all endpoints
    - Request signing for critical operations
  
  Data:
    - Encryption at rest (ZFS encryption, LUKS)
    - Encryption in transit (TLS 1.3)
    - Client-side encryption for backups
```

---

## Part 3: Software Stack

### 3.1 Core Infrastructure

```yaml
Local Node Stack:
  OS:
    - Ubuntu Server LTS (recommended)
    - Debian (stable, minimal)
    - Proxmox VE (if virtualizing)
  
  Container Runtime:
    - Docker + Docker Compose (standard)
    - Podman (rootless, daemonless)
  
  LLM Inference:
    - Ollama (easiest, recommended)
    - llama.cpp (maximum control)
    - vLLM (high throughput)
  
  Networking:
    - Tailscale (mesh VPN)
    - Traefik (reverse proxy)
    - Pi-hole/Unbound (DNS filtering)
  
  Storage:
    - ZFS (recommended)
    - btrfs (acceptable)
    - ext4 (basic, no snapshots)
```

### 3.2 OpenClaw Agent Configuration

```yaml
# local-node-config.yaml
local_node:
  identity: "home-base-01"
  location: "on_premise"
  
  capabilities:
    - local_llm        # Ollama endpoint available
    - file_storage     # NAS accessible
    - home_automation  # Home Assistant integrated
    - gpu_accelerated  # NVIDIA GPU present
  
  resources:
    gpu:
      available: true
      vram_gb: 16
      cuda_version: "12.4"
    memory:
      total_gb: 64
      available_gb: 48
    storage:
      fast_ssd_gb: 2048    # NVMe
      slow_hdd_gb: 16384   # NAS
  
  ollama:
    endpoint: "http://localhost:11434"
    default_models:
      - qwen2.5:7b
      - llama3.2:latest
      - nomic-embed-text:latest
    
  cloud_bridge:
    vpn_provider: tailscale
    tailscale_auth: "tskey-auth-<redacted>"
    cloud_agent_endpoint: "https://cloud.openclaw.local:8443"
    
  security:
    enforce_local_only: true    # Refuse to upload certain data types
    encryption_at_rest: true
    allowed_egress:
      - tailscale.com
      - docker.io
      - ghcr.io
```

### 3.3 Service Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                      DOCKER COMPOSE STACK                     │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │   Ollama    │  │  Home Asst  │  │   Traefik   │          │
│  │   :11434    │  │   :8123     │  │   :80/443   │          │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘          │
│         │                │                │                  │
│  ┌──────┴──────┐  ┌──────┴──────┐  ┌──────┴──────┐          │
│  │  NVIDIA     │  │  Mosquitto  │  │  Tailscale  │          │
│  │ Container   │  │   (MQTT)    │  │   Sidecar   │          │
│  │  Toolkit    │  │   :1883     │  │             │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │  OpenClaw   │  │  Postgres   │  │   Redis     │          │
│  │ Local Agent │  │  (vector    │  │   (cache)   │          │
│  │             │  │   store)    │  │             │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │  Paperless  │  │  Immich     │  │   Jellyfin  │          │
│  │  (docs)     │  │  (photos)   │  │  (media)    │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## Part 4: Implementation Guide

### 4.1 Hardware Recommendations by Use Case

| Use Case | Hardware | Est. Cost | Ollama Models |
|----------|----------|-----------|---------------|
| **Budget Starter** | Pi 5 8GB + NVMe HAT | $150 | 0.5B-3B models |
| **Home Assistant Hub** | Pi 5 16GB + NVMe | $200 | Small models, automation focus |
| **Balanced Local Node** | NUC/mini PC 32GB + RTX 4060 Ti 16GB | $1000 | 7B-13B models, good speed |
| **Power User** | Mini PC 64GB + RTX 4070 Ti Super | $1800 | 13B models fast, 70B slow |
| **Maximum Local** | Custom build + RTX 4090 | $3500+ | 70B models usable |
| **Storage First** | TrueNAS + separate compute node | $1500+ | Models on compute, data on NAS |

### 4.2 Step-by-Step Setup

#### Phase 1: Hardware Assembly
```bash
# 1. Choose your hardware tier from above
# 2. For Pi 5: Install NVMe HAT, flash Ubuntu Server to NVMe
# 3. For NUC/Mini PC: Install RAM, SSD(s), GPU if applicable
# 4. For NAS: Install drives, configure RAID/ZFS
```

#### Phase 2: OS Installation
```bash
# Ubuntu Server LTS (recommended)
# 1. Flash ISO to USB
# 2. Install with:
#    - Full disk encryption: YES
#    - OpenSSH server: YES
#    - Docker: Install manually (newer version)

# Post-install essentials
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl wget git htop ncdu tmux
```

#### Phase 3: Tailscale Setup
```bash
# Install Tailscale
curl -fsSL https://tailscale.com/install.sh | sh

# Authenticate (creates 100.x.y.z IP)
sudo tailscale up

# Verify
tailscale status
ping <your-node-name>.tailnet-name.ts.net
```

#### Phase 4: Docker + Ollama
```bash
# Install Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker

# docker-compose.yaml for Ollama
cat > docker-compose.yml << 'EOF'
services:
  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    volumes:
      - ./ollama:/root/.ollama
    ports:
      - "11434:11434"
    environment:
      - OLLAMA_HOST=0.0.0.0:11434
    # For NVIDIA GPU support:
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    restart: unless-stopped

  # Optional: Web UI for Ollama
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: open-webui
    ports:
      - "3000:8080"
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
    volumes:
      - ./open-webui:/app/backend/data
    depends_on:
      - ollama
    restart: unless-stopped
EOF

# Start services
docker compose up -d

# Pull models
docker exec -it ollama ollama pull qwen2.5:7b
docker exec -it ollama ollama pull nomic-embed-text
```

#### Phase 5: OpenClaw Agent Setup
```bash
# Create agent configuration
mkdir -p ~/.openclaw/local-node
cat > ~/.openclaw/local-node/config.yaml << 'EOF'
node:
  name: "home-base-01"
  type: "local"
  
ollama:
  endpoint: "http://localhost:11434"
  models:
    default: "qwen2.5:7b"
    embed: "nomic-embed-text"
    
cloud:
  gateway: "wss://cloud.openclaw.local/agent"
  auth_token: "${CLOUD_AGENT_TOKEN}"
  
services:
  exposed:
    - name: "ollama"
      port: 11434
      auth: "api_key"
    - name: "home-assistant"
      port: 8123
      auth: "none"  # HA handles auth
      
privacy:
  local_only_patterns:
    - "*.medical.*"
    - "*.financial.*"
    - "password*"
    - "*ssn*"
  require_explicit_cloud_upload: true
EOF

# Run local agent (via Docker or systemd)
docker run -d \
  --name openclaw-local-agent \
  --network host \
  -v ~/.openclaw/local-node:/config \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -e CLOUD_AGENT_TOKEN=<your_token> \
  ghcr.io/openclaw/local-agent:latest
```

#### Phase 6: Verification
```bash
# Test Ollama
curl http://localhost:11434/api/generate -d '{
  "model": "qwen2.5:7b",
  "prompt": "Say hello from the local node"
}'

# Test from cloud (via Tailscale)
curl http://home-base-01.tailnet-name.ts.net:11434/api/tags

# Check agent status
docker logs openclaw-local-agent -f
```

### 4.3 Maintenance Schedule

| Task | Frequency | Command |
|------|-----------|---------|
| Update packages | Weekly | `sudo apt update && sudo apt upgrade -y` |
| Update containers | Weekly | `docker compose pull && docker compose up -d` |
| Clean Docker | Monthly | `docker system prune -a` |
| ZFS scrub | Monthly | `sudo zpool scrub tank` |
| Backup verification | Monthly | Test restore from backup |
| Full system audit | Quarterly | Review logs, access, updates |

---

## Part 5: Troubleshooting & FAQ

### Common Issues

**Q: Ollama slow on CPU only?**  
A: Expected. 7B models on CPU = 5-10 tokens/sec. Add GPU or use smaller models.

**Q: Tailscale connection drops?**  
A: Enable MagicDNS, check for conflicting VPNs, ensure UDP 41641 isn't blocked.

**Q: Docker containers can't reach local services?**  
A: Use `host.docker.internal` or `network_mode: host` for direct access.

**Q: ZFS out of space?**  
A: Check `zfs list -o space`. Run `zpool list` to see actual allocation.

**Q: GPU not detected in Docker?**  
A: Install NVIDIA Container Toolkit: `distribution=$(. /etc/os-release;echo $ID$VERSION_ID) && curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add - && curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list && sudo apt update && sudo apt install -y nvidia-container-toolkit && sudo systemctl restart docker`

---

## Appendix A: Model Performance Reference

### Raspberry Pi 5 (8GB)
| Model | Speed | Notes |
|-------|-------|-------|
| qwen2.5:0.5b | 25 tok/s | Usable for simple tasks |
| gemma:2b | 8 tok/s | Slow but works |
| llama3.2:3b | 5 tok/s | Borderline usable |

### Intel NUC + RTX 4060 Ti (16GB)
| Model | Speed | VRAM Used |
|-------|-------|-----------|
| llama3.1:8b Q4 | 45 tok/s | ~6GB |
| qwen2.5:14b Q4 | 28 tok/s | ~10GB |
| llama3.3:70b Q4 | 4 tok/s | ~42GB (offloads to system RAM) |

### RTX 4090 (24GB) Workstation
| Model | Speed | VRAM Used |
|-------|-------|-----------|
| llama3.1:8b Q4 | 120+ tok/s | ~6GB |
| qwen2.5:32b Q4 | 35 tok/s | ~20GB |
| llama3.3:70b Q4 | 15 tok/s | ~42GB (partial offload) |

---

## Appendix B: Security Checklist

- [ ] Full disk encryption enabled
- [ ] No SSH password auth (keys only)
- [ ] Fail2ban or similar rate limiting
- [ ] Tailscale ACLs configured
- [ ] Containers running non-root
- [ ] Secrets not in environment variables (use files/Vault)
- [ ] Automated backups to encrypted remote storage
- [ ] ZFS snapshots enabled with retention policy
- [ ] Firewall rules restricting inter-VLAN traffic
- [ ] Physical access controls (locked cabinet/server room)

---

*Document Version: 1.0*  
*Last Updated: 2026-02-02*  
*Maintained by: 🌐 The Bridge — Remote Local Node*

> "The cloud is someone else's computer. Make sure you have one of your own." — Ancient Sysadmin Proverb
