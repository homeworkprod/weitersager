Weitersager Changelog
=====================


Version 0.2
-----------

Unreleased

- Raised minimum Python version to 3.7.
- HTTP protocol was changed: only a single channel is allowed per
  message.
- Divided code base into separate modules in a package.
- Dependency versions have been pinned.
- Updated irc version to 19.0.1 (from 12.3).
- Updated blinker to 1.4 (from 1.3).
- Do not use tox for tests anymore.
- Use `dataclass` instead of `namedtuple` for value objects.
- Allowed for custom shutdown predicate.


Version 0.1
-----------

Released 2015-04-24 at LANresort 2015

- First official release
