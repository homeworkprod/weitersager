"""
weitersager.processor
~~~~~~~~~~~~~~~~~~~~~

Connect HTTP server and IRC bot.

:Copyright: 2007-2020 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from time import sleep

from .httpreceiver import start_receive_server
from .irc import create_bot
from .signals import (
    channel_joined,
    message_approved,
    message_received,
    shutdown_requested,
)
from .util import log


class Processor:

    def __init__(self):
        self.enabled_channel_names = set()
        self.shutdown = False

    def connect_to_signals(self):
        channel_joined.connect(self.enable_channel)
        message_received.connect(self.handle_message)
        shutdown_requested.connect(self.handle_shutdown_requested)

    def enable_channel(self, sender, *, channel_name=None):
        log('Enabled forwarding to channel {}.', channel_name)
        self.enabled_channel_names.add(channel_name)

    def handle_message(
        self, sender, *, channel_name=None, text=None, source_address=None
    ):
        """Log and announce an incoming message."""
        source = f'{source_address[0]}:{source_address[1]:d}'

        log(
            'Received message from {} for channel {} with text "{}"',
            source,
            channel_name,
            text,
        )

        if channel_name not in self.enabled_channel_names:
            log(
                'Could not send message to channel {}, not joined.',
                channel_name,
            )
            return

        message_approved.send(channel_name=channel_name, text=text)

    def handle_shutdown_requested(self, sender):
        self.shutdown = True

    def run(self):
        """Run the main loop until shutdown is requested."""
        while not self.shutdown:
            sleep(0.5)

        log('Shutting down ...')


def start(irc_config, http_config, **options):
    """Start the IRC bot and HTTP listen server."""
    bot = create_bot(irc_config, **options)
    message_approved.connect(bot.say)

    processor = Processor()

    # Up to this point, no signals must have been sent.

    processor.connect_to_signals()

    # Signals are allowed be sent from here on.

    start_receive_server(http_config)
    bot.start()

    processor.run()
