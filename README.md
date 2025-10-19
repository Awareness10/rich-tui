# rich-tui

A lightweight, extensible terminal UI framework built on Rich for creating interactive command-line applications.

## Overview

rich-tui provides a widget-based architecture for building terminal user interfaces with minimal boilerplate. It handles rendering, input processing, and layout management while letting you focus on application logic.

## Requirements

- Python 3.13 or higher

## Installation

### Using uv (recommended)

This project uses uv for dependency management. Dependencies (including Rich) will be installed automatically.

```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone <repository-url>
cd rich-tui

# Create virtual environment and install dependencies
uv sync
```

### Using pip and venv

For users who prefer not to use uv:

```bash
# Clone the repository
git clone <repository-url>
cd rich-tui

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

```python
from src import TerminalUI, CounterWidget
from rich.layout import Layout

class MyApp(TerminalUI):
    def setup_layout(self):
        self.layout = Layout()
        counter = CounterWidget()
        self.add_widget("counter", counter, "main")

if __name__ == "__main__":
    MyApp().run()
```

Run the example application:

```bash
python main.py
```

## Project Structure

```
rich-tui/
  - src/
    - TerminalUI/
      - terminal_ui.py      # Core framework
      - Widget/             # Built-in widgets
  - main.py                 # Example application
  - pyproject.toml          # Project configuration
```

## Features

- Widget-based architecture for reusable UI components
- Automatic rendering and layout management
- Built-in input handling and event processing
- Extensible widget system
- Performance monitoring capabilities

## License

To be determined.