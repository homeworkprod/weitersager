"""
weitersager.config
~~~~~~~~~~~~~~~~~~

Configuration loading

:Copyright: 2007-2020 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

import rtoml

from .httpreceiver import Config as HttpConfig
from .irc import Channel, Config as IrcConfig, Server as IrcServer


DEFAULT_HTTP_HOST = '127.0.0.1'
DEFAULT_HTTP_PORT = 8080
DEFAULT_IRC_SERVER_PORT = 6667
DEFAULT_IRC_REALNAME = 'Weitersager'


def load_config(path):
    """Load configuration from file."""
    data = rtoml.load(path)

    http_config = _get_http_config(data)
    irc_config = _get_irc_config(data)

    return irc_config, http_config


def _get_http_config(data):
    data_http = data.get('http', {})

    host = data_http.get('host', DEFAULT_HTTP_HOST)
    port = int(data_http.get('port', DEFAULT_HTTP_PORT))
    api_tokens = data_http.get('api_tokens')
    if api_tokens:
        api_tokens = set(api_tokens)

    return HttpConfig(host, port, api_tokens)


def _get_irc_config(data):
    data_irc = data['irc']

    server = _get_irc_server(data_irc)
    nickname = data_irc['bot']['nickname']
    realname = data_irc['bot'].get('realname', DEFAULT_IRC_REALNAME)
    channels = list(_get_irc_channels(data_irc))

    return IrcConfig(
        server=server,
        nickname=nickname,
        realname=realname,
        channels=channels,
    )


def _get_irc_server(data_irc):
    data_server = data_irc.get('server')
    if data_server is None:
        return None

    host = data_server.get('host')
    if not host:
        return None

    port = int(data_server.get('port', DEFAULT_IRC_SERVER_PORT))
    password = data_server.get('password')

    return IrcServer(host, port, password)


def _get_irc_channels(data_irc):
    for channel in data_irc.get('channels', []):
        name = channel['name']
        password = channel.get('password')
        yield Channel(name, password)
