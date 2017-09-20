#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from nti.base.deprecation import moved


def _patch():
    """
    move old modules that contained persitent objects to their
    new location. DO NOT Remove
    """
    moved('nti.dublincore.mixins', 'nti.base.mixins')


_patch()
del _patch


def patch():
    pass
