Weitersager Changelog
=====================


Version 0.3
-----------

Released 2020-09-16

- Introduced TOML-based configuration file.

  - Added dependency on rtoml 0.3.0.

  - Moved IRC channel configuration from Python code to configuration
    file.

  - Moved IRC server and bot name configuration from command line
    arguments to configuration file.

  - Moved HTTP receiver configuration from command line arguments to
    configuration file.

  - Made configuration filename a required command line argument.

- Turned the stray run script into an actual entry point console script.

- Added support for IRC server password.

- Added optional HTTP authorization via API tokens.


Version 0.2
-----------

Released 2020-09-13

- Raised minimum Python version to 3.7.

- HTTP protocol was changed:

  - Only a single channel is allowed per message.

  - Response code for successful submit was changed from 200 (OK) to
    more appropriate 202 (Accepted).

- Divided code base into separate modules in a package.

- Switch to a ``src/`` layout.

- Dependency versions have been pinned.

- Updated irc version to 19.0.1 (from 12.3).

- Updated blinker to 1.4 (from 1.3).

- Do not use tox for tests anymore.

- Use ``dataclass`` instead of ``namedtuple`` for value objects.

- Allowed for custom shutdown predicate.


Version 0.1
-----------

Released 2015-04-24 at LANresort 2015

- First official release
