#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Interfaces and support for metadata properties.

.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from zope import interface

from zope.dublincore.interfaces import IWriteZopeDublinCore


@interface.implementer(IWriteZopeDublinCore)
def none_dublincore_adapter(unused_context):
    """
    A None dublincore adapter. Useful for objects that implement `IAnnotatable`,
    but do not want want the default `ZDCAnnotatableAdapter` implementation.
    """
    return
