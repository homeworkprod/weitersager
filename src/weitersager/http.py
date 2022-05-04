"""
weitersager.http
~~~~~~~~~~~~~~~~

HTTP server to receive messages

:Copyright: 2007-2022 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from __future__ import annotations
from dataclasses import dataclass
from http import HTTPStatus
import logging
import sys
from typing import Optional
from wsgiref.simple_server import make_server, ServerHandler, WSGIServer

from werkzeug.exceptions import abort, HTTPException
from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Request, Response

from .config import HttpConfig
from .signals import message_received
from .util import start_thread


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Message:
    channel: str
    text: str


def create_app(api_tokens: set[str]):
    return Application(api_tokens)


class Application:
    def __init__(self, api_tokens: set[str]):
        self._api_tokens = api_tokens

        self._url_map = Map(
            [
                Rule('/', endpoint='root'),
            ]
        )

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    @Request.application
    def wsgi_app(self, request):
        adapter = self._url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            handler = getattr(self, f'on_{endpoint}')
            return handler(request, **values)
        except HTTPException as exc:
            return exc

    def on_root(self, request):
        if self._api_tokens:
            api_token = _get_api_token(request.headers)
            if not api_token:
                abort(HTTPStatus.UNAUTHORIZED)

            if api_token not in self._api_tokens:
                abort(HTTPStatus.FORBIDDEN)

        if not request.is_json:
            abort(HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

        try:
            message = _parse_json_message(request.json)
        except (KeyError, ValueError):
            logger.info(
                'Invalid message received from %s.', request.remote_addr
            )
            abort(HTTPStatus.BAD_REQUEST)

        message_received.send(
            channel_name=message.channel,
            text=message.text,
            source_ip_address=request.remote_addr,
        )

        return Response('', status=HTTPStatus.ACCEPTED)


def _get_api_token(headers) -> Optional[str]:
    authorization_value = headers.get('Authorization')
    if not authorization_value:
        return None

    prefix = 'Token '
    if not authorization_value.startswith(prefix):
        return None

    return authorization_value[len(prefix) :]


def _parse_json_message(data: dict[str, str]) -> Message:
    """Extract message from JSON."""
    channel = data['channel']
    text = data['text']

    return Message(channel=channel, text=text)


# Override value of `Server:` header sent by wsgiref.
ServerHandler.server_software = 'Weitersager'


def create_server(config: HttpConfig) -> WSGIServer:
    """Create the HTTP server."""
    app = create_app(config.api_tokens)

    return make_server(config.host, config.port, app)


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
