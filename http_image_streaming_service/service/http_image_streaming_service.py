#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2014-2015, Human Brain Project
# Cyrille Favreau <cyrille.favreau@epfl.ch>
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
This module contains the actual application that serves the HTTP requests
"""

# pylint: disable=W0403
import json
import hashlib

from flask import Flask, request, Response, make_response
import os
import custom_logging as log
import settings
from route_manager import RouteManager
from rest_frame_grabber import RestFrameGrabber

# Contains the default 'not found' image
frame_not_found = open(os.path.dirname(__file__) +
                       '/../resources/image_not_found.jpg', 'rb').read()

application = Flask(__name__)
route_manager = RouteManager()


def streamer(session_id, frame_grabber):
    """
    Serves a given image stream
    :param session_id: Id of the session to stream
    :param frame_grabber: Implementation of the class in charge of fetching the images
    """
    while True:
        with application.app_context():
            frame = None
            uri = ''
            try:
                uri = route_manager.get_route_target(session_id)
                frame = frame_grabber.get_frame(uri)
            except KeyError:
                # Returns an empty frame
                frame = frame_not_found

            # Optimization: Generate an MD5 for the current frame and push
            # it to the client only if it is different from the previous
            # one
            frame_md5 = int(hashlib.md5(frame).hexdigest(), 16)
            if route_manager.get_frame_md5(session_id) != frame_md5:
                route_manager.set_frame_md5(session_id, frame_md5)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@application.route('/' + settings.APPLICATION_NAME + '/' + settings.API_VERSION +
                   '/routes', methods=['GET'])
def list_routes():
    """
    Lists existing routes. No session ID is required
    """
    if request.method == 'GET':
        response = route_manager.list_routes()
        return make_response(response, 200)


@application.route('/' + settings.APPLICATION_NAME + '/' + settings.API_VERSION +
                   '/route', methods=['GET', 'DELETE', 'POST'])
def route_management():
    """
    Manages the routes according to the request type:
    POST: Create new route
    DELETE: Remove existing route
    GET: List existing routes
    """
    try:
        session_id = request.cookies[settings.HBP_COOKIE]
        if request.method == 'GET':
            response = route_manager.get_route(session_id)
            return make_response(response, 200)
        if request.method == 'POST':
            if request.data is None:
                response = 'Error: Data must be provided for POST operations'
                log.error(response)
                return make_response(response, 401)
            json_data = json.loads(request.data)
            uri = json_data['uri']
            log.info(1, 'Creating new route for ' + uri)
            response = route_manager.create_route(session_id, uri)
            return make_response(response, 201)
        else:
            return route_manager.delete_route(session_id)
    except KeyError as e:
        response = str(e)
        log.info(1, response)
        return make_response(response, 404)


@application.route('/' + settings.APPLICATION_NAME + '/' + settings.API_VERSION +
                   '/image_streaming_feed/<string:session_id>')
def image_streaming_feed(session_id):
    """
    Handles the image stream according to the given session
    :param session_id: Id of the session to stream
    """
    log.info(1, 'Creating streamer for ' + str(session_id))
    return Response(streamer(session_id, RestFrameGrabber()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    log.info(1, 'Serving requests on ' + settings.HISS_HOSTNAME +
             ':' + str(settings.HISS_PORT))
    application.run(host=settings.HISS_HOSTNAME,
                    port=settings.HISS_PORT,
                    debug=settings.HISS_DEBUG,
                    threaded=settings.HISS_THREADED)