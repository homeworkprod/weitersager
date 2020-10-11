"""
weitersager.tokencli
~~~~~~~~~~~~~~~~~~~~

Command line tool to generate secret tokens

:Copyright: 2007-2020 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from secrets import token_urlsafe


def generate_token():
    """Generate an random, secure, URL-safe token."""
    return token_urlsafe()


def main():
    """Write a secure token to STDOUT."""
    token = generate_token()
    print(token)


if __name__ == '__main__':
    main()