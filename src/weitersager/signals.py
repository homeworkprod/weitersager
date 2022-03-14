"""
weitersager.signals
~~~~~~~~~~~~~~~~~~~

Signals

:Copyright: 2007-2022 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from blinker import Signal


irc_channel_joined = Signal()
message_received = Signal()
