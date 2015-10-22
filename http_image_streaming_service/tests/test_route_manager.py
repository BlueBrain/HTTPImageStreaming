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

from http_image_streaming_service.service.http_image_streaming_service import application
import http_image_streaming_service.service.settings \
    as settings

import json
import unittest

DEFAULT_SESSION_ID = 'testsession'
DEFAULT_ROUTE = 'http://localhost:3000'
BASE_URL = settings.APPLICATION_NAME + '/' + settings.API_VERSION + '/'


class FlaskTestCase(unittest.TestCase):

    def test_create_route(self):
        tester = application.test_client(self)
        headers = {'Cookie': 'HBP='+DEFAULT_SESSION_ID+';'}
        response = tester.post(BASE_URL + 'route',
                               content_type='application/json',
                               headers=headers,
                               data=json.dumps({'uri': DEFAULT_ROUTE}))
        self.assertEqual(response.status_code, 201)

    def test_get_route(self):
        tester = application.test_client(self)
        headers = {'Cookie': 'HBP='+DEFAULT_SESSION_ID+';'}
        # create route
        response = tester.post(BASE_URL + 'route',
                               content_type='application/json',
                               headers=headers,
                               data=json.dumps({'uri': DEFAULT_ROUTE}))
        self.assertEqual(response.status_code, 201)

        # validate route existence and value
        response = tester.get(BASE_URL + 'route',
                              content_type='application/json',
                              headers=headers)
        self.assertEqual(response.status_code, 200)
        expected_uri = settings.HISS_URL + \
                       '/image_streaming_feed/' + DEFAULT_SESSION_ID
        self.assertEqual(response.data, json.dumps({'uri': expected_uri}))

        # delete route
        response = tester.delete(BASE_URL + 'route',
                                 content_type='application/json',
                                 headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_create_duplicated_route(self):
        tester = application.test_client(self)
        headers = {'Cookie': 'HBP='+DEFAULT_SESSION_ID+';'}
        # create route with erroneous uri
        response = tester.post(BASE_URL + 'route',
                               content_type='application/json',
                               headers=headers,
                               data=json.dumps({'uri': 'http://test.com'}))
        self.assertEqual(response.status_code, 201)

        # re-create route with same session id
        response = tester.post(BASE_URL + 'route',
                               content_type='application/json',
                               headers=headers,
                               data=json.dumps({'uri': DEFAULT_ROUTE}))
        self.assertEqual(response.status_code, 201)

        # validate route existence and value
        response = tester.get(BASE_URL + 'route',
                              content_type='application/json',
                              headers=headers)
        self.assertEqual(response.status_code, 200)
        expected_uri = settings.HISS_URL + \
                       '/image_streaming_feed/' + DEFAULT_SESSION_ID
        self.assertEqual(response.data, json.dumps({'uri': expected_uri}))

        # delete route
        response = tester.delete(BASE_URL + 'route',
                                 content_type='application/json',
                                 headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_list_routes(self):
        tester = application.test_client(self)
        headers = {'Cookie': 'HBP=1;'}
        # create route 1
        response = tester.post(BASE_URL + 'route',
                               content_type='application/json',
                               headers=headers,
                               data=json.dumps({'uri': 'http://test1.com'}))
        self.assertEqual(response.status_code, 201)

        # create route 2
        headers = {'Cookie': 'HBP=2;'}
        response = tester.post(BASE_URL + 'route',
                               content_type='application/json',
                               headers=headers,
                               data=json.dumps({'uri': 'http://test2.com'}))
        self.assertEqual(response.status_code, 201)

        # validate routes existence and values
        response = tester.get(BASE_URL + 'routes',
                              content_type='application/json')
        self.assertEqual(response.status_code, 200)
        expected_response = json.dumps([['1', 'http://test1.com'], ['2', 'http://test2.com']])
        self.assertEqual(response.data, expected_response)

        # delete routes
        headers = {'Cookie': 'HBP=1;'}
        response = tester.delete(BASE_URL + 'route',
                                 content_type='application/json',
                                 headers=headers)
        self.assertEqual(response.status_code, 200)
        headers = {'Cookie': 'HBP=2;'}
        response = tester.delete(BASE_URL + 'route',
                                 content_type='application/json',
                                 headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_route(self):
        tester = application.test_client(self)
        headers = {'Cookie': 'HBP='+DEFAULT_SESSION_ID+';'}
        # create route
        response = tester.post(BASE_URL + 'route',
                               content_type='application/json',
                               headers=headers,
                               data=json.dumps({'uri': 'http://test1.com'}))
        self.assertEqual(response.status_code, 201)

        # test route
        response = tester.get(BASE_URL + 'image_streaming_feed/' + DEFAULT_SESSION_ID,
                              content_type='application/json',
                              headers=headers)
        self.assertEqual(response.status_code, 200)

        response = tester.delete(BASE_URL + 'route',
                                 content_type='application/json',
                                 headers=headers)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
