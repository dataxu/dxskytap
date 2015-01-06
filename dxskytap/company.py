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

from dxskytap.restobject import RestObject

class Company(RestObject):
    def __init__(self, connect):
        super(Company, self).__init__(connect, "company/quotas")

    def company_quota_request(self):
        return Company_Quota(self._connect, self._resource, self.alldata(), self)


class Company_Quota(RestObject):
    def __init__(self, connect, res, initial_data, parent):
        super(Company_Quota, self).__init__(connect, res, initial_data, is_full=True)

        self.list_of_resources_with_limits = ('concurrent_svms', 'concurrent_vms', 'concurrent_storage_size',
        'cumulative_svms', 'concurrent_public_ips', 'concurrent_networks')
        self.quota_fields = ('quota_type', 'units', 'limit', 'usage', 'subscription', 'max_limit')
        self.company_quota_data_structure = {}

        for group in initial_data:
            tmp_dict = {}
            for key, value in group.iteritems():
                tmp_dict[key] = value
            self.company_quota_data_structure[group['id']] = tmp_dict 

    def request_resource_by_id(self, in_id, in_quota_field):

        return_value = None

        if in_id not in self.list_of_resources_with_limits:
            print "Invalid resource type: %s " % str(in_id)
            raise Exception("Unknown resource type for finding a limit")
        if in_quota_field not in self.quota_fields:
            print "Invalid quota field: %s " % str(in_quota_field)
            raise Exception("Unknown quota field")

        get_value = self.company_quota_data_structure[in_id][in_quota_field]
        if get_value is not None:
            return_value = get_value

        return return_value
