# -*- coding: utf-8 -*-
from fixtures_mongoengine import Fixture
from tests.models.user import User


class FixtureUser(Fixture):

    document_class = User

    data_file = 'tests.data.fixture_user'


class FixtureUserInvalidData(FixtureUser):

    attr_name = 'fixture_data_invalid'
