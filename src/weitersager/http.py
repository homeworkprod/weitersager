"""
weitersager.http
~~~~~~~~~~~~~~~~

HTTP server to receive messages

:Copyright: 2007-2022 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from __future__ import annotations
from dataclasses import dataclass
from functools import partial
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import logging
import sys
from typing import Optional

from .config import HttpConfig
from .signals import message_received
from .util import start_thread


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Message:
    channel: str
    text: str


def parse_json_message(json_data: str) -> Message:
    """Extract message from JSON."""
    data = json.loads(json_data)

    channel = data['channel']
    text = data['text']

    return Message(channel=channel, text=text)


class RequestHandler(BaseHTTPRequestHandler):
    """Handler for messages submitted via HTTP."""

    def __init__(self, api_tokens: set[str], *args, **kwargs) -> None:
        self.api_tokens = api_tokens
        super().__init__(*args, **kwargs)

    def do_POST(self) -> None:
        if self.path != '/':
            self.send_error(HTTPStatus.NOT_FOUND)
            return

        if self.api_tokens:
            api_token = self._get_api_token()
            if not api_token:
                self.send_error(HTTPStatus.UNAUTHORIZED)
                return

            if api_token not in self.api_tokens:
                self.send_error(HTTPStatus.FORBIDDEN)
                return

        try:
            content_length = int(self.headers.get('Content-Length', 0))
            data = self.rfile.read(content_length).decode('utf-8')
            message = parse_json_message(data)
        except (KeyError, ValueError):
            logger.info(
                'Invalid message received from %s.', self.address_string()
            )
            self.send_error(HTTPStatus.BAD_REQUEST)
            return

        self.send_response(HTTPStatus.ACCEPTED)
        self.end_headers()

        message_received.send(
            channel_name=message.channel,
            text=message.text,
            source_address=self.client_address,
        )

    def _get_api_token(self) -> Optional[str]:
        authorization_value = self.headers.get('Authorization')
        if not authorization_value:
            return None

        prefix = 'Token '
        if not authorization_value.startswith(prefix):
            return None

        return authorization_value[len(prefix) :]

    def version_string(self) -> str:
        """Return custom server version string."""
        return 'Weitersager'


def create_server(config: HttpConfig) -> ThreadingHTTPServer:
    """Create the HTTP server."""
    address = (config.host, config.port)
    handler_class = partial(RequestHandler, config.api_tokens)
    return ThreadingHTTPServer(address, handler_class)


def start_receive_server(config: HttpConfig) -> None:
    """Start in a separate thread."""
    try:
        server = create_server(config)
    except OSError as e:
        sys.stderr.write(f'Error {e.errno:d}: {e.strerror}\n')
        sys.stderr.write(
            f'Probably no permission to open port {config.port}. '
            'Try to specify a port number above 1,024 (or even '
            '4,096) and up to 65,535.\n'
        )
        sys.exit(1)

    thread_name = server.__class__.__name__
    start_thread(server.serve_forever, thread_name)
    logger.info('Listening for HTTP requests on %s:%d.', *server.server_address)
