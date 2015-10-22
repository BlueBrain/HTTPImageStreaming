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
This module contains the class in charge of managing the routes
"""

# pylint: disable=W0403
from flask import make_response
import json
import custom_logging as log
import settings


class RouteManager(object):

    """
    Constructor
    """
    def __init__(self):
        self.routes = dict()
        self.frame_md5s = dict()

    def get_route(self, session_id):
        """
        Returns a JSON formatted list of active routes
        """
        # Check for the existence of the route. Raise a KeyError exception
        # if not found
        # pylint: disable=W0104
        self.routes[session_id]
        response = json.dumps(
            {'uri': settings.HISS_URL +
                '/image_streaming_feed/' +
                str(session_id)})
        log.info(1, 'Route for ' + session_id + ' is ' + str(response))
        return response

    def get_route_target(self, session_id):
        """
        Returns a JSON formatted list of active routes
        """
        log.info(1, 'Route target for session ' + session_id + ' is...')
        response = self.routes[session_id]
        log.info(1, 'Route target for session ' + session_id + ' is ' + str(response))
        return response

    def get_frame_md5(self, session_id):
        """
        Returns the latest frame md5 for the given session
        :param session_id: Id of the session for which the route was created
        """
        response = None
        try:
            response = self.frame_md5s[session_id]
            log.debug(1, 'Hashed frame for ' + session_id + ' is ' + str(response))
        except KeyError:
            log.debug(1, 'No hashed frame for ' + session_id)
        return response

    def set_frame_md5(self, session_id, md5):
        """
        Sets the latest frame md5 for the given session
        :param session_id: Id of the session for which the route was created
        :param md5: MD5 of the frame
        """
        self.frame_md5s[session_id] = md5

    def list_routes(self):
        """
        Returns a JSON formatted list of active routes
        """
        log.info(1, 'Getting all routes')
        response = ''
        for key, value in self.routes.items():
            response = response + '{' + key + ': ' + value + '}'
        response = json.dumps(self.routes.items())
        log.info(1, response)
        return make_response(response, 200)

    def create_route(self, session_id, uri):
        """
        Adds a new route. If the route already exists for the given session, the
        current URI is replaced by the new one
        :param session_id: Id of the session for which the route was created
        :param uri: URI of new route
        """
        self.routes[session_id] = uri
        log.info(1, 'Route ' + self.routes[session_id] + ' successfully added')
        return make_response(self.routes[session_id], 201)

    def delete_route(self, session_id):
        """
        Removes an existing route
        :param session_id: Id of the session for which the route was created
        """
        log.info(1, 'Removing route for session ' + str(session_id))
        try:
            uri = self.routes[session_id]
            del self.routes[session_id]
            response = 'Route ' + uri + ' successfully removed'
            log.info(1, response)
            return make_response(response, 200)
        except KeyError:
            response = 'Route does not exist'
            log.info(1, response)
            return make_response(response, 404)

    def clear_routes(self):
        """
        Removes all existing routes
        """
        self.routes.clear()
        return [200, 'Routes cleared']
