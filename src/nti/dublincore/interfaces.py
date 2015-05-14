#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Interfaces and support for metadata properties.

.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

from zope.dublincore.interfaces import IDCDescriptiveProperties

from nti.schema.field import ValidText as Text
from nti.schema.field import ValidTextLine as TextLine

class IDCOptionalDescriptiveProperties(IDCDescriptiveProperties):
	"""
	Makes title and description optional.
	"""
	title = TextLine(title="The human-readable section name of this item; alias for `__name__`",
					 default='')  # also defined by IDCDescriptiveProperties as required

	description = Text(title="The human-readable description",
					   default='')  # also defined by IDCDescriptiveProperties as required


import zope.deferredimport
zope.deferredimport.initialize()

zope.deferredimport.deprecatedFrom(
	"Moved to nti.coremetadata.interfaces",
	"nti.coremetadata.interfaces",
	"ICreatedTime",
	"ILastModified"
)
