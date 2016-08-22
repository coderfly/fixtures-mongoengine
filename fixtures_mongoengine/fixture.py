# -*- coding: utf-8 -*-
import importlib

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

    def __getitem__(self, item):
        if isinstance(item, six.string_types) and item in self._data:
            return self._data[item]
        raise KeyError('There is no key "{}" in fixture {}'.format(item, self.__class__.__name__))

    @property
    def loaded(self):
        return self._loaded

    def init_depend_fixtures(self, fixtures):
        """
        :param fixtures: dict, {fixture_class: fixture}
        """
        for name, fixture_class in six.iteritems(self.depends):
            if name not in fixtures:
                raise FixturesMongoengineException('Depended fixture "{}: {}" not found in fixtures dict.'
                                                   .format(name, fixture_class.__name__))
            self._depend_fixtures[name] = fixtures[fixture_class]

    def before_load(self):
        pass

    def load(self):
        self._validate_depend_fixtures()

        raw_data = self._get_raw_data()
        for key, row in six.iteritems(raw_data):
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
        if self.depends is not None:
            pass
        return row
