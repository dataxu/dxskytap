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

class PublicIP(RestObject):
    
    def __init__(self, connect, base_resource, uid, initial_data):
        res = "%s/public_ips/%s" % (base_resource, uid)
        super(PublicIP, self).__init__(connect, res, initial_data)
        
    uid = RestAttribute('id', readonly=True)
    address = RestAttribute('address')

    
class PublicIPs(RestMap):

    def __init__(self, connect, resource):
        super(PublicIps, self).__init__(connect,
            "%s/public_ips" % (resource),
            lambda conn, data: PublicIP(conn, resource, data, data))
        
class PublishedService(RestObject):
    
    def __init__(self, connect, base_resource, uid, initial_data):
        res = "%s/services/%s" % (base_resource, uid)
        super(PublishedService, self).__init__(connect, res,
            initial_data)
        
    uid = RestAttribute('id', readonly=True)
    external_port = RestAttribute('external_port', readonly=True)
    internal_port = RestAttribute('internal_port')
    external_ip = RestAttribute('external_ip', readonly=True)
    
class PublishedServices(RestMap):

    def __init__(self, connect, resource):
        super(PublishedServices, self).__init__(connect,
            "%s/services" % (resource),
            lambda conn, data: PublishedService(conn, resource, data['id'],
                data))

class Interface(RestObject):
    def __init__(self, connect, base_resource, uid, intial_data):
        res = "%s/interfaces/%s" % (base_resource, uid)
        super(Interface, self).__init__(connect, res, intial_data)
    
    uid = RestAttribute("id", readonly=True)
    hostname = RestAttribute("hostname")
    # pylint: disable=C0103
    ip = RestAttribute("ip")
    # pylint: enable=C0103
    mac = RestAttribute("mac")
    network_id = RestAttribute("network_id", readonly=True)
    network_name = RestAttribute("network_name", readonly=True)
    network_subnet = RestAttribute("network_subnet", readonly=True)
    network_type = RestAttribute("network_type", readonly=True)
    nic_type = RestAttribute("nic_type")
    status = RestAttribute("status", readonly=True)
    vm_id = RestAttribute("vm_id", readonly=True)
    vm_name = RestAttribute("vm_name", readonly=True)
    public_ips_count = RestAttribute("public_ips_count", readonly=True)
    services_count = RestAttribute("services_count", readonly=True)
    
    # FIX PUBLIC IPs TO INCLUDE ADD and DELETE
    def public_ips(self):
        return [ips['address'] for ips in self.alldata()['public_ips']]
    
    def services(self):
        return PublishedServices(self._connect, self._resource)
    
    
class Interfaces(RestMap):
    
    def __init__(self, connect, resource):
        super(Interfaces, self).__init__(connect,
            "%s/interfaces" % (resource),
            lambda conn, data: Interface(conn, resource, data['id'], data),
            name_field='network_name')
