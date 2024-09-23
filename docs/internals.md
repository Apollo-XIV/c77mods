# Project Internals

The current method does the following:
- list all archives in config.archives_dir
- filter by profile settings
- do a dry run of the extraction to get a record of the created files
- load the current state from the statefile
- compare new state and current state, find differences
- 
