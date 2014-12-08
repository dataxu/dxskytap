===========================
Skytap API Client
===========================

This module contains a client library for accessing
[Skytap](http://www.skytap.com)'s cloud API . This code was originally
developed at [DataXu](http://www.dataxu.com) and released as open source.

Code Style
==========

Please follow `PEP-008 <http://www.python.org/dev/peps/pep-0008/>`_.

Install
======

The best way to install the `dxskytap` tool is to install direct from the 
github using pip:

```
# Replace [TAG] with a dxskytap git ref (such as master)
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
$ python setup.py nosetests
```

To run any individual tests, call nosetests directly. Refer to 
http://nose.readthedocs.org/en/latest/usage.html for details on using nose.

When you add a new test, be sure to add it as an import to all.py

