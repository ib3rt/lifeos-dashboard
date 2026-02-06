"""
Playback logic for mouse macro recorder.
Handles replaying recorded mouse events with timing accuracy.
"""
import time
import threading
from typing import Optional, Callable
from pynput.mouse import Controller as MouseController, Button

from models import MouseEvent, EventType, Macro


class MacroPlayer:
    """
    Plays back recorded mouse macros with timing accuracy.
    
    Usage:
        player = MacroPlayer()
        player.load_macro(macro)
        player.start_playback()
        # Macro plays back...
        player.stop_playback()
    """
    
    def __init__(self):
        self._mouse_controller = MouseController()
        self._playing = False
        self._paused = False
        self._stop_event = threading.Event()
        self._play_thread: Optional[threading.Thread] = None
        self._current_event_index = 0
        self._on_event_callback: Optional[Callable[[MouseEvent, int], None]] = None
        self._on_complete_callback: Optional[Callable[[], None]] = None
        self._on_stopped_callback: Optional[Callable[[], None]] = None
    
    def load_macro(self, macro: Macro) -> None:
        """
        Load a macro for playback.
        
        Args:
            macro: Macro object to play back
            
        Raises:
            ValueError: If macro has no events
        """
        if not macro.events:
            raise ValueError("Macro has no events to play")
        self._macro = macro
    
    def load_from_file(self, filepath: str) -> None:
        """
        Load a macro from a JSON file.
        
        Args:
            filepath: Path to the JSON file
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file contains invalid data
        """
        import json
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        macro = Macro.from_dict(data)
        self.load_macro(macro)
    
    def start_playback(
        self, 
        loop: bool = False, 
        delay_before: float = 0.0
    ) -> None:
        """
        Start playing the loaded macro.
        
        Args:
            loop: If True, repeat playback until stop() is called
            delay_before: Delay in seconds before playback starts
            
        Raises:
            ValueError: If no macro is loaded
        """
        if not hasattr(self, '_macro'):
            raise ValueError("No macro loaded. Call load_macro() first.")
        
        if self._playing:
            return
        
        self._playing = True
        self._paused = False
        self._stop_event.clear()
        
        # Start playback in a separate thread
        self._play_thread = threading.Thread(
            target=self._playback_loop,
            args=(loop, delay_before),
            daemon=True
        )
        self._play_thread.start()
    
    def stop_playback(self) -> None:
        """
        Stop the current playback.
        Blocks until playback has completely stopped.
        """
        if not self._playing:
            return
        
        self._stop_event.set()
        
        if self._play_thread and self._play_thread.is_alive():
            self._play_thread.join(timeout=2.0)
        
        self._playing = False
        self._paused = False
        
        # Call stopped callback
        if self._on_stopped_callback:
            try:
                self._on_stopped_callback()
            except Exception:
                pass
    
    def pause_playback(self) -> None:
        """Pause the current playback."""
        if self._playing:
            self._paused = True
    
    def resume_playback(self) -> None:
        """Resume a paused playback."""
        if self._paused:
            self._paused = False
    
    def is_playing(self) -> bool:
        """Return True if currently playing."""
        return self._playing and not self._paused
    
    def is_paused(self) -> bool:
        """Return True if playback is paused."""
        return self._paused
    
    def is_active(self) -> bool:
        """Return True if playing or paused."""
        return self._playing
    
    def set_event_callback(
        self, 
        callback: Optional[Callable[[MouseEvent, int], None]]
    ) -> None:
        """
        Set a callback for each event during playback.
        
        Args:
            callback: Function(event, event_index) called for each event
        """
        self._on_event_callback = callback
    
    def set_complete_callback(self, callback: Callable[[], None]) -> None:
        """Set a callback called when playback completes (non-looping)."""
        self._on_complete_callback = callback
    
    def set_stopped_callback(self, callback: Callable[[], None]) -> None:
        """Set a callback called when playback is stopped."""
        self._on_stopped_callback = callback
    
    def get_current_event_index(self) -> int:
        """Return the index of the currently playing event."""
        return self._current_event_index
    
    def get_progress(self) -> float:
        """
        Return playback progress as a percentage (0.0 to 1.0).
        Returns 0.0 if no macro is loaded.
        """
        if not hasattr(self, '_macro') or not self._macro.events:
            return 0.0
        return self._current_event_index / len(self._macro.events)
    
    def _playback_loop(self, loop: bool, delay_before: float) -> None:
        """Internal playback loop running in a thread."""
        events = self._macro.events
        
        while self._playing and not self._stop_event.is_set():
            # Initial delay
            if delay_before > 0:
                time.sleep(delay_before)
                if self._stop_event.is_set():
                    break
            
            for i, event in enumerate(events):
                if self._stop_event.is_set():
                    break
                
                # Handle pause
                while self._paused and not self._stop_event.is_set():
                    time.sleep(0.05)
                
                if self._stop_event.is_set():
                    break
                
                self._current_event_index = i
                
                # Call event callback
                if self._on_event_callback:
                    try:
                        self._on_event_callback(event, i)
                    except Exception:
                        pass
                
                # Play the event
                self._play_event(event)
                
                # Wait for the next event (timing from recording)
                if i < len(events) - 1:
                    next_timestamp = events[i + 1].timestamp
                    current_timestamp = event.timestamp
                    wait_time = next_timestamp - current_timestamp
                    if wait_time > 0:
                        time.sleep(wait_time)
            
            if not loop:
                break
        
        self._playing = False
        
        # Call complete callback if not stopped early
        if not self._stop_event.is_set() and self._on_complete_callback:
            try:
                self._on_complete_callback()
            except Exception:
                pass
    
    def _play_event(self, event: MouseEvent) -> None:
        """
        Play a single mouse event.
        
        Args:
            event: MouseEvent to play
        """
        try:
            if event.event_type == EventType.MOVE.value:
                self._mouse_controller.position = (event.x, event.y)
            
            elif event.event_type == EventType.CLICK.value:
                btn = self._name_to_button(event.button)
                if event.pressed:
                    self._mouse_controller.press(btn)
                else:
                    self._mouse_controller.release(btn)
            
            elif event.event_type == EventType.SCROLL.value:
                self._mouse_controller.scroll(event.dx, event.dy)
        
        except Exception:
            # Position may be out of bounds or other errors
            pass
    
    def _name_to_button(self, button_name: str) -> Button:
        """Convert button name string to pynput Button."""
        if button_name == MouseButton.LEFT.value:
            return Button.left
        elif button_name == MouseButton.RIGHT.value:
            return Button.right
        elif button_name == MouseButton.MIDDLE.value:
            return Button.middle
        else:
            return Button.unknown


class PlaybackController:
    """
    Higher-level controller for managing playback sessions with UI integration.
    """
    
    def __init__(self):
        self.player = MacroPlayer()
        self._macro: Optional[Macro] = None
    
    def load_macro(self, macro: Macro) -> None:
        """Load a macro for playback."""
        self._macro = macro
        self.player.load_macro(macro)
    
    def get_loaded_macro(self) -> Optional[Macro]:
        """Return the currently loaded macro."""
        return self._macro
    
    def start(
        self, 
        loop: bool = False, 
        delay_before: float = 0.0
    ) -> None:
        """Start playback."""
        self.player.start_playback(loop=loop, delay_before=delay_before)
    
    def stop(self) -> None:
        """Stop playback."""
        self.player.stop_playback()
    
    def pause(self) -> None:
        """Pause playback."""
        self.player.pause_playback()
    
    def resume(self) -> None:
        """Resume playback."""
        self.player.resume_playback()


if __name__ == "__main__":
    # Simple test/demo
    print("MacroPlayer module loaded.")
    print("Usage:")
    print("  player = MacroPlayer()")
    print("  player.load_macro(macro)")
    print("  player.start_playback()")
    print("  player.stop_playback()")
