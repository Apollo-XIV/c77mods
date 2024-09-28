import fnmatch
from rich import print
from dataclasses import dataclass, field
from c77.archive_handlers import Handler, ZipHandler
from c77.config import Profile
import os
from c77.utils import try_wrap
from pathlib import Path
from c77.logging import AppLogger


@dataclass
class Mod:
    source: Path # the archive file to extract
    archive_handler: Handler = ZipHandler()
    state: str = "uninstalled"

    def filter_profile(self, profile: Profile):
    # add all that match whitelist wildcarding
        desired_state = "uninstalled"
        if fnmatch.fnmatch(self.source, profile.whitelist):
            desired_state = "installed"

        # remove all that match blacklist wildcards
        if fnmatch.fnmatch(self.source, profile.blacklist):
            desired_state = "uninstalled"

        # re-add any include files
        if self.source.name in profile.include:
            desired_state = "installed"

        if self.source in profile.exclude:
            desired_state = "uninstalled"

        self.state = desired_state
        return self

    @property
    def files(self):
        return self.archive_handler.files(self.source)

    def make_install(self, dest):
        def install():
            handler = self.archive_handler
            handler.extract(self.source, dest=dest)
            print(f"[yellow]  >>[/] Install ran for {self.source.name}")
            return self
        return install

    def make_uninstall(self, path):
        log = AppLogger(__name__).get_logger()
        def uninstall():
            print(f"[red]  <<[/] Uninstall ran for {self.source.name}")
            files = self.files
            files.reverse()
            for file in files:
                full_path = f"{path}/{file}"
                if os.path.isdir(full_path):
                    try_wrap(os.removedirs, full_path).or_else(lambda _: log.debug(f"directory not empty {file}"))
                    continue
                log.debug(f"Deleting {file}")
                try_wrap(os.remove, "", full_path).or_else(lambda e: log.error(e))
        return uninstall

    def install(self):
        self.archive_handler.extract(path=self.source,dest="test-game-dir")
        print(f"[yellow]  >>[/] Install ran for {self.source.name}")

    def uninstall(self):
        print(f"[red]  << Uninstall ran for {self.source.name}")
        pass
