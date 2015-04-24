#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
===========
Weitersager
===========

Receive messages via HTTP and show them on IRC.

Based on syslog2IRC_.


Requirements
------------

- Python 3.4+ (tested with 3.4.2)
- irc_ (tested with 12.1.1)
- blinker_ (tested with 1.3)


Installation
------------

irc_ and blinker_ can be installed via pip_:

.. code:: sh

    $ pip install irc blinker

In order to shut down Weitersager, send a query message with the text
"shutdown!" to the IRC bot. It should then quit, and Weitersager should
exit.


.. _syslog2IRC:  http://homework.nwsnet.de/releases/c474/#syslog2irc
.. _irc:         https://bitbucket.org/jaraco/irc
.. _blinker:     http://pythonhosted.org/blinker/
.. _pip:         http://www.pip-installer.org/


:Copyright: 2007-2015 `Jochen Kupperschmidt <http://homework.nwsnet.de/>`_
:Date: 24-Apr-2015
:License: MIT, see LICENSE for details.
:Version: 0.1
"""

import argparse
from collections import namedtuple
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import sys
from threading import Thread
from time import sleep

from blinker import signal
from irc.bot import ServerSpec, SingleServerIRCBot
from irc.buffer import LenientDecodingLineBuffer


DEFAULT_HTTP_IP_ADDRESS = '0.0.0.0'
DEFAULT_HTTP_PORT = 8080
DEFAULT_IRC_PORT = ServerSpec('').port


# A note on threads (implementation detail):
#
# This tool uses threads. Besides the main thread, there are two
# additional threads: one for the message receiver and one for the IRC
# bot. Both are configured to be daemon threads.
#
# A Python application exits if no more non-daemon threads are running.
#
# In order to exit Weitersager when shutdown is requested on IRC, the IRC
# bot will call `die()`, which will join the IRC bot thread. The main
# thread and the (daemonized) message receiver thread remain.
#
# Additionally, a dedicated signal is sent that sets a flag that causes
# the main loop to stop. As the message receiver thread is the only one
# left, but runs as a daemon, the application exits.
#
# The dummy bot, on the other hand, does not run in a thread. The user
# has to manually interrupt the application to exit.
#
# For details, see the documentation on the `threading` module that is
# part of Python's standard library.


# -------------------------------------------------------------------- #
# logging


def log(message, *args, **kwargs):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(timestamp, message.format(*args, **kwargs))


# -------------------------------------------------------------------- #
# signals


channel_joined = signal('channel-joined')
message_received = signal('message-received')
message_approved = signal('message-approved')
shutdown_requested = signal('shutdown-requested')


# -------------------------------------------------------------------- #
# HTTP message receiver


class Message(namedtuple('Message', 'channels text')):

    @classmethod
    def from_json(cls, json_data):
        data = json.loads(json_data)

        channels = frozenset(map(str, data['channels']))
        text = data['text']

        return cls(channels=channels, text=text)


class RequestHandler(BaseHTTPRequestHandler):
    """Handler for messages submitted via HTTP."""

    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            data = self.rfile.read(content_length).decode('utf-8')
            message = Message.from_json(data)
        except (KeyError, ValueError):
            log('Invalid message received from {}:{:d}.', *self.client_address)
            self.send_error(400)
            return

        self.send_response(200)
        self.end_headers()

        message_received.send(channel_names=message.channels,
                              text=message.text,
                              source_address=self.client_address)


class ReceiveServer(HTTPServer):
    """HTTP server that waits for messages."""

    def __init__(self, ip_address, port):
        address = (ip_address, port)
        HTTPServer.__init__(self, address, RequestHandler)
        log('Listening for HTTP requests on {}:{:d}.', *address)

    @classmethod
    def start(cls, ip_address, port):
        """Start in a separate thread."""
        try:
            receiver = cls(ip_address, port)
        except Exception as e:
            sys.stderr.write(
                'Error {0.errno:d}: {0.strerror}\n'.format(e))
            sys.stderr.write(
                'Probably no permission to open port {}. '
                'Try to specify a port number above 1,024 (or even '
                '4,096) and up to 65,535.\n'.format(port))
            sys.exit(1)

        thread_name = cls.__name__
        start_thread(receiver.serve_forever, thread_name)


# -------------------------------------------------------------------- #
# IRC


class Channel(namedtuple('Channel', 'name password')):
    """An IRC channel with optional password."""

    def __new__(cls, name, *, password=None):
        return super(Channel, cls).__new__(cls, name, password)


class Bot(SingleServerIRCBot):
    """An IRC bot to forward messages to IRC channels."""

    def __init__(self, server_spec, nickname, realname, channels):
        log('Connecting to IRC server {0.host}:{0.port:d} ...', server_spec)

        SingleServerIRCBot.__init__(self, [server_spec], nickname,
            realname)

        # Avoid `UnicodeDecodeError` on non-UTF-8 messages.
        self.connection.buffer_class = LenientDecodingLineBuffer

        # Note: `self.channels` already exists in super class.
        self.channels_to_join = channels

    def start(self):
        """Connect to the server, in a separate thread."""
        start_thread(super().start, self.__class__.__name__)

    def get_version(self):
        return 'Weitersager'

    def on_welcome(self, conn, event):
        """Join channels after connect."""
        log('Connected to {}:{:d}.', *conn.socket.getpeername())

        channel_names = sorted(c.name for c in self.channels_to_join)
        log('Channels to join: {}', ', '.join(channel_names))

        for channel in self.channels_to_join:
            log('Joining channel {} ...', channel.name)
            conn.join(channel.name, channel.password or '')

    def on_nicknameinuse(self, conn, event):
        """Choose another nickname if conflicting."""
        self._nickname += '_'
        conn.nick(self._nickname)

    def on_join(self, conn, event):
        """Successfully joined channel."""
        joined_nick = event.source.nick
        channel_name = event.target

        if joined_nick == self._nickname:
            log('Joined IRC channel: {}', channel_name)
            channel_joined.send(channel_name=channel_name)

    def on_badchannelkey(self, conn, event):
        """Channel could not be joined due to wrong password."""
        channel = event.arguments[0]
        log('Cannot join channel {} (bad key).', channel)

    def on_privmsg(self, conn, event):
        """React on private messages.

        Shut down, for example.
        """
        whonick = event.source.nick
        message = event.arguments[0]
        if message == 'shutdown!':
            log('Shutdown requested on IRC by user {}.', whonick)
            shutdown_requested.send()
            self.die('Shutting down.')  # Joins IRC bot thread.

    def say(self, sender, *, channel_name=None, text=None):
        """Say message on channel."""
        self.connection.privmsg(channel_name, text)


class DummyBot(object):

    def __init__(self, server_spec, nickname, realname, channels):
        self.channels = channels

    def start(self):
        # Fake channel joins.
        for channel in self.channels:
            channel_joined.send(channel_name=channel.name)

    def say(self, sender, *, channel_name=None, text=None):
        log('{}> {}', channel_name, text)


def create_bot(server, nickname, realname, channels):
    """Create and return an IRC bot according to the configuration."""
    if server:
        bot_class = Bot
    else:
        log('No IRC server specified; will write to STDOUT instead.')
        bot_class = DummyBot

    return bot_class(server, nickname, realname, channels)


# -------------------------------------------------------------------- #
# threads


def start_thread(target, name):
    """Create, configure, and start a new thread."""
    t = Thread(target=target, name=name)
    t.daemon = True
    t.start()


# -------------------------------------------------------------------- #


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


# -------------------------------------------------------------------- #
# command line argument parsing


def parse_args():
    """Setup and apply the command line arguments parser."""
    parser = argparse.ArgumentParser()

    parser.add_argument('--irc-nickname',
        dest='irc_nickname',
        default='Weitersager',
        help='the IRC nickname the bot should use',
        metavar='NICKNAME')

    parser.add_argument('--irc-realname',
        dest='irc_realname',
        default='Weitersager',
        help='the IRC realname the bot should use',
        metavar='REALNAME')

    parser.add_argument('--irc-server',
        dest='irc_server',
        type=parse_irc_server_arg,
        help='IRC server (host and, optionally, port) to connect to'
            + ' [e.g. "irc.example.com" or "irc.example.com:6669";'
            + ' default port: {:d}]'.format(DEFAULT_IRC_PORT),
        metavar='SERVER')

    parser.add_argument('--http-listen-ip-address',
        dest='http_ip_address',
        default=DEFAULT_HTTP_IP_ADDRESS,
        help='the IP address to listen on for HTTP requests [default: {}]'
             .format(DEFAULT_HTTP_IP_ADDRESS),
        metavar='IP_ADDRESS')

    parser.add_argument('--http-listen-port',
        dest='http_port',
        type=int,
        default=DEFAULT_HTTP_PORT,
        help='the port to listen on for HTTP requests [default: {:d}]'
             .format(DEFAULT_HTTP_PORT),
        metavar='PORT')

    return parser.parse_args()


def parse_irc_server_arg(value):
    """Parse a hostname with optional port."""
    fragments = value.split(':', 1)
    if len(fragments) > 1:
        fragments[1] = int(fragments[1])
    return ServerSpec(*fragments)


# -------------------------------------------------------------------- #


def start(irc_server, irc_nickname, irc_realname, irc_channels,
          http_ip_address, http_port):
    """Start the IRC bot and HTTP listen server."""
    bot = create_bot(irc_server, irc_nickname, irc_realname, irc_channels)
    message_approved.connect(bot.say)

    processor = Processor()

    # Up to this point, no signals must have been sent.

    processor.connect_to_signals()

    # Signals are allowed be sent from here on.

    ReceiveServer.start(http_ip_address, http_port)
    bot.start()

    processor.run()


# -------------------------------------------------------------------- #


if __name__ == '__main__':
    args = parse_args()

    # IRC channels to join and to announce messages to
    channels = [
        Channel('#examplechannel1'),
        Channel('#examplechannel2', password='zePassword'),
    ]

    start(
        args.irc_server,
        args.irc_nickname,
        args.irc_realname,
        channels,
        args.http_ip_address,
        args.http_port)
