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

from dxskytap.vms import VirtualMachine, VirtualMachines
from dxskytap.networks import VirtualNetworks
from dxskytap.tags import Notes, Labels
from dxskytap.publish_sets import PublishSets
from dxskytap.restobject import RestMap, RestAttribute, SkytapException
from dxskytap.assignableobject import AssignableObject
from dxskytap.stateful import StatefulObject
import time

class Configuration(AssignableObject, StatefulObject):
    """
    Like a template, a configuration is a specification that describes one or more
    virtual machine images, associated resources, and metadata around ownership,
    composition and resources. Unlike a template, many more of the properties of a
    configuration may be modified. More importantly, a configuration can be run.
    
    Attributes:
        runstate
        uid
        name
        url
        disable_internet
        error
        lockversion
        routable
        suspendOnIdle
        useSmartClient
    """

    def __init__(self, connect, uid, initial_data, template_cls, user_cls):
        """
        Constructor for a Configuration object.
    
        Parameters
            connect - the Connect object that managed REST requests to skytap
            uid - the skytap unique identifier for the Configuration object
            initialData - a partial dictionary of properties for the Configuration.
                This partial data is obtained from the Configurations object when
                it queries skytap for a list of configurations.
            templateCls - This parameter a reference to the dxskytap.Template
                class. It is required as a parameter to solve a dependency
                problem, which is explained here.
        """
        super(Configuration, self).__init__(connect,
            "configurations/%s" % (uid),
            initial_data, "configurations", user_cls)
        self._template_cls = template_cls
        
    uid = RestAttribute('id', readonly=True)
    name = RestAttribute('name')
    url = RestAttribute('url', readonly=True)
    disable_internet = RestAttribute('disable_internet')
    error = RestAttribute('error', readonly=True)
    lockversion = RestAttribute('lockversion', readonly=True)
    routable = RestAttribute('routable')
    suspendOnIdle = RestAttribute('suspend_on_idle')
    useSmartClient = RestAttribute('use_smart_client')
    region = RestAttribute('region', readonly=True)
    
    def publish_sets(self):
        return PublishSets(self._connect, self._resource, VirtualMachine)
    
    def vms(self):
        return VirtualMachines(self._connect, self._resource)
    
    def networks(self):
        return VirtualNetworks(self._connect, self._resource)
    
    def notes(self):
        return Notes(self._connect, self._resource)
    
    def labels(self):
        return Labels(self._connect, self._resource, "ConfigurationTemplate")
    
    def merge_template(self, template_id, vm_ids=None):
        body = {'template_id':template_id}
        if(vm_ids is not None):
            body['vm_ids'] = vm_ids 
        return self._connect.put(self._resource, body=body)

    def create_template(self, vm_ids=None):
        body = {'configuration_id':self.uid}
        if(vm_ids is not None):
            body['vm_ids'] = vm_ids
        result = self._connect.post("templates", body=body)
        return self._template_cls(self._connect, result['id'], result,
            Configuration, self._user_cls)

    def wait_for(self, states=None, check_interval=15, check_limit=20):
        resources = [self]
        resources.extend(self.vms().values())
        for network in self.networks().values():
            resources.extend(network.tunnels())
        # TODO: add VPN to resource list
        remaining = check_limit
        ready = False
        while not ready and remaining > 0:
            remaining -= 1
            ready = True
            for res in resources:
                try:
                    res.refresh()
                except ValueError:
                    pass
                ready &= res.check_state(states)
            if not ready:
                time.sleep(check_interval)
        if not ready:
            raise SkytapException("Failed to wait for state change on "
                "configuration %s" % self.uid)

class Configurations(RestMap):

    def __init__(self, connect, template_cls, user_cls):
        super(Configurations, self).__init__(connect, "configurations",
            lambda conn, data: Configuration(conn, data['id'], data,
                template_cls, user_cls))
        self._template_cls = template_cls
        self._user_cls = user_cls
        
    def create_configuration(self, template_id):
        args = { 'template_id':template_id }
        result = self._connect.post("configurations", args)
        return Configuration(self._connect, result['id'], result, 
           self._template_cls, self._user_cls)
        
        
    
