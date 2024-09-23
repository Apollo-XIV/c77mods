import pickle
import copy
import os 
import logging
import traceback
from dataclasses import dataclass, field
from typing import Callable
from c77.utils import try_wrap
from c77.models import Mod
from c77.logging import AppLogger


def load_save_data(file_path: str) -> dict:
    logger = AppLogger(__name__).get_logger()
    # if savefile doesn't exist, return empty dict
    if not os.path.exists(file_path):
        return {}

    try:
        with open(file_path, "rb") as file:  # Use 'rb' for reading in binary mode
            loaded_data = pickle.load(file)
            logger.info(f"Loaded state data from {file_path}")
            return loaded_data
    except Exception as e:
        logger.critical(e)
        exit(1)

def persist_save_data(file_path:str, data: dict) -> None:
    logger = AppLogger(__name__).get_logger()
    with open(file_path, "wb") as file:  # Use 'wb' for writing in binary mode
        pickle.dump(data, file)
        logger.info(f"Persisted to {file_path}")

def list_archives(archive_path: str) -> list[str]:
    logger = AppLogger().get_logger()
    all_files = [archive_path + "/" + a for a in os.listdir(archive_path)]
    out = [Mod(source=f_path) for f_path in all_files]
    logger.debug(f"Found the following archives: {out}")
    return out

@dataclass
class SaveData:
    deployed_to: str
    state: list[str, Mod] = field(default_factory=list)

    @classmethod
    def load_state(cls, save_file) -> 'SaveData':
        logger = AppLogger(__name__).get_logger()

        if not os.path.exists(save_file):
            logger.info("Save file doesn't exist, blank slate")
            return SaveData(
                deployed_to = "",
                state = {}
            )

        with open(save_file, 'rb') as file:
            save_data = pickle.load(file)
            if (
                not isinstance(save_data, SaveData)
                or not isinstance(save_data.deployed_to, str)
                or not isinstance(save_data.state, list[str, Mod])
            ):
                raise ValueError("Save file is corrupted")
        
        return save_data

    @classmethod
    def generate_state(cls, config):
        logger = AppLogger(__name__).get_logger()
        # load mods from archive_dir
        mods = list_archives(config.archive_dir)
        mods = [mod.filter_profile(config.profile) for mod in mods]

        logger.debug(f"generated the following state: {mods}")

        save_data = SaveData(
            deployed_to = config.game_dir,
            state = mods
        )
        return save_data


    def diff(self, o: 'SaveData') -> dict[Mod, list[Callable[[Mod],None]]]:
        """
            {
                new_state => actions for remediation
            }
            returns a dicitonary that links the mods in the output with the functions to execute to create it
        """
        output = {}
        old_state = copy.deepcopy(self)
        new_state = copy.deepcopy(o)
        print(old_state)
        print(new_state)
        for mod in old_state.state:
            # find mod in new state
            result = try_wrap([new_mod.source for new_mod in o.state].index, "Mod should be deleted", mod.source)
            print(result)
            # if can't be found, or deployed_to is different, add uninstalled state to diff and removal actions
            # if state is different, remediate

        # for the remaining new_state mods, add install methods to output

        

