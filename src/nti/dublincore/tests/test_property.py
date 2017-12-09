#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import is_
from hamcrest import is_not
from hamcrest import assert_that
from hamcrest import has_property
does_not = is_not

import unittest
from datetime import datetime

from nti.base.mixins import ModifiedTimeMixin

from nti.dublincore.property import TimeProperty

from nti.dublincore.tests import SharedConfiguringTestLayer


class TestProperty(unittest.TestCase):

    layer = SharedConfiguringTestLayer
    
    def test_model(self):
        modified = TimeProperty('lastModified', writable=False, cached=True)
        assert_that(modified.__get__(None, None), is_(modified))
        assert_that(modified.__get__(object(), None), is_(datetime))

        class A(ModifiedTimeMixin):
            modified = TimeProperty('lastModified', writable=False, cached=True)

        c = A()
        c.modified = 100
        assert_that(c, has_property('modified', is_(datetime)))
        
        class B(ModifiedTimeMixin):
            modified = TimeProperty('lastModified', writable=True, cached=True)
        c = B()
        c.modified = datetime.now()
        
        class C(ModifiedTimeMixin):
            modified = TimeProperty('lastModified', writable=True,
                                    write_name='_prop_set', cached=True)
            def _prop_set(self, v):
                self.lastModified = v
        c = C()
        c.modified = datetime.now()
