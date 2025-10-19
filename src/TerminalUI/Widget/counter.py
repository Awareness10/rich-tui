#!/usr/bin/env python3
from rich.align import Align
from rich.text import Text
from rich.table import Table

from .widget_base import Widget

class CounterWidget(Widget):
    def __init__(self):
        super().__init__()
        self.value = 0
        self.last_op = "Ready"
        
    def render(self):
        style = "bold red" if self.value < 0 else "bold yellow" if self.value > 100 else "bold green"
        self._dirty = False
        table = Table(expand=True, show_header=False, box=None)
        table.add_row(Text("Counter Value", style="dim bold"))
        table.add_row(Text(str(self.value), style=style + " bold"))
        table.add_row(Text(self.last_op, style="italic dim"))
        return Align.center(table, vertical="middle")
    
    def handle_key(self, key: str) -> bool:
        old = self.value
        if key == 'i':
            self.value += 1
            self.last_op = f"Incremented ({old} → {self.value})"
        elif key == 'd':
            self.value -= 1
            self.last_op = f"Decremented ({old} → {self.value})"
        elif key == 'r':
            self.value = 0
            self.last_op = f"Reset (was {old})"
        elif key == 'm':
            self.value *= 2
            self.last_op = f"Doubled ({old} → {self.value})"
        elif key == 'v':
            self.value //= 2
            self.last_op = f"Halved ({old} → {self.value})"
        else:
            return False
        self._dirty = True
        return True