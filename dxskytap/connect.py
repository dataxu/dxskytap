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
 - TimeoutException
 - NoResponseException
'''

try:
    import json as simplejson
except ImportError:
    import simplejson

from base64 import b64encode
import httplib2
import urlparse
import urllib
import signal
import re
import logging

class SkytapException(Exception):
    """
    Base class for Exceptions thrown by dxskytap library.
    """
    pass

class TimeoutException(SkytapException):
    """
    Exception thrown when http request doesn't respond within 
    REQUEST_TIMEOUT limit.
    """
    pass

class NoResponseException(SkytapException):
    """
    Exception thrown when http is successful, but no response
    message is available.
    """
    pass

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
        :request_timeout: throw a TimeoutException if Skytap doesn't respond
            within this window.
        """
        (scheme, host, path, _, _) = urlparse.urlsplit(url)
            
        self.base_url = u"%s://%s" % (scheme, host)
        self.path = path

        self.username = username
        self.password = password
        
        self._request_timeout = request_timeout
        # Create Http class with support for Digest HTTP Authentication
        self.http = httplib2.Http(cache=None, ca_certs=ca_certs)
        self.http.follow_all_redirects = True
        
        self.logger = logging.getLogger('dxskytap')

    def _makeurl(self, resource, args):
        """
        Generate a URL from the resource path and HTTP POST arguments.
        Additionally, a base path maybe defined for this Connection.
        This base path will be prepended to the URL if the base path
        exists.
        """
        path = urllib.quote(resource)
        if args:
            path += u"?" + urllib.urlencode(args)

        parts = [x for x in [self.path, path] if x is not None]
        full_path = u"/".join(parts)
        return urlparse.urljoin(self.base_url, full_path)

    def request(self, url, method, body=None, headers=None):
        """
        HTTP request. Default handling uses 'application/json' for
        request/response, but this can be overridden in the headers.
        """
        if headers is None:
            headers = {}
        encoded_auth = b64encode('%s:%s' % (self.username, self.password))
        headers['User-Agent'] = 'Basic Agent'
        headers['Authorization'] = 'Basic %s' % (encoded_auth)
        
        if method in ["post", "put"]:
            headers['Content-Type'] = 'application/json'
        
        headers['Accept'] = 'application/json'

        if isinstance(body, dict):
            text_body = simplejson.dumps(body)
        else:
            text_body = body

        if body:
            headers['Content-Length'] = str(len(text_body))
        else:
            headers['Content-Length'] = '0'

        return self._perform_request(url, method, text_body, headers)

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
            body_txt = re.escape(body)
        self.logger.debug("%s_body: %s", msg, body_txt)

    def _perform_request(self, url, method, body, headers):
        """
        Internal method for performing the http request after
        Connect.request() generates the final url and header.
        """

        def _request_timeout_handler(_arg1, _arg2):
            """
            Internal function for handling the timeout signal
            around the http.request call.
            """
            raise TimeoutException("Timed out!")
        
        if self.logger.isEnabledFor(logging.DEBUG):
            self._log_http_request(url, method, body, headers)

        tries_remaining = 3
        resp = None
        while resp is None and tries_remaining > 0:
            tries_remaining = tries_remaining - 1
            try:
                signal.signal(signal.SIGALRM, _request_timeout_handler)
                signal.alarm(self._request_timeout)
                resp, content = self.http.request(url, method.upper(),
                    body=body, headers=headers)
                signal.alarm(0)
            except TimeoutException:
                resp = None

        if resp is None:
            raise NoResponseException("Unable to get a response in"
                "a reasonable amount of time.")
        
        content_txt = content.decode('UTF-8')
        if self.logger.isEnabledFor(logging.DEBUG):
            self._log_http_response(resp, content_txt)

        ret_data = {}
        if(content_txt.strip() != ''):
            try:
                ret_data = simplejson.loads(content_txt)
            except ValueError:
                ret_data = content_txt

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
        return self.request(self._makeurl(resource, args),
            "get", body, headers)
    
    def post(self, resource, args = None, body = None, headers=None):
        """
        HTTP POST Request
        """
        return self.request(self._makeurl(resource, args),
            "post", body, headers)

    def put(self, resource, args = None, body = None, headers=None):
        """
        HTTP PUT Request
        """
        return self.request(self._makeurl(resource, args),
            "put", body, headers)
    
    def delete(self, resource, args = None, body = None, headers=None):
        """
        HTTP DELETE Request
        """
        return self.request(self._makeurl(resource, args),
            "delete", body, headers)
