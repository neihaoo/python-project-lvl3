"""Page Loader Download Module."""

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Union

import requests
from page_loader.logger import get_logger, write_traceback
from page_loader.parser import parse_page
from page_loader.url import make_filename, make_foldername
from progress.bar import IncrementalBar
from requests.exceptions import RequestException

DEFAULT_DESTINATION_FOLDER = os.getcwd()

logger = get_logger(__name__)


def get_resource(url: str) -> bytes:
    """Download file to destination folder."""
    try:
        req = requests.get(url)
        req.raise_for_status()
    except RequestException as exc:
        logger.warning('Resource "{0}" wasn\'t downloaded.'.format(url))
        logger.debug(exc, exc_info=True)
        raise

    return req.content


def save(file_content: Union[str, bytes], destination: str, name: str) -> str:
    """Save downloaded content to destination folder."""
    page_path = os.path.join(destination, name)

    mode = 'w' if isinstance(file_content, str) else 'wb'

    try:
        with open(page_path, mode) as filename:
            filename.write(file_content)
    except OSError as exc:
        logger.error(exc)
        write_traceback()
        raise

    return page_path


def download_asset(
    asset_url: str,
    destination: str,
    asset_name: str,
    progress: IncrementalBar,
) -> str:
    """Download and save page asset."""
    asset_content = get_resource(asset_url)
    save(asset_content, destination, asset_name)
    progress.next()

    return asset_url


def download_assets(assets: list, destination: str) -> None:
    """Download page asset."""
    if not assets:
        return

    logger.info('Start download assets.')

    if not os.path.exists(destination):
        logger.info('Create "{0}" folder for assets.'.format(destination))

        os.mkdir(destination)

    with IncrementalBar(
        'Downloading',
        max=len(assets),
        suffix='%(percent)d%%',
    ) as progress:
        with ThreadPoolExecutor(max_workers=len(assets)) as executor:
            futures = [
                executor.submit(
                    download_asset,
                    asset_url,
                    destination,
                    asset_name,
                    progress,
                )
                for asset_url, asset_name in assets
            ]

            futures_result = [
                future.result() for future in as_completed(futures)
            ]

            logger.info(
                'List assets that was downloaded: {0}.'.format(
                    ', '.join(', '.join(futures_result)),
                ),
            )


def download(url: str, destination: str = DEFAULT_DESTINATION_FOLDER) -> str:
    """Download html page to destination folder."""
    logger.info('Start download "{0}" to "{1}".'.format(url, destination))

    page_content = get_resource(url)
    assets_path = make_foldername(url)
    html, assets = parse_page(page_content, assets_path, url)
    page_path = save(html, destination, make_filename(url))

    download_assets(assets, os.path.join(destination, assets_path))

    logger.info('Finish download "{0}".'.format(url))

    return page_path
