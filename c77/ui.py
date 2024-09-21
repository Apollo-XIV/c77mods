import rich
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich import box
from importlib.metadata import version, metadata

console = Console()

def create_header(config):
    # meta = metadata("c77")
    # Create a styled Text object with a header
    app_version = version('c77')
    console.print(r"""[yellow]
      ___ _____ _____                    _     
     / __\___  |___  | __ ___   ___   __| |___ 
    / /     / /   / / '_ ` _ \ / _ \ / _` / __|
   / /___  / /   / /| | | | | | (_) | (_| \__ \
   \____/ /_/   /_/ |_| |_| |_|\___/ \__,_|___/ [/]""" + f"[bold]{app_version}[/]")
    width = console.size.width

    # Print a line of forward slashes that matches the width of the terminal
    console.print("\n"+"[yellow]"+"/" * width)

    details_table = Table(
        show_header = False,
        box=None,
        expand=True
    )

    details_table.add_column("key", min_width=15, no_wrap=True)
    details_table.add_column("value", justify="left", no_wrap=True)
    details_table.add_row("active profile", config.active_profile)
    details_table.add_row("save file", config.save_file)
    details_table.add_row("archive dir", config.archive_dir)
    details_table.add_row("game dir", config.game_dir)

    # Create a panel around the details table with additional styling
    header_panel = Panel(
        details_table, 
        expand=True,  # Expand to the full width of the terminal
        border_style="green",  # Color of the panel border
        box=box.MINIMAL
    )

    # Print the header panel to the console
    console.print(header_panel)
    console.rule()
