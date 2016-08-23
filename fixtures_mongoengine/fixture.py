# -*- coding: utf-8 -*-
import importlib
import re
import six

from fixtures_mongoengine.exceptions import FixturesMongoengineException


class Fixture(object):

    document_class = None

    depends = {}

    data_file = None

    attr_name = 'fixture_data'

    validate = True

    def __init__(self):
        super(Fixture, self).__init__()

        if self.document_class is None:
            raise FixturesMongoengineException('"document_class" must be set.')

        self._data = {}
        self._loaded = False
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

    def init_depend_fixtures(self, fixtures):
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
        self._validate_depend_fixtures()

        raw_data = self._get_raw_data()
        for key, row in six.iteritems(raw_data):
            row = self._resolve_depends(row)
            model = self.document_class(**row)
            model.save(self.validate)
            self._data[key] = model

        self._loaded = True

    def after_load(self):
        pass

    def before_unload(self):
        pass

    def unload(self):
        self._data = {}
        self.document_class.objects().delete()

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
        module = importlib.import_module(self.data_file)
        return getattr(module, self.attr_name)

    def _resolve_depends(self, row):
        copy = dict(row)
        if self.depends:
            for key, value in six.iteritems(copy):
                if isinstance(value, six.string_types):
                    copy[key] = self._get_resolved_value(key, value)

        return copy

    def _get_resolved_value(self, key, value):
        match = self.depend_re.match(value)
        if not match:
            return value

        ref = match.group(1)
        parts = ref.split('.')
        if len(parts) != 2:
            msg = 'Wrong depend reference "{}" in fixture "{}"'.format(ref, self.__class__.__name__)
            raise FixturesMongoengineException(msg)

        ref_fixture = parts[0]
        if ref_fixture not in self._depend_fixtures:
            msg = 'Fixture "{}" not fount in depended fixtures.'.format(ref_fixture)
            raise FixturesMongoengineException(msg)

        fixture = self._depend_fixtures[ref_fixture]
        ref_model = parts[1]
        if ref_model not in fixture:
            msg = 'Model "{}" not fount in depended fixture "{}".'.format(ref_model, ref_fixture)
            raise FixturesMongoengineException(msg)

        return fixture[ref_model].pk



