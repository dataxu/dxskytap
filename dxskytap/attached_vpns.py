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
from dxskytap.restobject import RestBoolAttribute
from dxskytap.vpns import VPN

class AttachedVPN(RestObject):
    """
    This object represents the relationship between a Virtual Network
    and a VPN. A Virtual Network can be attached to multiple VPNs, and
    a VPN can have multiple Virtual Networks. This object represent a
    single pair of a an Attached Virtual Network, and the VPN it is 
    attached to.
    """ 
    
    def __init__(self, connect, base_resource, vpn_id, intial_data):
        res = "%s/vpns/%s" % (base_resource, vpn_id)
        super(AttachedVPN, self).__init__(connect, res, intial_data,
            is_full=True)

    uid = RestAttribute('id', readonly=True)
    connected = RestBoolAttribute('connected')

    def network_id(self):
        """
        Return the skytap id for the Virtual Network attached to the
        VPN.
        """
        return self.alldata()['network']['id']

    def configuration_id(self):
        """
        Every virtual network belongs to a Skytap configuration. This
        method returns the id of the configuration that the attached
        virtual network belongs to.
        """
        return self.alldata()['network']['configuration_id']

    def vpn_id(self):
        """
        Return the id for the attached VPN.
        """
        return self.alldata()['vpn']['id']

    def vpn(self):
        """
        Return the VPN object the virtual network is attached to.
        """
        data = self.alldata()['vpn']
        return VPN(self._connect, self.vpn_id(), data)

    def detach(self):
        """
        Detach the virtual network from the VPN. This method is
        equivalent to calling delete() on this object.
        """
        return self.delete()

