# -*- coding: utf-8 -*-
from fixtures_mongoengine import FixturesMixin
from tests.fixtures.fixture_post import FixturePost, FixturePostWithReference, FixturePostWrongDepended, FixturePostWrongRef
from tests.fixtures.fixture_user import FixtureUser
from tests.models.user import User
from tests.test_case import MongoTestCase


# class BaseMixinLoadFixtureTestCase(MongoTestCase, FixtureMixin):
#
#     def __init__(self, methodName='runTest'):
#         super(BaseMixinLoadFixtureTestCase, self).__init__(methodName)
#         FixtureMixin.__init__(self)
#
#     def setUp(self):
#         super(BaseMixinLoadFixtureTestCase, self).setUp()
#
#         self.unload_fixtures()
#         self.load_fixtures()


class MixinSimpleUserTestCase(MongoTestCase, FixturesMixin):

    fixtures_conf = {
        'users': FixtureUser
    }

    def test_load(self):
        self.assertEqual(type(self.users), FixtureUser)


class MixinPostTestCase(MongoTestCase):
    fixtures_conf = {
        'posts': FixturePost
    }

    def test_load(self):
        self.assertEqual(type(self.posts), FixturePost)


class MixinPostWithReferenceTestCase(MongoTestCase):
    fixtures_conf = {
        'posts': FixturePostWithReference
    }

    def test_load(self):
        self.assertEqual(type(self.posts), FixturePostWithReference)


class MixinPostWrongDependedTestCase(MongoTestCase):
    fixtures_conf = {
        'posts': FixturePostWrongDepended
    }

    def test_load(self):
        self.assertEqual(type(self.posts), FixturePost)


class MixinPostWrongRefTestCase(MongoTestCase):
    fixtures_conf = {
        'posts': FixturePostWrongRef
    }

    def test_load(self):
        self.assertEqual(type(self.posts), FixturePost)
