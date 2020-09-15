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
from typing import Optional, Set

from .signals import message_received
from .util import log, start_thread


@dataclass(frozen=True)
class Config:
    """An HTTP receiver configuration."""
    host: str
    port: int
    api_tokens: Optional[Set[str]] = None


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
        valid_api_tokens = self.server.api_tokens
        if valid_api_tokens:
            api_token = self._get_api_token()
            if not api_token:
                self.send_response(HTTPStatus.UNAUTHORIZED)
                self.end_headers()
                return

            if api_token not in valid_api_tokens:
                self.send_response(HTTPStatus.FORBIDDEN)
                self.end_headers()
                return

        try:
            content_length = int(self.headers.get('Content-Length', 0))
            data = self.rfile.read(content_length).decode('utf-8')
            message = parse_json_message(data)
        except (KeyError, ValueError):
            log(f'Invalid message received from {self.address_string()}.')
            self.send_error(HTTPStatus.BAD_REQUEST)
            return

        self.send_response(HTTPStatus.ACCEPTED)
        self.end_headers()

        message_received.send(
            channel_name=message.channel,
            text=message.text,
            source_address=self.client_address,
        )

    def _get_api_token(self):
        authorization_value = self.headers.get('authorization')
        if not authorization_value:
            return None

        prefix = 'WTRSGR '
        if not authorization_value.startswith(prefix):
            return None

        return authorization_value[len(prefix) :]

    def version_string(self):
        """Return custom server version string."""
        return 'Weitersager'


class ReceiveServer(HTTPServer):
    """HTTP server that waits for messages."""

    def __init__(self, config):
        address = (config.host, config.port)
        HTTPServer.__init__(self, address, RequestHandler)
        log('Listening for HTTP requests on {}:{:d}.', *address)

        self.api_tokens = config.api_tokens

def start_receive_server(config):
    """Start in a separate thread."""
    try:
        receiver = ReceiveServer(config)
    except Exception as e:
        sys.stderr.write(f'Error {e.errno:d}: {e.strerror}\n')
        sys.stderr.write(
            f'Probably no permission to open port {config.port}. '
            'Try to specify a port number above 1,024 (or even '
            '4,096) and up to 65,535.\n'
        )
        sys.exit(1)

    thread_name = receiver.__class__.__name__
    start_thread(receiver.serve_forever, thread_name)
