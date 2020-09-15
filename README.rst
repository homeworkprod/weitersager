===========
Weitersager
===========

A proxy that receives text messages via JSON over HTTP and shows them on
IRC.

Based on syslog2IRC_.

:Copyright: 2007-2020 `Jochen Kupperschmidt <http://homework.nwsnet.de/>`_
:License: MIT, see LICENSE for details.

.. _syslog2IRC: http://homework.nwsnet.de/releases/c474/#syslog2irc


Code Status
===========

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
============

- Python 3.7+
- irc_
- blinker_

.. _irc: https://bitbucket.org/jaraco/irc
.. _blinker: http://pythonhosted.org/blinker/


Installation
============

Weitersager and its dependencies can be installed via pip_:

.. code:: sh

    $ pip install weitersager

.. _pip: http://www.pip-installer.org/


Usage
=====

Start Weitersager with a configuration file:

.. code:: sh

   $ weitersager example.toml


Configuration
-------------

An example configuration file, ``example.toml``, in TOML_ format:

.. code:: toml

   [http]
   host = "127.0.0.1"         # optional
   port = 8080                # optional
   api_tokens = [ "123xyz" ]  # optional

   [irc.server]
   host = "irc.server.example"
   port = 6667                # optional
   password = "secret"        # optional

   [irc.bot]
   nickname = "Weitersager"
   realname = "Weitersager"   # optional

   [irc]
   channels = [
       { name = "#party" },
       { name = "#secretlab", password = "555-secret" },
   ]

.. _TOML: https://toml.io/


IRC Dummy Mode
--------------

If no value for ``irc.server.host`` is set, Weitersager will not attempt
to connect to an IRC server and start in IRC dummy mode. It will still
accept messages, but it will write them to STDOUT. This can be useful
for testing.


HTTP API
--------

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

Example HTTPie_ call to send a message to Weitersager on localhost, port 8080:

.. code:: sh

   $ http --json post :8080 channel='#party' text='Oh yeah!'

.. _HTTPie: https://httpie.org/


Authorization
~~~~~~~~~~~~~

To protect the HTTP API a bit, requests can be required to include an
authorization header with a valid token to be accepted.

The authorization check becomes active if at least one API token is
configured.

Multiple API tokens can be configured so that each legitimate client
can be given its own token which can than be revoked (by removing it
from the configuration, and restarting) individually.

Header format:

.. code:: http

   Authorization: WTRSGR <a token of your choosing>

Example authorization header:

.. code:: http

   Authorization: WTRSGR e72CbijlYLqjaRIv0uMNBpgZKl397FEp-Y8PNEXn5vM

Example HTTPie_ call with authorization header:

.. code:: sh

   $ http --json post :8080 Authorization:'WTRSGR e72CbijlYLqjaRIv0uMNBpgZKl397FEp-Y8PNEXn5vM' channel='#party' text='Oh yeah!'

Note that Weitersager itself only uses unencrypted HTTP, so the API
tokens are passed in the clear. That might suffice if you run it on the
same host as the HTTP clients. Otherwise you might want to look into
hiding Weitersager behind a web server or proxy that can add TLS
encryption.


Implementation Details
======================


Shutdown
--------

Weitersager can be modified so that it can be shut down via private IRC
message.

This can be useful for testing, when external auto-restart is set up, or
as a starting point to implement custom private message handling.

To enable it, pass keyword argument
``shutdown_predicate=default_shutdown_predicate`` to the constructor of
``weitersager.irc.Bot``. If enabled, in order to shut down Weitersager,
send a query message with the text ``shutdown!`` to the IRC bot. The bot
should then quit, and Weitersager should exit.


A Note on Threads
-----------------

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
