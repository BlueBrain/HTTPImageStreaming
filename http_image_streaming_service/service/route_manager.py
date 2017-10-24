#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2014-2017, Human Brain Project
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
import sqlite3


class RouteManager(object):

    """
    Constructor
    """
    def __init__(self):
        self._frame_md5s = dict()
        log.info(1, 'Route manager initialized')

    @staticmethod
    def get_route(session_id):
        """
        Returns a JSON formatted list of active routes
        """
        # Check for the existence of the route. Raise a KeyError exception
        # if not found
        # pylint: disable=W0104
        if session_id != 'demo':
            conn = sqlite3.connect(settings.HISS_DB)
            try:
                cur = conn.cursor()
                cur.execute('select uri from routes where session_id=?', (session_id,))
                rows = cur.fetchall()
                if len(rows) == 0:
                    raise KeyError
            finally:
                conn.close()

        response = json.dumps(
            {'uri': settings.HISS_URL +
                '/image_streaming_feed/' +
                str(session_id)})
        log.info(1, 'Route for ' + str(session_id) + ' is ' + str(response))
        return response

    @staticmethod
    def get_route_target(session_id):
        """
        Returns a JSON formatted list of active routes
        """
        log.info(1, 'Route target for session ' + session_id + ' is...')
        conn = sqlite3.connect(settings.HISS_DB)
        try:
            cur = conn.cursor()
            cur.execute('select uri from routes where session_id=?', (session_id,))
            rows = cur.fetchall()
            response = rows[0][0]
        finally:
            conn.close()
        log.info(1, 'Route target for session ' + session_id + ' is ' + str(response))
        return response

    def get_frame_md5(self, session_id):
        """
        Returns the latest frame md5 for the given session
        :param session_id: Id of the session for which the route was created
        """
        response = None
        try:
            response = self._frame_md5s[session_id]
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
        self._frame_md5s[session_id] = md5

    @staticmethod
    def list_routes():
        """
        Returns a JSON formatted list of active routes
        """
        log.info(1, 'Getting all routes')
        routes = dict()
        conn = sqlite3.connect(settings.HISS_DB)
        try:
            cur = conn.cursor()
            cur.execute('select session_id, uri from routes')
            rows = cur.fetchall()
            for row in rows:
                routes[row[0]] = row[1]
        finally:
            conn.close()
        response = json.dumps(routes.items())
        log.info(1, response)
        return make_response(response, 200)

    @staticmethod
    def create_route(session_id, uri):
        """
        Adds a new route. If the route already exists for the given session, the
        current URI is replaced by the new one
        :param session_id: Id of the session for which the route was created
        :param uri: URI of new route
        """
        conn = sqlite3.connect(settings.HISS_DB)
        try:
            cur = conn.cursor()
            cur.execute('insert into routes (session_id, uri) values(?, ?)', (session_id, uri))
            conn.commit()
        finally:
            conn.close()

        # self.routes[session_id] = uri
        msg = 'Route ' + uri + ' successfully added'
        log.info(1, msg)
        response = json.dumps({'contents': msg})
        return make_response(response, 201)

    @staticmethod
    def delete_route(session_id):
        """
        Removes an existing route
        :param session_id: Id of the session for which the route was created
        """
        log.info(1, 'Removing route for session ' + str(session_id))
        conn = sqlite3.connect(settings.HISS_DB)
        try:
            cur = conn.cursor()
            cur.execute('delete from routes where session_id=?', (session_id,))
            conn.commit()
            msg = 'Route ' + session_id + ' successfully removed'
            response = json.dumps({'contents': msg})
            log.info(1, response)
            return make_response(response, 200)
        except KeyError:
            response = json.dumps({'contents': 'Route does not exist'})
            log.info(1, response)
            return make_response(response, 404)
        finally:
            conn.close()

    @staticmethod
    def clear_routes():
        """
        Removes all existing routes
        """
        conn = sqlite3.connect(settings.HISS_DB)
        try:
            cur = conn.cursor()
            cur.execute('delete from routes')
            conn.commit()
        finally:
            conn.close()
        return [200, 'Routes cleared']
