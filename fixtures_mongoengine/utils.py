# -*- coding: utf-8 -*-
from __future__ import absolute_import

import inspect
import os
import sys


def can_persist_fixtures():
    """Returns True if it's possible to persist fixtures across tests.

    Flask-Fixtures uses the setUpClass and tearDownClass methods to persist
    fixtures across tests. These methods were added to unittest.TestCase in
    python 2.7. So, we can only persist fixtures when using python 2.7.
    However, the nose and py.test libraries add support for these methods
    regardless of what version of python we're running, so if we're running
    with either of those libraries, return True to persist fixtures.

    """
    # If we're running python 2.7 or greater, we're fine
    if sys.hexversion >= 0x02070000:
        return True

    # Otherwise, nose and py.test support the setUpClass and tearDownClass
    # methods, so if we're using either of those, go ahead and run the tests
    filename = inspect.stack()[-1][1]
    executable = os.path.split(filename)[1]
    return executable in ('py.test', 'nosetests')
