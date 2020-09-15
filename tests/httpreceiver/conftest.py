"""
:Copyright: 2007-2020 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from threading import Thread

import pytest

from weitersager.httpreceiver import Config, ReceiveServer


@pytest.fixture
def make_server():

    # Per default, bind to localhost on random user port.
    def _wrapper(host='', port=0):
        config = Config(host, port)

        server = ReceiveServer(config)

        thread = Thread(target=server.handle_request)
        thread.start()

        return server

    return _wrapper


@pytest.fixture
def server(make_server):
    return make_server()
