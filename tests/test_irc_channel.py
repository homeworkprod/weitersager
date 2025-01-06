"""
:Copyright: 2007-2025 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

import pytest

from weitersager.irc import IrcChannel


@pytest.mark.parametrize(
    'channel, expected_name, expected_password',
    [
        (IrcChannel('#example'), '#example', None),
        (IrcChannel('#example', password=None), '#example', None),
        (IrcChannel('#whq', password='secret'), '#whq', 'secret'),
    ],
)
def test_irc_channel_creation(channel, expected_name, expected_password):
    assert channel.name == expected_name
    assert channel.password == expected_password
