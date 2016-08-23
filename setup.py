#!/usr/bin/env python
from distutils.core import setup

setup(name='fixtures_mongoengine',
      version='0.1',
      description='MongoEngine Fixtures.',
      author='Vitaly Nikitin',
      url='https://github.com/coderfly/fixtures-mongoengine/',
      install_requires=['mongoengine>=0.8.6'],
      packages=['fixtures_mongoengine'],
      keywords=['testing', 'fixtures']
      )
