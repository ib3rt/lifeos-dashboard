#!/usr/bin/env python3
"""
Mouse Macro Recorder - Main Application Entry Point

A GUI application for recording, playing, and managing mouse macros.

Features:
- Record mouse movements, clicks, and scrolls with timestamps
- Play back recorded macros with timing accuracy
- Save and load macros to/from JSON files
- Configurable delay before playback
- Loop option for repetitive tasks

Usage:
    python main.py

Requirements:
    - Python 3.7+
    - pynput library (install via requirements.txt)

Author: AI Assistant
Version: 1.0.0
"""

import sys
import os

# Add the application directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui import MacroRecorderUI, create_app


def main():
    """
    Main entry point for the application.
    
    Creates and runs the macro recorder GUI.
    """
    print("=" * 50)
    print("  Mouse Macro Recorder v1.0.0")
    print("=" * 50)
    print()
    print("Starting application...")
    print()
    print("Controls:")
    print("  - Record: Start recording mouse actions")
    print("  - Stop: Stop recording/playback")
    print("  - Play: Replay recorded macro")
    print("  - Save/Load: Store or retrieve macros")
    print("  - ESC: Emergency stop (in any mode)")
    print()
    print("-" * 50)
    
    # Create and run the application
    app = create_app()
    
    try:
        app.run()
    except KeyboardInterrupt:
        print("\nApplication closed by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
