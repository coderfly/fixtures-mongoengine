# -*- coding: utf-8 -*-
from collections import OrderedDict

import six

from fixtures_mongoengine import FixturesMongoengineException
from fixtures_mongoengine.fixture import Fixture


class FixtureMixin(object):

    fixtures_conf = []
    """
    Declares the fixtures that are needed by the current test case.
    The return value of this method must be an array of fixture configurations. For example,
    ```python
    [
        'users' => UserFixture,
        'articles' => ArticleFixture
    ]
    ```
    """

    def __init__(self):
        super(FixtureMixin, self).__init__()
        self.__fixtures = None

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]

        if name in self.get_fixtures():
            return self.get_fixtures()[name]

        return super(FixtureMixin, self).__getattribute__(name)

    def load_fixtures(self):

        for fixture in self.get_fixtures().values():
            fixture.before_load()

        for fixture in self.get_fixtures().values():
            fixture.load()

        fixtures = self.get_fixtures().values()
        fixtures.reverse()
        for fixture in fixtures:
            fixture.after_load()

    def unload_fixtures(self):

        for fixture in self.get_fixtures().values():
            fixture.before_unload()

        fixtures = self.get_fixtures().values()
        fixtures.reverse()
        for fixture in fixtures:
            fixture.unload()

        for fixture in fixtures:
            fixture.unload()

    def get_fixtures(self):
        """
        :rtype: OrderedDict[Fixture]
        """
        if self.__fixtures is None:
            self.__fixtures = self._create_fixtures()

        return self.__fixtures

    def _create_fixtures(self):
        aliases = {}
        for name, fixture_class in six.iteritems(self.fixtures_conf):
            aliases[fixture_class] = name

        instances = {}
        stack = [fixture_class for name, fixture_class in six.iteritems(self.fixtures_conf)]
        stack.reverse()
        while len(stack) > 0:
            fixture = stack.pop()
            if isinstance(fixture, Fixture):
                fixture_class = fixture.__class__
                if fixture_class in instances:
                    del instances[fixture_class]
                instances[fixture_class] = fixture
            else:
                fixture_class = fixture
                if fixture_class not in instances:
                    instances[fixture_class] = None
                    fixture = fixture_class()
                    stack.append(fixture)
                    for dep in fixture.depends.values():
                        stack.append(dep)
                elif instances[fixture_class] is None:
                    msg = 'A circular dependency is detected for fixture {}.'.format(fixture_class.__name__)
                    raise FixturesMongoengineException(msg)

        fixtures = {}
        for fixture_class, fixture in six.iteritems(instances):
            fixture.init_depend_fixtures(instances)
            name = aliases[fixture_class] if fixture_class in aliases else fixture_class.__name__
            fixtures[name] = fixture

        return fixtures
