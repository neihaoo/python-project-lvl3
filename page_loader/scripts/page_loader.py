#!/usr/bin/env python

"""Page Loader Main Script."""

import argparse
import sys

from page_loader.download import DEFAULT_DST_FOLDER, download
from requests.exceptions import RequestException

DESCRIPTION = 'Page Loader'
HELP_MESSAGE = 'output dir (default: "{0}")'.format(DEFAULT_DST_FOLDER)
SUCCESS_MESSAGE = "Page was successfully download into '{0}'"


def main():
    """Run Page Loader script."""
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('url')
    parser.add_argument(
        '-o',
        '--output',
        help=HELP_MESSAGE,
        default=DEFAULT_DST_FOLDER,
    )

    args = parser.parse_args()

    try:
        page_path = download(args.url, args.output)
    except (RequestException, Exception):
        sys.exit(1)

    print(SUCCESS_MESSAGE.format(page_path))


if __name__ == '__main__':
    main()
