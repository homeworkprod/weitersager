"""
:Copyright: 2007-2020 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from threading import Thread

import pytest

from weitersager.config import HttpConfig
from weitersager.http import ReceiveServer


@pytest.fixture
def make_server():
    # Per default, bind to localhost on random user port.
    def _wrapper(host='', port=0, *, api_tokens=None):
        config = HttpConfig(host, port, api_tokens=api_tokens)

        server = ReceiveServer(config)

        thread = Thread(target=server.handle_request)
        thread.start()

        return server

    return _wrapper


@pytest.fixture
def server(make_server):
    return make_server()
