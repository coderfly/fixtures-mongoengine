# -*- coding: utf-8 -*-
import importlib

import six


class Fixture(object):

    document_class = None

    depends = None

    data_file = None

    attr_name = 'fixture_data'

    validate = True

    def __init__(self):
        super(Fixture, self).__init__()

        if self.document_class is None:
            raise Exception('"document_class" must be set.')

        self.data = {}

    def before_load(self):
        pass

    def load(self):
        raw_data = self._get_raw_data()
        for key, row in six.iteritems(raw_data):
            model = self.document_class(**row)
            model.save(self.validate)
            self.data[key] = model

    def after_load(self):
        pass

    def before_unload(self):
        pass

    def unload(self):
        self.data = {}
        self.document_class.objects().delete()

    def after_unload(self):
        pass

    def _get_raw_data(self):
        """
        :rtype: dict
        """
        module = importlib.import_module(self.data_file)
        return getattr(module, self.attr_name)
