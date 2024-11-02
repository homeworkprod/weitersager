Changelog
=========


0.11 (unreleased)
-----------------

- Updated Werkzeug to 3.1.1 (from 3.0.4).

- Updated coverage to 7.6.4 (from 7.4.4).

- Updated mypy to 1.13.0 (from 1.9.0).

- Updated ruff to 0.7.2 (from 0.4.1).

- Use uv as package and project manager.

- Manage development, test dependencies via dependency groups and uv.

- Removed `requirements[-{dev, test}].txt` files. Use uv to install
  dependencies.


0.10 (2024-09-30)
-----------------

- Added support for Python 3.11 and 3.12.

- Removed support for Python 3.7 and 3.8.

- Changed authentication scheme name in authorization header from custom
  ``Token`` to the common ``Bearer``.

- Updated blinker to 1.8.2 (from 1.4).

- Updated irc to 20.5.0 (from 20.0.0).

- Updated rtoml to 0.11.0 (from 0.7.1).

- Updated Werkzeug to 3.0.4 (from 2.1.2).

- Renamed ``docker-compose.yaml`` to ``compose.yaml``.

- Switched from Python 3.9 to Python 3.11 Docker base image.

- Publish Docker images for platform ``linux/arm64`` (in addition to
  ``linux/amd64``).

- Migrated project metadata from ``setup.cfg`` to ``pyproject.toml``.

- Changed build system from setuptools to Hatchling.

- Switched code formatter and linter from Black to Ruff.


0.9 (2022-05-07)
----------------

- Introduced alternative endpoints using secret "channel tokens" as part
  of the URL.


0.8.1 (2022-05-05)
------------------

- Fixed Werkzeug dependency missing in ``setup.cfg``.


0.8 (2022-05-04)
----------------

- Recreated HTTP server as a WSGI application, built with Werkzeug and
  served by wsgiref.

- Return status code 415 ("Unsupported Media Type") if request content
  type is not ``application/json``.


0.7.2 (2022-05-03)
------------------

- Return status code 404 ("Not Found") on requests to any path other
  than ``/``.

- Added Docker-specific configuration file example.

- Added configuration file for Docker Compose.


0.7.1 (2022-04-27)
------------------

- Changed application path in Docker container from ``/home/user`` to
  ``/app``. This is relevant when mounting the configuration file into the
  container.


0.7 (2022-04-26)
----------------

- Added support for Python 3.10.

- Expect config file to be mounted into Docker container.

- Use non-inline array of tables for IRC channels in TOML configuration
  examples.

- Reintroduce announcer as abstraction.

- Updated irc version to 20.0.0 (from 19.0.1).

- Updated rtoml to 0.7.1 (from 0.6.1).


0.6 (2021-05-07)
----------------

- Switched to using Python's logging mechanism directly, with different
  log levels. Removed function ``util.log``.

- Made the application's log level configurable.

- Enabled threading for the HTTP server to reduce blocking.

- Introduced an internal queue to decouple reception of HTTP requests
  from announcing messages on IRC.

- Added support for custom IRC commands to send after connecting
  (authentication, cloaking, flood protection, etc.).

- Updated rtoml to 0.6.1 (from 0.5.0).


0.5 (2021-02-07)
----------------

- Added support for Python 3.9.

- Added support for SSL connections to IRC servers.

- Changed prefix of authorization header value from ``WTRSGR`` to less
  awkward ``Token``.

- Removed handler to shut down Weitersager via private IRC message. It
  doesn't provide enough relevant value.

- Added command line option ``--version`` to show Weitersager's version.

- Updated rtoml to 0.5.0 (from 0.4.0).

- Include tests and other useful files in source distribution archive.


0.4 (2020-10-11)
----------------

- Added command line tool to generate secure tokens (which can be used as
  API tokens).

- Allow to configure a rate limit for the IRC connection, i.e. the maximum
  number of messages per second to send. This can prevent the bot from
  getting kicked (or even banned) from a channel because of flooding.

- Added exemplary Dockerfile.

- Added type hints.

- Updated rtoml to 0.4.0 (from 0.3.0).


0.3 (2020-09-16)
----------------

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


0.2 (2020-09-13)
----------------

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


0.1 (2015-04-24)
----------------

- First official release (at LANresort 2015)
