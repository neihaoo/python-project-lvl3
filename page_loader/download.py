"""Page Loader Download Module."""

import os
import re

import requests

DEFAULT_DST_FOLDER = os.getcwd()


def download(source: str, destination: str = DEFAULT_DST_FOLDER) -> str:
    """Download files to destination folder."""
    file_name = source.split('//')[-1]
    local_filename = '{0}{1}'.format(re.sub(r'\W', '-', file_name), '.html')

    req = requests.get(source, stream=True)

    with open(os.path.join(destination, local_filename), 'wb') as filename:
        for chunk in req.iter_content():
            filename.write(chunk)

    return os.path.join(destination, local_filename)
