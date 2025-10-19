#!/usr/bin/env python3
import sys
import threading
import time

if sys.platform != "win32":
    import select
    import tty
    import termios
else:
    import msvcrt

from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

from .Widget import Widget

class TerminalUI:
    """Main UI framework - just add widgets"""
    
    # For smooth rendering on high refresh displays
    TARGET_FPS = 120  # Terminals can't really go higher
    FRAME_TIME = 1.0 / TARGET_FPS
    
    def __init__(self):
        self.console = Console()
        self.running = True
        self.widgets: dict[str, Widget] = {}
        self.widget_order: list[str] = []
        self.widget_panels: dict[str, dict[str, str]] = {}  # widget_name -> display info
        self.layout: Layout = Layout()  # Initialize it properly, not None
        self.start_time = time.time()
        self.ui_frames = 0
        self.post_frame_hook = None
        self._lock = threading.Lock()
        self._setup_terminal()
        
    def _setup_terminal(self):
        if sys.platform != "win32":
            self.old_term = termios.tcgetattr(sys.stdin.fileno())
            tty.setcbreak(sys.stdin.fileno())
    
    def _restore_terminal(self):
        if sys.platform != "win32" and hasattr(self, 'old_term'):
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, self.old_term)
    
    def _get_key(self) -> str | None:
        if sys.platform == "win32":
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key in (b'\x00', b'\xe0'):
                    msvcrt.getch()
                    return None
                try:
                    return key.decode('utf-8', errors='ignore')
                except:
                    return None
        else:
            if select.select([sys.stdin], [], [], 0)[0]:
                return sys.stdin.read(1)
        return None
    
    def add_widget(self, name: str, widget: Widget, layout_name: str, title: str = "", border_style: str = "green"):
        """Add a widget to the UI with display info"""
        self.widgets[name] = widget
        self.widget_order.append(name)
        self.widget_panels[name] = {
            "layout": layout_name,
            "title": title or name.title(),
            "border_style": border_style
        }
    
    def setup_layout(self):
        """Override this to define your layout"""
        self.layout = Layout()
        self.layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=4)
        )
        
        # Static header
        self.layout["header"].update(Panel(
            Align.center(Text("⚡ Terminal UI", style="bold cyan"), vertical="middle"),
            style="bright_blue"
        ))
        
        # Static footer
        footer = Text("Press [bold red]q[/] to quit | Your keys here", style="white")
        self.layout["footer"].update(Panel(
            Align.center(footer, vertical="middle"),
            style="yellow"
        ))
    
    def update_widget_display(self, name: str, widget: Widget):
        """Update a widget's display"""
        if name in self.widget_panels:
            info = self.widget_panels[name]
            panel = Panel(
                widget.render(),
                title=f"[bold]{info['title']}[/]",
                border_style=info['border_style'],
                expand=True
            )
            self.layout[info['layout']].update(panel)
    
    def _handle_input(self):
        """Input thread - minimal work here"""
        while self.running:
            key = self._get_key()
            if key:
                with self._lock:
                    if key in ('q', '\x1b'):
                        self.running = False
                    else:
                        # Let widgets handle keys in order
                        for name in self.widget_order:
                            if self.widgets[name].handle_key(key):
                                break
            time.sleep(0.005)  # 200Hz polling is plenty
    
    def run(self):
        self.setup_layout()
        
        input_thread = threading.Thread(target=self._handle_input, daemon=True)
        input_thread.start()
        
        try:
            with Live(
                self.layout, 
                console=self.console, 
                refresh_per_second=self.TARGET_FPS,
                transient=False,
                auto_refresh=False,  # WE control when to refresh
                screen=True
            ) as live:
                last_frame = time.time()
                
                while self.running:
                    now = time.time()
                    delta = now - last_frame
                    
                    # Only update if needed OR if enough time passed (for stats)
                    if delta >= self.FRAME_TIME:
                        with self._lock:
                            self.ui_frames += 1
                            if self.post_frame_hook:
                                self.post_frame_hook()
                        
                        needs_refresh = False
                        
                        with self._lock:
                            for name, widget in self.widgets.items():
                                if widget.needs_update():
                                    self.update_widget_display(name, widget)
                                    needs_refresh = True
                        
                        if needs_refresh:
                            live.refresh()
                        
                        last_frame = now
                    
                    # Precise frame timing
                    frame_cost = time.time() - now
                    sleep_time = max(0.0001, self.FRAME_TIME - frame_cost)
                    time.sleep(sleep_time)
                    
        except KeyboardInterrupt:
            self.running = False
        finally:
            self._restore_terminal()
            self.console.clear()
            self.console.print("\n[bold green]Done![/]")