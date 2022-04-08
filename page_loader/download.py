"""Page Loader Download Module."""

import os
import re
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

DEFAULT_DST_FOLDER = os.getcwd()

links_attrs = {
    'img': 'src',
    'link': 'href',
    'script': 'src',
}


def has_attr(tag: str) -> bool:
    """Check if tag has attrs 'src' or 'href'."""
    return tag.has_attr('src') or tag.has_attr('href')


def is_local_domain(outer_host: str, inner_host: str) -> bool:
    """Check local assets for local domain."""
    outer_url_parts = urlparse(outer_host)
    inner_url_parts = urlparse(inner_host)

    return (
        inner_url_parts.hostname is None
        or outer_url_parts.hostname == inner_url_parts.hostname
    )


def make_filename(url) -> str:
    """Make name for assets."""
    url_parts = urlparse(url)
    filename, extension = os.path.splitext(url_parts.path[1:])

    filename = re.sub(r'\W', '-', os.path.join(url_parts.hostname, filename))
    extension = extension if extension else '.html'

    return '{0}{1}'.format(filename, extension)


def make_folder(url: str, dst: str) -> str:
    """Create folder for assets and return folder name."""
    filename, _ = os.path.splitext(make_filename(url))
    folder_name = '{0}{1}'.format(filename, '_files')

    os.mkdir(os.path.join(dst, folder_name))

    return folder_name


def download_asset(url: str, dst: str) -> str:
    """Download asset for page."""
    req = requests.get(url, stream=True)
    asset_name = make_filename(url)

    with open(os.path.join(dst, asset_name), 'wb') as filename:
        filename.write(req.content)

    return asset_name


def parse_html(url: str, dst: str, html: str) -> str:
    """Parse html file."""
    soup = BeautifulSoup(html, 'html.parser')
    assets = (
        asset
        for asset in soup.find_all(['img', 'link', 'script'])
        if is_local_domain(url, asset.get(links_attrs[asset.name]))
    )

    if assets:
        assets_dst = make_folder(url, dst)

        for asset in assets:
            asset_name = download_asset(
                urljoin(url, asset.get(links_attrs[asset.name])),
                os.path.join(dst, assets_dst),
            )

            asset[links_attrs[asset.name]] = os.path.join(
                assets_dst,
                asset_name,
            )

    return soup.prettify()


def download(url: str, dst: str = DEFAULT_DST_FOLDER) -> str:
    """Download html page to dst folder."""
    req = requests.get(url, stream=True)

    html_name = make_filename(url)
    html_data = parse_html(url, dst, req.text)

    with open(os.path.join(dst, html_name), 'w') as filename:
        filename.write(html_data)

    return os.path.join(dst, html_name)
