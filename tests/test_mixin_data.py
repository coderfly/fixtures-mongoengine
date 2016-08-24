# -*- coding: utf-8 -*-

from tests.test_case import MongoFixturesTestCase


# class BaseMixinDataFixtureTestCase(MongoFixturesTestCase):
#
#     def __init__(self, methodName='runTest'):
#         super(BaseMixinDataFixtureTestCase, self).__init__(methodName)
#         FixtureMixin.__init__(self)
#
#     def setUp(self):
#         super(BaseMixinDataFixtureTestCase, self).setUp()
#
#         self.unload_fixtures()
#         self.load_fixtures()
