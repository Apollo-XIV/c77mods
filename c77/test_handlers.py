import tempfile
import zipfile
import os
from c77.archive_handlers import ZipHandler
from c77.logging import AppLogger

def create_test_zipfile(file_count=3, file_prefix="test_file", zip_name="test_zipfile.zip"):
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create some temporary files in the directory
        file_paths = []
        for i in range(file_count):
            file_path = os.path.join(temp_dir, f"{file_prefix}_{i}.txt")
            with open(file_path, 'w') as temp_file:
                temp_file.write(f"This is test file {i}\n")
            file_paths.append(file_path)
        
        # Create the zip file
        zip_file_path = os.path.join(zip_name)
        with zipfile.ZipFile(zip_file_path, 'w') as zipf:
            for file_path in file_paths:
                # Add each file to the zip
                zipf.write(file_path, os.path.basename(file_path))
        
        # Return the path to the zip file
        return zip_file_path


def test_handler():
    logger = AppLogger(__name__, print_to_console=True).get_logger()
    test_file = create_test_zipfile()
    handler = ZipHandler()

    # Test file listing
    files = handler.files(path=test_file)
    logger.info(files)
    print(files)
    assert files == ["test_file_0.txt", "test_file_1.txt", "test_file_2.txt",]

def test_extract():
    logger = AppLogger(__name__, print_to_console=True).get_logger()
    test_file = create_test_zipfile()
    handler = ZipHandler()
    # Extract all files from given archive and test creation
    with tempfile.TemporaryDirectory() as temp_dir:
        files = handler.extract(test_file, temp_dir)
        for f in files:
            assert os.path.exists(temp_dir + "/" + f)

def test_extract_files():
    logger = AppLogger(__name__, print_to_console=True).get_logger()
    test_file = create_test_zipfile()
    handler = ZipHandler()
    # Extract only a subset of files
    with tempfile.TemporaryDirectory() as temp_dir:
        subset = ["test_file_0.txt"]
        files = handler.extract_files(test_file, subset, temp_dir)
        files_in_temp_dir = os.listdir(temp_dir)
        assert files == files_in_temp_dir
