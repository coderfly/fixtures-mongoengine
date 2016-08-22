# -*- coding: utf-8 -*-

from fixtures_mongoengine import Fixture
from tests.fixtures.fixture_user import FixtureUser
from tests.models.post import Post


class FixturePost(Fixture):

    document_class = Post

    depends = {
        'users': FixtureUser
    }

    data_file = 'tests.data.fixture_post'
