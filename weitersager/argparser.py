"""
weitersager.argparser
~~~~~~~~~~~~~~~~~~~~~

Command line argument parsing

:Copyright: 2007-2015 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from argparse import ArgumentParser

from irc.bot import ServerSpec


DEFAULT_HTTP_IP_ADDRESS = '127.0.0.1'
DEFAULT_HTTP_PORT = 8080
DEFAULT_IRC_PORT = ServerSpec('').port


def parse_args():
    """Setup and apply the command line arguments parser."""
    parser = ArgumentParser()

    parser.add_argument('--irc-nickname',
        dest='irc_nickname',
        default='Weitersager',
        help='the IRC nickname the bot should use',
        metavar='NICKNAME')

    parser.add_argument('--irc-realname',
        dest='irc_realname',
        default='Weitersager',
        help='the IRC realname the bot should use',
        metavar='REALNAME')

    parser.add_argument('--irc-server',
        dest='irc_server',
        type=parse_irc_server_arg,
        help='IRC server (host and, optionally, port) to connect to'
            + ' [e.g. "irc.example.com" or "irc.example.com:6669";'
            + ' default port: {:d}]'.format(DEFAULT_IRC_PORT),
        metavar='SERVER')

    parser.add_argument('--http-listen-ip-address',
        dest='http_ip_address',
        default=DEFAULT_HTTP_IP_ADDRESS,
        help='the IP address to listen on for HTTP requests [default: {}]'
             .format(DEFAULT_HTTP_IP_ADDRESS),
        metavar='IP_ADDRESS')

    parser.add_argument('--http-listen-port',
        dest='http_port',
        type=int,
        default=DEFAULT_HTTP_PORT,
        help='the port to listen on for HTTP requests [default: {:d}]'
             .format(DEFAULT_HTTP_PORT),
        metavar='PORT')

    return parser.parse_args()


def parse_irc_server_arg(value):
    """Parse a hostname with optional port."""
    fragments = value.split(':', 1)
    if len(fragments) > 1:
        fragments[1] = int(fragments[1])
    return ServerSpec(*fragments)
