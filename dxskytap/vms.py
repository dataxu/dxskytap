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
from dxskytap.interfaces import Interfaces
from dxskytap.hardware import Hardware
from dxskytap.tags import Notes, Labels, Credentials
from dxskytap.publish_sets import PublishSet
from dxskytap.stateful import StatefulObject

class VirtualMachine(StatefulObject):
    
    def __init__(self, connect, base_resource, uid, initial_data):
        res = "%s/vms/%s" % (base_resource, uid)
        super(VirtualMachine, self).__init__(connect, res, initial_data)
    
    uid = RestAttribute('id', readonly=True)
    name = RestAttribute('name')
    assetId = RestAttribute('asset_id')
    can_change_object_state = RestAttribute('can_change_object_state')
    desktop_resizable = RestAttribute('desktop_resizable')
    error = RestAttribute('error', readonly=True)
    local_mouse_cursor = RestAttribute('local_mouse_cursor')
    
    def credentials(self):
        return Credentials(self._connect, self._resource)
    
    def notes(self):
        return Notes(self._connect, self._resource)
    
    def labels(self):
        return Labels(self._connect, self._resource, "VmInstance")

    def interfaces(self):
        return Interfaces(self._connect, self._resource)
    
    def mount_iso(self, asset_id):
        self._connect.put(self._resource, args={'asset_id':asset_id})

    def hardware(self):
        return Hardware(self._connect, self._resource, self.data['hardware'],
            self)
 
    @classmethod   
    def _extract_path(cls, resource_paths):
        for path in resource_paths:
            items = path.split("/")
            yield ('/'.join(items[3:-2]), items[-1])
            
    def publish_sets(self):
        publish_set_data = self.alldata().get('publish_set_refs') or []
        path_tuples = self._extract_path(publish_set_data)
        return [PublishSet(self._connect, pset[0], pset[1], {}, VirtualMachine) 
            for pset in path_tuples]
    
class VirtualMachines(RestMap):

    def __init__(self, connect, resource):
        super(VirtualMachines, self).__init__(connect,
            "%s/vms" % (resource),
            lambda conn, data: VirtualMachine(conn, resource, data['id'], data))
