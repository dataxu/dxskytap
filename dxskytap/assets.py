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

from dxskytap.restobject import RestMap, RestAttribute
from dxskytap.assignableobject import AssignableObject

class Asset(AssignableObject):
    """
    Generally, a customer asset is any data available in the Skytap
    Cloud context. Typically this is data that a customer has loaded
    into Skytap Cloud to support running applications.
    Assets are top-level elements in the API data model.
    In the current release of the API, Assets can only be viewed, 
    referenced and ownership managed, but not created, modified,
    or deleted.
    
    Attributes
        uid - unique identifier for asset object.
        name - human friendly name for the asset.
        public - True or false this asset is with other users in skytap.
        size - the size of the asset file.
        url - a url that can used to download a copy of the asset.
    """
    def __init__(self, connect, uid, initial_data, user_cls):
        '''
        Constructor
        
        Create a new Asset object
        
        Parameters
            connect - A connect.Connect object used to communicate with the
                Skytap REST API.
            uid - The unique identifier for the Asset object.
            initialData  - A dict containing a partial cache of the name/value 
                attributes for this asset.
        '''
        super(Asset, self).__init__(connect,
            "assets/%s" % (uid),
            initial_data, "assets", user_cls)

    uid = RestAttribute("id", readonly=True)
    name = RestAttribute("name", readonly=True)
    public = RestAttribute("public", readonly=True)
    size = RestAttribute("size", readonly=True)
    url = RestAttribute("url", readonly=True)

class Assets(RestMap):
    """
    A readonly collection of user assets stored in Skytap.
    The Skytap REST API supports a readonly interface for
    assets. There is no way to create or delete assets 
    through this collection.
    """
    def __init__(self, connect, user_cls):
        super(Assets, self).__init__(connect, "assets",
            lambda conn, data: Asset(conn, data['id'], data, user_cls))
