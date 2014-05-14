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

from dxskytap.restobject import RestMap, RestObject, RestAttribute

class User(RestObject):
    def __init__(self, connect, uid, intial_data):
        super(User, self).__init__(connect,
            "users/%s" % (uid), intial_data)
    
    email = RestAttribute("email")
    first_name = RestAttribute("first_name")
    uid = RestAttribute("id", readonly=True)
    last_name = RestAttribute("last_name")
    login_name = RestAttribute("login_name")
    title = RestAttribute("title")
    account_role = RestAttribute("account_role")
    activated = RestAttribute("activated")
    can_export = RestAttribute("can_export")
    can_import = RestAttribute("can_import")
    sra_compression = RestAttribute("sra_compression")
    lockversion = RestAttribute("lockversion", readonly=True)
    password = RestAttribute("password")
    #u'configurations': [],
    #u'assets': [],
    #u'quotas': [],
    #u'templates': []

class Users(RestMap):

    def __init__(self, connect):
        super(Users, self).__init__(connect, "users",
            lambda conn, data: User(conn, data['id'], data),
            name_field='login_name')

    def create_user(self, login_name,  password, email):
        body = { 'login_name':login_name,
                 'password':password,
                 'email':email }
        result = self._connect.post("users", body)
        return User(self._connect, result['id'], result)
