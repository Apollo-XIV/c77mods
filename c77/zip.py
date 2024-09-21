import zipfile
import time
from pathlib import Path
import re
import os
from rich.progress import track
from c77.logging import AppLogger

def is_zip(filename: str) -> bool:
    pattern = r'^.*\.zip$'
    return re.match(pattern, filename, re.IGNORECASE) is not None

def list_archives(archive_path: str) -> set[str]:
    logger = AppLogger().get_logger()
    out = set([archive_path + "/" + a for a in os.listdir(archive_path) if is_zip(a)])
    logger.debug(f"Found the following archives: {out}")
    return out


def unzip_file(zip_path, dest, dry_run = False) -> list:
    """
        returns a dictionary of the archives and the files they created
    """
    logger = AppLogger().get_logger()
    os.makedirs(dest, exist_ok=True)
    outputs = []

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for zip_info in zip_ref.infolist():
            if dry_run is False:
                extracted_file_path = zip_ref.extract(zip_info, dest)
                outputs.append(Path(extracted_file_path))
                logger.debug(f"Created: {extracted_file_path}")
    if not dry_run:
        logger.info(f"Inflated: {zip_path}")
    return set(outputs)

def unzip_files(files: list[str], config, dry_run = False) -> dict:
    if len(files) == 0:
        return {}
    outputs = {}
    if not dry_run:
        files = track(files, description="  Inflating archives")
    for file in files:
        out = unzip_file(file, config.game_dir, dry_run=dry_run)
        outputs[Path(file)] = out
    return outputs

def remove_files(files: set[str]):
    logger = AppLogger().get_logger()
    if len(files) == 0:
        return
    for f in track(files, description="  Removing old files"):
        if os.path.isdir(f):
            continue
        try:
            os.remove(f)
        except FileNotFoundError as e:
            continue
        logger.info(f"Removed: {f}")
