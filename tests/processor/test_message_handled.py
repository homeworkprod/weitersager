"""
:Copyright: 2007-2022 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

import pytest

from weitersager.config import Config, HttpConfig, IrcConfig
from weitersager.processor import Processor
from weitersager.signals import irc_channel_joined, message_received


@pytest.fixture
def processor():
    http_config = HttpConfig('localhost', 8080, set())

    irc_config = IrcConfig(
        server=None,
        nickname='Nick',
        realname='Nick',
        commands=[],
        channels=set(),
    )

    config = Config(log_level="debug", http=http_config, irc=irc_config)

    return Processor(config)


def test_message_handled(processor):
    channel_name = '#foo'
    text = 'Knock, knock.'

    received_signal_data = []

    def announce(channel_name, text):
        received_signal_data.append((channel_name, text))

    processor.announcer.announce = announce

    fake_channel_join(channel_name)

    send_message_received_signal(channel_name, text)

    processor.process_queue(timeout_seconds=1)

    assert received_signal_data == [
        (channel_name, text),
    ]


def fake_channel_join(channel_name):
    irc_channel_joined.send(channel_name=channel_name)


def send_message_received_signal(channel_name, text):
    source_address = ('127.0.0.1', 12345)
    message_received.send(
        None,
        channel_name=channel_name,
        text=text,
        source_address=source_address,
    )
