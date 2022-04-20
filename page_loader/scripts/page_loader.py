#!/usr/bin/env python

"""Page Loader Main Script."""

import argparse
import sys

import logger
from page_loader.download import DEFAULT_DST_FOLDER, download

DESCRIPTION = 'Page Loader'
HELP_MESSAGE = 'set output folder'


def main():
    """Run Page Loader script."""
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('source')
    parser.add_argument(
        '-o',
        '--output',
        help=HELP_MESSAGE,
        default=DEFAULT_DST_FOLDER,
    )

    args = parser.parse_args()

    try:
        download(args.source, args.output)
    except Exception as error:
        logger.error(error)


if __name__ == '__main__':
    sys.exit(main())
