import pickle
import os 
import logging
import traceback
from c77.logging import AppLogger


def load_save_data(file_path: str) -> dict:
    logger = AppLogger(__name__).get_logger()
    # if savefile doesn't exist, return empty dict
    if not os.path.exists(file_path):
        return {}

    try:
        with open(file_path, "rb") as file:  # Use 'rb' for reading in binary mode
            loaded_data = pickle.load(file)
            logger.info(f"Loaded state data from {file_path}")
            return loaded_data
    except Exception as e:
        logger.critical(e)
        exit(1)

def persist_save_data(file_path:str, data: dict) -> None:
    logger = AppLogger(__name__).get_logger()
    with open(file_path, "wb") as file:  # Use 'wb' for writing in binary mode
        pickle.dump(data, file)
        logger.info(f"Persisted to {file_path}")
