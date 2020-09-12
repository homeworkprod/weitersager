import json

import pytest

from weitersager.httpreceiver import Message


@pytest.mark.parametrize(
    'channels, text',
    [
        (['#example'             ], 'ohai, kthxbye!'                  ),
        (['#partyline', '#idlers'], 'Nothing to see here, move along.'),
    ],
)
def test_from_json(channels, text):
    data = {
        'channels': channels,
        'text': text,
    }
    json_data = json.dumps(data)

    message = Message.from_json(json_data)

    assert message.channels == frozenset(channels)
    assert message.text == text
