import time
import logging
import pickle
from pprint import pprint
from pathlib import Path
import re
from yaml import load, dump
from rich import print
from c77.zip import *
from c77.logging import AppLogger

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

logger = AppLogger("mods").get_logger()


def config(filepath):
    return load(open(filepath, 'r').read(), Loader=Loader)

# load config settings
config = config("./config.yaml")
save_file = config["state-file"]
logger.info("Loaded config from file")

# load profile
profile_name = "default"
profile = config["profiles"][profile_name]
logger.info(f"Loaded profile '{profile_name}'")

# load save data
try:
    with open(save_file, "rb") as file:  # Use 'rb' for reading in binary mode
        loaded_data = pickle.load(file)
        logger.info("Found state data")
except:
    logger.error("Couldn't find any state data")
    loaded_data = {}

# generate new output prediction
archives = [a for a in list_archives(config["archives-dir"])]
outputs = {}
for zip in archives:
    # pass
    out = unzip_file(zip, config["game-dir"], dry_run=True)
    outputs[Path(zip)] = out

# find diff between outputs

existing_archives = loaded_data.keys()
new_files = outputs.keys()
to_generate = new_files - existing_archives
to_destroy = existing_archives - new_files
for f in to_generate:
    print(f"[green] + {f.name}")

for f in to_destroy:
    print(f"[red] - {f.name}")

# deploy the new archives
# pprint(outputs)

# save data to file
with open(save_file, "wb") as file:  # Use 'wb' for writing in binary mode
    pickle.dump(outputs, file)
