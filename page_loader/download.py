"""Page Loader Download Module."""

import os
from urllib.parse import urljoin

import requests
from page_loader.common import make_filename, make_foldername
from page_loader.logger import logger
from page_loader.parser import parse_page

DEFAULT_DST_FOLDER = os.getcwd()
CHUNK_SIZE = 128


def read_file(file_path: str) -> str:
    """Read downloaded file."""
    with open(file_path) as filename:
        return filename.read()


def download_file(url: str, dst: str) -> str:
    """Download file to dst folder."""
    file_name = make_filename(url)
    file_path = os.path.join(dst, file_name)

    try:
        req = requests.get(url, stream=True)
    except Exception as error:
        logger.error(error)

    try:
        with open(file_path, 'wb') as filename:
            for chunk in req.iter_content(CHUNK_SIZE):
                filename.write(chunk)
    except FileNotFoundError as file_error:
        logger.error(file_error)

    return file_name


def download_assets(url: str, assets_urls: str, dst: str) -> str:
    """Download page asset."""
    assets_folder = make_foldername(url)
    assets_path = os.path.join(dst, assets_folder)

    if not os.path.exists(assets_path):
        try:
            os.mkdir(assets_path)
        except OSError as error:
            logger.exception(error)

    for asset_url in assets_urls:
        download_file(urljoin(url, asset_url), assets_path)


def download(url: str, dst: str = DEFAULT_DST_FOLDER) -> str:
    """Download html page to dst folder."""
    page_name = download_file(url, dst)
    page_path = os.path.join(dst, page_name)
    page_data, assets_urls = parse_page(url, read_file(page_path))

    with open(page_path, 'w') as filename:
        filename.write(page_data)

    if assets_urls:
        download_assets(url, assets_urls, dst)

    return page_path
