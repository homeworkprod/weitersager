# -*- coding: utf-8 -*-

import json
from unittest import TestCase

from nose2.tools import params

from weitersager.httpreceiver import Message


class MessageTestCase(TestCase):

    @params(
        (['#example'             ], 'ohai, kthxbye!'                  ),
        (['#partyline', '#idlers'], 'Nothing to see here, move along.'),
    )
    def test_from_json(self, channels, text):
        data = {
            'channels': channels,
            'text': text,
        }
        json_data = json.dumps(data)

        message = Message.from_json(json_data)

        self.assertEqual(message.channels, frozenset(channels))
        self.assertEqual(message.text, text)
