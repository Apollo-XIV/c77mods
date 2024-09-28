"""
    This module is used to link a directory of archives to a game directory.
"""
import time
from pathlib import Path
from rich import print
from rich.prompt import Confirm
from rich.console import Console
from rich.progress import Progress
from rich.status import Status
from rich.spinner import Spinner
from dataclasses import dataclass
from typing import Callable
from c77.config import Config
from c77.models import Mod
from c77.state import SaveData, persist_save_data
from c77.logging import AppLogger

console = Console()

@dataclass
class GameBinding:
    archive_dir: str
    game_dir: str
    state: SaveData

    @classmethod
    def from_config(cls, config: Config) -> 'GameBinding':
        out = GameBinding(
            archive_dir = config.archive_dir,
            game_dir = config.game_dir,
            state = SaveData.load_state(config.save_file)
        )
        return out

    def list_deployed_mods(self):
        installed_mods = [mod for mod in self.state.state if mod.state == "installed"]
        out_string = (
            '\n'.join([str("    ► " + repr(x.name)) for x in installed_mods])
            if len(installed_mods) != 0
            else "[red]NONE[/]"
        )
        print(f"   [bold]Deployed Mods: [green]{out_string}[/]")
        return installed_mods

    def diff(self, config) -> list[Callable[[Mod],None]]:
        old_state = self.state
        desired_state = SaveData.generate_state(config)
        diff = old_state.diff(desired_state)

        def make_filter(keyword: str):
            def filter(seq):
                names = [f.__name__ for f in seq]
                if keyword in names and len(seq) == 1:
                    return True
                return False
            return filter
        
        to_remove = [
            f"[red]  - {key.name}"
            for key, value in diff.items()
            if make_filter("uninstall")(value)
        ]
        # list files to be removed
        if len(to_remove) != 0:
            print(f"[red]  UNINSTALLING:")
            print('\n'.join(to_remove))

        # list files to replace
        to_replace = [
            f"[yellow]  ~ {key.name}"
            for key, value in diff.items()
            if (
                not make_filter("install")(value) 
                and not make_filter("uninstall")(value)
            )
        ]
        # list files to be removed
        if len(to_replace) != 0:
            print(f"[yellow]  REPLACING:")
            print('\n'.join(to_replace))

        to_install = [
            f"[green]   + {key.name}"
            for key, value in diff.items()
            if make_filter("install")(value)
        ]
        # list files to be added
        if len(to_install) != 0:
            print(f"[green]  ADDING:")
            print('\n'.join(to_install))

        return diff

    def sync(self, config):
        todo = self.diff(config)
        if len(todo) == 0:
            print("  Nothing to change, [red]EXITING[/]...\n")
            return
        console.rule()
        end_state = []
        if not Confirm.ask("  Would you like to deploy these changes?"):
            return
        with Status(status="running commands", spinner="aesthetic", spinner_style="yellow") as status:
            for path, actions in todo.items():
                status.update(f"Installing {path.name}")
                output = None
                for action in actions:
                    output = action()
                end_state.append(output)
                time.sleep(0.5)
        end_state = [s for s in end_state if s != None]
        persist_save_data(config.save_file,SaveData(deployed_to=config.game_dir, state=end_state))
