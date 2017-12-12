# -*- coding: utf-8 -*-
import importlib
import re
import six

from fixtures_mongoengine.exceptions import FixturesMongoengineException

_fixture_registry = {}


def get_fixture_class(name):
    doc = _fixture_registry.get(name, None)
    if not doc:
        # Possible old style name
        single_end = name.split('.')[-1]
        compound_end = '.%s' % single_end
        possible_match = [k for k in _fixture_registry.keys()
                          if k.endswith(compound_end) or k == single_end]
        if len(possible_match) == 1:
            doc = _fixture_registry.get(possible_match.pop(), None)
    if not doc:
        raise FixturesMongoengineException('"{}" has not been registered in the fixture registry.'.format(name))
    return doc


def getattr_recursive(o, path):
    """
    :type o:
    :type path: list
    :rtype:
    """
    name = path.pop(0)
    if len(path) == 0:
        return getattr(o, name)
    else:
        return getattr_recursive(getattr(o, name), path)


class MetaFixture(type):
    def __new__(mcs, name, bases, attrs):
        new_class = super(MetaFixture, mcs).__new__(mcs, name, bases, attrs)

        _fixture_registry[new_class.__name__] = new_class
        return new_class


class BaseFixture(object):

    depends = {}

    data_file = None

    data = None

    attr_name = 'fixture_data'

    validate = True

    pk_field_name = None

    def __init__(self):
        super(BaseFixture, self).__init__()

        self._loaded = False
        self._data = {}
        self._depend_fixtures = {}
        self.depend_re = re.compile('\{([^\}]+)\}')

    def __getitem__(self, item):
        if isinstance(item, six.string_types) and item in self._data:
            return self._data[item]
        raise KeyError('There is no key "{}" in fixture {}'.format(item, self.__class__.__name__))

    def __contains__(self, item):
        return item in self._data

    @property
    def loaded(self):
        return self._loaded

    def init_depended_fixtures(self, fixtures):
        """
        :param fixtures: dict, {fixture_class: fixture}
        """
        for name, fixture_class in six.iteritems(self.depends):
            if fixture_class not in fixtures:
                raise FixturesMongoengineException('Depended fixture "{}: {}" not found in fixtures dict.'
                                                   .format(name, fixture_class.__name__))
            self._depend_fixtures[name] = fixtures[fixture_class]

    def before_load(self):
        pass

    def load(self):
        pass

    def after_load(self):
        pass

    def before_unload(self):
        pass

    def unload(self):
        pass

    def after_unload(self):
        pass

    def _validate_depend_fixtures(self):
        if not self.depends:
            return

        for name, fixture_class in six.iteritems(self.depends):
            if name not in self._depend_fixtures:
                raise FixturesMongoengineException('Depended fixture "{}" wasn\'t created.'.format(name))

            fixture = self._depend_fixtures[name]
            if not fixture.loaded:
                raise FixturesMongoengineException('Depended fixture "{}" wasn\'t loaded.'.format(name))

    def _get_raw_data(self):
        """
        :rtype: dict
        """
        if self.data is not None:
            return self.data
        else:
            data_module = importlib.import_module(self.data_file)
            return getattr(data_module, self.attr_name)

    def _resolve_depends(self, value):
        if isinstance(value, six.string_types):
            return self._get_resolved_value(value)
        elif isinstance(value, dict):
            return self._get_resolved_dict(value)
        elif isinstance(value, list):
            return self._get_resolved_list(value)

        return value

    def _get_resolved_dict(self, value):
        copy = dict(value)
        for key, value in six.iteritems(copy):
            copy[key] = self._resolve_depends(value)

        return copy

    def _get_resolved_list(self, value):
        copy = []
        for item in value:
            copy.append(self._resolve_depends(item))

        return copy

    def _get_resolved_value(self, value):
        match = self.depend_re.match(value)
        if not match:
            return value

        ref = match.group(1)
        parts = ref.split('.')
        if len(parts) < 2:
            msg = 'Wrong depend reference "{}" in fixture "{}"'.format(ref, self.__class__.__name__)
            raise FixturesMongoengineException(msg)

        ref_fixture = parts.pop(0)
        if ref_fixture not in self._depend_fixtures:
            msg = 'Fixture "{}" not fount in depended fixtures.'.format(ref_fixture)
            raise FixturesMongoengineException(msg)

        fixture = self._depend_fixtures[ref_fixture]
        ref_model = parts.pop(0)
        if ref_model not in fixture:
            msg = 'Model "{}" not fount in depended fixture "{}".'.format(ref_model, ref_fixture)
            raise FixturesMongoengineException(msg)

        if len(parts) == 0:
            return getattr(fixture[ref_model], fixture.pk_field_name)
        else:
            return getattr_recursive(fixture[ref_model], parts)


class Fixture(six.with_metaclass(MetaFixture, BaseFixture)):

    document_class = None

    pk_field_name = 'pk'

    def __init__(self):
        super(Fixture, self).__init__()

        if self.document_class is None:
            raise FixturesMongoengineException('"document_class" must be set.')

    def load(self):
        self._validate_depend_fixtures()

        raw_data = self._get_raw_data()
        for key, row in six.iteritems(raw_data):
            if self.depends:
                row = self._resolve_depends(row)
            model = self.document_class(**row)
            model.save(self.validate)
            self._data[key] = model

        self._loaded = True

    def unload(self):
        self._data = {}
        self.document_class.objects().delete()
