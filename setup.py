#!/usr/bin/env python
from distutils.core import setup

setup(name='fixtures_mongoengine',
      version='1.0.0',
      description='MongoEngine Fixtures.',
      author='Vitaly Nikitin',
      url='https://github.com/coderfly/fixtures-mongoengine/',
      download_url='https://github.com/coderfly/fixtures-mongoengine/tarball/1.0.0',
      install_requires=['mongoengine>=0.8.6'],
      packages=['fixtures_mongoengine'],
      keywords=['testing', 'fixtures', 'mongoengine']
      )
