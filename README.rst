===========
Weitersager
===========

.. image:: https://raw.githubusercontent.com/homeworkprod/weitersager/main/assets/weitersager_logo.svg
   :alt: Weitersager logo
   :height: 200
   :width: 200

A proxy that receives text messages via JSON over HTTP and shows them on
IRC.

Based on syslog2IRC_.

:Copyright: 2007-2021 `Jochen Kupperschmidt <http://homework.nwsnet.de/>`_
:License: MIT, see LICENSE for details.

.. _syslog2IRC: http://homework.nwsnet.de/releases/c474/#syslog2irc


Code Status
===========

|badge_travis-ci_build|
|badge_scrutinizer-ci_coverage|
|badge_scrutinizer-ci_quality-score|
|badge_code-climate_maintainability|

.. |badge_travis-ci_build| image:: https://travis-ci.org/homeworkprod/weitersager.svg?branch=main
   :alt: Build Status
   :target: https://travis-ci.org/homeworkprod/weitersager

.. |badge_scrutinizer-ci_coverage| image:: https://scrutinizer-ci.com/g/homeworkprod/weitersager/badges/coverage.png?b=main
   :alt: Scrutinizer Code Coverage
   :target: https://scrutinizer-ci.com/g/homeworkprod/weitersager/?branch=main

.. |badge_scrutinizer-ci_quality-score| image:: https://scrutinizer-ci.com/g/homeworkprod/weitersager/badges/quality-score.png?b=main
   :alt: Scrutinizer Code Quality
   :target: https://scrutinizer-ci.com/g/homeworkprod/weitersager/?branch=main

.. |badge_code-climate_maintainability| image:: https://api.codeclimate.com/v1/badges/f45b29ee321c1920a85c/maintainability
   :alt: Code Climate
   :target: https://codeclimate.com/github/homeworkprod/weitersager


Requirements
============

- Python 3.7+
- Dependencies: blinker_, irc_, rtoml_

.. _blinker: http://pythonhosted.org/blinker/
.. _irc: https://bitbucket.org/jaraco/irc
.. _rtoml: https://github.com/samuelcolvin/rtoml


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

    $ weitersager config.toml


Configuration
-------------

Configuration is done as a file in TOML_ format.

A very basic configuration is very short. By default, the HTTP server
runs on port 8080 on ``localhost``. All that needs to be specified are
the IRC server host, bot nickname, and channel(s) to join.

.. code:: toml

    [irc.server]
    host = "irc.server.example"

    [irc.bot]
    nickname = "Weitersager"

    [irc]
    channels = [
      { name = "#lobby" },
    ]

A lot more can be configured, though:

.. code:: toml

    log_level = "debug"         # optional

    [http]
    host = "127.0.0.1"          # optional
    port = 8080                 # optional
    api_tokens = [ "123xyz" ]   # optional

    [irc.server]
    host = "irc.server.example"
    port = 6667                 # optional
    ssl = false                 # optional
    password = "secret"         # optional
    rate_limit = 0.5            # optional; limit of messages per second

    [irc.bot]
    nickname = "Weitersager"
    realname = "Weitersager"    # optional

    [irc]
    commands = [                # optional
      "MODE Weitersager +i",
    ]
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
configured. A command line tool is provided to generate secure tokens:

.. code:: sh

    $ weitersager-token
    e72CbijlYLqjaRIv0uMNBpgZKl397FEp-Y8PNEXn5vM

Multiple API tokens can be configured so that each legitimate client
can be given its own token which can than be revoked (by removing it
from the configuration, and restarting) individually.

Header format:

.. code:: http

    Authorization: Token <a token of your choosing>

Example authorization header:

.. code:: http

    Authorization: Token e72CbijlYLqjaRIv0uMNBpgZKl397FEp-Y8PNEXn5vM

Example HTTPie_ call with authorization header:

.. code:: sh

    $ http --json post :8080 Authorization:'Token e72CbijlYLqjaRIv0uMNBpgZKl397FEp-Y8PNEXn5vM' channel='#party' text='Oh yeah!'

Note that Weitersager itself only uses unencrypted HTTP, so the API
tokens are passed in the clear. That might suffice if you run it on the
same host as the HTTP clients. Otherwise you might want to look into
hiding Weitersager behind a web server or proxy that can add TLS
encryption.


Implementation Details
======================


A Note on Threads
-----------------

This tool uses threads. Besides the main thread, there are two
additional threads: one for the message receiver and one for the IRC
bot. Both are configured to be daemon threads.

The dummy bot, on the other hand, does not run in a thread.

A Python application exits if no more non-daemon threads are running.

The user has to manually interrupt the application to exit.

For details, see the documentation on the ``threading`` module that is
part of Python's standard library.
