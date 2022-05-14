"""Common Utils Module."""

import os
import re
from typing import Tuple
from urllib.parse import urlparse

extensions = {
    'page': '.html',
    'folder': '_files',
}


def parse_url(url: str) -> Tuple[str, str]:
    """Get from url hostname, filename."""
    parts = urlparse(url)

    return parts.hostname, parts.path


def prepare_name(host: str, name: str) -> str:
    """Prepare filename."""
    name = name.strip('/')
    filename = os.path.join(host, name) if name else host

    return re.sub(r'\W', '-', filename)


def make_filename(url: str) -> str:
    """Make name for assets."""
    hostname, path = parse_url(url)
    filename, extension = os.path.splitext(path)

    filename = prepare_name(hostname, filename)
    extension = extension if extension else extensions['page']

    return '{0}{1}'.format(filename, extension)


def make_foldername(url: str) -> str:
    """Create name folder for assets."""
    hostname, path = parse_url(url)
    filename, _ = os.path.splitext(path)

    filename = prepare_name(hostname, filename)

    return '{0}{1}'.format(filename, extensions['folder'])
