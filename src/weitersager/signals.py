"""
weitersager.signals
~~~~~~~~~~~~~~~~~~~

Signals

:Copyright: 2007-2021 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from blinker import signal


irc_channel_joined = signal('irc-channel-joined')
message_received = signal('message-received')
