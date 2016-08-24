# -*- coding: utf-8 -*-
from fixtures_mongoengine import Fixture
from fixtures_mongoengine import FixturesMixin
from tests.models.circular import Circular


class FixtureCircular(Fixture):
    document_class = Circular

    depends = {
        'circular': 'FixtureCircular2'
    }


class FixtureCircular2(Fixture):
    document_class = Circular

    depends = {
        'circular': FixtureCircular
    }


class FixtureCircularMixin(FixturesMixin):
    fixtures_conf = {
        'circular': FixtureCircular
    }



