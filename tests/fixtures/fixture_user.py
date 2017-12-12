# -*- coding: utf-8 -*-
import datetime

from fixtures_mongoengine import Fixture
from tests.models.user import User


class FixtureUser(Fixture):

    document_class = User

    data_file = 'tests.data.fixture_user'


class FixtureUserWithInlineData(Fixture):

    document_class = User

    data = {
        'user1': {
            'first_name': 'Joyce',
            'last_name': 'Ray',
            'email': 'jray0@quantcast.com',
            'birthday': datetime.date(1983, 7, 12)
        },
        'user2': {
            'first_name': 'Amy',
            'last_name': 'Myers',
            'email': 'amyers1@live.com',
            'birthday': datetime.date(1987, 11, 27)
        }
    }


class FixtureUserInvalidData(FixtureUser):

    attr_name = 'fixture_data_invalid'
