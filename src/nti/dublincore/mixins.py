#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import zope.deferredimport
zope.deferredimport.initialize()
zope.deferredimport.deprecated(
    "Import from nti.base.mixins instead",
    CreatedTimeMixin='nti.base.mixins:CreatedTimeMixin',
    ModifiedTimeMixin='nti.base.mixins:ModifiedTimeMixin',
    CreatedAndModifiedTimeMixin='nti.base.mixins:CreatedAndModifiedTimeMixin')
