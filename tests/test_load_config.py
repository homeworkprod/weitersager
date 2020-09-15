"""
:Copyright: 2007-2020 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from io import StringIO

from weitersager.config import load_config
from weitersager.httpreceiver import Config as HttpConfig
from weitersager.irc import Channel, Config as IrcConfig, Server as IrcServer


TOML_CONFIG = '''\
[http]
host = "0.0.0.0"
port = 55555

[irc.server]
host = "orion.astrochat.test"
port = 6669
password = "ToTheStars!"

[irc.bot]
nickname = "SpaceCowboy"
realname = "Monsieur Weitersager"

[irc]
channels = [
    { name = "#skyscreeners" },
    { name = "#elite-astrology", password = "twinkle-twinkle" },
    { name = "#hubblebubble" },
]
'''


def test_load_config():
    toml = StringIO(TOML_CONFIG)

    irc_config, http_config = load_config(toml)

    assert irc_config == IrcConfig(
        server=IrcServer('orion.astrochat.test', 6669, 'ToTheStars!'),
        nickname='SpaceCowboy',
        realname='Monsieur Weitersager',
        channels=[
            Channel('#skyscreeners'),
            Channel('#elite-astrology', password='twinkle-twinkle'),
            Channel('#hubblebubble'),
        ],
    )
    assert http_config == HttpConfig('0.0.0.0', 55555)


TOML_CONFIG_WITH_DEFAULTS = '''\
[irc.server]
host = "irc.onlinetalk.test"

[irc.bot]
nickname = "TownCrier"
'''


def test_load_config_with_defaults():
    toml = StringIO(TOML_CONFIG_WITH_DEFAULTS)

    irc_config, http_config = load_config(toml)

    assert irc_config == IrcConfig(
        server=IrcServer('irc.onlinetalk.test', 6667),
        nickname='TownCrier',
        realname='Weitersager',
        channels=[],
    )
    assert http_config == HttpConfig('127.0.0.1', 8080)


TOML_CONFIG_WITHOUT_IRC_SERVER_TABLE = '''\
[irc.bot]
nickname = "Lokalrunde"
'''


def test_load_config_without_irc_server_table():
    toml = StringIO(TOML_CONFIG_WITHOUT_IRC_SERVER_TABLE)

    irc_config, _ = load_config(toml)

    assert irc_config.server is None


TOML_CONFIG_WITHOUT_IRC_SERVER_HOST = '''\
[irc.server]

[irc.bot]
nickname = "Lokalrunde"
'''


def test_load_config_without_irc_server_host():
    toml = StringIO(TOML_CONFIG_WITHOUT_IRC_SERVER_HOST)

    irc_config, _ = load_config(toml)

    assert irc_config.server is None
