# 🎙️ ElevenLabs Voice Cloning Setup

## Overview
Setting up voice cloning for Podcast Pablo to create authentic-sounding podcast content using your voice.

## Requirements

### 1. ElevenLabs Account
- Sign up at: https://elevenlabs.io
- Recommended plan: Starter ($5/month) or Creator ($22/month)
- Free tier: 10,000 characters/month (limited)

### 2. Voice Recording Session
**Duration:** 10-30 minutes of clean audio

**Recording Setup:**
- Quiet room (no echo, no background noise)
- Good microphone (USB mic or better)
- Consistent distance from mic (6-12 inches)
- Natural speaking voice (conversational, not robotic)

**Recording Content (Read Aloud):**
```
Welcome to the Life OS podcast. I'm your host, and today we're exploring
how autonomous AI agents can transform your productivity. 

The concept is simple: you have a team of 15 specialized AI agents, each
with their own personality and expertise. They work 24/7 on your behalf,
handling research, content creation, monitoring, and more.

In this episode, we'll dive deep into the perpetual task system that keeps
all agents constantly improving. We'll also look at real results from the
first month of operation, including the 45 concurrent missions currently
in progress.

Whether you're an entrepreneur, developer, or just curious about AI,
this system represents the future of personal productivity.

Let's get started.
```

**Alternative Content Ideas:**
- Read from a favorite book/article
- Explain a technical concept you know well
- Tell a personal story
- Discuss your vision for Life OS

### 3. Minimum Audio Requirements
- **Length:** Minimum 1 minute (longer = better quality)
- **Format:** MP3, WAV, or M4A
- **Quality:** 44.1kHz, 16-bit minimum
- **No:** Background music, noise, other voices

## Setup Steps

### Step 1: Record Your Voice
```bash
# Option 1: Use arecord (Linux)
arecord -f cd -t wav voice-sample.wav

# Option 2: Use ffmpeg
ffmpeg -f alsa -i default -ar 44100 -ac 1 voice-sample.wav

# Option 3: Use phone voice recorder app
# Transfer file to computer
```

### Step 2: Upload to ElevenLabs
1. Go to https://elevenlabs.io/voice-lab
2. Click "Add Generative or Cloned Voice"
3. Select "Instant Voice Cloning"
4. Upload your audio file
5. Name it: "b3rt-podcast-host"
6. Wait for processing (1-5 minutes)

### Step 3: Test Voice
```bash
# Install ElevenLabs Python SDK
pip install elevenlabs

# Test script
python3 << 'PYEOF'
from elevenlabs import generate, play

audio = generate(
    text="Welcome to the Life OS podcast. I'm b3rt, and this is my AI-powered show.",
    voice="b3rt-podcast-host",  # Your cloned voice name
    model="eleven_multilingual_v2"
)
play(audio)
PYEOF
```

### Step 4: Podcast Pablo Integration
Once voice is cloned, Pablo can:
- Generate podcast scripts
- Convert to audio using your voice
- Create intro/outro segments
- Produce episode content automatically

## Usage Examples

### Generate Podcast Intro
```python
from elevenlabs import generate, save

intro = generate(
    text="""Welcome to Episode 12 of the Life OS Podcast. 
    Today we're diving into the perpetual task system that keeps 
    15 AI agents working 24/7 on your behalf. I'm your host, b3rt.""",
    voice="b3rt-podcast-host",
    model="eleven_multilingual_v2"
)

save(intro, "episode-12-intro.mp3")
```

### Full Episode Generation
```python
# Pablo will handle this automatically
script = pablo.generate_episode_script(topic="AI Productivity")
audio = elevenlabs.generate(text=script, voice="b3rt-podcast-host")
save(audio, f"episode-{episode_num}.mp3")
```

## Cost Estimation

| Plan | Monthly Characters | Cost | Episodes (10min) |
|------|-------------------|------|------------------|
| Free | 10,000 | $0 | ~1 episode |
| Starter | 30,000 | $5 | ~3 episodes |
| Creator | 100,000 | $22 | ~10 episodes |
| Pro | 500,000 | $99 | ~50 episodes |

*10-minute episode ≈ 1,500-2,000 words ≈ 8,000-10,000 characters*

## Next Steps

1. **Record your voice sample** (10-30 min)
2. **Create ElevenLabs account**
3. **Upload and clone voice**
4. **Test with sample script**
5. **Pablo takes over** - automated podcast production

## Resources

- ElevenLabs: https://elevenlabs.io
- Voice Lab: https://elevenlabs.io/voice-lab
- API Docs: https://elevenlabs.io/docs

---
*Prepared for Podcast Pablo | Life OS*
