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

class Tunnel(RestObject):
    """
    A network tunnel created by connecting two virtual skytap networks
    together. Note: the networks must use non-overlaping subnets.
    """
    def __init__(self, connect, uid, initial_data):
        super(Tunnel, self).__init__(connect, "tunnels/%s" % (uid), 
            initial_data)
    
    uid = RestAttribute("id", readonly=True)
    status = RestAttribute("status", readonly=True)
    
    def source_network(self):
        """
        Returns the network id for the source network in the tunnel.
        """
        return self.alldata()["source_network"]["id"]

    def target_network(self):
        """
        Returns the network id for the target network in the tunnel.
        """
        return self.alldata()["target_network"]["id"]

    def check_state(self, states=None):
        """
        Return a boolean value yes or no. The tunnel is in one of the 
        states passed in states argument. If states is None, then check
        for any state except 'busy'.
        """
        if states is None:
            return self.status != 'busy'
        elif self.status in states:
            return True
        else:
            return False
    
class Tunnels(RestMap):
    """
    A python dictionary of all the network tunnels in Skytap the user can
    access. The dictionary uses the Tunnel ID value for its key.
    """

    def __init__(self, connect):
        super(Tunnels, self).__init__(connect, "tunnels",
            lambda conn, data: Tunnel(conn, data['id'], data))

    def create_tunnel(self, source_network_id, target_network_id):
        """
        Create a connection between two virtual networks in Skytap.
        The two networks must have non-overlaping subnets, and the
        target network must have the 'tunnelable' attribute set to 
        'True'.
        """
        body = {'source_network_id': str(source_network_id),
                'target_network_id': str(target_network_id)}
        result = self._connect.post("tunnels", body)
        return Tunnel(self._connect, result['id'], result)
