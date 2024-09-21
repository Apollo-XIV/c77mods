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

## Limitations
This is a very simple tool, and I honestly can't recommend it unless you're familiar with the manual install process and just want to automate it. The following important features are missing from this tool, and should be considered by the user:
 - incorrectly packaged zip archives (i.e. archives that don't automatically extract to the correct subpath)
 - non-zip archives such as 7z and rar
 - file collisions after extraction

There are plans to deal with these limitations, but they aren't implemented yet:
 - zip repackaging tool
 - add handlers for non-zip archives
 - track individual files created when making diffs

## Example
```
      ___ _____ _____                    _
     / __\___  |___  | __ ___   ___   __| |___
    / /     / /   / / '_ ` _ \ / _ \ / _` / __|
   / /___  / /   / /| | | | | | (_) | (_| \__ \
   \____/ /_/   /_/ |_| |_| |_|\___/ \__,_|___/ v.0.0.1
                                                                                           
////////////////////////////////////////////////////////////////////////////////
                                                                                           
   active profile         default
   save file              'state.pkl'
   archive dir            '/home/my_user/.c77mods/archives'
   game dir               '/home/my_user/.c77mods/test-game-dir'
                                                                                           
────────────────────────────────────────────────────────────────────────────────
  ADDING:
  + mod_settings.zip-4885-0-2-8-1710978150.zip
────────────────────────────────────────────────────────────────────────────────
  + 1 to add
  Do you want to apply these changes? [y/n] (n): y
  Inflating archives ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00

```
