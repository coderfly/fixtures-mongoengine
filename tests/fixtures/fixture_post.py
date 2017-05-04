# -*- coding: utf-8 -*-

from fixtures_mongoengine import Fixture
from tests.fixtures.fixture_user import FixtureUser
from tests.models.post import Post, PostWithReference, PostWithEmbedded, PostWithList


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


class FixturePostWithEmbedded(Fixture):
    document_class = PostWithEmbedded

    depends = {
        'users': FixtureUser
    }

    data_file = 'tests.data.fixture_post'

    attr_name = 'fixture_data_embedded'


class FixturePostWithList(Fixture):
    document_class = PostWithList

    depends = {
        'users': FixtureUser
    }

    data_file = 'tests.data.fixture_post'

    attr_name = 'fixture_data_list'


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
