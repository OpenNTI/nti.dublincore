#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from datetime import datetime as _datetime
from calendar import timegm as _calendar_timegm

class TimeProperty(object):

	_cached = None

	def __init__(self,
				 name,
				 writable=True,
				 write_name=None,
				 cached=False):
		self._name = intern(str(name))
		self._writable = writable
		self._write_name = write_name
		if cached:
			self._cached = str('_v_time_property_' + name)

	def __get__(self, inst, klass):
		if inst is None:
			return self

		cached_ts, dt = None, None
		if self._cached:
			try:
				cached_ts, dt =  getattr(inst, self._cached)
			except AttributeError:
				pass

		inst_time = None
		try:
			inst_time = getattr(inst, self._name)
		except (AttributeError, TypeError, OSError):
			# catch OSError to allow for using the filesystem
			pass

		if (cached_ts is not None
			and inst_time is not None
			and cached_ts == inst_time):
			return dt

		if inst_time is None:
			inst_time = 0

		dt = _datetime.utcfromtimestamp(inst_time)
		if self._cached:
			try:
				setattr(inst, self._cached, (inst_time, dt))
			except AttributeError:
				pass
		return dt

	def __set__(self, instance, value):
		if not self._writable:
			return

		if self._cached:
			try:
				delattr( instance, self._cached)
			except AttributeError:
				pass

		value = _calendar_timegm(value.utctimetuple())
		if self._write_name and callable(getattr(instance, self._write_name, None)):
			getattr(instance, self._write_name)(value)
		else:
			setattr(instance, self._name, value)
