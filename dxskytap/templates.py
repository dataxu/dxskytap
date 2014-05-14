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

from dxskytap.vms import VirtualMachines
from dxskytap.networks import VirtualNetworks
from dxskytap.restobject import RestMap, RestAttribute, SkytapException
from dxskytap.assignableobject import AssignableObject
import time

class Template(AssignableObject):
    """
    A template is a specification of one or more virtual machine images,
    plus associated resources such as network configurations, as well as
    metadata such as notes and tags.

    The purpose of a template is to serve as a blueprint from which any
    number of runnable configurations can be created. As such, a template
    is not directly runnable, and there are constraints on the ways a
    template can be modified once created. Many of the template attributes
    in the API are only informative, and cannot be modified unless working
    on an equivalent configuration. For example, the "runstate" attribute
    will list the state of the VMs in this template, but cannot be changed
    in the API.
    """
    
    def __init__(self, connect, uid, intial_data, configuration_cls, user_cls):
        super(Template, self).__init__(connect, "templates/%s" % (uid),
            intial_data, "templates", user_cls)
        self._configuration_cls = configuration_cls
        
    uid = RestAttribute('id', readonly=True)
    name = RestAttribute('name')
    url = RestAttribute('url', readonly=True)
    busy = RestAttribute('busy', readonly=True)
    description = RestAttribute('description')
    lockversion = RestAttribute('lockversion', readonly=True)
    public = RestAttribute('public')
    tagList = RestAttribute('tag_list')
    region = RestAttribute('region', readonly=True)
                    
    def vms(self):
        return VirtualMachines(self._connect, self._resource)
            
    def networks(self):
        return VirtualNetworks(self._connect, self._resource)
    
    def create_configuration(self, vm_ids=None):
        body = {'template_id':self.uid}
        if vm_ids is not None:
            body['vm_ids'] = vm_ids
        result = self._connect.post("configurations", body=body)
        return self._configuration_cls(self._connect, result['id'],
            result, Template, self._user_cls)

    def wait_for(self, check_interval=15, check_limit=20):
        remaining = check_limit
        busy = True
        while busy and remaining > 0:
            remaining -= 1
            self.refresh()
            busy = self.busy
            if busy:
                time.sleep(check_interval)
        if busy:
            raise SkytapException("Failed to wait for state change on "
                "template %s" % self.uid)

class Templates(RestMap):

    def __init__(self, connect, configuration_cls, user_cls):
        super(Templates, self).__init__(connect, "templates",
            lambda conn, data: Template(conn, data['id'], data, 
                configuration_cls, user_cls))
        self._configuration_cls = configuration_cls
        self._user_cls = user_cls

    def create_template(self, configuration_id, publish_sets):
        args = { 'configuration_id': configuration_id,
                 'publish_sets': publish_sets }
        result = self._connect.post("templates", args)
        return Template(self._connect, result['id'], result, 
            self._configuration_cls, self._user_cls)


