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

from persistent import Persistent

from nti.dublincore.time_mixins import ModifiedTimeMixin

from nti.dublincore.tests import SharedConfiguringTestLayer


class TestTimeMixins(unittest.TestCase):

    layer = SharedConfiguringTestLayer
    
    def test_modified_time_mixin(self):
        class C(ModifiedTimeMixin, Persistent):
            pass
        c = C()
        c.__setstate__(100.0)
        assert_that(c, has_property('lastModified', is_(100)))
