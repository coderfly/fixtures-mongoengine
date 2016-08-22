# -*- coding: utf-8 -*-
from fixtures_mongoengine import FixtureMixin
from tests.fixtures.fixture_post import FixturePost
from tests.fixtures.fixture_user import FixtureUser
from tests.models.user import User
from tests.test_case import MongoTestCase


class BaseFixtureMixinTestCase(MongoTestCase, FixtureMixin):

    def __init__(self, methodName='runTest'):
        super(BaseFixtureMixinTestCase, self).__init__(methodName)
        FixtureMixin.__init__(self)

    def setUp(self):
        super(BaseFixtureMixinTestCase, self).setUp()

        self.unload_fixtures()
        self.load_fixtures()


class SimpleUserMixinTestCase(BaseFixtureMixinTestCase):

    fixtures_conf = {
        'users': FixtureUser
    }

    def test_load(self):
        self.assertEqual(type(self.users), FixtureUser)


class SimplePostMixinTestCase(BaseFixtureMixinTestCase):
    fixtures_conf = {
        'posts': FixturePost
    }

    def test_load(self):
        self.assertEqual(type(self.posts), FixturePost)
