from dataclasses import dataclass
import yaml
import fnmatch
from yaml import Loader as Loader
from rich import print
from c77.logging import AppLogger


def load_config(filepath):
    logger = AppLogger(__name__).get_logger()
    data = yaml.load(open(filepath, 'r').read(), Loader=Loader)
    # get required values, error if missing
    game_dir = data.get("game-dir")
    archive_dir = data.get("archive-dir")
    if game_dir is None:
        logger.critical(f"game-dir attribute is missing from {filepath}")
        exit(1)
    if archive_dir is None:
        logger.critical(f"archive-dir attribute is missing from {filepath}")
        exit(1)

    # load profiles
    profiles = {
        k: Profile(
            whitelist=p.get("whitelist", "*"),
            blacklist=p.get("blacklist", ""),
            include=p.get("include", []),
            exclude=p.get("exclude", [])
        ) for k, p in data.get("profiles").items()
    }

    logger.debug(f"profiles: {profiles}")

    return Config(
        game_dir = game_dir,
        archive_dir = archive_dir,
        save_file = data.get("save-file", "state.pkl"),
        active_profile = data.get("active-profile", "default"),
        profiles = profiles
    )

@dataclass
class Profile:
    whitelist: str
    blacklist: str
    include: list[str]
    exclude: list[str]

@dataclass
class Config:
    game_dir: str
    archive_dir: str
    save_file: str
    active_profile: str
    profiles: dict[str, Profile]

    @property
    def profile(self):
        try:
            return self.profiles[self.active_profile]
        except:
            print(f"   [bold red]Could not find any profile '{self.active_profile}'")
            exit(1)

def filter_archives_by_config(archives: set[str], config: Config) -> set[str]:
    output = []
    logger = AppLogger(__name__).get_logger()
    profile = config.profile
    # add all that match whitelist wildcarding
    whitelisted = fnmatch.filter(archives, profile.whitelist)
    logger.debug(f"Whitelisted Files: {whitelisted}")
    output.extend(whitelisted)

    # remove all that match blacklist wildcards
    blacklisted = fnmatch.filter(archives, profile.blacklist)
    output = list(set(output) - set(blacklisted))
    logger.debug(f"Blacklisted Files: {blacklisted}")

    # re-add any include files
    for file in profile.include:
        if not os.path.exists(config.archive_dir + "/" + file):
            raise OSError(f"{file} does not exist in {config.archive_dir}")
        output.append(file)

    # re-remove any exclude files
    for file in profile.exclude:
        archive_path = config.archive_dir + "/" + file
        if archive_path in output:
            output.remove(archive_path)

    return set(output)
