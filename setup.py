#!/usr/bin/env python
#-*- coding:utf-8 -*-

# Copyright Bernardo Heynemann <heynemann@gmail.com>

# Licensed under the Open Software License ("OSL") v. 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.opensource.org/licenses/osl-3.0.php

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from mi7.version import Version
from setuptools import setup, find_packages

setup(
    name = 'MI7',
    version = Version,
    description = """MI7 is a lightweight and fun spying test framework. It's
    main goal is to be as easy to use as possible.""",
    long_description = """
    MI7 is a lightweight and fun spying test framework. It's main goal is to be as easy to use as possible.

    Python is not a language where one expects to be doing a lot of dependency
    injection, mocking, stubbing and other techniques that are fairly common in
    other languages. That "modus operandi" is what Python developers call being
    Pythonic.

    MI7 is a framework that wants to operate pretty much like James Bond (the old
    one): in stealth mode. The main goal of the library is to be invisible to your
    production code, and as invisible as possible in your tests.

    Experience shows that using current Python test helpers, tests tend to become
    rapidly verbosy. There's nothing worse than writing 10 lines of boilerplate
    code in a test so that you can start testing what you want.

    With MI7, we are trying to answer that call. A call for a library that helps us
    write tests with clear intent and change the current view that Pythonists do
    not like Test Driven Development.
    """,
    keywords = 'Spy Test Framework Mock TDD',
    author = 'Bernardo Heynemann',
    author_email = 'heynemann@gmail.com',
    url = 'https://github.com/heynemann/mi7/wiki',
    license = 'OSI',
    classifiers = ['Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved',
                   'Natural Language :: English',
                   'Operating System :: MacOS',
                   'Operating System :: Microsoft :: Windows',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python :: 2.6',],
    packages = ['mi7'],
    include_package_data=True,
    install_requires=[
    ],
    entry_points = {
    },
)

