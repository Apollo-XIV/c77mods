import zipfile
from pathlib import Path
import re
import os

def is_zip(filename: str) -> bool:
    pattern = r'^.*\.zip$'
    return re.match(pattern, filename, re.IGNORECASE) is not None

def list_archives(archive_path: str) -> set[str]:
    return [archive_path + "/" + a for a in os.listdir(archive_path) if is_zip(a)]


def unzip_file(zip_path, dest, dry_run = False) -> list:
    """
        returns a dictionary of the archives and the files they created
    """
    os.makedirs(dest, exist_ok=True)
    outputs = []

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for zip_info in zip_ref.infolist():
            if dry_run is False:
                extracted_file_path = zip_ref.extract(zip_info, dest)
                outputs.append(Path(extracted_file_path))
    return set(outputs)
