"""
GUI components for mouse macro recorder.
Uses tkinter for a simple, cross-platform interface.
"""
import json
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Optional, Callable

from models import Macro, MouseEvent
from recorder import MacroRecorder
from player import MacroPlayer


class MacroRecorderUI:
    """
    Main GUI window for the mouse macro recorder.
    
    Features:
    - Record, Stop, Play, Save, Load buttons
    - Configurable delay before playback
    - Loop option for repetitive tasks
    - Event counter and status display
    """
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Mouse Macro Recorder")
        self.root.geometry("500x400")
        self.root.resizable(True, True)
        
        # Controllers
        self.recorder = MacroRecorder()
        self.player = MacroPlayer()
        self._current_macro: Optional[Macro] = None
        self._recording_start_time = 0.0
        
        # State
        self._is_recording = False
        self._is_playing = False
        
        # Callbacks for real-time updates
        self.recorder.set_event_callback(self._on_recording_event)
        self.player.set_event_callback(self._on_playback_event)
        self.player.set_complete_callback(self._on_playback_complete)
        self.player.set_stopped_callback(self._on_playback_stopped)
        
        # Setup UI
        self._setup_ui()
        self._setup_bindings()
    
    def _setup_ui(self) -> None:
        """Create and arrange all UI elements."""
        # Main frame with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="Mouse Macro Recorder",
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        status_frame.columnconfigure(1, weight=1)
        
        self.status_label = ttk.Label(status_frame, text="Ready", foreground="blue")
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        self.event_count_label = ttk.Label(status_frame, text="Events: 0")
        self.event_count_label.grid(row=0, column=1, sticky=tk.E)
        
        self.duration_label = ttk.Label(status_frame, text="Duration: 0.0s")
        self.duration_label.grid(row=1, column=1, sticky=tk.E)
        
        # Control buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=2, column=0, columnspan=2, pady=15)
        
        # Record button (red)
        self.record_btn = ttk.Button(
            buttons_frame, 
            text="Record",
            command=self._toggle_recording,
            state="normal"
        )
        self.record_btn.grid(row=0, column=0, padx=5)
        
        # Stop button
        self.stop_btn = ttk.Button(
            buttons_frame,
            text="Stop",
            command=self._toggle_playback,
            state="disabled"
        )
        self.stop_btn.grid(row=0, column=1, padx=5)
        
        # Play button
        self.play_btn = ttk.Button(
            buttons_frame,
            text="Play",
            command=self._start_playback,
            state="disabled"
        )
        self.play_btn.grid(row=0, column=2, padx=5)
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Playback Options", padding="10")
        options_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Delay before playback
        delay_frame = ttk.Frame(options_frame)
        delay_frame.grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Label(delay_frame, text="Delay before playback (seconds):").pack(side=tk.LEFT)
        self.delay_var = tk.DoubleVar(value=2.0)
        self.delay_entry = ttk.Spinbox(
            delay_frame,
            from_=0.0,
            to=60.0,
            increment=0.5,
            textvariable=self.delay_var,
            width=8
        )
        self.delay_entry.pack(side=tk.LEFT, padx=5)
        
        # Loop checkbox
        self.loop_var = tk.BooleanVar(value=False)
        self.loop_check = ttk.Checkbutton(
            options_frame,
            text="Loop playback (repeat until stopped)",
            variable=self.loop_var
        )
        self.loop_check.grid(row=1, column=0, sticky=tk.W, pady=2)
        
        # Macro info frame
        info_frame = ttk.LabelFrame(main_frame, text="Current Macro", padding="10")
        info_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        info_frame.columnconfigure(1, weight=1)
        
        ttk.Label(info_frame, text="Name:").grid(row=0, column=0, sticky=tk.W)
        self.macro_name_var = tk.StringVar(value="(no macro loaded)")
        self.macro_name_entry = ttk.Entry(
            info_frame, 
            textvariable=self.macro_name_var,
            state="readonly"
        )
        self.macro_name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        
        # Save/Load buttons frame
        file_frame = ttk.Frame(main_frame)
        file_frame.grid(row=5, column=0, columnspan=2, pady=15)
        
        self.save_btn = ttk.Button(
            file_frame,
            text="Save Macro",
            command=self._save_macro,
            state="disabled"
        )
        self.save_btn.grid(row=0, column=0, padx=5)
        
        self.load_btn = ttk.Button(
            file_frame,
            text="Load Macro",
            command=self._load_macro
        )
        self.load_btn.grid(row=0, column=1, padx=5)
        
        # Help text
        help_text = (
            "Instructions:\n"
            "1. Click 'Record' to start recording mouse actions\n"
            "2. Perform your mouse movements, clicks, and scrolls\n"
            "3. Click 'Stop' to stop recording\n"
            "4. Click 'Play' to replay your actions\n"
            "5. Use 'Save' to store your macro for later"
        )
        help_label = ttk.Label(
            main_frame, 
            text=help_text,
            font=("Arial", 8),
            foreground="gray"
        )
        help_label.grid(row=6, column=0, columnspan=2, pady=(10, 0))
    
    def _setup_bindings(self) -> None:
        """Setup keyboard shortcuts."""
        self.root.bind('<Escape>', lambda e: self._stop_all())
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
    
    def _toggle_recording(self) -> None:
        """Start or stop recording."""
        if not self._is_recording:
            self._start_recording()
        else:
            self._stop_recording()
    
    def _start_recording(self) -> None:
        """Start recording mouse events."""
        self._is_recording = True
        self._current_macro = None
        self.record_btn.config(text="Stop Recording")
        self.play_btn.config(state="disabled")
        self.save_btn.config(state="disabled")
        self.load_btn.config(state="disabled")
        self._update_status("Recording... (press Stop or Esc to finish)", "red")
        self.recorder.start_recording()
    
    def _stop_recording(self) -> None:
        """Stop recording and create a macro."""
        self._is_recording = False
        events = self.recorder.stop_recording()
        
        # Create macro
        name = f"Macro_{len(events)}events"
        self._current_macro = self.recorder.get_macro(name, "Recorded macro")
        
        # Update UI
        self.record_btn.config(text="Record")
        self.play_btn.config(state="normal")
        self.save_btn.config(state="normal")
        self.load_btn.config(state="normal")
        self._update_status(f"Recorded {len(events)} events", "blue")
        self._update_macro_info()
    
    def _toggle_playback(self) -> None:
        """Start or stop playback."""
        if not self._is_playing:
            self._start_playback()
        else:
            self._stop_playback()
    
    def _start_playback(self) -> None:
        """Start playing the current macro."""
        if not self._current_macro:
            return
        
        self._is_playing = True
        self.stop_btn.config(text="Stop Playback")
        self.record_btn.config(state="disabled")
        self.play_btn.config(state="disabled")
        self.save_btn.config(state="disabled")
        self.load_btn.config(state="disabled")
        
        delay = self.delay_var.get()
        loop = self.loop_var.get()
        
        self._update_status("Playing... (press Stop or Esc to cancel)", "green")
        
        # Start playback
        self.player.load_macro(self._current_macro)
        self.player.start_playback(loop=loop, delay_before=delay)
    
    def _stop_playback(self) -> None:
        """Stop playback."""
        self.player.stop_playback()
    
    def _stop_all(self) -> None:
        """Stop both recording and playback."""
        if self._is_recording:
            self._stop_recording()
        elif self._is_playing:
            self._stop_playback()
    
    def _save_macro(self) -> None:
        """Save the current macro to a JSON file."""
        if not self._current_macro:
            return
        
        # Ask for file path
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=f"{self._current_macro.name.replace(' ', '_')}.json"
        )
        
        if not filepath:
            return
        
        # Save to file
        try:
            with open(filepath, 'w') as f:
                json.dump(self._current_macro.to_dict(), f, indent=2)
            self._update_status(f"Saved to {filepath}", "blue")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save macro: {e}")
    
    def _load_macro(self) -> None:
        """Load a macro from a JSON file."""
        # Ask for file path
        filepath = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if not filepath:
            return
        
        # Load from file
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            self._current_macro = Macro.from_dict(data)
            self._update_status(f"Loaded: {self._current_macro.name}", "blue")
            self._update_macro_info()
            
            # Enable buttons
            self.play_btn.config(state="normal")
            self.save_btn.config(state="normal")
            
        except json.JSONDecodeError as e:
            messagebox.showerror("Error", f"Invalid JSON file: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load macro: {e}")
    
    def _on_recording_event(self, event: MouseEvent) -> None:
        """Handle event during recording (called from recorder thread)."""
        self.root.after(0, self._update_recording_ui)
    
    def _on_playback_event(
        self, 
        event: MouseEvent, 
        index: int
    ) -> None:
        """Handle event during playback (called from player thread)."""
        self.root.after(0, self._update_playback_ui, index)
    
    def _on_playback_complete(self) -> None:
        """Called when playback completes (non-looping)."""
        self._is_playing = False
        self.root.after(0, self._reset_playback_ui)
    
    def _on_playback_stopped(self) -> None:
        """Called when playback is stopped by user."""
        self._is_playing = False
        self.root.after(0, self._reset_playback_ui)
    
    def _update_status(self, text: str, color: str = "black") -> None:
        """Update the status label."""
        self.status_label.config(text=text, foreground=color)
    
    def _update_recording_ui(self) -> None:
        """Update UI during recording."""
        if self._current_macro:
            count = len(self._current_macro.events)
            duration = self._current_macro.duration()
            self.event_count_label.config(text=f"Events: {count}")
            self.duration_label.config(text=f"Duration: {duration:.2f}s")
    
    def _update_playback_ui(self, index: int) -> None:
        """Update UI during playback."""
        if self._current_macro:
            progress = self.player.get_progress()
            self.event_count_label.config(
                text=f"Event: {index + 1}/{len(self._current_macro.events)}"
            )
            self.duration_label.config(
                text=f"Progress: {progress * 100:.1f}%"
            )
    
    def _update_macro_info(self) -> None:
        """Update macro name display."""
        if self._current_macro:
            self.macro_name_var.set(
                f"{self._current_macro.name} ({len(self._current_macro.events)} events)"
            )
    
    def _reset_playback_ui(self) -> None:
        """Reset UI after playback stops."""
        self.stop_btn.config(text="Stop")
        self.record_btn.config(state="normal")
        self.play_btn.config(state="normal")
        self.save_btn.config(state="normal")
        self.load_btn.config(state="normal")
        self._update_status("Ready", "blue")
        self._update_macro_info()
    
    def _on_close(self) -> None:
        """Handle window close."""
        self._stop_all()
        self.root.destroy()
    
    def run(self) -> None:
        """Start the application."""
        self.root.mainloop()


def create_app() -> MacroRecorderUI:
    """Create and return the application instance."""
    return MacroRecorderUI()


if __name__ == "__main__":
    app = create_app()
    app.run()
