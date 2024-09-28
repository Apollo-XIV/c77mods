import argparse
from c77.config import load_config
from c77.logging import AppLogger
from c77.ui import create_header
from c77.game_binding import GameBinding
import logging

def main():
    args = parse_arguments()
    logger = AppLogger(__name__, log_file=f"app.log", log_level=10, print_to_console=args.debug).get_logger()
    config = load_config(args.config, args.profile)

    game_binding = GameBinding.from_config(config)
    create_header(config, small_header = True)

    if args.action == "list":
        game_binding.list_deployed_mods()
    elif args.action == "diff":
        diff = game_binding.diff(config)
        # generate_diff(game_binding) # returns a list of actions to execute
    elif args.action == "sync":
        game_binding.sync(config)
        # game_binding.sync()
    

def parse_arguments():
    parser = argparse.ArgumentParser(description="Cyberpunk 2077 Mod Manager")
    parser.add_argument("action", help="enable debug logging")
    parser.add_argument("--debug", action="store_true", help="enable debug logging")
    parser.add_argument("--profile", default=None, help="which profile to deploy")
    parser.add_argument("--config", default="config.yaml", help="configuration file to use")
    args = parser.parse_args()
    if args.action not in ["list", "diff", "sync"]:
        print(f"[bold red]Error: Unknown command '{args.action}'")
        exit(1)
    
    return args
