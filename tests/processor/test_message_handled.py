from unittest import TestCase

from weitersager.processor import Processor
from weitersager.signals import channel_joined, message_approved, \
    message_received


class MessageHandledTestCase(TestCase):

    def setUp(self):
        self.received_signal_data = []

    def test_message_handled(self):
        channel_names = ['#foo', '#bar']
        text = 'Knock, knock.'

        @message_approved.connect
        def handle_message_approved(sender, **data):
            self.storeReceivedSignalData(data)

        processor = Processor()
        processor.connect_to_signals()

        self.fake_channel_joins(channel_names)

        self.send_message_received_signal(channel_names, text)

        self.assertReceivedSignalDataEqual([
            {
                'channel_name': '#foo',
                'text': text,
            },
            {
                'channel_name': '#bar',
                'text': text,
            },
        ])

    def fake_channel_joins(self, channel_names):
        for channel_name in channel_names:
            channel_joined.send(channel_name=channel_name)

    def send_message_received_signal(self, channel_names, text):
        source_address = ('127.0.0.1', 12345)
        message_received.send(None,
                              channel_names=channel_names,
                              text=text,
                              source_address=source_address)

    def storeReceivedSignalData(self, data):
        self.received_signal_data.append(data)

    def assertReceivedSignalDataEqual(self, expected):
        self.assertEqual(self.received_signal_data, expected)
