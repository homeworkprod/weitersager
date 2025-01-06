"""
weitersager.cli
~~~~~~~~~~~~~~~

Command line entry point

:Copyright: 2007-2025 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from __future__ import annotations
from argparse import ArgumentParser, Namespace
import importlib.metadata
from pathlib import Path
import sys

from .config import load_config
from .processor import start
from .util import configure_logging


def parse_args(args: list[str]) -> Namespace:
    """Parse command line arguments."""
    version = importlib.metadata.version('weitersager')

    parser = ArgumentParser()
    parser.add_argument(
        '--version', action='version', version=f'Weitersager {version}'
    )
    parser.add_argument('config_filename', type=Path)
    return parser.parse_args(args)


def main() -> None:
    """Load the configuration file, start the IRC bot and HTTP listen server."""
    namespace = parse_args(sys.argv[1:])
    config = load_config(namespace.config_filename)
    configure_logging(config.log_level)
    start(config)


if __name__ == '__main__':
    main()
