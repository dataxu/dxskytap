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

"""
Classes:
   Project - a Skytap Project used to share configurations, templates and 
      assets used by a group of users for a specific project.
   Projects - a python dictionary of all Skytap projects the user has access
       to.
"""

from dxskytap.restobject import RestMap, RestObject
from dxskytap.restobject import RestAttribute, RestBoolAttribute
from dxskytap.configurations import Configuration
from dxskytap.templates import Template
from dxskytap.users import User

class Project (RestObject):
    """
    A project is a simple object in skytap used to share resources
    (configurations, templates and assets) between users. Add 
    resources to projects and assign users roles as part of a project.

    Attributes:
        uid
        name
        summary
        show-project-members
        auto-add-role-name
    """

    def __init__(self, connect, uid, initial_data):
        """
        Constructor for a Project object.
    
        Parameters
            connect - the Connect object that managed REST requests to skytap
            uid - the skytap unique identifier for the Configuration object
            initialData - a partial dictionary of properties for the Project.
                This partial data is obtained from the Projects object when
                it queries skytap for a list of projects.
        """
        super(Project, self).__init__(connect, "projects/%s" % (uid),
            initial_data)
        
    uid = RestAttribute('id', readonly=True)
    name = RestAttribute('name')
    summary = RestAttribute('summary')
    showProjectMembers = RestBoolAttribute('show-project-members')
    autoAddRoleName = RestAttribute('auto-add-role-name')

    def templates(self):
        """
        Returns a list of all Skytap templates that are part of this
        project.
        """
        results = self._connect.get("templates")
        return [Template(self._connect, data['id'], data, Configuration, User)
            for data in results]

    def configurations(self):
        """
        Returns a list of all Skytap configurations that are part of this
        project.
        """
        results = self._connect.get("configurations")
        return [Configuration(self._connect, data['id'], data, Template, User)
            for data in results]

    def add(self, obj, obj_type, role=None):
        """
        :obj: Skytap Resource to be added to the project
        :obj_type: configurations, templates, assets, group, or users
        :role: viewer, participant, editor or manager
        """
        args = {} 
        if role is not None: 
            args['role'] = str(role)
        self._connect.post("%s/%s/%s" % (self._resource, obj_type, obj.uid),
            args=args)

class Projects(RestMap):
    """
    A dictionary containing all of the user's Skytap Projects.
    """

    def __init__(self, connect):
        super(Projects, self).__init__(connect, "projects",
            lambda conn, data: Project(conn, data['id'], data))

    def create_project(self, name):
        """
        Create a new Skytap project.
        """
        args = { 'name': name }
        result = self._connect.post("projects", args)
        return Project(self._connect, result['id'], result)
