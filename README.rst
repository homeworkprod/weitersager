===========
Weitersager
===========

Receive messages via HTTP and show them on IRC.

Based on syslog2IRC_.


Requirements
------------

- Python 3.4+ (tested with 3.4.2)
- irc_ (tested with 12.1.1)
- blinker_ (tested with 1.3)


Installation
------------

irc_ and blinker_ can be installed via pip_:

.. code:: sh

    $ pip install irc blinker

In order to shut down Weitersager, send a query message with the text
"shutdown!" to the IRC bot. It should then quit, and Weitersager should
exit.


.. _syslog2IRC:  http://homework.nwsnet.de/releases/c474/#syslog2irc
.. _irc:         https://bitbucket.org/jaraco/irc
.. _blinker:     http://pythonhosted.org/blinker/
.. _pip:         http://www.pip-installer.org/


:Copyright: 2007-2015 `Jochen Kupperschmidt <http://homework.nwsnet.de/>`_
:Date: 19-Apr-2015
:License: MIT, see LICENSE for details.
:Version: 0.0
