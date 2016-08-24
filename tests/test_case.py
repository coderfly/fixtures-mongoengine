# -*- coding: utf-8 -*-
from unittest import TestCase

from mongoengine import connect

from fixtures_mongoengine import FixturesMixin


class MongoTestCase(TestCase):
    """
    TestCase class that clear the collection between the tests
    """

    def __init__(self, methodName='runTest'):
        self.db = connect('fixtures_mongoengine_test')['fixtures_mongoengine_test']
        super(MongoTestCase, self).__init__(methodName)


class MongoWithClearTestCase(MongoTestCase):

    def tearDown(self):
        super(MongoTestCase, self).tearDown()
        for collection in self.db.collection_names():
            if collection == 'system.indexes':
                continue

            self.db.drop_collection(collection)


class MongoFixturesTestCase(MongoTestCase, FixturesMixin):
    pass
