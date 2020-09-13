"""
:Copyright: 2007-2020 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from io import StringIO

from weitersager.config import load_config
from weitersager.irc import Channel, Config as IrcConfig, Server as IrcServer


TOML_CONFIG = '''\
[http]
host = "127.0.0.1"
port = 55555

[irc.server]
host = "orion.astrochat.test"
port = 6669

[irc.bot]
nickname = "SpaceCowboy"
realname = "Monsieur Weitersager"

[[irc.channels]]
name = "#skyscreeners"

[[irc.channels]]
name = "#elite-astrology"
password = "twinkle-twinkle"

[[irc.channels]]
name = "#hubblebubble"
'''


def test_load_config():
    toml = StringIO(TOML_CONFIG)

    irc_config, http_host, http_port = load_config(toml)

    assert irc_config == IrcConfig(
        server=IrcServer('orion.astrochat.test', 6669),
        nickname='SpaceCowboy',
        realname='Monsieur Weitersager',
        channels=[
            Channel('#skyscreeners'),
            Channel('#elite-astrology', password='twinkle-twinkle'),
            Channel('#hubblebubble'),
        ],
    )
    assert http_host == '127.0.0.1'
    assert http_port == 55555
