import fnmatch
from dataclasses import dataclass, field
from c77.archive_handlers import Handler, ZipHandler
from c77.config import Profile

@dataclass
class Mod:
    source: str # the archive file to extract
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
        if self.source in profile.include:
            desired_state = "installed"

        if self.source in profile.exclude:
            desired_state = "uninstalled"

        self.state = desired_state
        return self

    @property
    def files(self):
        return self.archive_handler.files()

    def install():
        pass

    def uninstall():
        pass
