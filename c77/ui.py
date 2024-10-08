import rich
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich import box
from importlib.metadata import version, metadata

console = Console()

def create_header(config, small_header=False):
    # meta = metadata("c77")
    # Create a styled Text object with a header
    app_version = "v.0.0.1"
    if small_header:
        console.print()
        title = "◤c77mods◢"
        template = "█"*(console.size.width - 25) + "[bold black on yellow]v.0.0.1[/]◤◢◤╱╱"
        start = 2
        end = min(len(template), len(title))
        border = template[:start] + title + template[end:]
        console.print("[yellow]"+border)
        pass
    else:
#         console.print(r"""[yellow]
#           ___ _____ _____                    _     
#          ╱ __\___  |___  | __ ___   ___   __| |___ 
#         ╱ ╱     ╱ ╱   ╱ ╱ '_ ` _ \ ╱ _ \ ╱ _` ╱ __|
# [black on yellow]       / /___  / /   / ╱| | | | | | (_) | (_| \__ \ [/][bold black on yellow]v.0.0.1[/]◤◢◤╱╱
#        \____╱ ╱_╱   ╱_╱ |_| |_| |_|\___╱ \__,_|___╱ [/]""")
#         width = console.size.width

        console.print(r"""[yellow]
                                                            ,,          
                                                          `7MM          
                                                            MM          
 ,p6"bo M******A'M******A'`7MMpMMMb.pMMMb.  ,pW"Wq.    ,M""bMM  ,pP"Ybd 
6M'  OO Y     A' Y     A'   MM    MM    MM 6W'   `Wb ,AP    MM  8I   `" 
8M           A'       A'    MM    MM    MM 8M     M8 8MI    MM  `YMMMa. 
YM.    ,    A'       A'     MM    MM    MM YA.   ,A9 `Mb    MM  L.   I8 
 YMbmd'    A'       A'    .JMML  JMML  JMML.`Ybmd9'   `Wbmd"MML.M9mmmP' 
[black on yellow]          A'       A'                          [bold]v.0.1.0[/][/]◤◢◤╱╱
         A'       A'                                                    
        """)

        width = console.size.width

        # Print a line of forward slashes that matches the width of the terminal
        # console.print("\n"+"[yellow]"+"/" * width)

    details_table = Table(
        show_header = False,
        box=None,
        expand=True
    )

    details_table.add_column("key", min_width=15, no_wrap=True)
    details_table.add_column("value", justify="left", no_wrap=True)
    details_table.add_row("active profile", config.active_profile)
    details_table.add_row("save file", repr(config.save_file))
    details_table.add_row("archive dir", repr(config.archive_dir))
    details_table.add_row("game dir", repr(config.game_dir))

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
