#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2014-2015, Human Brain Project
#                          Cyrille Favreau <cyrille.favreau@epfl.ch>
#
# This file is part of RenderingResourceManager
# <https://github.com/BlueBrain/HTTPImageStreaming>
#
# This library is free software; you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License version 3.0 as published
# by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# All rights reserved. Do not distribute without further notice.

"""
This module contains the service settings
"""

# Application name
APPLICATION_NAME = 'image-streaming-service'

# API version
API_VERSION = 'v1'

# Image streaming service parameters
HISS_HOSTNAME = '128.178.97.241'
HISS_PORT = 8385
HISS_URL = 'http://' + HISS_HOSTNAME + ':' + str(HISS_PORT) + \
           '/' + APPLICATION_NAME + '/' + API_VERSION
HISS_DEBUG = False
HISS_THREADED = True

# ID of cookie containing the session ID. The session ID is used to identify
# the route that should be used to fetch images
HBP_COOKIE = 'HBP'
