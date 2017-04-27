# -*- coding: utf-8 -*-
from mongoengine import ValidationError

from fixtures_mongoengine import FixturesMongoengineException
from tests.fixtures.fixture_post import (
    FixturePost, FixturePostWithReference, FixturePostWrongDepended,
    FixturePostWrongRefFormat, FixturePostWrongRef, FixturePostWithEmbedded
)
from tests.fixtures.fixture_user import FixtureUser, FixtureUserInvalidData
from tests.models.user import User
from tests.test_case import MongoWithClearTestCase


class LoadFixtureTestCase(MongoWithClearTestCase):

    def test_fixture_without_dependencies(self):

        fixture = FixtureUser()
        fixture.load()

        self.assertEqual(fixture['user1'].first_name, 'Joyce')
        self.assertEqual(fixture['user2'].first_name, 'Amy')

        user1 = User.objects(first_name='Joyce').first()
        self.assertIsNotNone(user1)
        self.assertEqual(user1.last_name, 'Ray')

    def test_fixture_with_dependencies(self):
        fixture_user = FixtureUser()
        fixture_post = FixturePost()
        fixture_post.init_depended_fixtures({FixtureUser: fixture_user})
        fixture_user.load()
        fixture_post.load()

        self.assertEqual(fixture_post['post1'].author, fixture_user['user1'].pk)

    def test_fixture_with_reference_dependencies(self):
        fixture_user = FixtureUser()
        fixture_post = FixturePostWithReference()
        fixture_post.init_depended_fixtures({FixtureUser: fixture_user})
        fixture_user.load()
        fixture_post.load()

        self.assertIsInstance(fixture_post['post1'].author, User)
        self.assertEqual(fixture_post['post1'].author.pk, fixture_user['user1'].pk)

    def test_fixture_with_embedded_dependencies(self):
        fixture_user = FixtureUser()
        fixture_post = FixturePostWithEmbedded()
        fixture_post.init_depended_fixtures({FixtureUser: fixture_user})
        fixture_user.load()
        fixture_post.load()

        self.assertEqual(fixture_post['post1'].author.id, fixture_user['user1'].pk)

    def test_fixture_with_wrong_dependency(self):
        fixture_user = FixtureUser()
        fixture_post = FixturePostWrongDepended()
        fixture_post.init_depended_fixtures({FixtureUser: fixture_user})
        fixture_user.load()

        with self.assertRaises(FixturesMongoengineException) as cm:
            fixture_post.load()
        self.assertRegexpMatches(cm.exception.message, 'not fount in depended fixtures')

    def test_fixture_with_wrong_ref_format(self):
        fixture_user = FixtureUser()
        fixture_post = FixturePostWrongRefFormat()
        fixture_post.init_depended_fixtures({FixtureUser: fixture_user})
        fixture_user.load()

        with self.assertRaises(FixturesMongoengineException) as cm:
            fixture_post.load()
        self.assertRegexpMatches(cm.exception.message, 'Wrong depend reference')

    def test_fixture_with_wrong_ref(self):
        fixture_user = FixtureUser()
        fixture_post = FixturePostWrongRef()
        fixture_post.init_depended_fixtures({FixtureUser: fixture_user})
        fixture_user.load()

        with self.assertRaises(FixturesMongoengineException) as cm:
            fixture_post.load()
        self.assertRegexpMatches(cm.exception.message, 'Model .* not fount in depended fixture')

    def test_fixture_skip_init_depended(self):
        fixture_post = FixturePost()

        with self.assertRaises(FixturesMongoengineException) as cm:
            fixture_post.load()
        self.assertRegexpMatches(cm.exception.message, 'Depended fixture .* wasn\'t created')

    def test_fixture_skip_depended_load(self):
        fixture_user = FixtureUser()
        fixture_post = FixturePost()
        fixture_post.init_depended_fixtures({FixtureUser: fixture_user})

        with self.assertRaises(FixturesMongoengineException) as cm:
            fixture_post.load()
        self.assertRegexpMatches(cm.exception.message, 'Depended fixture .* wasn\'t loaded')


class UnloadFixtureTestCase(MongoWithClearTestCase):

    def test_unload(self):

        fixture = FixtureUser()
        fixture.load()
        fixture.unload()

        with self.assertRaises(KeyError):
            print(fixture['user1'].first_name)

        user1 = User.objects(first_name='Joyce').first()
        self.assertIsNone(user1)


class UserFixtureInvalidDataTestCase(MongoWithClearTestCase):

    def test_load(self):
        fixture = FixtureUserInvalidData()
        self.assertRaises(ValidationError, fixture.load)
