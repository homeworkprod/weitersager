import codecs

from setuptools import setup


with codecs.open('README.rst', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='Weitersager',
    version='0.2-dev',
    description='A proxy to forward messages received via HTTP to to IRC',
    long_description=long_description,
    url='http://homework.nwsnet.de/releases/1cda/#weitersager',
    author='Jochen Kupperschmidt',
    author_email='homework@nwsnet.de',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Other Audience',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Topic :: Communications :: Chat :: Internet Relay Chat',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: System :: Logging',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
    packages=['weitersager'],
    install_requires=[
        'blinker==1.3',
        'irc==12.3',
    ],
    extras_require={
        'test': ['nose2', 'tox'],
    },
)
