#!/usr/bin/env python
# pylint: disable=R0801

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

"""setup.py"""
import os

from setuptools import setup  # pylint:disable=E0611,F0401
from http_image_streaming_service.version import VERSION
from pip.req import parse_requirements
from optparse import Option

BASEDIR = os.path.dirname(os.path.abspath(__file__))


def parse_reqs(reqs_file):
    ''' parse the requirements '''
    options = Option("--workaround")
    options.skip_requirements_regex = None
    install_reqs = parse_requirements(reqs_file, options=options)
    return [str(ir.req) for ir in install_reqs]


REQS = parse_reqs(os.path.join(BASEDIR, "requirements.txt"))

EXTRA_REQS_PREFIX = 'requirements_'
EXTRA_REQS = {}
for file_name in os.listdir(BASEDIR):
    if not file_name.startswith(EXTRA_REQS_PREFIX):
        continue
    base_name = os.path.basename(file_name)
    (extra, _) = os.path.splitext(base_name)
    extra = extra[len(EXTRA_REQS_PREFIX):]
    EXTRA_REQS[extra] = parse_reqs(file_name)

setup(name="http_image_streaming_service",
      version=VERSION,
      description="Service in charge of image streaming rendering resources",

      packages=['http_image_streaming_service',
                'http_image_streaming_service/service',
                'http_image_streaming_service/resources'],
      include_package_data=True,
      url='https://github.com/BlueBrain/HTTPImageStreaming.git',
      author='Cyrille Favreau',
      author_email='cyrille.favreau@epfl.ch',
      license='GNU LGPL',
      install_requires=REQS,
      extras_require=EXTRA_REQS,)
