"""
:Copyright: 2007-2015 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from weitersager.processor import Processor
from weitersager.signals import channel_joined, message_approved, \
    message_received


def test_message_handled():
    channel_names = ['#foo', '#bar']
    text = 'Knock, knock.'

    received_signal_data = []

    @message_approved.connect
    def handle_message_approved(sender, **data):
        received_signal_data.append(data)

    processor = Processor()
    processor.connect_to_signals()

    fake_channel_joins(channel_names)

    send_message_received_signal(channel_names, text)

    assert received_signal_data == [
        {
            'channel_name': '#foo',
            'text': text,
        },
        {
            'channel_name': '#bar',
            'text': text,
        },
    ]


def fake_channel_joins(channel_names):
    for channel_name in channel_names:
        channel_joined.send(channel_name=channel_name)


def send_message_received_signal(channel_names, text):
    source_address = ('127.0.0.1', 12345)
    message_received.send(
        None,
        channel_names=channel_names,
        text=text,
        source_address=source_address,
    )
