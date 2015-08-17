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


# A note on threads (implementation detail):
#
# This tool uses threads. Besides the main thread, there are two
# additional threads: one for the message receiver and one for the IRC
# bot. Both are configured to be daemon threads.
#
# A Python application exits if no more non-daemon threads are running.
#
# In order to exit Weitersager when shutdown is requested on IRC, the IRC
# bot will call `die()`, which will join the IRC bot thread. The main
# thread and the (daemonized) message receiver thread remain.
#
# Additionally, a dedicated signal is sent that sets a flag that causes
# the main loop to stop. As the message receiver thread is the only one
# left, but runs as a daemon, the application exits.
#
# The dummy bot, on the other hand, does not run in a thread. The user
# has to manually interrupt the application to exit.
#
# For details, see the documentation on the `threading` module that is
# part of Python's standard library.


if __name__ == '__main__':
    # IRC channels to join and to announce messages to
    channels = [
        Channel('#examplechannel1'),
        Channel('#examplechannel2', password='zePassword'),
    ]

    start_with_args(channels)
