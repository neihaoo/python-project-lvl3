"""Page Loader Download Module."""

import logging
import os
import sys

import requests
from page_loader.common import make_filename, make_foldername
from page_loader.parser import parse_page
from requests.exceptions import RequestException

DEFAULT_DST_FOLDER = os.getcwd()

logging.basicConfig(stream=sys.stderr)
logger = logging.getLogger(__name__)


def save_data(content_data: str, dst: str, url: str) -> str:
    """Save downloaded data to dst folder."""
    file_name = make_filename(url)
    file_path = os.path.join(dst, file_name)

    mode = 'wt' if isinstance(content_data, str) else 'wb'

    try:
        with open(file_path, mode) as filename:
            filename.write(content_data)
    except OSError as exc:
        logger.error(exc)
        raise OSError

    return file_path


def download_data(url: str) -> str:
    """Download file to dst folder."""
    req = requests.get(url)

    try:
        req.raise_for_status()
    except RequestException as exc:
        logger.error(exc)
        raise RequestException

    return req.content


def download_assets(assets_urls: str, dst: str, url: str) -> None:
    """Download page asset."""
    assets_folder = make_foldername(url)
    assets_path = os.path.join(dst, assets_folder)

    if not os.path.exists(assets_path):
        try:
            os.mkdir(assets_path)
        except OSError as exc:
            logger.error(exc)
            raise OSError

    for asset_url in assets_urls:
        asset_data = download_data(asset_url)
        save_data(asset_data, assets_path, asset_url)


def download(url: str, dst: str = DEFAULT_DST_FOLDER) -> str:
    """Download html page to dst folder."""
    page_data = download_data(url)
    html, assets_urls = parse_page(page_data, url)

    page_path = save_data(html, dst, url)

    if assets_urls:
        download_assets(assets_urls, dst, url)

    return page_path
