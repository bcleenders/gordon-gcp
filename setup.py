#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2017 Spotify AB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import codecs
import os
import re

from setuptools import setup


HERE = os.path.abspath(os.path.dirname(__file__))


#####
# Helper functions
#####
def read(*filenames, **kwargs):
    """
    Build an absolute path from ``*filenames``, and  return contents of
    resulting file.  Defaults to UTF-8 encoding.
    """
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for fl in filenames:
        with codecs.open(os.path.join(HERE, fl), 'rb', encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


def find_meta(meta):
    """Extract __*meta*__ from META_FILE."""
    re_str = r"^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=meta)
    meta_match = re.search(re_str, META_FILE, re.M)
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError('Unable to find __{meta}__ string.'.format(meta=meta))


def install_requires():
    reqs_txt = read('requirements.txt')
    parsed = reqs_txt.split('\n')
    parsed = [r.split('==')[0] for r in parsed]
    return [r for r in parsed if len(r) > 0]


#####
# Project-specific constants
#####
NAME = 'gordon-dns-gcp'
PACKAGE_NAME = 'gordon_gcp'
PACKAGES = ['gordon_gcp']
META_PATH = os.path.join(PACKAGE_NAME, '__init__.py')
KEYWORDS = ['dns', 'gcp', 'gce', 'pubsub' 'google cloud platform']
CLASSIFIERS = [
    'Development Status :: 1 - Planning',
    'License :: OSI Approved :: Apache Software License',
    'Natural Language :: English',
    'Operating System :: POSIX :: Linux',
    'Operating System :: MacOS :: MacOS X',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python :: Implementation :: PyPy',
    'Topic :: Internet :: Name Service (DNS)',
]
META_FILE = read(META_PATH)


setup(
    name=NAME,
    version=find_meta('version'),
    license=find_meta('license'),
    description=find_meta('description'),
    url=find_meta('uri'),
    author=find_meta('author'),
    author_email=find_meta('email'),
    maintainer=find_meta('author'),
    maintainer_email=find_meta('email'),
    packages=PACKAGES,
    entry_points={
        'gordon.plugins': [
            'gcp.compute = gordon_gcp.compute:ComputeEngineClient',
            'gcp.dns = gordon_gcp.dns:CloudDNSClient',
            'gcp.pubsub = gordon_gcp.pubsub:PubSubClient',
        ],
    },
    data_files=[
        'schema/schemas/audit-log.schema.json',
        'schema/schemas/event.schema.json'
    ],
    classifiers=CLASSIFIERS,
    keywords=KEYWORDS,
    zip_safe=False,
    install_requires=install_requires(),
)
