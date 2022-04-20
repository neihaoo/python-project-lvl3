"""App Logging Module."""

import logging

logger = logging.getLogger(__name__)

console_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()

console_handler.setLevel(logging.WARNING)
console_handler.setFormatter(console_format)

file_format = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
file_handler = logging.FileHandler('page-loader.log')

file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(file_format)

logger.addHandler(console_handler)
logger.addHandler(file_handler)
