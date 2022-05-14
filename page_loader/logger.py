"""App Logging Module."""

import logging
import traceback

LOG_FILE = 'page-loader.log'
DATE_FORMAT = '%d-%b-%y %H:%M:%S'

log_formats = {
    'DEBUG': '%(levelname)s: %(asctime)s - %(message)s',
    'WARNING': '%(levelname)s: %(message)s',
}


def get_file_handler() -> logging.Handler:
    """Get Logging FileHandler."""
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter(log_formats['DEBUG'], DATE_FORMAT),
    )

    return file_handler


def get_stream_handler() -> logging.Handler:
    """Get Logging StreamHandler."""
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.WARNING)
    stream_handler.setFormatter(logging.Formatter(log_formats['WARNING']))

    return stream_handler


def get_logger(name: str) -> logging.Logger:
    """Get Logger."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_file_handler())
    logger.addHandler(get_stream_handler())

    return logger


def write_traceback() -> None:
    """Write to loog file."""
    with open(LOG_FILE, 'a') as log_file:
        traceback.print_exc(file=log_file)
