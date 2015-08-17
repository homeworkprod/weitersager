#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
weitersager
~~~~~~~~~~~

:Copyright: 2007-2015 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from weitersager.irc import Channel
from weitersager.processor import start_with_args


if __name__ == '__main__':
    # IRC channels to join and to announce messages to
    channels = [
        Channel('#examplechannel1'),
        Channel('#examplechannel2', password='zePassword'),
    ]

    start_with_args(channels)
