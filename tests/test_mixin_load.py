# -*- coding: utf-8 -*-
import six

from fixtures_mongoengine import FixturesMongoengineException
from tests.fixtures.fixture_circular import FixtureCircularMixin
from tests.fixtures.fixture_inner_dependent import FixtureInnerDependentMixin, FixtureInnerMain, FixtureInnerLevel1, \
    FixtureInnerLevel2
from tests.fixtures.fixture_post import FixturePost
from tests.fixtures.fixture_user import FixtureUser
from tests.fixtures.fixture_wrong_depended import FixtureWrongDependedClassMixin
from tests.test_case import MongoFixturesTestCase, MongoWithClearTestCase


class SimpleFixturesTestCase(MongoFixturesTestCase):

    fixtures_conf = {
        'users': FixtureUser
    }

    def test_load(self):

        self.assertEqual(type(self.users), FixtureUser)


class DependedFixturesTestCase(MongoFixturesTestCase):
    fixtures_conf = {
        'posts': FixturePost
    }

    def test_load(self):
        self.assertEqual(type(self.posts), FixturePost)


class CreateFixturesTestCase(MongoWithClearTestCase):

    def test_circular(self):

        mixin = FixtureCircularMixin()

        with self.assertRaises(FixturesMongoengineException) as cm:
            mixin.get_fixtures()
        self.assertRegexpMatches(cm.exception.message, 'A circular dependency is detected for fixture')

    def test_missing_depended_class(self):

        mixin = FixtureWrongDependedClassMixin()
        with self.assertRaises(FixturesMongoengineException) as cm:
            mixin.get_fixtures()
        self.assertRegexpMatches(cm.exception.message, 'has not been registered in the fixture registry')

    def test_inner_dependent(self):

        mixin = FixtureInnerDependentMixin()
        fixtures = mixin.get_fixtures()

        iterator = six.itervalues(fixtures)
        self.assertEqual(type(next(iterator)), FixtureInnerLevel2)
        self.assertEqual(type(next(iterator)), FixtureInnerLevel1)
        self.assertEqual(type(next(iterator)), FixtureInnerMain)
