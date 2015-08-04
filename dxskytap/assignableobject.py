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

from dxskytap.restobject import RestObject, RestAttribute
try:
   import urllib.parse as urlparse
except ImportError:
   import urlparse

class AssignableObject(RestObject):
    """
    Assignable Object is a base class for Skytap objects like Configuration and
    Template that can assigned or re-assigned an owner. Assignable Objects can
    also manage access by adding itself to Skytap projects.

    Attributes:
       none
    """

    def __init__(self, connect, resource, initial_data, obj_type, user_cls):
        """
        Constructor for a Assignable object.
    
        Parameters
            connect - the Connect object that managed REST requests to skytap
            resource- the path to skytap resource for this Assignable object
            initialData - a partial dictionary of properties for the Assignable
                object. This partial data is obtained from the parent list
                when the library queries skytap for a list of objects.
        """
        super(AssignableObject, self).__init__(connect, resource,
            initial_data)
        self._obj_type = obj_type
        self._user_cls = user_cls

    owner_url = RestAttribute('owner')

    def owner(self):
        if self.owner_url is None:
            return None
        (_, _, path, _, _) = urlparse.urlsplit(self.owner_url)
        owner_id = path.split('/')[-1]
        return self._user_cls(self._connect, owner_id, {})

    def reassign(self, user, project=None):
        """
        Reassign the user that owns this skytap resource.
        Parameters
            user - The skytap object for the user. Lookup the user in the
                   skytap.users() dictionary.
            project - Reassigning the owner will clear the projects this
                   resource belongs to. You have to option of passing a
                   single project that the resource will be added to.
        """
        body = { 'owner':user.uid }
        if(project is not None):
            body['reassign_context'] = project.uid
        self.data = self._connect.put(self._resource, body=body)

    def add_to_project(self, project, role=None):
        """
        Add this resource to a Skytap project.
        Parameters
            project - The project object can be found in the skytap.projects()
                      dictionary.
            role - Optional parameter used when adding user or group object to
                   a project. Valid values are 'viewer', 'participant', 
                   'editor' or 'manager'.
        """
        project.add(self, self._obj_type, role)
