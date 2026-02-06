"""
Recording logic for mouse macro recorder.
Handles capturing mouse events using pynput.
"""
import time
import threading
from typing import Callable, List, Optional
from pynput.mouse import Listener as MouseListener, Controller as MouseController
from pynput.mouse import Button

from models import MouseEvent, EventType, MouseButton


class MacroRecorder:
    """
    Records mouse events and stores them as a sequence of MouseEvent objects.
    
    Usage:
        recorder = MacroRecorder()
        recorder.start_recording()
        # ... perform mouse actions ...
        recorder.stop_recording()
        macro = recorder.get_macro("My Macro")
    """
    
    def __init__(self):
        self._recording = False
        self._start_time = 0.0
        self._events: List[MouseEvent] = []
        self._mouse_listener: Optional[MouseListener] = None
        self._on_event_callback: Optional[Callable[[MouseEvent], None]] = None
    
    def start_recording(self) -> None:
        """
        Start recording mouse events.
        Begins listening for mouse movements, clicks, and scrolls.
        
        Raises:
            RuntimeError: If already recording
        """
        if self._recording:
            raise RuntimeError("Already recording")
        
        self._recording = True
        self._start_time = time.time()
        self._events = []
        
        # Create and start the mouse listener
        self._mouse_listener = MouseListener(
            on_move=self._on_move,
            on_click=self._on_click,
            on_scroll=self._on_scroll
        )
        self._mouse_listener.start()
    
    def stop_recording(self) -> List[MouseEvent]:
        """
        Stop recording and return the recorded events.
        
        Returns:
            List of recorded MouseEvent objects
            
        Raises:
            RuntimeError: If not currently recording
        """
        if not self._recording:
            raise RuntimeError("Not currently recording")
        
        self._recording = False
        
        if self._mouse_listener:
            self._mouse_listener.stop()
            self._mouse_listener = None
        
        return self._events.copy()
    
    def get_macro(self, name: str, description: str = "") -> "Macro":
        """
        Get the recorded events as a Macro object.
        
        Args:
            name: Name for the macro
            description: Optional description
            
        Returns:
            Macro object containing all recorded events
            
        Raises:
            RuntimeError: If still recording
        """
        if self._recording:
            raise RuntimeError("Cannot get macro while recording. Stop recording first.")
        
        from models import Macro
        return Macro(
            name=name,
            created_at=self._start_time,
            events=self._events.copy(),
            description=description
        )
    
    def set_event_callback(
        self, 
        callback: Optional[Callable[[MouseEvent], None]]
    ) -> None:
        """
        Set a callback function to be called for each recorded event.
        
        Args:
            callback: Function to call with each MouseEvent, or None to disable
        """
        self._on_event_callback = callback
    
    def _timestamp(self) -> float:
        """Get the elapsed time since recording started."""
        return time.time() - self._start_time
    
    def _on_move(self, x: int, y: int) -> None:
        """Handle mouse movement events."""
        if not self._recording:
            return
        
        event = MouseEvent.create_move(self._timestamp(), x, y)
        self._events.append(event)
        self._call_callback(event)
    
    def _on_click(
        self, 
        x: int, 
        y: int, 
        button: Button, 
        pressed: bool
    ) -> None:
        """Handle mouse click events."""
        if not self._recording:
            return
        
        btn_name = self._button_to_name(button)
        event = MouseEvent.create_click(
            self._timestamp(), x, y, btn_name, pressed
        )
        self._events.append(event)
        self._call_callback(event)
    
    def _on_scroll(self, x: int, y: int, dx: int, dy: int) -> None:
        """Handle mouse scroll events."""
        if not self._recording:
            return
        
        event = MouseEvent.create_scroll(self._timestamp(), x, y, dx, dy)
        self._events.append(event)
        self._call_callback(event)
    
    def _button_to_name(self, button: Button) -> str:
        """Convert pynput Button to button name string."""
        if button == Button.left:
            return MouseButton.LEFT.value
        elif button == Button.right:
            return MouseButton.RIGHT.value
        elif button == Button.middle:
            return MouseButton.MIDDLE.value
        else:
            return MouseButton.UNKNOWN.value
    
    def _call_callback(self, event: MouseEvent) -> None:
        """Call the event callback if set."""
        if self._on_event_callback:
            try:
                self._on_event_callback(event)
            except Exception:
                # Callback errors should not interrupt recording
                pass
    
    @property
    def is_recording(self) -> bool:
        """Return True if currently recording."""
        return self._recording


class RecordingController:
    """
    Higher-level controller for managing recording sessions with UI integration.
    """
    
    def __init__(self):
        self.recorder = MacroRecorder()
        self._record_thread: Optional[threading.Thread] = None
    
    def start_recording(
        self, 
        name: str = "Unnamed Macro",
        callback: Optional[Callable[[MouseEvent], None]] = None
    ) -> None:
        """
        Start a recording session.
        
        Args:
            name: Name for the eventual macro
            callback: Optional callback for each event
        """
        self.recorder.set_event_callback(callback)
        self.recorder.start_recording()
    
    def stop_recording(self) -> "Macro":
        """
        Stop recording and return the macro.
        
        Returns:
            The recorded Macro object
        """
        events = self.recorder.stop_recording()
        return events


if __name__ == "__main__":
    # Simple test/demo
    print("MacroRecorder module loaded.")
    print("Usage:")
    print("  recorder = MacroRecorder()")
    print("  recorder.start_recording()")
    print("  # ... perform mouse actions ...")
    print("  recorder.stop_recording()")
    print("  macro = recorder.get_macro('My Macro')")
