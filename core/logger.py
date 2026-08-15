"""
=========================================================
GSIS INSTITUTIONAL
Logger
Version: 1.0
=========================================================
"""

import logging
import os


class GSISLogger:

    def __init__(self,
                 log_file="logs/gsis.log",
                 level=logging.INFO):

        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        self.logger = logging.getLogger("GSIS")

        if not self.logger.handlers:

            self.logger.setLevel(level)

            formatter = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(message)s"
            )

            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)

            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

    def debug(self, message):
        self.logger.debug(message)
