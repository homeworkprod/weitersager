"""
weitersager.config
~~~~~~~~~~~~~~~~~~

Configuration loading

:Copyright: 2007-2020 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

import rtoml

from .irc import Channel


def load_irc_channels(path):
    """Load IRC channel configuration from file."""
    data = rtoml.load(path)
    return list(_get_irc_channels(data))


def _get_irc_channels(data):
    for channel in data['irc']['channels']:
        name = channel['name']
        password = channel.get('password')
        yield Channel(name, password)
