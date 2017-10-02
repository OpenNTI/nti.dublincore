#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Base-class and mixin implementations.

.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import numbers
import collections

import zope.deferredimport

from zope import interface

from zope.dublincore.interfaces import IDCTimes

from persistent import Persistent

from nti.base.mixins import ModifiedTimeMixin as _ModifiedTimeMixin
from nti.base.mixins import CreatedAndModifiedTimeMixin as _CreatedAndModifiedTimeMixin

from nti.dublincore.property import TimeProperty

from nti.zodb import minmax

from nti.zodb.persistentproperty import PersistentPropertyHolder

logger = __import__('logging').getLogger(__name__)


zope.deferredimport.initialize()
zope.deferredimport.deprecated(
    "Import from nti.base.mixins instead",
    CreatedTimeMixin='nti.base.mixins:CreatedTimeMixin')


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
    modified = TimeProperty('lastModified',
                            write_name='updateLastModIfGreater')


#: last modified property in mixin
__LM__ = '_lastModified'


class ModifiedTimeMixin(_ModifiedTimeMixin):
    """
    Maintains an lastModified attribute containing a time.time()
    modification stamp. Use updateLastMod() to update this value.
    Typically subclasses of this class should be 
    :class:`nti.zodb.persistentproperty.PersistentPropertyHolder`
    """

    lastModified = minmax.NumericPropertyDefaultingToZero(str(__LM__),
                                                          minmax.NumericMaximum,
                                                          as_number=True)

    def __new__(cls, *args, **kwargs):
        if      issubclass(cls, Persistent) \
            and not issubclass(cls, PersistentPropertyHolder):
            print("ERROR: subclassing Persistent, but not PersistentPropertyHolder", cls)
        return super(ModifiedTimeMixin, cls).__new__(cls, *args, **kwargs)

    def __setstate__(self, data):
        if      isinstance(data, collections.Mapping) \
            and __LM__ in data \
            and isinstance(data[__LM__], numbers.Number):
            # Are there actually any objects still around that have this condition?
            # A migration to find them is probably difficult
            data[__LM__] = minmax.NumericMaximum(data[__LM__])
        elif isinstance(data, (float, int)):  # Not sure why we get float here
            data = {__LM__: minmax.NumericMaximum(data)}
        # We may or may not be the base of the inheritance tree; usually we are not,
        # but occasionally (mostly in tests) we are
        try:
            super(ModifiedTimeMixin, self).__setstate__(data)
        except AttributeError:
            self.__dict__.clear()
            self.__dict__.update(data)
ModDateTrackingObject = ModifiedTimeMixin  # BWC


class CreatedAndModifiedTimeMixin(_CreatedAndModifiedTimeMixin,
                                  ModifiedTimeMixin,
                                  DCTimesLastModifiedMixin):
    pass


class PersistentCreatedAndModifiedTimeObject(CreatedAndModifiedTimeMixin,
                                             PersistentPropertyHolder):
    # order of inheritance matters; if Persistent is first, we can't have our own __setstate__;
    # only subclasses can
    pass
