"""Page-loader Parser Module."""

import os
from typing import Tuple
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from page_loader.url import make_filename, make_foldername

links = ['img', 'link', 'script']
links_attrs = {
    'img': 'src',
    'link': 'href',
    'script': 'src',
}


def is_hosts_equal(page_host: str, asset_host: str) -> bool:
    """Check if asset host belongs to page host."""
    return asset_host is None or page_host == asset_host


def parse_page(page_data: str, url: str) -> Tuple[str, str, list]:
    """Parse html page."""
    html = BeautifulSoup(page_data, 'html.parser')

    assets = []

    assets_path = make_foldername(url)

    for asset in html.find_all(links):
        asset_attr = links_attrs[asset.name]
        asset_src = asset.get(asset_attr)

        if is_hosts_equal(urlparse(url).hostname, urlparse(asset_src).hostname):
            asset_url = urljoin(url, asset_src)
            asset_name = make_filename(asset_url)

            asset[asset_attr] = os.path.join(assets_path, asset_name)

            assets.append((asset_url, asset_name))

    return html.prettify(), assets_path, assets
