import time
from dataclasses import dataclass
from datetime import datetime

from rich.align import Align
from rich.table import Table

from .widget_base import Widget

@dataclass
class StatsData:
    start_time: float
    ui_frames: int

class StatsWidget(Widget):
    def __init__(self, stats_data: StatsData):
        super().__init__()
        self.start_time = stats_data.start_time
        self._last_time_str = ""
        self._ui_frames = stats_data.ui_frames  # Update externally as needed
        
    def update_frames(self, frames: int) -> None:
        self._ui_frames = frames
        
    def render(self):
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Property", style="cyan")
        table.add_column("Value", justify="right")
        
        current_time = datetime.now().strftime("%H:%M:%S")
        runtime = time.time() - self.start_time
        
        table.add_row("Time", current_time)
        table.add_row("Runtime", f"{int(runtime)}s")
        table.add_row("FPS", f"{self._ui_frames / runtime if runtime > 0 else 0:.1f}")
        
        self._last_time_str = current_time
        self._dirty = False
        return Align.center(table, vertical="middle")
    
    def needs_update(self) -> bool:
        current = datetime.now().strftime("%H:%M:%S")
        changed = current != self._last_time_str
        self._dirty = changed
        return self._dirty