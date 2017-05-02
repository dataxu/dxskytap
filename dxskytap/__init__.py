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
The dxskytap module is a library that wraps the Skytap REST API. Dxskytap
makes it easier for users to develop python applications for test automation.

Classes:
 - Skytap
'''

from dxskytap.assets import Assets
from dxskytap.users import Users, User
from dxskytap.configurations import Configurations, Configuration
from dxskytap.templates import Templates, Template
from dxskytap.vpns import VPNs
from dxskytap.projects import Projects
from dxskytap.reports import Reports
from dxskytap.company import Company

try:
   from ConfigParser import ConfigParser
except ImportError:
   from configparser import ConfigParser

import os
import sys
from dxskytap.connect import Connect   
from dxskytap.settings import SKYTAP_URL, DEFAULT_SKYTAP_CONFIG_FILE

__all__ = ["Skytap"]

class Skytap(object):
    '''
    This class is connector providing access to the Skytap REST API.
    To use this class setup your credentials in ~/.skytap_config and
    construct an instance of this class.
    
    import dxskytap
    
    skytap = dxskytap.Skytap()
    
    Once created all objects and functions in the Skytap API are accessible
    through the skytap object.
    '''

    def __init__(self, username=None, password=None, request_timeout=(9.1, 300)):
        '''
        Constructor
        
        To authorize access to Skytap Cloud resources, each API request must
        include a security credential encoded in an HTTP "Basic Auth" header
        (for more details on "Basic Auth" see
        http://httpd.apache.org/docs/1.3/howto/auth.html#intro). By default,
        Skytap usernames and passwords are used with Basic Auth. If an 
        account administrator has enabled the "Require security
        tokens for API requests" option under Access Policy, security 
        tokens must be used in place of passwords. When this option is 
        enabled, each Skytap user can find their current security token 
        under "My Account".
        
        The user name and password can be passed into this constructor or 
        stored in the ~/.skytap_config file. A sample .skytap_config file 
        is shown below:
        [credentials]
        username: fakeuser
        password: <password>

        :username: authenticating username
        :password: username's password
        :request_timeout: throw a TimeoutException if Skytap doesn't respond
            within this window. Default: 5 minutes
        '''
        if username is None and password is None:
            config = ConfigParser()
            filepath = os.path.expanduser(os.getenv('SKYTAP_CONFIG',
                DEFAULT_SKYTAP_CONFIG_FILE))
            config.read(filepath)
            if(config.has_option("credentials", "username")
               and config.has_option("credentials", "password")):
                username = config.get("credentials", "username")
                password = config.get("credentials", "password")
            else:
                raise Exception("No login credentials specified "
                    "in ~/.skytap_config")
        path = os.path.dirname(sys.modules[Skytap.__module__].__file__)
        self.connect = Connect(SKYTAP_URL, None, username, password,
            request_timeout)
    
    def assets(self):
        """
        This function returns the dictionary of assets that the
        logged in user is able to access. 
        """
        return Assets(self.connect, User)
    
    def users(self):
        """
        This function returns the dictionary of users managed by the
        Skytap Account. 
        """
        return Users(self.connect)

    def company(self):
        """
        This function returns company quota numbers
        """
        return Company(self.connect)
    
    def projects(self):
        """
        This function returns the dictionary of projects the user can access in
        Skytap.
        """
        return Projects(self.connect)

    def configurations(self):
        """
        This function returns the dictionary of configurations that the 
        logged in user is able to access. 
        """
        return Configurations(self.connect, Template, User)
    
    def templates(self):
        """
        This function returns the dictionary of templates that the logged in
        user is able to access. 
        """
        return Templates(self.connect, Configuration, User)
    
    def vpns(self):
        """
        This function returns the dictionary of vpns connection setup for the
        Skytap Account.
        """
        return VPNs(self.connect)

    def reports(self):
        return Reports(self.connect)
