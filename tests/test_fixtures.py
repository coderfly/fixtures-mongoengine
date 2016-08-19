# -*- coding: utf-8 -*-
from tests.fixtures.fixture_user import FixtureUser
from tests.models.user import User
from tests.test_case import MongoTestCase


class SimpleUserFixtureTestCase(MongoTestCase):

    def test_load(self):

        fixture = FixtureUser()
        fixture.load()

        self.assertEqual(fixture.data['user1'].first_name, 'Joyce')
        self.assertEqual(fixture.data['user2'].first_name, 'Amy')

        user1 = User.objects(first_name='Joyce').first()
        self.assertIsNotNone(user1)
        self.assertEqual(user1.last_name, 'Ray')


    def test_unload(self):
        fixture = FixtureUser()
        fixture.load()
        fixture.unload()




