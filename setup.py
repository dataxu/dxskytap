"""
(c) Copyright 2013, 2014. DataXu, Inc. All Rights Reserved.
:license:   BSD-new, see LICENSE for more details.

dx_skytap module setup and package.
"""

import re
import sys

from setuptools import setup, Command, find_packages

VERSIONFILE = "dxskytap/version.py"
VERSION_REGEX = r"^__version__ = ['\"]([^'\"]*)['\"]"

with open(VERSIONFILE, "rt") as version_file:
    version_data = version_file.read()
    match_obj = re.search(VERSION_REGEX, version_data, re.M)
if match_obj:
    version = match_obj.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

class PylintCommand(Command):
    user_options = [
        ('pylint-output=', None, "Output results to a file")]

    def initialize_options(self):
        self.pylint_output = 'pylint.log'

    def finalize_options(self):
        pass

    def run(self):
        if self.distribution.install_requires:
            self.distribution.fetch_build_eggs(self.distribution.install_requires)

        if self.distribution.tests_require:
            self.distribution.fetch_build_eggs(self.distribution.tests_require)
        self.lint_output = open(self.pylint_output, 'w')
        stdout, sys.stdout = sys.stdout, self.lint_output
        stderr, sys.stdout = sys.stderr, self.lint_output

        packages = find_packages(exclude=["*tests", "*tests*", "tests*", "tests"])

        import os.path
        setup_directory = os.path.dirname(os.path.realpath(__file__))
        args = ["--rcfile=" + os.path.join(setup_directory, ".pylintrc"), "--msg-template='{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}'"]

        from pylint.lint import Run
        from pylint.reporters.text import TextReporter
        Run(packages + args, reporter=TextReporter(stdout), exit=False)
        sys.stdout = stdout
        sys.stderr = stderr

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
    install_requires=[
        'requests >= 2.10',
        'pexpect >= 2.4, < 4.0',
        'urllib3 >= 1.20',
        'pyOpenSSL >= 0.14',
        'cryptography >= 1.3.4',
        'idna >= 2.0.0'],
    cmdclass={'pylint': PylintCommand},
    tests_require=['nose','coverage'],
    test_suite='test.all',
    url='http://www.dataxu.com',
    version=version,
    keywords='skytap cloud client rest api development',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
)
