"""
(c) Copyright 2013, 2014. DataXu, Inc. All Rights Reserved.
:license:   BSD-new, see LICENSE for more details.

dx_skytap module setup and package.
"""

from setuptools import setup

setup(
    name='dxskytap',
    author='DataXu',
    author_email='rcarey@dataxu.com',
    description='DataXu Utilities for Skytap',
    long_description="""
This module contains a client library for accessing
[Skytap](http://www.skytap.com)'s cloud API . This code was originally
developed at [DataXu](http://www.dataxu.com) and released as open source.
""",
    license='BSD-new',
    packages=['dxskytap'],
    package_data={'dxskytap': ['*.pem']},
    install_requires=['httplib2 >= 0.8','pexpect >= 2.4'],
    tests_require=['nose','coverage'],
    test_suite='test.all',
    url='http://www.dataxu.com',
    version='1.0.0-SNAPSHOT',
    keywords='skytap cloud client rest api development',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.4',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries'
    ],
)
