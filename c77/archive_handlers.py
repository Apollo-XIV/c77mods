import zipfile
import os
from abc import ABC, abstractmethod
from typing import Callable
from c77.logging import AppLogger

class Handler(ABC):
    @abstractmethod
    def extract(path: str, dest:str) -> list:
        """
            Extracts all the files in an archive to the destination path
        """
        pass

    @abstractmethod
    def files(path: str) -> list:
        """
            List all the files in an archive
        """
        pass

    @abstractmethod
    def extract_files(path: str, files: list[str], dest: str) -> list:
        """
           When given a list of relative paths, it extracts those from the given archive 
        """
        pass

class ZipHandler(Handler):
    @staticmethod
    def files(path: str) -> list:
        outputs = []
        with zipfile.ZipFile(path, 'r') as zip_ref:
            for zip_info in zip_ref.infolist():
                outputs.append(zip_info.filename)
        return outputs

    @staticmethod
    def extract(path: str, dest: str) -> list:
        outputs = []
        with zipfile.ZipFile(path, 'r') as zip_ref:
            for zip_info in zip_ref.infolist():
                outputs.append(zip_info.filename)
                extracted_file_path = zip_ref.extract(zip_info, dest)
        return outputs

    @staticmethod
    def extract_files(path: str, files:str, dest: str) -> list:
        outputs = []
        with zipfile.ZipFile(path, 'r') as zip_ref:
            for zip_info in zip_ref.infolist():
                outputs.append(zip_info.filename)
                extracted_file_path = zip_ref.extract(zip_info, dest)
        return outputs

