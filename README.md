===========================
DataXu Skytap API Utilities
===========================

This module contains utilities for accessing SkyTap's available API
functions. This code was originally developed at [DataXu](www.dataxu.com)
and released as open source.

Code Style
==========

Please follow `PEP-008 <http://www.python.org/dev/peps/pep-0008/>`_.

Install
======

The only way to run the `dxautoskytap` tool is to install from pip:

```
# Replace [TAG] with a dxskytap git ref
  $ pip install git+git@github.com:dataxu/dxskytap.git@[TAG]#egg=dxskytap

# Example
  $ pip install git+git@github.com:dataxu/dxskytap.git@latest-stable#egg=dxskytap
```

To install, from this directory:

```
$ sudo python setup.py install
```

Credential Setup
----------------

To authenticate this module expects your credentials to be found in a
config file here \~/.skytap\_config in the form:

    [credentials]
    username: <username>
    password: <API token>

Note: your API token is found here: https://cloud.skytap.com/account

Tests
=====

To run all tests, from this directory:

```bash
$ python -m test.all
```

To run any individual test, just replace "all" with the name of the test.

When you add a new test, be sure to add it as an import to all.py

