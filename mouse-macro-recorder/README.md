# Mouse Macro Recorder

A Python application for recording, playing, and managing mouse macros with a simple GUI interface.

## Features

- **Record**: Capture mouse movements, clicks, and scrolls with precise timestamps
- **Playback**: Replay recorded macros with accurate timing
- **Save/Load**: Store macros as JSON files for later use
- **Configurable Delay**: Set a delay before playback starts (0-60 seconds)
- **Loop Mode**: Repeat playback indefinitely until stopped
- **User-Friendly GUI**: Simple tkinter-based interface

## Requirements

- Python 3.7 or higher
- Linux, macOS, or Windows
- `pynput` library (install via requirements.txt)

## Installation

1. Navigate to the project directory:
   ```bash
   cd mouse-macro-recorder
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## Usage

### Recording a Macro

1. Click the **Record** button to start recording
2. Perform your mouse actions:
   - Move the mouse to desired positions
   - Click (left, right, or middle button)
   - Scroll up/down/left/right
3. Click **Stop** (or press Esc) when finished

### Playing a Macro

1. Ensure a macro is loaded (recorded or loaded from file)
2. Optionally configure:
   - **Delay**: Time to wait before playback starts
   - **Loop**: Enable infinite repetition
3. Click **Play** to start playback
4. Click **Stop** (or press Esc) to cancel

### Saving a Macro

1. Record or load a macro
2. Click **Save Macro**
3. Choose a file location and name
4. The macro is saved as JSON with all event data

### Loading a Macro

1. Click **Load Macro**
2. Select a previously saved JSON file
3. The macro is ready to play

## File Format

Macros are saved as JSON files with the following structure:

```json
{
  "name": "My Macro",
  "created_at": 1234567890.123,
  "events": [
    {
      "timestamp": 0.0,
      "event_type": "move",
      "x": 100,
      "y": 200,
      "button": null,
      "pressed": null,
      "dx": null,
      "dy": null
    },
    {
      "timestamp": 0.5,
      "event_type": "click",
      "x": 100,
      "y": 200,
      "button": "left",
      "pressed": true,
      "dx": null,
      "dy": null
    }
  ],
  "description": "My recorded macro",
  "version": "1.0"
}
```

### Event Types

| Type | Description | Fields |
|------|-------------|--------|
| `move` | Mouse movement | `x`, `y` |
| `click` | Mouse button press/release | `x`, `y`, `button`, `pressed` |
| `scroll` | Mouse wheel scroll | `x`, `y`, `dx`, `dy` |

## Keyboard Shortcuts

- **Esc**: Stop recording or playback immediately

## Troubleshooting

### Permission Errors (Linux)

On Linux, you may need to grant access to input devices:

```bash
# Option 1: Run with sudo (not recommended for security)
sudo python main.py

# Option 2: Add user to input group
sudo usermod -aG input $USER
# Then log out and back in
```

### Events Not Being Recorded

- Ensure no other application is capturing mouse events
- Check that pynput is properly installed: `pip show pynput`
- Try running as administrator/root on Windows

### Playback Not Accurate

- Avoid moving the mouse during playback
- Close other applications that might interfere
- Reduce system load for better timing precision

## Architecture

```
mouse-macro-recorder/
├── main.py          # Application entry point
├── models.py        # Data models (MouseEvent, Macro)
├── recorder.py      # Recording logic using pynput
├── player.py        # Playback logic with timing
├── ui.py            # tkinter GUI components
├── requirements.txt # Python dependencies
└── README.md        # This file
```

## API Usage (Programmatic)

### Recording

```python
from recorder import MacroRecorder

recorder = MacroRecorder()
recorder.start_recording()
# ... perform mouse actions ...
events = recorder.stop_recording()
macro = recorder.get_macro("My Macro")
```

### Playback

```python
from player import MacroPlayer
from models import Macro

player = MacroPlayer()
player.load_macro(macro)
player.start_playback(delay_before=2.0, loop=False)
```

## License

MIT License - Feel free to use and modify for any purpose.

## Contributing

Contributions welcome! Please fork the repository and submit a pull request.
