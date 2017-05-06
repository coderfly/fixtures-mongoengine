# -*- coding: utf-8 -*-
from fixtures_mongoengine import Fixture
from fixtures_mongoengine import FixturesMixin
from tests.models.simple import Simple


class FixtureInnerLevel2(Fixture):
    document_class = Simple

    data_file = 'tests.data.fixture_simple'


class FixtureInnerLevel1(Fixture):
    document_class = Simple

    depends = {
        'level2': FixtureInnerLevel2
    }

    data_file = 'tests.data.fixture_simple'


class FixtureInnerMain(Fixture):
    document_class = Simple

    depends = {
        'level1': FixtureInnerLevel1
    }

    data_file = 'tests.data.fixture_simple'


class FixtureInnerDependentMixin(FixturesMixin):
    fixtures_conf = {
        'main': FixtureInnerMain
    }
