#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

__version__ = "0.6.1"

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

try:
    requirements = open('requirements.txt').readlines()
except FileNotFoundError:
    requirements = []

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

try:
    db_requirements = open('requirements.db.txt').readlines()
except FileNotFoundError:
    db_requirements = []

setup(
    author="Kyle Cribbs",
    author_email='kylecribbs@outlook.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
    ],
    description="Python client library for interfacing with RSA Archer.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='pyarcher',
    name='pyarcher',
    packages=find_packages(include=['pyarcher']),
    setup_requires=setup_requirements,
    extras_require={
        "db": db_requirements
    },
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/kylecribbs/pyarcher',
    version=__version__,
    zip_safe=False,
)
