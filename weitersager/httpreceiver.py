"""
weitersager.httpreceiver
~~~~~~~~~~~~~~~~~~~~~~~~

HTTP server to receive messages

:Copyright: 2007-2020 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import sys
from typing import Set

from .signals import message_received
from .util import log, start_thread


@dataclass(frozen=True)
class Message:
    channels: Set[str]
    text: str

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
            sys.stderr.write(f'Error {e.errno:d}: {e.strerror}\n')
            sys.stderr.write(
                f'Probably no permission to open port {port}. '
                'Try to specify a port number above 1,024 (or even '
                '4,096) and up to 65,535.\n'
            )
            sys.exit(1)

        thread_name = cls.__name__
        start_thread(receiver.serve_forever, thread_name)
