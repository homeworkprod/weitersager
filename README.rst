Weitersager
===========

A proxy that receives text messages via JSON over HTTP and shows them on
IRC.

Based on syslog2IRC_.

:Copyright: 2007-2020 `Jochen Kupperschmidt <http://homework.nwsnet.de/>`_
:License: MIT, see LICENSE for details.

.. _syslog2IRC: http://homework.nwsnet.de/releases/c474/#syslog2irc


Code Status
-----------

|badge_travis-ci_build|
|badge_scrutinizer-ci_coverage|
|badge_scrutinizer-ci_quality-score|

.. |badge_travis-ci_build| image:: https://travis-ci.org/homeworkprod/weitersager.svg?branch=main
   :alt: Build Status
   :target: https://travis-ci.org/homeworkprod/weitersager

.. |badge_scrutinizer-ci_coverage| image:: https://scrutinizer-ci.com/g/homeworkprod/weitersager/badges/coverage.png?b=main
   :alt: Scrutinizer Code Coverage
   :target: https://scrutinizer-ci.com/g/homeworkprod/weitersager/?branch=main

.. |badge_scrutinizer-ci_quality-score| image:: https://scrutinizer-ci.com/g/homeworkprod/weitersager/badges/quality-score.png?b=main
   :alt: Scrutinizer Code Quality
   :target: https://scrutinizer-ci.com/g/homeworkprod/weitersager/?branch=main


Requirements
------------

- Python 3.7+
- irc_
- blinker_

.. _irc: https://bitbucket.org/jaraco/irc
.. _blinker: http://pythonhosted.org/blinker/


Installation
------------

Weitersager and its dependencies can be installed via pip_:

.. code:: sh

    $ pip install weitersager

.. _pip: http://www.pip-installer.org/


Configuration
-------------

An example configuration file, ``example.toml``, in TOML_ format:

.. code:: toml

   [http]
   host = "127.0.0.1"         # optional
   port = 8080                # optional

   [irc.server]
   host = "irc.server.example"
   port = 6667                # optional
   password = "secret"        # optional

   [irc.bot]
   nickname = "Weitersager"
   realname = "Weitersager"   # optional

   [[irc.channels]]
   name = "#party"

   [[irc.channels]]
   name = "#secretlab"
   password = "555-secret"

.. _TOML: https://toml.io/


Usage
-----

Start Weitersager with a configuration file:

.. code:: sh

   $ weitersager example.toml

To send messages to IRC, send an HTTP POST request to URL path ``/`` at
the address and port the application is listening on.

The body has to be in JSON_ format and contain two keys, ``channel`` and
``text``, with string values:

.. code:: json

   {
     "channel": "#party",
     "text": "Oh yeah!"
   }

.. _JSON: https://www.json.org/


Shutdown
--------

In order to shut down Weitersager, send a query message with the text
``shutdown!`` to the IRC bot. It should then quit, and Weitersager
should exit.


A Note on Threads (Implementation Detail)
-----------------------------------------

This tool uses threads. Besides the main thread, there are two
additional threads: one for the message receiver and one for the IRC
bot. Both are configured to be daemon threads.

A Python application exits if no more non-daemon threads are running.

In order to exit Weitersager when shutdown is requested on IRC, the IRC
bot will call ``die()``, which will join the IRC bot thread. The main
thread and the (daemonized) message receiver thread remain.

Additionally, a dedicated signal is sent that sets a flag that causes
the main loop to stop. As the message receiver thread is the only one
left, but runs as a daemon, the application exits.

The dummy bot, on the other hand, does not run in a thread. The user
has to manually interrupt the application to exit.

For details, see the documentation on the ``threading`` module that is
part of Python's standard library.
