"""Common Utils Module."""

import os
import re
from urllib.parse import urlparse


def make_filename(url: str) -> str:
    """Make name for assets."""
    url_parts = urlparse(url)
    filename, extension = os.path.splitext(url_parts.path[1:])

    filename = (
        os.path.join(url_parts.hostname, filename)
        if filename
        else url_parts.hostname
    )
    filename = re.sub(r'\W', '-', filename)
    extension = extension if extension else '.html'

    return '{0}{1}'.format(filename, extension)


def make_foldername(url: str) -> str:
    """Create name folder for assets."""
    return make_filename(url).replace('.html', '_files')
