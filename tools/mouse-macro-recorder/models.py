"""
Data models for mouse macro recorder.
Defines event structures for recording and playback.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Any
import time


class EventType(Enum):
    """Types of mouse events that can be recorded."""
    MOVE = "move"
    CLICK = "click"
    SCROLL = "scroll"


class MouseButton(Enum):
    """Mouse button identifiers."""
    LEFT = "left"
    RIGHT = "right"
    MIDDLE = "middle"
    UNKNOWN = "unknown"


@dataclass
class MouseEvent:
    """
    Represents a single mouse event.
    
    Attributes:
        timestamp: Time offset from recording start (in seconds)
        event_type: Type of mouse event (move, click, scroll)
        x: X coordinate (None for non-move events)
        y: Y coordinate (None for non-move events)
        button: Mouse button for click events (None otherwise)
        pressed: True if button pressed, False if released (for clicks)
        dx: Horizontal scroll amount (for scroll events)
        dy: Vertical scroll amount (for scroll events)
    """
    timestamp: float
    event_type: str
    x: Optional[int] = None
    y: Optional[int] = None
    button: Optional[str] = None
    pressed: Optional[bool] = None
    dx: Optional[int] = None
    dy: Optional[int] = None
    
    def to_dict(self) -> dict:
        """Convert event to dictionary for JSON serialization."""
        return {
            "timestamp": self.timestamp,
            "event_type": self.event_type,
            "x": self.x,
            "y": self.y,
            "button": self.button,
            "pressed": self.pressed,
            "dx": self.dx,
            "dy": self.dy
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "MouseEvent":
        """Create event from dictionary (JSON deserialization)."""
        return cls(
            timestamp=data.get("timestamp", 0),
            event_type=data.get("event_type", ""),
            x=data.get("x"),
            y=data.get("y"),
            button=data.get("button"),
            pressed=data.get("pressed"),
            dx=data.get("dx"),
            dy=data.get("dy")
        )
    
    @classmethod
    def create_move(cls, timestamp: float, x: int, y: int) -> "MouseEvent":
        """Create a move event."""
        return cls(
            timestamp=timestamp,
            event_type=EventType.MOVE.value,
            x=x,
            y=y
        )
    
    @classmethod
    def create_click(
        cls, 
        timestamp: float, 
        x: int, 
        y: int, 
        button: str, 
        pressed: bool
    ) -> "MouseEvent":
        """Create a click event."""
        return cls(
            timestamp=timestamp,
            event_type=EventType.CLICK.value,
            x=x,
            y=y,
            button=button,
            pressed=pressed
        )
    
    @classmethod
    def create_scroll(
        cls, 
        timestamp: float, 
        x: int, 
        y: int, 
        dx: int, 
        dy: int
    ) -> "MouseEvent":
        """Create a scroll event."""
        return cls(
            timestamp=timestamp,
            event_type=EventType.SCROLL.value,
            x=x,
            y=y,
            dx=dx,
            dy=dy
        )


@dataclass
class Macro:
    """
    Represents a complete macro recording.
    
    Attributes:
        name: Display name of the macro
        created_at: Unix timestamp when recording started
        events: List of mouse events in order
        description: Optional description of what the macro does
    """
    name: str
    created_at: float = field(default_factory=time.time)
    events: list = field(default_factory=list)
    description: str = ""
    version: str = "1.0"
    
    def to_dict(self) -> dict:
        """Convert macro to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "created_at": self.created_at,
            "events": [e.to_dict() for e in self.events],
            "description": self.description,
            "version": self.version
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Macro":
        """Create macro from dictionary (JSON deserialization)."""
        events = [MouseEvent.from_dict(e) for e in data.get("events", [])]
        return cls(
            name=data.get("name", "Unnamed Macro"),
            created_at=data.get("created_at", time.time()),
            events=events,
            description=data.get("description", ""),
            version=data.get("version", "1.0")
        )
    
    def duration(self) -> float:
        """Return total duration of the macro in seconds."""
        if not self.events:
            return 0.0
        return self.events[-1].timestamp
    
    def event_count(self) -> int:
        """Return total number of events."""
        return len(self.events)
