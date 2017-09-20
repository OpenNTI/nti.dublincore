#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Interfaces and support for metadata properties.

.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import zope.deferredimport

from zope.dublincore.interfaces import IDCDescriptiveProperties

from nti.schema.field import ValidText as Text
from nti.schema.field import ValidTextLine as TextLine


class IDCOptionalDescriptiveProperties(IDCDescriptiveProperties):
    """
    Makes title and description optional.
    """
    title = TextLine(title=u"The human-readable section name of this item; alias for `__name__`",
                     default=u'')  # also defined by IDCDescriptiveProperties as required

    description = Text(title=u"The human-readable description",
                       default=u'')  # also defined by IDCDescriptiveProperties as required


zope.deferredimport.initialize()
zope.deferredimport.deprecatedFrom(
    "Moved to nti.base.interfaces",
    "nti.base.interfaces",
    "ICreatedTime",
    "ILastModified"
)
