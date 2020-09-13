"""
weitersager.httpreceiver
~~~~~~~~~~~~~~~~~~~~~~~~

HTTP server to receive messages

:Copyright: 2007-2020 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from dataclasses import dataclass
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import sys

from .signals import message_received
from .util import log, start_thread


@dataclass(frozen=True)
class Message:
    channel: str
    text: str


def parse_json_message(json_data):
    """Extract message from JSON."""
    data = json.loads(json_data)

    channel = data['channel']
    text = data['text']

    return Message(channel=channel, text=text)


class RequestHandler(BaseHTTPRequestHandler):
    """Handler for messages submitted via HTTP."""

    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            data = self.rfile.read(content_length).decode('utf-8')
            message = parse_json_message(data)
        except (KeyError, ValueError):
            log('Invalid message received from {}:{:d}.', *self.client_address)
            self.send_error(HTTPStatus.BAD_REQUEST)
            return

        self.send_response(HTTPStatus.ACCEPTED)
        self.end_headers()

        message_received.send(
            channel_name=message.channel,
            text=message.text,
            source_address=self.client_address,
        )


class ReceiveServer(HTTPServer):
    """HTTP server that waits for messages."""

    def __init__(self, ip_address, port):
        address = (ip_address, port)
        HTTPServer.__init__(self, address, RequestHandler)
        log('Listening for HTTP requests on {}:{:d}.', *address)


def start_receive_server(ip_address, port):
    """Start in a separate thread."""
    try:
        receiver = ReceiveServer(ip_address, port)
    except Exception as e:
        sys.stderr.write(f'Error {e.errno:d}: {e.strerror}\n')
        sys.stderr.write(
            f'Probably no permission to open port {port}. '
            'Try to specify a port number above 1,024 (or even '
            '4,096) and up to 65,535.\n'
        )
        sys.exit(1)

    thread_name = receiver.__class__.__name__
    start_thread(receiver.serve_forever, thread_name)
