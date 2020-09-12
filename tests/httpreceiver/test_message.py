"""
:Copyright: 2007-2020 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

import json

import pytest

from weitersager.httpreceiver import Message


@pytest.mark.parametrize(
    'channel, text',
    [
        ('#example', 'ohai, kthxbye!'                  ),
        ('#idlers' , 'Nothing to see here, move along.'),
    ],
)
def test_from_json(channel, text):
    data = {
        'channel': channel,
        'text': text,
    }
    json_data = json.dumps(data)

    message = Message.from_json(json_data)

    assert message.channel == channel
    assert message.text == text
