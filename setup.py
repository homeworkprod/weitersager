# -*- coding: utf-8 -*-

import codecs

from setuptools import setup


with codecs.open('README.rst', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='Weitersager',
    version='0.1',
    description='A proxy to forward messages received via HTTP to to IRC',
    long_description=long_description,
    author='Jochen Kupperschmidt',
    author_email='homework@nwsnet.de',
    url='http://homework.nwsnet.de/',
)
