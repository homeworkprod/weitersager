"""
weitersager.cli
~~~~~~~~~~~~~~~

Command line entry point

:Copyright: 2007-2020 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from argparse import ArgumentParser, Namespace
from pathlib import Path
import sys
from typing import List

from .config import load_config
from .processor import start


def parse_args(args: List[str]) -> Namespace:
    """Parse command line arguments."""
    parser = ArgumentParser(prog='weitersager')
    parser.add_argument('config_filename', type=Path)
    return parser.parse_args(args)


def main() -> None:
    """Load the configuration file, start the IRC bot and HTTP listen server."""
    namespace = parse_args(sys.argv[1:])
    config = load_config(namespace.config_filename)
    start(config)


if __name__ == '__main__':
    main()
