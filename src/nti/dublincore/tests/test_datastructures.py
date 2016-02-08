#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import is_not
from hamcrest import raises
from hamcrest import calling
from hamcrest import assert_that

import unittest

import persistent

from nti.dublincore.datastructures import PersistentExternalizableWeakList

from nti.dublincore.tests import SharedConfiguringTestLayer

class TestPersistentExternalizableWeakList(unittest.TestCase):

	layer = SharedConfiguringTestLayer

	def test_plus_extend(self):
		class C(persistent.Persistent):
			pass
		c1 = C()
		c2 = C()
		c3 = C()
		l = PersistentExternalizableWeakList()
		l += [c1, c2, c3]
		assert_that(l, is_([c1, c2, c3]))
		assert_that([c1, c2, c3], is_(l))

		# Adding things that are already weak refs.
		l += l
		assert_that(l, is_([c1, c2, c3, c1, c2, c3]))

		l = PersistentExternalizableWeakList()
		l.extend([c1, c2, c3])
		assert_that(l, is_([c1, c2, c3]))
		assert_that(l, is_(l))

	def test_mutate(self):

		obj = PersistentExternalizableWeakList()

		# Cannot set non-persistent objects
		assert_that(calling(obj.append).with_args(object()),
					raises(AttributeError))

		pers = persistent.Persistent()
		obj.append(pers)
		assert_that(obj[0], is_(pers))

		pers2 = persistent.Persistent()
		obj[0] = pers2
		assert_that(obj[0], is_(pers2))
		assert_that(obj.count(pers2), is_(1))
		assert_that(obj.count(pers), is_(0))

		# iteration
		for x in obj:
			assert_that(x, is_(pers2))
		assert_that(obj.index(pers2), is_(0))

		assert_that(obj.pop(), is_(pers2))
		assert_that(calling(obj.pop), raises(IndexError))

		assert_that(obj, is_(obj))

		obj.append(pers2)
		# mul
		assert_that(obj * 2, is_(PersistentExternalizableWeakList([pers2, pers2])))

		# imul
		obj *= 2
		assert_that(obj, is_(PersistentExternalizableWeakList([pers2, pers2])))

		obj.pop()
		# insert
		obj.insert(1, pers2)
		assert_that(obj, is_(PersistentExternalizableWeakList([pers2, pers2])))

		assert_that(obj, is_([pers2, pers2]))
		assert_that(obj, is_not([pers2, pers]))
		assert_that(obj, is_not(pers))
