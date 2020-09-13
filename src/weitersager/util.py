"""
weitersager.util
~~~~~~~~~~~~~~~~

Utilities

:Copyright: 2007-2020 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from datetime import datetime
from threading import Thread


def log(message, *args, **kwargs):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(timestamp, message.format(*args, **kwargs))


def start_thread(target, name):
    """Create, configure, and start a new thread."""
    t = Thread(target=target, name=name, daemon=True)
    t.start()
