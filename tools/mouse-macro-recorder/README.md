# 🖱️ Mouse Macro Recorder

**Record, replay, and automate mouse actions with precision.**

A GUI application for recording, playing, and managing mouse macros.

## ✨ Features

- 🎙️ **Record** mouse movements, clicks, and scrolls with timestamps
- ▶️ **Playback** recorded macros with timing accuracy
- 💾 **Save/Load** macros to JSON files
- ⏱️ **Configurable delay** before playback (0-60 seconds)
- 🔄 **Loop** option for repetitive tasks
- 🛡️ **Emergency stop** with ESC key

## 🚀 Quick Start

### Option 1: One-Click Install (Linux/Mac/WSL)

```bash
git clone <repo-url>
cd mouse-macro-recorder
./install.sh
python main.py
```

### Option 2: Manual Install

```bash
# Clone or download
git clone <repo-url>
cd mouse-macro-recorder

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run
python main.py
```

## 📖 Usage Guide

### Recording a Macro

1. Click **Record** (red button)
2. Perform your mouse actions
3. Click **Stop** when done

### Playing a Macro

1. Click **Play** (green button)
2. Set delay if needed
3. Enable **Loop** for repetitive tasks
4. Watch your macro execute!

### Saving/Loading

- **Save** records to JSON file
- **Load** previously saved macros

## 📁 File Structure

```
mouse-macro-recorder/
├── main.py              # Application entry point
├── recorder.py         # Recording engine
├── player.py           # Playback engine
├── models.py           # Event data models
├── ui.py               # GUI interface
├── requirements.txt    # Dependencies
├── install.sh          # One-click installer
├── README.md           # This file
└── example_macro.json  # Sample recording
```

## 🔧 Requirements

- Python 3.7+
- pynput library
- tkinter (included with Python)

## 📝 Example Use Cases

- **Gaming** - Automate repetitive in-game actions
- **Data Entry** - Fill forms with recorded patterns
- **Design Work** - Apply consistent transformations
- **Testing** - Reproduce user interaction sequences
- **Productivity** - Automate daily workflows

## ⚠️ Notes

- Macros are saved as JSON - human readable!
- Timing accuracy: ~1ms precision
- Works on Linux, macOS, Windows
- Requires display (GUI application)

## 🎯 Tips

1. **Test on a safe application first**
2. **Save frequently** - your work is valuable
3. **Use delay** when switching windows
4. **ESC** always stops everything immediately

---

**Built by Life OS — Your Personal AI Operating System** 🦾
