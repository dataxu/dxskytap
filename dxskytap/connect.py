# Copyright (c) 2013, DataXu Inc.
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of DataXu Inc. nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL DATAXU INC. BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''
Provide a HTTP Connection to the Skytap REST API.

Classes:
 - Connect

Exceptions:
 - SkytapException
 - NoResponseException
'''

import urllib3.contrib.pyopenssl
urllib3.contrib.pyopenssl.inject_into_urllib3()

import logging
from re import escape
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from requests.exceptions import Timeout
from time import sleep

try:
   from urlparse import urlsplit, urljoin
except ImportError:
   from urllib.parse import urlsplit, urljoin


class SkytapException(Exception):
    """
    Base class for Exceptions thrown by dxskytap library.
    """
    pass

class NoResponseException(SkytapException):
    """
    Exception thrown when http is successful, but no response
    message is available.
    """
    pass

class SecureAdapter(HTTPAdapter):
    """
    Define constructor for passing root certificate object
    """
    def __init__(self, ca_certs=None):
        self.ca_certs = ca_certs
        super(SecureAdapter, self).__init__()

    """
    HTTP Adapter for requests module to force use of TLS v1.2
    """
    def init_poolmanager(self, connections, maxsize, block=False):
        """
        initialize connection pool for HTTP
        """
        self.poolmanager = PoolManager(num_pools=connections,
                                   maxsize=maxsize,
                                   block=block,
                                   cert_reqs='CERT_REQUIRED',
                                   ca_certs=self.ca_certs)

class Connect(object):
    """
    Class for managing the core REST HTTP Connection.
    """


    def __init__(self, url, ca_certs, username, password, request_timeout):
        """
        Construct a HTTP Connection class to the Skytap REST API.

        :url: REST url to access
        :ca_certs: certificates used for authentication
        :username: authenticating username
        :password: username's password
        :request_timeout: throw a NoResponseException if Skytap doesn't respond
            within this window.
        """
        (scheme, host, path, _, _) = urlsplit(url)
            
        self.base_url = u"%s://%s" % (scheme, host)
        self.path = path

        self.username = username
        
        self._request_timeout = request_timeout
        # Create Http class with support for Digest HTTP Authentication
        self.session = requests.Session()
        self.session.mount('https://', SecureAdapter(ca_certs))        
        self.session.auth = (username, password)
 
        self.logger = logging.getLogger('dxskytap')

    def _makeurl(self, resource):
        return urljoin(self.base_url, resource)

    def request(self, url, method, params=None, body=None, headers=None,
                accept_type='application/json'):
        """
        HTTP request. Default handling uses 'application/json' for
        request/response, but this can be overridden in the headers.
        """
        data = None
        json = None
        if headers is None:
            headers = {}
        
        if method in ["post", "put"]:
            headers['Content-Type'] = 'application/json'
        
        headers['Accept'] = accept_type

        if isinstance(body, dict):
            json = body
        else:
            data = body

        return self._perform_request(url, method, params, data, json, headers, accept_type)

    def _log_http_request(self, url, method, body, headers):
        """
        Append HTTP request message to the logger.
        """
        self.logger.debug('send: %s %s', method.upper(), url)
        self._log_header_body("request", headers, body)

    def _log_http_response(self, headers, body):
        """
        Append HTTP response message to the logger.
        """
        self._log_header_body("response", headers, body)

    def _log_header_body(self, msg, headers, body):
        """
        Append contents of HTTP request/response header and message
        body to the logger.
        """
        for (key, val) in headers.items():
            self.logger.debug("%s_header: %s: %s", msg, key, val)
        if body is None:
            body_txt =  ''
        else:
            body_txt = escape(body)
        self.logger.debug("%s_body: %s", msg, body_txt)

    def _perform_request(self, url, method, params, body, json, headers, accept_type):
        """
        Internal method for performing the http request after
        Connect.request() generates the final url and header.
        """
        if self.logger.isEnabledFor(logging.DEBUG):
            self._log_http_request(url, method, body, headers)

        tries_remaining = 5
        resp = None
        while resp is None and tries_remaining > 0:
            tries_remaining = tries_remaining - 1
            try:
                resp = self.session.request(
                    method=method.upper(),
                    url=url,
                    params=params,
                    data=body,
                    json=json,
                    headers=headers,
                    timeout=self._request_timeout)
                if resp.status_code in (423, 429):
                    wait_time = 10
                    if 'Retry-After' in resp.headers:
                        wait_time = int(resp.headers['Retry-After'])
                    sleep(wait_time)    
            except Timeout:
                resp = None

        if resp is None:
            raise NoResponseException("Unable to get a response in"
                "a reasonable amount of time.")
        
        if self.logger.isEnabledFor(logging.DEBUG):
            self._log_http_response(resp.headers, resp.text)
        
        ret_data = None
        if accept_type != 'application/json':
            ret_data = resp.text
        else:
            if(resp.text.strip() != ''):
                ret_data = resp.json()

            accepted_values = ['', False, None, 'None']
            if(isinstance(ret_data, dict) and 
                ret_data.get('errors','') not in accepted_values):

                raise ValueError(ret_data['errors'])
            elif(isinstance(ret_data, dict) and 
                ret_data.get('error','') not in accepted_values):

                raise ValueError(ret_data['error'])
        return ret_data

    def get(self, resource, args = None, body = None,  headers=None):
        """
        HTTP GET Request
        """
        return self.request(self._makeurl(resource), params=args,
            method="get", body=body, headers=headers)
    
    def post(self, resource, args = None, body = None, headers=None):
        """
        HTTP POST Request
        """
        return self.request(self._makeurl(resource), params=args,
            method="post", body=body, headers=headers)

    def put(self, resource, args = None, body = None, headers=None):
        """
        HTTP PUT Request
        """
        return self.request(self._makeurl(resource), params=args,
            method="put", body=body, headers=headers)
    
    def delete(self, resource, args = None, body = None, headers=None):
        """
        HTTP DELETE Request
        """
        return self.request(self._makeurl(resource), params=args,
            method="delete", body=body, headers=headers)
