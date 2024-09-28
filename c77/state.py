import pickle
import copy
import os 
import logging
from rich import print
from pathlib import Path
import traceback
from dataclasses import dataclass, field
import json
from result import Ok, do
from typing import Callable
from c77.utils import try_wrap, debug
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
    all_files = [Path(archive_path + "/" + a) for a in os.listdir(archive_path)]
    out = [Mod(source=f_path) for f_path in all_files]
    logger.debug(f"Found the following archives: {out}")
    return out

@dataclass
class SaveData:
    deployed_to: str
    state: list[str | Path, Mod] = field(default_factory=list)

    @classmethod
    def load_state(cls, save_file) -> 'SaveData':
        logger = AppLogger(__name__).get_logger()

        if not os.path.exists(save_file):
            logger.info("Save file doesn't exist, blank slate")
            save_data = SaveData(
                deployed_to = "",
                state = []
            )
        else:
            with open(save_file, 'rb') as file:
                save_data = pickle.load(file)
                if (
                    not isinstance(save_data, SaveData)
                    or not isinstance(save_data.deployed_to, str)
                    or not isinstance(save_data.state, list)
                ):
                    print("[black on red]ERROR[/] Save file is corrupted")
                    logger.debug(f"Got {save_data}")
                    exit(1)
        
        logger.info(f"Loaded the following from {save_file}:\n{save_data}")
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
        log = AppLogger(__name__).get_logger()
           
        old_state = copy.deepcopy(self)
        new_state = copy.deepcopy(o)

        new_mods = [mod.source for mod in new_state.state]
        old_mods = [mod.source for mod in old_state.state]

        for mod in old_state.state:
            # if its installed check following
            if mod.state == "installed":
                # check if uninstalled or not present in result
                new_mod_state = do(
                    Ok(new_mod_state)
                    for mod_index in try_wrap(new_mods.index, "", mod.source)
                    for new_mod in Ok(new_state.state[mod_index])
                    for new_mod_state in Ok(new_mod.state)
                ).unwrap_or("uninstalled")

                if new_mod_state != "installed" or old_state.deployed_to != new_state.deployed_to:
                    log.debug(f"Adding remove instructions for {mod.source}")
                    # add remove instructions
                    instr_list = output.get(mod.source, [])
                    instr_list.append(mod.make_uninstall(old_state.deployed_to))
                    output[mod.source] = instr_list

                else:
                    log.debug(f"Mod is already installed: {mod.source}")

        for mod in new_state.state:
            # only run for mods that are meant to be installed
            if mod.state == "installed":
                old_mod_state = do(
                    Ok(old_mod_state_filtered)
                    for mod_index in try_wrap(old_mods.index, "", mod.source)
                    for old_mod in Ok(old_state.state[mod_index])
                    for old_mod_state in Ok(old_mod.state)
                    for old_mod_state_filtered in (Ok(old_mod_state) if old_state.deployed_to == new_state.deployed_to else Ok("uninstalled"))
                ).unwrap_or("uninstalled")

                if old_mod_state == "installed":
                    continue

                log.debug(f"Adding install instructions for {mod.source}")
                instr_list = output.get(mod.source, [])
                instr_list.append(mod.make_install(new_state.deployed_to))
                output[mod.source] = instr_list
                    
        return output

