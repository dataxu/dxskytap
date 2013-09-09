Skytap Setup
============

The Skytap API Python Library can be installed from the releng git repository::

    git clone git@github.com:dataxu/dxskytap.git

To install the library in your local python, run the following from the dxskytap project::

    python setup.py install

.. _credentials:

Credential Setup
----------------
To authenticate this module expects your credentials to be found in a config file here ~/.skytap_config in the form:

::

    [credentials]
    username: <username>
    password: <API token>

Note: your API token is found here: `<https://cloud.skytap.com/account>`_
