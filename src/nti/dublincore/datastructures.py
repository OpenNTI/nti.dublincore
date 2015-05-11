#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.externalization.persistence import PersistentExternalizableList as _PersistentExternalizableList
from nti.externalization.persistence import PersistentExternalizableWeakList as _PersistentExternalizableWeakList

from nti.zodb.persistentproperty import PersistentPropertyHolder

from .time_mixins import CreatedAndModifiedTimeMixin

class CreatedModDateTrackingObject(CreatedAndModifiedTimeMixin):
	"""
	Adds the `creator` and `createdTime` attributes.
	"""

	def __init__( self, *args, **kwargs ):
		super(CreatedModDateTrackingObject,self).__init__( *args, **kwargs )
		# Some of our subclasses have class attributes for fixed creators.
		# don't override those unless we have to
		if not hasattr(self, 'creator'):
			try:
				self.creator = None
			except AttributeError:
				# A read-only property in the class dict that
				# isn't available yet
				pass

class PersistentCreatedModDateTrackingObject(CreatedModDateTrackingObject,
											 PersistentPropertyHolder):
	# order of inheritance matters; if Persistent is first,
	# we can't have our own __setstate__; # only subclasses can
	pass

# For BWC, we apply these properties to the base class too,
# but the implementation is not correct as they do not get updated...
_PersistentExternalizableList.__bases__ = (PersistentCreatedModDateTrackingObject,) + \
										  _PersistentExternalizableList.__bases__

class PersistentExternalizableWeakList(_PersistentExternalizableWeakList,
									   PersistentCreatedModDateTrackingObject):

	"""
	Stores :class:`persistent.Persistent` objects as weak references, invisibly to the user.
	Any weak references added to the list will be treated the same.
	"""

	def remove(self,value):
		super(PersistentExternalizableWeakList,self).remove( value )
		self.updateLastMod()

	def __setitem__(self, i, item):
		super(PersistentExternalizableWeakList,self).__setitem__( i, item )
		self.updateLastMod()

	def __iadd__(self, other):
		# We must wrap each element in a weak ref
		# Note that the builtin list only accepts other lists,
		# but the UserList from which we are descended accepts
		# any iterable.
		result = super(PersistentExternalizableWeakList,self).__iadd__(other)
		self.updateLastMod()
		return result

	def __imul__(self, n):
		result = super(PersistentExternalizableWeakList,self).__imul__(n)
		self.updateLastMod()
		return result

	def append(self, item):
		super(PersistentExternalizableWeakList,self).append(item)
		self.updateLastMod()

	def insert(self, i, item):
		super(PersistentExternalizableWeakList,self).insert( i, item )
		self.updateLastMod()

	def pop(self, i=-1):
		rtn = super(PersistentExternalizableWeakList,self).pop( i )
		self.updateLastMod()
		return rtn
