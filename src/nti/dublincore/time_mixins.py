#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Base-class and mixin implementations.

.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import numbers
import collections
from datetime import datetime as _datetime
from calendar import timegm as _calendar_timegm

from zope import interface

from zope.dublincore.interfaces import IDCTimes

from persistent import Persistent

from nti.zodb import minmax
from nti.zodb.persistentproperty import PersistentPropertyHolder

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

@interface.implementer(IDCTimes)
class DCTimesLastModifiedMixin(object):
	"""
	A mixin that implements dublincore times using the timestamp
	information from ILastModified. Requires no storage,
	can be added to persistent objects at any time.

	These datetimes are always naive datetime objects, normalized
	to UTC.
	"""

	created = TimeProperty('createdTime')
	modified = TimeProperty('lastModified', write_name='updateLastModIfGreater')

import zope.deferredimport
zope.deferredimport.initialize()
zope.deferredimport.deprecated(
	"Import from nti.dublincore.mixins instead",
	CreatedTimeMixin='nti.dublincore.mixins:CreatedTimeMixin')

from nti.dublincore.mixins import ModifiedTimeMixin as _ModifiedTimeMixin
from nti.dublincore.mixins import CreatedAndModifiedTimeMixin as _CreatedAndModifiedTimeMixin

class ModifiedTimeMixin(_ModifiedTimeMixin):
	"""
	Maintains an lastModified attribute containing a time.time()
	modification stamp. Use updateLastMod() to update this value.
	Typically subclasses of this class should be :class:`nti.zodb.persistentproperty.PersistentPropertyHolder`
	"""

	lastModified = minmax.NumericPropertyDefaultingToZero( str('_lastModified'),
														   minmax.NumericMaximum,
														   as_number=True )

	def __new__( cls, *args, **kwargs ):
		if 		issubclass(cls, Persistent) \
			and not issubclass(cls, PersistentPropertyHolder):
			print("ERROR: subclassing Persistent, but not PersistentPropertyHolder", cls)
		return super(ModifiedTimeMixin,cls).__new__( cls, *args, **kwargs )

	def __setstate__(self, data):
		if 	isinstance(data, collections.Mapping) and \
			'_lastModified' in data and isinstance(data['_lastModified'], numbers.Number):
			# Are there actually any objects still around that have this condition?
			# A migration to find them is probably difficult
			data[str('_lastModified')] = minmax.NumericMaximum(data['_lastModified'])
		elif isinstance(data, (float, int)):  # Not sure why we get float here
			data = {str('_lastModified'):minmax.NumericMaximum('data')}

		# We may or may not be the base of the inheritance tree; usually we are not,
		# but occasionally (mostly in tests) we are
		try:
			super(ModifiedTimeMixin, self).__setstate__(data)
		except AttributeError:
			self.__dict__.clear()
			self.__dict__.update(data)
ModDateTrackingObject = ModifiedTimeMixin # BWC

class CreatedAndModifiedTimeMixin(_CreatedAndModifiedTimeMixin,
								  ModifiedTimeMixin,
								  DCTimesLastModifiedMixin):
	pass

class PersistentCreatedAndModifiedTimeObject(CreatedAndModifiedTimeMixin,
											 PersistentPropertyHolder):
	# order of inheritance matters; if Persistent is first, we can't have our own __setstate__;
	# only subclasses can
	pass
