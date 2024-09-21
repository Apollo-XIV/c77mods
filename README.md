# C77mods
*A Cyberpunk 2077 mod manager written in python*

This is a simplistic mod manager written using python. It mostly works by unzipping the files in the archive directory into the cyberpunk directory and tracking what changes were made. On subsequent deployments it finds the differences between them and then synchronises on user approval.

## Usage

```bash
c77 <subcommand> [options]
# subcommands
  list # list all the currently deployed mods
  diff # show a diff of files that would be deployed
  sync # deploy the changed mods
# options
  --debug # display log output information in the terminal
  --profile <profile-name> # override the "active_profile" value in config.yaml
```

## Configuration
Configuration of c77 is done via a config.yaml file. This file sets the location of archives to install, the location of your Cyberpunk install, configures profiles (see below), and more.
```yaml
archive-dir: /path/to/mod/files # a directory containing zip files
game-dir: /path/to/cyberpunk # (typically $STEAMDIR/steam/steamapps/common/Cyberpunk 2077)
save-file: state.pkl # the file to save state data to. This lets c77 track the files it creates
active-profile: default # which of the profiles to deploy
profiles: # dictionary of profile objects, see below for configuration information
  default:
    whitelist: "*"
```

### Profiles
```yaml
profile-name:
  whitelist: "*" # 
  blacklist: "" #
  include: [] #
  exclude: [] #
```
