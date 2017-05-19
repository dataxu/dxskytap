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

import math
from dxskytap.restobject import RestMap, RestObject, RestAttribute

class VPN(RestObject):
    def __init__(self, connect, uid, intial_data):
        super(VPN, self).__init__(connect, "vpns/%s" % (uid), intial_data)
    
    dpd_enabled = RestAttribute('dpd_enabled')
    enabled = RestAttribute('enabled')
    error = RestAttribute('error', readonly=True)
    uid = RestAttribute('id', readonly=True)
    local_peer_ip = RestAttribute('local_peer_ip')
    local_subnet = RestAttribute('local_subnet')
    maximum_segment_size = RestAttribute('maximum_segment_size')
    phase_1_dh_group = RestAttribute('phase_1_dh_group')
    phase_1_encryption_algorithm = RestAttribute('phase_1_encryption_algorithm')
    phase_1_hash_algorithm = RestAttribute('phase_1_hash_algorithm')
    phase_1_sa_lifetime = RestAttribute('phase_1_sa_lifetime')
    # pylint: disable=C0103
    phase_2_authenticatioDn_algorithm = RestAttribute(
        'phase_2_authentication_algorithm')
    phase_2_encryption_algorithm = RestAttribute('phase_2_encryption_algorithm')
    phase_2_perfect_forward_secrecy = RestAttribute(
        'phase_2_perfect_forward_secrecy')
    # pylint: enable=C0103
    phase_2_pfs_group = RestAttribute('phase_2_pfs_group')
    phase_2_sa_lifetime = RestAttribute('phase_2_sa_lifetime')
    remote_peer_ip = RestAttribute('remote_peer_ip')
    status = RestAttribute('status')
    region = RestAttribute('region', readonly=True)

    #u'remote_subnets': [   {   u'cidr_block': u'10.1.0.0/23',
    #                           u'excluded': False,
    #                           u'id': u'10.1.0.0/23'}]
    #u'test_results': {   u'connect': False,
    #                     u'phase1': True,
    #                     u'phase2': True,
    #                     u'ping': False}}
    #u'network_attachments': [   {   u'configuration_id': u'536580',
    #                              u'configuration_name': u'rwh-singleNode',
    #                              u'configuration_type': u'configuration',
    #                              u'connected': True,
    #                              u'network_id': u'339508',
    #                              u'network_name': u'Network 1',
    #                              u'owner_id': u'22638',
    #                              u'owner_name': u'Bill Mepham (bmepham)',
    #                              u'subnet': u'192.168.0.0/24'} ]

    def list_allocations(self, min_net_class=24):
        vpn = self.alldata()
        total = vpn['local_subnet'].split("/")
        alloc = []
        for net in vpn['network_attachments']:
            subnet = net['network']['subnet'].split("/")
            ip_num = VPN.ip_to_number(subnet[0])
            alloc.append((net['network']['configuration_id'], ip_num,
                int(subnet[1]), subnet[0]))
        alloc.sort(key=lambda tup: tup[1])
        start = VPN.ip_to_number(total[0])
        end = start + math.pow(2, 32 - int(total[1]))
        index = start
            
        subnets = []
        for cur in alloc:
            if(index < cur[1]):
                VPN.unallocated(index, cur[1], min_net_class, subnets)
            network = { "configuration_id": cur[0],
                        "subnet": "%s/%d" % (cur[3], cur[2]) }
            subnets.append(network)
            index = cur[1] + math.pow(2, 32 - int(cur[2]))
        if(index < end):
            VPN.unallocated(index, end, min_net_class, subnets)
        return subnets
    
    @staticmethod          
    def unallocated(start, end, min_net_class, results):
        if(start < end):
            inc = min(32 - min_net_class, math.floor(math.log(end - start, 2)))
            power = math.pow(2, inc)
            rem = start % power
            if(rem != 0):
                VPN.unallocated(start, start + rem, min_net_class, results)
                VPN.unallocated(start + rem, end, min_net_class, results)
            else:
                rec = { "configuration_id": "UNALLOCATED",
                        "subnet": "%s/%d" % (VPN.number_to_ip(start),
                             32 - inc) }
                results.append(rec)
                if(inc != 0 and start + power < end):
                    VPN.unallocated(start + power, end, min_net_class, results)
    
    @staticmethod    
    def ip_to_number(ip_addr):
        "convert decimal dotted quad string to long integer"

        hexn = ''.join(["%02X" % long(seg) for seg in ip_addr.split('.')])
        return long(hexn, 16)
    
    @staticmethod
    def number_to_ip(val):
        "convert long int to dotted quad string"
        denom = 256 * 256 * 256
        quad = []
        while denom > 0:
            seg, val = divmod(val, denom)
            quad.append(str(int(seg)))
            denom = denom / 256
        return '.'.join(quad)
    
class VPNs(RestMap):

    def __init__(self, connect):
        super(VPNs, self).__init__(connect, "vpns", 
            lambda conn, data: VPN(conn, data['id'], data))

