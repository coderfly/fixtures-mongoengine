# -*- coding: utf-8 -*-
from fixtures_mongoengine.fixtures import Fixture
from tests.models.user import User


class FixtureUser(Fixture):

    document_class = User

    data_file = 'tests.data.fixture_user'
