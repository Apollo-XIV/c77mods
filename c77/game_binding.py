"""
    This module is used to link a directory of archives to a game directory.
"""
from rich import print
from dataclasses import dataclass
from typing import Callable
from c77.config import Config
from c77.models import Mod
from c77.state import SaveData
from c77.logging import AppLogger

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
        old_state.diff(desired_state)


