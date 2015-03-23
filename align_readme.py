#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Copy the docstring of the main module to the README file."""

import weitersager


with open('README.rst', 'w') as f:
    text = weitersager.__doc__.strip()
    f.write(text + '\n')
