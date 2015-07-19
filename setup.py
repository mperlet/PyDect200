#!/usr/bin/env python

from distutils.core import setup
from PY_DECT200 import PY_DECT200

setup(name='PY_DECT200',
      version=PY_DECT200.__version__,
      description=PY_DECT200.__description__,
      author=PY_DECT200.__author__,
      author_email=PY_DECT200.__author_email__,
      url='https://github.com/mperlet/PY_DECT200',
      packages=['PY_DECT200'],
      keywords = ['avm', 'dect200', 'fritzbox', 'dect', 'switch', 'smart home'], 
     )
