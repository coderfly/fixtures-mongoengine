# -*- coding: utf-8 -*-

from fixtures_mongoengine import Fixture
from tests.fixtures.fixture_user import FixtureUser
from tests.models.post import Post, PostWithReference


class FixturePost(Fixture):
    document_class = Post

    depends = {
        'users': FixtureUser
    }

    data_file = 'tests.data.fixture_post'


class FixturePostWithReference(Fixture):
    document_class = PostWithReference

    depends = {
        'users': FixtureUser
    }

    data_file = 'tests.data.fixture_post'


class FixturePostWrongDepended(Fixture):
    document_class = Post

    depends = {
        'wrong_users': FixtureUser
    }

    data_file = 'tests.data.fixture_post'


class FixturePostWrongRefFormat(Fixture):
    document_class = Post

    depends = {
        'users': FixtureUser
    }

    data_file = 'tests.data.fixture_post'

    attr_name = 'fixture_data_wrong_ref_format'


class FixturePostWrongRef(Fixture):
    document_class = Post

    depends = {
        'users': FixtureUser
    }

    data_file = 'tests.data.fixture_post'

    attr_name = 'fixture_data_wrong_ref'
