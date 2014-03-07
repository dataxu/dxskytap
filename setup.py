"""
(c) Copyright 2013. DataXu, Inc. All Rights Reserved.

dx_skytap module setup and package.
"""

from setuptools import setup

setup(
    name='dxskytap',
    author='DataXu',
    author_email='rcarey@dataxu.com',
    description='DataXu Utilities for Skytap',
    license='BSD-new',
    packages=['dxskytap'],
    package_data={'dxskytap': ['*.pem']},
    install_requires=['httplib2 >= 0.8','pexpect >= 2.4'],
    setup_requires=['httplib2', 'pexpect'],
    url='http://www.dataxu.com',
    version='0.9.1'
)
