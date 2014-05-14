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
from dxskytap.restobject import  RestBoolAttribute
from dxskytap.tunnels import Tunnel
from dxskytap.attached_vpns import AttachedVPN

class VirtualNetwork(RestObject):
    
    def __init__(self, connect, base_resource, uid, intial_data):
        res = "%s/networks/%s" % (base_resource, uid)
        super(VirtualNetwork, self).__init__(connect, res, intial_data)
        
    uid = RestAttribute('id', readonly=True)
    name = RestAttribute('name')
    domain = RestAttribute('domain')
    gateway = RestAttribute('gateway')
    network_type = RestAttribute('network_type')
    primary_nameserver = RestAttribute('primary_nameserver')
    secondary_nameserver = RestAttribute('secondary_nameserver')
    subnet = RestAttribute('subnet', readonly=True)
    subnet_addr = RestAttribute('subnet_addr')
    subnet_size = RestAttribute('subnet_size')
    tunnelable = RestBoolAttribute('tunnelable')

    def tunnels(self):
        return [Tunnel(self._connect, tunnel['id'], tunnel)
            for tunnel in self.alldata()['tunnels']]
    
    def create_tunnel(self, target_network):
        args = { 'source_network_id': str(self.uid),
                 'target_network_id': str(target_network) }
        result = self._connect.post("tunnels", args)
        return Tunnel(self._connect, result['id'], result)
    
    def attach_vpn(self, vpn):
        body = { 'vpn_id': vpn.uid }
        result = self._connect.post("%s/vpns" % self._resource, body)
        return AttachedVPN(self._connect, self._resource, vpn.uid, result)

    def vpns(self):
        return [AttachedVPN(self._connect, self._resource, att['vpn']['id'],
            att) for att in self.alldata()['vpn_attachments']]        

class VirtualNetworks(RestMap):

    def __init__(self, connect, resource):
        super(VirtualNetworks, self).__init__(connect,
            "%s/networks" % (resource),
            lambda conn, data: VirtualNetwork(conn, resource, data['id'], data))
