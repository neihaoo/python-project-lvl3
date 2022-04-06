"""Page Loader Download Module."""

import os
import re
from typing import Tuple
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

DEFAULT_DST_FOLDER = os.getcwd()


def check_domain(outer_host: str, inner_host: str) -> bool:
    """Check local assets for local domain."""
    url_parts = urlparse(inner_host)

    return url_parts.hostname is None or outer_host in url_parts.hostname


def parse_url(url: str) -> Tuple:
    """Split url on host and path."""
    url_parts = urlparse(url)

    return (url_parts.hostname, url_parts.path[1:])


def make_name(url) -> str:
    """Make name for assets."""
    hostname, path = parse_url(url)
    name, extension = os.path.splitext(path)

    name = re.sub(r'\W', '-', os.path.join(hostname, name))
    extension = extension if extension else '.html'

    return '{0}{1}'.format(name, extension)


def make_folder(filename: str, dst: str) -> str:
    """Create folder for assets and return folder name."""
    foldername = filename.replace('.html', '_files')
    os.mkdir(os.path.join(dst, foldername))

    return foldername


def download_assets(src: str, dst: str) -> None:
    """Download assets for page."""
    req = requests.get(src, stream=True)
    assert_name = make_name(src)

    with open(os.path.join(dst, assert_name), 'wb') as filename:
        filename.write(req.content)

    return assert_name


def parse_html(url: str, dst: str, html: str) -> Tuple:
    """Parse html file."""
    html_name = make_name(url)

    soup = BeautifulSoup(html, 'html.parser')
    assets = (
        asset
        for asset in soup.find_all('img')
        if check_domain(url, asset.get('src'))
    )

    if assets:
        assets_dst = make_folder(html_name, dst)

        for asset in assets:
            asset_name = download_assets(
                urljoin(url, asset.get('src')),
                os.path.join(dst, assets_dst),
            )

            asset['src'] = os.path.join(assets_dst, asset_name)

    return html_name, soup.prettify()


def download(src: str, dst: str = DEFAULT_DST_FOLDER) -> str:
    """Download html page to dst folder."""
    req = requests.get(src)
    html_name, html_data = parse_html(src, dst, req.text)

    with open(os.path.join(dst, html_name), 'w') as filename:
        filename.write(html_data)

    return os.path.join(dst, html_name)
