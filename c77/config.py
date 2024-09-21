from dataclasses import dataclass
import yaml
from yaml import Loader as Loader
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
        return self.profiles[self.active_profile]
