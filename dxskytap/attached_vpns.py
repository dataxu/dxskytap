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
from dxskytap.restobject import RestBoolAttribute
from dxskytap.vpns import VPN

class AttachedVPN(RestObject):
    
    def __init__(self, connect, base_resource, vpn_id, intial_data):
        res = "%s/vpns/%s" % (base_resource, vpn_id)
        RestObject.__init__(self, connect, res, intial_data, is_full=True)

    uid = RestAttribute('id', readonly=True)
    connected = RestBoolAttribute('connected')

    def network_id(self):
        return self.alldata()['network']['id']

    def configuration_id(self):
        return self.alldata()['network']['configuration_id']

    def vpn_id(self):
        return self.alldata()['vpn']['id']

    def vpn(self):
        data = self.alldata()['vpn']
        'vpns/%s' % (self.vpn_id())
        return VPN(self._connect, self.vpn_id(), data)

    def detach(self):
        return self.delete()


class AttachedVPNs(RestMap):

    def __init__(self, connect, res):
        RestMap.__init__(self, connect, "%s/vpns" % (res),
            lambda conn, data: AttachedVPN(conn, res, data['vpn']['id'], data))
