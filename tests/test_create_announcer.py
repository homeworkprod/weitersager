"""
:Copyright: 2007-2021 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

import pytest

from weitersager.irc import (
    Bot,
    create_announcer,
    DummyBot,
    IrcConfig,
    IrcServer,
)


@pytest.mark.parametrize(
    'server, expected_type',
    [
        (IrcServer('irc.server.test'), Bot),
        (None, DummyBot),
    ],
)
def test_create_announcer(server, expected_type):
    config = IrcConfig(
        server=server,
        nickname='nick',
        realname='Nick',
        commands=[],
        channels=set(),
    )

    announcer = create_announcer(config)

    assert type(announcer.bot) == expected_type
