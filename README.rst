Weitersager
===========

Receive messages via HTTP and show them on IRC.

Based on syslog2IRC_.


Requirements
------------

- Python 3.4+
- irc_
- blinker_


Installation
------------

The required dependencies can be installed via pip_:

.. code:: sh

    $ pip install -r requirements.txt

In order to shut down Weitersager, send a query message with the text
"shutdown!" to the IRC bot. It should then quit, and Weitersager should
exit.


.. _syslog2IRC:  http://homework.nwsnet.de/releases/c474/#syslog2irc
.. _irc:         https://bitbucket.org/jaraco/irc
.. _blinker:     http://pythonhosted.org/blinker/
.. _pip:         http://www.pip-installer.org/


A note on threads (implementation detail)
-----------------------------------------

This tool uses threads. Besides the main thread, there are two
additional threads: one for the message receiver and one for the IRC
bot. Both are configured to be daemon threads.

A Python application exits if no more non-daemon threads are running.

In order to exit Weitersager when shutdown is requested on IRC, the IRC
bot will call `die()`, which will join the IRC bot thread. The main
thread and the (daemonized) message receiver thread remain.

Additionally, a dedicated signal is sent that sets a flag that causes
the main loop to stop. As the message receiver thread is the only one
left, but runs as a daemon, the application exits.

The dummy bot, on the other hand, does not run in a thread. The user
has to manually interrupt the application to exit.

For details, see the documentation on the `threading` module that is
part of Python's standard library.


:Copyright: 2007-2015 `Jochen Kupperschmidt <http://homework.nwsnet.de/>`_
:License: MIT, see LICENSE for details.
