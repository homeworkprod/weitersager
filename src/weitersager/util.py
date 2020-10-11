"""
weitersager.util
~~~~~~~~~~~~~~~~

Utilities

:Copyright: 2007-2020 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from datetime import datetime
from threading import Thread
from typing import Any, Callable, Dict, Sequence


def log(message: str, *args: Any, **kwargs: Dict[str, Any]) -> None:
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(timestamp, message.format(*args, **kwargs))


def start_thread(target: Callable, name: str) -> None:
    """Create, configure, and start a new thread."""
    t = Thread(target=target, name=name, daemon=True)
    t.start()
