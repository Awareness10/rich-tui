#!/usr/bin/env python3
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.align import Align
from rich.panel import Panel
from rich.text import Text
import time
import sys
import threading
from datetime import datetime

if sys.platform != "win32":
    import tty, termios, select
    
class Counter:
    def __init__(self):
        self.value = 0
        self.last_op = "Ready"
        self.running = True
        self.fps = 0
        self.frame_count = 0
        self.start_time = time.time()
        
        # Setup terminal
        if sys.platform != "win32":
            self.old_term = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin)
        
        # Start input thread
        threading.Thread(target=self._handle_input, daemon=True).start()
    
    def _handle_input(self):
        while self.running:
            if sys.platform == "win32":
                import msvcrt
                if msvcrt.kbhit():
                    key = msvcrt.getch().decode('utf-8', errors='ignore')
                else:
                    time.sleep(0.01)
                    continue
            else:
                if select.select([sys.stdin], [], [], 0)[0]:
                    key = sys.stdin.read(1)
                else:
                    time.sleep(0.01)
                    continue
            
            if key == 'i':
                self.value += 1
                self.last_op = "Incremented"
            elif key == 'd':
                self.value -= 1
                self.last_op = "Decremented"
            elif key == 'r':
                self.value = 0
                self.last_op = "Reset"
            elif key == 'q':
                self.running = False
                break
    
    def render(self):
        # Calculate FPS
        elapsed = time.time() - self.start_time
        self.fps = self.frame_count / elapsed if elapsed > 0 else 0
        self.frame_count += 1
        
        # Build the UI
        table = Table.grid(padding=1)
        table.add_column(justify="center")
        
        # Counter display
        color = "red" if self.value < 0 else "yellow" if self.value > 100 else "green"
        table.add_row(Text(str(self.value), style=f"bold {color}", justify="center"))
        table.add_row(Text(self.last_op, style="dim italic"))
        table.add_row("")
        
        # Stats
        table.add_row(Text(f"Time: {datetime.now().strftime('%H:%M:%S')}", style="cyan"))
        table.add_row(Text(f"Runtime: {int(elapsed)}s", style="cyan"))
        table.add_row(Text(f"FPS: {self.fps:.1f}", style="cyan"))
        table.add_row("")
        
        # Controls
        table.add_row(Text("[i]ncrement [d]ecrement [r]eset [q]uit", style="yellow"))
        
        return Panel(Align.center(table, vertical="middle"), 
                    title="Terminal Counter", 
                    border_style="blue")
    
    def cleanup(self):
        if sys.platform != "win32" and hasattr(self, 'old_term'):
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_term)

def main():
    console = Console()
    counter = Counter()
    
    try:
        with Live(counter.render(), console=console, refresh_per_second=85) as live:
            while counter.running:
                live.update(counter.render())
                time.sleep(1/85)
    finally:
        counter.cleanup()
        console.print("\n[green]Goodbye![/green]")

if __name__ == "__main__":
    main()