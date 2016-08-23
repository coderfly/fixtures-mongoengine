# -*- coding: utf-8 -*-
from collections import OrderedDict

import six

from fixtures_mongoengine import FixturesMongoengineException
from fixtures_mongoengine.fixture import Fixture
from fixtures_mongoengine.utils import can_persist_fixtures

"""
Metaclass idea and parts of code taken from https://github.com/croach/Flask-Fixtures
"""

CLASS_SETUP_NAMES = ('setUpClass', 'setup_class', 'setup_all', 'setupClass', 'setupAll', 'setUpAll')
CLASS_TEARDOWN_NAMES = (
    'tearDownClass', 'teardown_class', 'teardown_all',
    'teardownClass', 'teardownAll', 'tearDownAll'
)
TEST_SETUP_NAMES = ('setUp',)
TEST_TEARDOWN_NAMES = ('tearDown',)


def setup(obj):
    """
    :type obj: FixturesMixin
    """
    obj.load_fixtures()


def teardown(obj):
    """
    :type obj: FixturesMixin
    """
    obj.unload_fixtures()


class MetaFixturesMixin(type):
    def __new__(mcs, name, bases, attrs):

        fixtures_conf = attrs.get('fixtures_conf', [])

        #  attrs['__fixtures'] = None

        # Should we persist fixtures across tests, i.e., should we use the
        # setUpClass and tearDownClass methods instead of setUp and tearDown?
        persist_fixtures = attrs.get('persist_fixtures', False) and can_persist_fixtures()

        # We only need to do something if there's a set of fixtures,
        # otherwise, do nothing. The main reason this is here is because this
        # method is called when the FixturesMixin class is created and we
        # don't want to do any test setup on that class.
        if fixtures_conf:
            if not persist_fixtures:
                child_setup_fn = mcs.get_child_fn(attrs, TEST_SETUP_NAMES, bases)
                child_teardown_fn = mcs.get_child_fn(attrs, TEST_TEARDOWN_NAMES, bases)
                attrs[child_setup_fn.__name__] = mcs.setup_handler(setup, child_setup_fn)
                attrs[child_teardown_fn.__name__] = mcs.teardown_handler(teardown, child_teardown_fn)
            else:
                child_setup_fn = mcs.get_child_fn(attrs, CLASS_SETUP_NAMES, bases)
                child_teardown_fn = mcs.get_child_fn(attrs, CLASS_TEARDOWN_NAMES, bases)
                attrs[child_setup_fn.__name__] = classmethod(mcs.setup_handler(setup, child_setup_fn))
                attrs[child_teardown_fn.__name__] = classmethod(mcs.teardown_handler(teardown, child_teardown_fn))

        classinit = attrs.get('__init__')  # could be None

        # define an __init__ function for the new class
        def __init__(self, *args, **kwargs):
            # call the __init__ functions of all the bases
            for base in type(self).__bases__:
                base.__init__(self, *args, **kwargs)
            # also call any __init__ function that was in the new class
            if classinit:  classinit(self, *args, **kwargs)
        # add the local function to the new class
        attrs['__init__'] = __init__

        return super(MetaFixturesMixin, mcs).__new__(mcs, name, bases, attrs)

    @staticmethod
    def setup_handler(setup_fixtures_fn, setup_fn):
        """Returns a function that adds fixtures handling to the setup method.

        Makes sure that fixtures are setup before calling the given setup method.
        """
        def handler(obj):
            setup_fixtures_fn(obj)
            setup_fn(obj)
        return handler

    @staticmethod
    def teardown_handler(teardown_fixtures_fn, teardown_fn):
        """Returns a function that adds fixtures handling to the teardown method.

        Calls the given teardown method first before calling the fixtures teardown.
        """
        def handler(obj):
            teardown_fn(obj)
            teardown_fixtures_fn(obj)
        return handler

    @staticmethod
    def get_child_fn(attrs, names, bases):
        """Returns a function from the child class that matches one of the names.

        Searches the child class's set of methods (i.e., the attrs dict) for all
        the functions matching the given list of names. If more than one is found,
        an exception is raised, if one is found, it is returned, and if none are
        found, a function that calls the default method on each parent class is
        returned.

        """
        def call_method(obj, method):
            """Calls a method as either a class method or an instance method.
            """
            # The __get__ method takes an instance and an owner which changes
            # depending on the calling object. If the calling object is a class,
            # the instance is None and the owner will be the object itself. If the
            # calling object is an instance, the instance will be the calling object
            # and the owner will be its class. For more info on the __get__ method,
            # see http://docs.python.org/2/reference/datamodel.html#object.__get__.
            if isinstance(obj, type):
                instance = None
                owner = obj
            else:
                instance = obj
                owner = obj.__class__
            method.__get__(instance, owner)()

        # Create a default function that calls the default method on each parent
        default_name = names[0]

        def default_fn(obj):
            for cls in bases:
                if hasattr(cls, default_name):
                    call_method(obj, getattr(cls, default_name))
        default_fn.__name__ = default_name

        # Get all of the functions in the child class that match the list of names
        fns = [(name, attrs[name]) for name in names if name in attrs]

        # Raise an error if more than one setup/teardown method is found
        if len(fns) > 1:
            raise RuntimeError("Cannot have more than one setup or teardown method per context (class or test).")
        # If one setup/teardown function was found, return it
        elif len(fns) == 1:
            name, fn = fns[0]

            def child_fn(obj):
                call_method(obj, fn)
            child_fn.__name__ = name
            return child_fn
        # Otherwise, return the default function
        else:
            return default_fn


class FixturesMixin(six.with_metaclass(MetaFixturesMixin, object)):

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

    persist_fixtures = False

    def __init__(self):
        super(FixturesMixin, self).__init__()

        self.__fixtures = None

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]

        if name in self.get_fixtures():
            return self.get_fixtures()[name]

        raise AttributeError('Attribute "{}" not found.'.format(name))

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
