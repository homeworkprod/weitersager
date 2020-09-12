import codecs

from setuptools import setup


def read_lines_from_file(filename):
    with codecs.open(filename, encoding='utf-8') as f:
        return [line.rstrip('\n') for line in f]


long_description = read_lines_from_file('README.rst')
requirements = read_lines_from_file('requirements.txt')


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
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Communications :: Chat :: Internet Relay Chat',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: System :: Logging',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
    packages=['weitersager'],
    install_requires=requirements,
)
