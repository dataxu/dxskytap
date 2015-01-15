# Copyright (c) 2014, DataXu Inc.
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

class Company(RestObject):
    def __init__(self, connect):
        super(Company, self).__init__(connect, "company/quotas")
        
    def refresh(self):
        unprocessed = self._connect.get(self._resource)
        self.data = {}
        for group in unprocessed:
            self.data[group['id']] = group
        self._is_full = True

    def concurrent_svms(self):
        return CompanyResourceLimit(self._connect, self._resource,
               self, 'concurrent_svms')

    def concurrent_vms(self):
        return CompanyResourceLimit(self._connect, self._resource,
               self, 'concurrent_vms')

    def concurrent_storage_size(self):
        return CompanyResourceLimit(self._connect, self._resource,
               self, 'concurrent_storage_size')

    def cumulative_svms(self):
        return CompanyResourceLimit(self._connect, self._resource,
               self, 'cumulative_svms')

    def concurrent_public_ips(self):
        return CompanyResourceLimit(self._connect, self._resource,
               self, 'concurrent_public_ips')

    def concurrent_networks(self):
        return CompanyResourceLimit(self._connect, self._resource,
               self, 'concurrent_networks')

class CompanyResourceLimit(RestObject):
    def __init__(self, connect, res, parent, attrname):
        super(CompanyResourceLimit, self).__init__(connect, res,
            parent.alldata().get(attrname),
            is_full=True, parent=parent, parent_attr=attrname)

    quota_type = RestAttribute('quota_type', readonly=True)
    units = RestAttribute('units', readonly=True)
    limit = RestAttribute('limit', readonly=True)
    usage = RestAttribute('subscription', readonly=True)
    max_limit = RestAttribute('max_limit', readonly=True)


