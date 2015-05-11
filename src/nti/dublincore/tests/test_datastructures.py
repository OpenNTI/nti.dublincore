#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import assert_that

import unittest

import persistent

from nti.dublincore.datastructures import PersistentExternalizableWeakList

from nti.dublincore.tests import SharedConfiguringTestLayer

class TestPersistentExternalizableWeakList(unittest.TestCase):

    layer = SharedConfiguringTestLayer
    
    def test_plus_extend( self ):
        class C( persistent.Persistent ): pass
        c1 = C()
        c2 = C()
        c3 = C()
        l = PersistentExternalizableWeakList()
        l += [c1, c2, c3]
        assert_that( l, is_( [c1, c2, c3] ) )
        assert_that( [c1, c2, c3], is_(l) )

        # Adding things that are already weak refs.
        l += l
        assert_that( l, is_( [c1, c2, c3, c1, c2, c3] ) )

        l = PersistentExternalizableWeakList()
        l.extend( [c1, c2, c3] )
        assert_that( l, is_( [c1, c2, c3] ) )
        assert_that( l, is_(l) )