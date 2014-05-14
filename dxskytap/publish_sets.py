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

class PublishSetVM(RestObject):
    def __init__(self, connect, res, initial_data, vm_cls):
        super(PublishSetVM, self).__init__(connect, res, initial_data,
            can_delete=True, is_full=True, can_refresh=False)
        self._vm_cls = vm_cls

        
    uid = RestAttribute("id", readonly=True)
    name = RestAttribute("name")
    access = RestAttribute("access")
    desktop_url = RestAttribute("desktop_url")
    run_and_use = RestAttribute("run_and_use")
    
    def virtual_machine(self):
        items = self.alldata()['vm_ref'].split("/")
        res = '/'.join(items[3:-2])
        uid = items[-1]
        return self._vm_cls(self._connect, res, uid, {'id':uid})
    
class PublishSet(RestObject):
    def __init__(self, connect, res, uid, intial_data, vm_cls):
        super(PublishSet, self).__init__(connect, 
            "%s/publish_sets/%s" % (res, uid), intial_data)
        self._vm_cls = vm_cls
        
    uid = RestAttribute("id", readonly=True)
    name = RestAttribute("name")
    password = RestAttribute("password")
    publish_set_type = RestAttribute("publish_set_type")
    start_time = RestAttribute("start_time")
    end_time = RestAttribute("end_time")
    time_zone = RestAttribute("time_zone")
    url = RestAttribute("url", readonly=True)
    useSmartClient = RestAttribute("use_smart_client", readonly=True)
    
    def published_vms(self):
        return [PublishSetVM(self._connect, self._resource, item, self._vm_cls)
            for item in self.alldata()['vms']]
    
class PublishSets(RestMap):

    def __init__(self, connect, resource, vm_class):
        super(PublishSets, self).__init__(connect,
            "%s/publish_sets" % (resource),
            lambda conn, data: PublishSet(conn, resource, data['id'], data,
                vm_class))
        self._base_resource = resource
        self._vm_class = vm_class

    def create_publish_set(self, name, publish_set_type, password, 
        start_time=None, end_time=None, time_zone=None):

        body = { 'name': name,
                 'publish_set_type': publish_set_type,
                 'password': password }
        if(start_time is not None):
            body['start_time'] = start_time
        if(end_time is not None):
            body['end_time'] = end_time
        if(time_zone is not None):
            body['time_zone'] = time_zone
        result = self._connect.post("publish_sets", body=body)
        return PublishSet(self._connect, self._base_resource, result['id'],
            result, self._vm_class)
