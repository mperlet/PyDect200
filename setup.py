#!/usr/bin/env python

from distutils.core import setup
from PyDect200 import PyDect200
try:
    PyDect200.__version__
except:
    PyDect200 = PyDect200.PyDect200

setup(name='PyDect200',
      version=PyDect200.__version__,
      description=PyDect200.__description__,
      author=PyDect200.__author__,
      author_email=PyDect200.__author_email__,
      url='https://github.com/mperlet/PyDect200',
      packages=['PyDect200'],
      keywords = ['avm', 'dect200', 'fritzbox', 'dect', 'switch', 'smart home', 'PowerLine 546E'],
     )
