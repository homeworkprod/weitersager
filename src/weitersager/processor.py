"""
weitersager.processor
~~~~~~~~~~~~~~~~~~~~~

Connect HTTP server and IRC bot.

:Copyright: 2007-2021 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

import logging
from time import sleep
from typing import Any, Optional, Set, Tuple

from .config import Config
from .http import start_receive_server
from .irc import create_bot
from .signals import irc_channel_joined, message_received


logger = logging.getLogger(__name__)


class Processor:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.irc_bot = create_bot(config.irc)
        self.enabled_channel_names: Set[str] = set()

        # Up to this point, no signals must have been sent.
        self.connect_to_signals()
        # Signals are allowed be sent from here on.

    def connect_to_signals(self) -> None:
        irc_channel_joined.connect(self.enable_channel)
        message_received.connect(self.handle_message)

    def enable_channel(self, sender, *, channel_name=None) -> None:
        logger.info('Enabled forwarding to channel %s.', channel_name)
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
        logger.debug(
            'Received message from %s:%d for channel %s with text "%s".',
            source_address[0],
            source_address[1],
            channel_name,
            text,
        )

        if channel_name not in self.enabled_channel_names:
            logger.warning(
                'Could not send message to channel %s, not joined.',
                channel_name,
            )
            return

        self.irc_bot.say(channel_name, text)

    def run(self) -> None:
        """Run the main loop."""
        self.irc_bot.start()
        start_receive_server(self.config.http)

        try:
            while True:
                sleep(0.5)
        except KeyboardInterrupt:
            pass

        logger.info('Shutting down ...')
        self.irc_bot.disconnect('Bye.')  # Joins bot thread.


def start(config: Config) -> None:
    """Start the IRC bot and the HTTP listen server."""
    processor = Processor(config)
    processor.run()
