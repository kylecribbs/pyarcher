# -*- coding: utf-8 -*-

"""Top-level package for RSA Archer Client Library."""
from pyarcher.archer import Archer
try:
    from ._db import *
except ImportError as exception:
    print(exception)
    pass

__author__ = """Kyle Cribbs"""
__email__ = 'kylecribbs@outlook.com'
__version__ = '0.6.0'
__all__ = ["Archer"]

name = "pyarcher"
