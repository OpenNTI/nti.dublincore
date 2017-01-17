#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Support for metadata descriptive properties, similar to,
and building on :mod:`zope.dublincore`.

.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.dublincore.datastructures import CreatedModDateTrackingObject
from nti.dublincore.datastructures import PersistentCreatedModDateTrackingObject

from nti.dublincore.time_mixins import TimeProperty
from nti.dublincore.time_mixins import ModifiedTimeMixin

from nti.dublincore.time_mixins import CreatedAndModifiedTimeMixin
from nti.dublincore.time_mixins import PersistentCreatedAndModifiedTimeObject
