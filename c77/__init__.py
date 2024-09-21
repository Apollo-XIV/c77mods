import time
import pickle
import argparse
from pprint import pprint
from pathlib import Path
import re
import time
from rich import print
from c77.zip import unzip_file, is_zip, list_archives
from c77.logging import AppLogger
from c77.state import load_save_data, persist_save_data
from c77.config import load_config
from c77.ui import create_header
import logging

def parse_arguments():
    parser = argparse.ArgumentParser(description="Greet the user")
    parser.add_argument("action", help="enable debug logging")
    parser.add_argument("--debug", action="store_true", help="enable debug logging")
    args = parser.parse_args()
    if args.action not in ["diff", "deploy"]:
        print(f"[bold red]Error: Unknown command '{args.action}'")
        exit(1)
    
    return args

def main():
    args = parse_arguments()
    # timestamp = int(str(time.time()).split(".")[0])
    timestamp = "app"
    logger = AppLogger(__name__, log_file=f"{timestamp}.log", log_level=logging.DEBUG, print_to_console=args.debug).get_logger()
    logger.info(f"Logging to {timestamp}.log")

    # load config settings
    config = load_config("./config.yaml")
    logger.info("Loaded config from file")

    # print config data
    create_header(config)

    # load save data
    save_file = config.save_file
    logger.debug(f"Save file: {save_file}")
    save_data = load_save_data(file_path = save_file)

    # generate new output prediction
    archives = [a for a in list_archives(config.archive_dir)]

    outputs = {}
    for zip in archives:
        # pass
        out = unzip_file(zip, config.game_dir, dry_run=True)
        outputs[Path(zip)] = out

    # find diff between outputs

    existing_archives = save_data.keys()
    new_files = outputs.keys()

    diff_str = lambda diff, prefix:"\n".join([f" {prefix} {f.name}" for f in diff])
    to_generate = new_files - existing_archives
    if len(to_generate) != 0:
        output = diff_str(to_generate, prefix="[green]+")
        print("[green]ADDING:")
        print(output)

    to_destroy = existing_archives - new_files
    if len(to_destroy) != 0:
        output = diff_str(to_destroy, prefix="[red]-")
        print("[red]REMOVING:")
        print(output)
    
    if args.action == "deploy":
        # deploy the new archives
        # pprint(outputs)

        # save data to file
        persist_save_data(save_file, outputs)

if __name__ == "__main__":
    main()
