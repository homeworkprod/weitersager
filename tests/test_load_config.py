"""
:Copyright: 2007-2020 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from io import StringIO

from weitersager.config import (
    HttpConfig,
    IrcChannel,
    IrcConfig,
    IrcServer,
    load_config,
)


TOML_CONFIG = '''\
[http]
host = "0.0.0.0"
port = 55555
api_tokens = ["qsSUx9KM-DBuDndUhGNi9_kxNHd08TypiHYM05ZTxVc"]

[irc.server]
host = "orion.astrochat.test"
port = 6669
password = "ToTheStars!"
rate_limit = 0.5

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
        server=IrcServer('orion.astrochat.test', 6669, 'ToTheStars!', 0.5),
        nickname='SpaceCowboy',
        realname='Monsieur Weitersager',
        channels=[
            IrcChannel('#skyscreeners'),
            IrcChannel('#elite-astrology', password='twinkle-twinkle'),
            IrcChannel('#hubblebubble'),
        ],
    )
    assert http_config == HttpConfig(
        host='0.0.0.0',
        port=55555,
        api_tokens={'qsSUx9KM-DBuDndUhGNi9_kxNHd08TypiHYM05ZTxVc'},
    )


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
    assert http_config == HttpConfig(
        host='127.0.0.1',
        port=8080,
        api_tokens=None,
    )


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
