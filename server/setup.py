__author__ = 'Radu'

#!/usr/bin/env python
from distutils.core import setup

setup(name='Crossco',
      version='1.0',
      description='Crossco Interconnect Platform',
      author='Ice Breakers',
      url='http://crossco.org',
      packages=['crossco'],
      install_requires=['flask',
                        'flask-login',
                        'flask-oauth',
                        'flask-restless',
                        'flask-sqlalchemy',
                        'facebook',
                        'oauth']
)