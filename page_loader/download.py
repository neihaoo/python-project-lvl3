"""Page Loader Download Module."""

import os
from typing import Union

import requests
from page_loader.logger import get_logger, write_traceback
from page_loader.parser import parse_page
from page_loader.url import make_filename
from progress.bar import IncrementalBar
from requests.exceptions import RequestException

DEFAULT_DST_FOLDER = os.getcwd()

logger = get_logger(__name__)


def get_resource(url: str) -> bytes:
    """Download file to dst folder."""
    try:
        req = requests.get(url)
        req.raise_for_status()
    except RequestException as exc:
        logger.warning('Resource "{0}" wasn\'t downloaded.'.format(url))
        logger.debug(exc, exc_info=True)
        raise

    return req.content


def save(file_content: Union[str, bytes], dst: str, name: str) -> str:
    """Save downloaded content to dst folder."""
    page_path = os.path.join(dst, name)

    mode = 'w' if isinstance(file_content, str) else 'wb'

    try:
        with open(page_path, mode) as filename:
            filename.write(file_content)
    except OSError as exc:
        logger.error(exc)
        write_traceback()
        raise

    return page_path


def download_assets(assets: list, dst: str) -> None:
    """Download page asset."""
    if not os.path.exists(dst):
        logger.info('Create "{0}" folder for assets.'.format(dst))

        try:
            os.mkdir(dst)
        except OSError as exc:
            logger.error(exc)
            write_traceback()
            raise

        with IncrementalBar(
            'Downloading:',
            max=len(assets),
            suffix='%(percent)d%%',
        ) as progress:
            for asset_url, asset_name in assets:
                asset_content = get_resource(asset_url)
                save(asset_content, dst, asset_name)
                progress.next()


def download(url: str, dst: str = DEFAULT_DST_FOLDER) -> str:
    """Download html page to dst folder."""
    logger.info('Start download "{0}" to "{1}".'.format(url, dst))

    page_content = get_resource(url)
    html, assets_path, assets = parse_page(page_content, url)
    page_path = save(html, dst, make_filename(url))

    if assets:
        logger.info('Start download assets.')

        download_assets(assets, os.path.join(dst, assets_path))

    logger.info('Finish download "{0}".'.format(url))

    return page_path
