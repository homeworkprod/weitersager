"""
weitersager.processor
~~~~~~~~~~~~~~~~~~~~~

Connect HTTP server and IRC bot.

:Copyright: 2007-2021 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from time import sleep
from typing import Any, Optional, Set, Tuple

from .config import Config
from .http import start_receive_server
from .irc import create_bot
from .signals import channel_joined, message_approved, message_received
from .util import log


class Processor:

    def __init__(self) -> None:
        self.enabled_channel_names: Set[str] = set()

    def connect_to_signals(self) -> None:
        channel_joined.connect(self.enable_channel)
        message_received.connect(self.handle_message)

    def enable_channel(self, sender, *, channel_name=None) -> None:
        log('Enabled forwarding to channel {}.', channel_name)
        self.enabled_channel_names.add(channel_name)

    def handle_message(
        self,
        sender: Optional[Any],
        *,
        channel_name: str,
        text: str,
        source_address: Tuple[str, int],
    ) -> None:
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

    def run(self) -> None:
        """Run the main loop."""
        try:
            while True:
                sleep(0.5)
        except KeyboardInterrupt:
            pass

        log('Shutting down ...')


def start(config: Config) -> None:
    """Start the IRC bot and the HTTP listen server."""
    bot = create_bot(config.irc)
    message_approved.connect(bot.say)

    processor = Processor()

    # Up to this point, no signals must have been sent.

    processor.connect_to_signals()

    # Signals are allowed be sent from here on.

    start_receive_server(config.http)
    bot.start()

    processor.run()

    bot.disconnect('Bye.')  # Joins bot thread.
