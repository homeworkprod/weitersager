"""
weitersager.config
~~~~~~~~~~~~~~~~~~

Configuration loading

:Copyright: 2007-2020 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

import rtoml

from .irc import Channel, Config as IrcConfig, Server as IrcServer


def load_config(path):
    """Load configuration from file."""
    data = rtoml.load(path)

    http_host, http_port = _get_http_config(data)
    irc_config = _get_irc_config(data)

    return irc_config, http_host, http_port


def _get_http_config(data):
    data_http = data['http']

    host = data_http['host']
    port = int(data_http['port'])

    return host, port


def _get_irc_config(data):
    data_irc = data['irc']

    server = _get_irc_server(data_irc)
    nickname = data_irc['bot']['nickname']
    realname = data_irc['bot']['realname']
    channels = list(_get_irc_channels(data_irc))

    return IrcConfig(
        server=server,
        nickname=nickname,
        realname=realname,
        channels=channels,
    )


def _get_irc_server(data_irc):
    data_server = data_irc['server']
    host = data_server['host']
    port = int(data_server['port'])

    return IrcServer(host, port)


def _get_irc_channels(data_irc):
    for channel in data_irc['channels']:
        name = channel['name']
        password = channel.get('password')
        yield Channel(name, password)
