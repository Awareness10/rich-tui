#!/usr/bin/env python3

from abc import ABC, abstractmethod
from rich.console import RenderableType

class Widget(ABC):
    """Base widget class - override render() and optionally handle_key()"""
    
    def __init__(self):
        self._dirty = True
    
    @abstractmethod
    def render(self) -> RenderableType:
        """Return a Rich renderable object"""
        pass
    
    def handle_key(self, key: str) -> bool:
        """Handle a key press. Return True if handled, False otherwise"""
        return False
    
    def needs_update(self) -> bool:
        """Override to implement smart updating"""
        return self._dirty