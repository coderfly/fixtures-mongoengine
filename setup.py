#!/usr/bin/env python
from setuptools import setup
from fixtures_mongoengine import __version__

setup(name='fixtures_mongoengine',
      version=__version__,
      description='MongoEngine Fixtures.',
      author='Vitaly Nikitin',
      author_email='alaris.nik@gmail.com',
      url='https://github.com/coderfly/fixtures-mongoengine/',
      download_url='https://github.com/coderfly/fixtures-mongoengine/tarball/'+__version__,
      install_requires=['mongoengine>=0.8.6'],
      packages=['fixtures_mongoengine'],
      keywords=['testing', 'fixtures', 'mongoengine']
      )
