"""
weitersager.argparser
~~~~~~~~~~~~~~~~~~~~~

Command line argument parsing

:Copyright: 2007-2020 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from argparse import ArgumentParser
from pathlib import Path


DEFAULT_HTTP_IP_ADDRESS = '127.0.0.1'
DEFAULT_HTTP_PORT = 8080


def create_parser():
    """Create the command line arguments parser."""
    parser = ArgumentParser()

    parser.add_argument('config_filename', type=Path, metavar='CONFIG_FILENAME')

    parser.add_argument(
        '--http-listen-ip-address',
        dest='http_ip_address',
        default=DEFAULT_HTTP_IP_ADDRESS,
        help='the IP address to listen on for HTTP requests '
        + f'[default: {DEFAULT_HTTP_IP_ADDRESS}]',
        metavar='IP_ADDRESS',
    )

    parser.add_argument(
        '--http-listen-port',
        dest='http_port',
        type=int,
        default=DEFAULT_HTTP_PORT,
        help='the port to listen on for HTTP requests '
        + f'[default: {DEFAULT_HTTP_PORT:d}]',
        metavar='PORT',
    )

    return parser


def parse_args():
    """Parse command line arguments."""
    parser = create_parser()
    return parser.parse_args()
