"""
weitersager.cli
~~~~~~~~~~~~~~~

Command line entry point

:Copyright: 2007-2020 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from argparse import ArgumentParser
from pathlib import Path
import sys

from .config import load_config
from .processor import start


def parse_args(args):
    """Parse command line arguments."""
    parser = ArgumentParser(prog='weitersager')
    parser.add_argument('config_filename', type=Path)
    return parser.parse_args(args)


def main():
    """Load the configuration file, start the IRC bot and HTTP listen server."""
    namespace = parse_args(sys.argv[1:])

    http_config, irc_config = load_config(namespace.config_filename)

    start(irc_config, http_config)


if __name__ == '__main__':
    main()
