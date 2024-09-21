import logging
import os
from pathlib import Path
from rich.logging import RichHandler  # For colorful console output
from rich.console import Console
from rich import traceback
traceback.install()

class SingletonMeta(type):
    """ A thread-safe implementation of Singleton. """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class AppLogger(metaclass=SingletonMeta):
    def __init__(self, logger_name: str, log_file: str = "app.log", log_level=logging.INFO, log_dir="logs", print_to_console=False):
        """
        Initializes the logger with both file and colorful console handlers.
        
        :param logger_name: The name of the logger.
        :param log_file: Name of the log file.
        :param log_level: Logging level (e.g., logging.INFO, logging.DEBUG).
        :param log_dir: Directory where the log file will be stored.
        """
        # Create logger
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(log_level)

        # Ensure the log directory exists
        Path(log_dir).mkdir(parents=True, exist_ok=True)
        log_file_path = os.path.join(log_dir, log_file)
        second_log_file_path = os.path.join(log_dir, "colored_output.log")

        # Add handlers only if they don't already exist
        if not self.logger.hasHandlers():
            # Create handlers
            file_handler = logging.FileHandler(log_file_path)

            # Set levels for each handler
            file_handler.setLevel(log_level)

            # File handler formatter (plain, non-colored, without date, but with time)
            file_log_format = "%(asctime)s %(levelname)s | %(message)s"
            file_formatter = logging.Formatter(file_log_format, datefmt="%H:%M:%S")
            file_handler.setFormatter(file_formatter)

            # Add handlers to the logger
            self.logger.addHandler(file_handler)
            if print_to_console:
                # Create a rich handler for colorful console output
                console_handler = RichHandler(log_time_format="[%X]")
                console_handler.setLevel(log_level)
                self.logger.addHandler(console_handler)
            else:
                # If console output is turned off, log colored output to a second file
                self.console = Console(file=open(second_log_file_path, 'w'))  # Create a console that captures logs
                self.second_file_handler = RichHandler(console=self.console)
                self.second_file_handler.setLevel(log_level)
                self.logger.addHandler(self.second_file_handler)

    def get_logger(self):
        """
        Returns the logger instance for use in other parts of the application.
        
        :return: The configured logger instance.
        """
        return self.logger

# # Example usage (optional, remove if you don't want to include this in the module):
# if __name__ == "__main__":
#     # Example: using the logger
#     logger = AppLogger("example_logger", log_file="example.log", log_level=logging.DEBUG).get_logger()

#     logger.debug("This is a debug message")
#     logger.info("This is an info message")
#     logger.warning("This is a warning message")
#     logger.error("This is an error message")
#     logger.critical("This is a critical message")
