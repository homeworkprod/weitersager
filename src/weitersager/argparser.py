"""
weitersager.argparser
~~~~~~~~~~~~~~~~~~~~~

Command line argument parsing

:Copyright: 2007-2020 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from argparse import ArgumentParser
from pathlib import Path


def create_parser():
    """Create the command line arguments parser."""
    parser = ArgumentParser()
    parser.add_argument('config_filename', type=Path)
    return parser


def parse_args():
    """Parse command line arguments."""
    parser = create_parser()
    return parser.parse_args()
