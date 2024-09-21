import time
import pickle
import argparse
from pprint import pprint
from pathlib import Path
import re
import time
from rich import print
from rich.console import Console
from rich.prompt import Confirm
from c77.zip import unzip_files, is_zip, list_archives,remove_files
from c77.logging import AppLogger
from c77.state import load_save_data, persist_save_data
from c77.config import load_config, filter_archives_by_config
from c77.ui import create_header
import logging

console = Console()

def parse_arguments():
    parser = argparse.ArgumentParser(description="Greet the user")
    parser.add_argument("action", help="enable debug logging")
    parser.add_argument("--debug", action="store_true", help="enable debug logging")
    parser.add_argument("--profile", default=None, help="which profile to deploy")
    args = parser.parse_args()
    if args.action not in ["list", "diff", "sync"]:
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
    if args.profile is not None:
        config.active_profile = args.profile
    logger.info("Loaded config from file")

    # print config data
    create_header(config, small_header=True)

    # load save data
    save_file = config.save_file
    logger.debug(f"Save file: {save_file}")
    save_data = load_save_data(file_path = save_file)

    if args.action == "list":
        print("   [bold]Deployed Mods:")
        print('\n'.join([str("    ► " + repr(x.name)) for x in save_data.keys()]))
        exit(0)

    # generate new output prediction
    archives = [a for a in list_archives(config.archive_dir)]

    # apply filters
    filtered_archives = filter_archives_by_config(archives, config)

    outputs = unzip_files(filtered_archives, config, dry_run=True)

    # find diff between outputs

    existing_archives = save_data.keys()
    new_files = outputs.keys()

    diff_str = lambda diff, prefix:"\n".join([f" {prefix} {f.name}" for f in diff])
    to_generate = new_files - existing_archives
    if len(to_generate) != 0:
        output = diff_str(to_generate, prefix=" [green]+")
        print("  [bold green]ADDING:")
        print(output)

    to_destroy = existing_archives - new_files
    if len(to_destroy) != 0:
        output = diff_str(to_destroy, prefix=" [red]-")
        print("  [bold red]REMOVING:")
        print(output)


    to_add = len(to_generate) > 0
    to_remove = len(to_destroy) > 0
    total = len(to_generate) + len(to_destroy)
    if to_add and to_remove:
        console.rule()
        print(f"  [yellow]~ {total} to change")
    elif to_add:
        console.rule()
        print(f"  [green]+ {total} to add")
    elif to_remove:
        console.rule()
        print(f"  [red]- {total} to remove")
    else:
        print("  [green] No required changes, exiting\n")
        exit(0)
    
    if args.action == "sync" and Confirm.ask("  Do you want to apply these changes?", default=False):
        # remove old files
        for files in to_destroy:
            remove_files(save_data[files])

        # add new files
        outputs = unzip_files(filtered_archives, config)
        # save data to file
        persist_save_data(save_file, outputs)

if __name__ == "__main__":
    main()
