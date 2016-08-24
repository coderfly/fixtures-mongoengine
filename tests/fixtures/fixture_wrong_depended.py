# -*- coding: utf-8 -*-
from fixtures_mongoengine import Fixture, FixturesMixin
from tests.models.user import User


class FixtureWrongDependedClass(Fixture):
    document_class = User

    depends = {
        'circular': 'FixtureWrongClass'
    }


class FixtureWrongDependedClassMixin(FixturesMixin):
    fixtures_conf = {
        'wrong_depended': FixtureWrongDependedClass
    }
