#!/usr/bin/env python3

import sys
from typing import cast

from rich.align import Align
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text

from src import TerminalUI, CounterWidget, StatsWidget, StatsData

class MyApp(TerminalUI):
    """Your actual application - just configure widgets and layout"""

    def post_frame(self):
        if "stats" in self.widgets:
            stats_widget = cast(StatsWidget, self.widgets["stats"])
            stats_widget.update_frames(self.ui_frames)
    
    def setup_layout(self):
        self.layout = Layout()
        self.layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="stats", size=5),
            Layout(name="footer", size=4)
        )
        
        # Add header
        self.layout["header"].update(Panel(
            Align.center(Text("⚡ Extensible Terminal UI", style="bold cyan"), vertical="middle"),
            style="bright_blue"
        ))
        
        # Add widgets with their layout locations
        counter = CounterWidget()
        stats_data = StatsData(start_time=self.start_time, ui_frames=self.ui_frames)
        stats = StatsWidget(stats_data)
        
        self.add_widget("counter", counter, "main", "Counter", "green")
        self.add_widget("stats", stats, "stats", "Statistics", "blue")
        
        # Initial render
        self.update_widget_display("counter", counter)
        self.update_widget_display("stats", stats)
        
        # Footer with controls
        footer = Text.assemble(
            ("[i]", "bold cyan"), ("ncrement ", "white"),
            ("[d]", "bold cyan"), ("ecrement ", "white"),
            ("[r]", "bold cyan"), ("eset ", "white"),
            ("[m]", "bold cyan"), ("ultiplyx2 ", "white"),
            ("di", "white"), ("[v]", "bold cyan"), ("ide ", "white"),
            ("[q]", "bold red"), ("uit", "white")
        )
        self.layout["footer"].update(Panel(
            Align.center(footer, vertical="middle"),
            style="yellow",
            title="[bold]Controls[/]"
        ))

        self.post_frame_hook = self.post_frame


if __name__ == "__main__":
    try:
        MyApp().run()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)