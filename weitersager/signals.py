"""
weitersager.signals
~~~~~~~~~~~~~~~~~~~

Signals

:Copyright: 2007-2020 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from blinker import signal


channel_joined = signal('channel-joined')
message_received = signal('message-received')
message_approved = signal('message-approved')
shutdown_requested = signal('shutdown-requested')
