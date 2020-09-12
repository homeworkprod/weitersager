"""
weitersager.processor
~~~~~~~~~~~~~~~~~~~~~

Connect HTTP server and IRC bot.

:Copyright: 2007-2015 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from time import sleep

from .argparser import parse_args
from .httpreceiver import ReceiveServer
from .irc import create_bot
from .signals import channel_joined, message_approved, \
    message_received, shutdown_requested
from .util import log


class Processor(object):

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

    def handle_message(self, sender, *, channel_names=None, text=None,
                       source_address=None):
        """Log and announce an incoming message."""
        source = '{0[0]}:{0[1]:d}'.format(source_address)

        log('Received message from {} for channels {} with text "{}"',
            source, ', '.join(channel_names), text)

        for channel_name in channel_names:
            if channel_name in self.enabled_channel_names:
                message_approved.send(channel_name=channel_name,
                                      text=text)
            else:
                log('Could not send message to channel {}, not joined.',
                    channel_name)

    def handle_shutdown_requested(self, sender):
        self.shutdown = True

    def run(self):
        """Run the main loop until shutdown is requested."""
        while not self.shutdown:
            sleep(0.5)

        log('Shutting down ...')


def start(irc_server, irc_nickname, irc_realname, irc_channels,
          http_ip_address, http_port, **options):
    """Start the IRC bot and HTTP listen server."""
    bot = create_bot(irc_server, irc_nickname, irc_realname, irc_channels,
                     **options)
    message_approved.connect(bot.say)

    processor = Processor()

    # Up to this point, no signals must have been sent.

    processor.connect_to_signals()

    # Signals are allowed be sent from here on.

    ReceiveServer.start(http_ip_address, http_port)
    bot.start()

    processor.run()


def start_with_args(irc_channels, **options):
    """Start the IRC bot and HTTP listen server,

    Most arguments (except for the IRC channels to join) are read from
    the command line.
    """
    args = parse_args()

    start(
        args.irc_server,
        args.irc_nickname,
        args.irc_realname,
        irc_channels,
        args.http_ip_address,
        args.http_port,
        **options)
