# -*- coding: utf-8 -*-
from fixtures_mongoengine import Fixture
from fixtures_mongoengine import FixturesMixin
from tests.models.simple import Simple


class FixtureCircular(Fixture):
    document_class = Simple

    depends = {
        'circular': 'FixtureCircular2'
    }


class FixtureCircular2(Fixture):
    document_class = Simple

    depends = {
        'circular': FixtureCircular
    }


class FixtureCircularMixin(FixturesMixin):
    fixtures_conf = {
        'circular': FixtureCircular
    }



