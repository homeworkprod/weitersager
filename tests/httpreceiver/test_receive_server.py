"""
:Copyright: 2007-2020 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

import json
from threading import Thread
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest

from weitersager.httpreceiver import Config, ReceiveServer


@pytest.fixture
def server():
    config = Config('', 0)  # Bind to localhost on random user port.
    server = ReceiveServer(config)

    thread = Thread(target=server.handle_request)
    thread.start()

    yield server

    thread.join()


def test_receive_server_with_valid_request(server):
    data = {
        'channel': '#party',
        'text': 'Limbo!',
    }
    request = build_request(server, data)

    response = urlopen(request)

    assert response.code == 202


def test_receive_server_without_channel(server):
    data = {
        'text': 'Which channel is this?!',
    }
    request = build_request(server, data)

    with pytest.raises(HTTPError) as excinfo:
        response = urlopen(request)

    assert excinfo.value.code == 400


def test_receive_server_without_text(server):
    data = {
        'channel': '#silence',
    }
    request = build_request(server, data)

    with pytest.raises(HTTPError) as excinfo:
        response = urlopen(request)

    assert excinfo.value.code == 400


def build_request(server, data):
    url = get_server_url(server)
    json_data = json.dumps(data).encode('utf-8')
    return Request(url, data=json_data, method='POST')


def get_server_url(server):
    server_host, server_port = server.server_address
    return f'http://{server_host}:{server_port}/'
