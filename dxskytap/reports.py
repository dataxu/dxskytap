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

from dxskytap.restobject import RestObject, RestAttribute, RestBoolAttribute
from dxskytap.connect import SkytapException
import csv
import time

class UsageReport(RestObject):
    def __init__(self, connect, uid, initial_data):
        '''
        Constructor
        
        Create a new Usage Report
        
        Parameters
            connect - A connect.Connect object used to communicate with the
                Skytap REST API.
            uid - The unique identifier for the Usage Report object.
            initialData  - A dict containing a partial cache of the name/value 
                attributes for this usage report.
        '''
        super(UsageReport, self).__init__(connect,
            "reports/%s" % uid,
            initial_data)

    uid = RestAttribute("id", readonly=True)
    start_date = RestAttribute("start_date")
    end_date = RestAttribute("end_date")
    utc = RestBoolAttribute("utc")
    resource_type = RestAttribute("resource_type")
    region = RestAttribute("region")
    ready = RestBoolAttribute("ready", readonly=True)
    url = RestAttribute("url", readonly=True)

    def wait_for(self, check_interval=10, check_limit=10):
        """
        Blocking call to wait for the usage report to be
        ready. Once the report is ready (finished generating),
        the get_reader() method can be used to read the data
        for the report.
        """
        remaining = check_limit
        ready = False
        while not ready and remaining > 0:
            remaining -= 1
            self.refresh()
            ready = self.ready
            if not ready:
                time.sleep(check_interval)
        if not ready:
            raise SkytapException("Timeout waiting for report %s"
                   "to be ready." % self.uid)

    def get_reader(self):
        """
        Returns a reader for the usage report data. The returned
        object is a csv.DictReader. Use method next() on DictReader
        to read each row of the report. Each row is a python dict
        with column names as key, and the values of the current row.
        """
        contents = self._connect.request(self.url, 'GET',
               accept_type='application/csv')
        clean_data = contents.encode('ascii', 'ignore')
        return csv.DictReader(clean_data.split('\n'))

class Reports(object):
    """
    Skytap adhoc report generating service.
    """
    def __init__(self, connect):
        self._connect = connect

    def generate_usage_report(self, start_date, end_date, resource_type='svms',
            utc=True, region='all', group_by='raw', aggregate_by='none'):
        """
        Generate Report for Storage or SVM usage from history data
        
        Parameters
            start_date
            end_date
            utc - boolean, if true use UTC time
            resource_type - 'storage' or 'svms'
            region - 'all', 'US-East', 'US-West', etc...
            group_by - 'user', 'group', 'region', or 'raw'
            aggregate_by - 'month', 'day', 'none'. Must be 'none' if group_by='raw'
        """
        args = {}
        args['start_date'] = start_date.strftime('%Y/%m/%d %H:%M:%S')
        args['end_date'] = end_date.strftime('%Y/%m/%d %H:%M:%S')
        args['utc'] = utc
        args['resource_type'] = resource_type
        args['region'] = region
        args['group_by'] = group_by
        args['aggregate_by'] = aggregate_by
        args['results_format'] = 'csv'
        report_data = self._connect.post('reports', args)
        return UsageReport(self._connect, report_data['id'], report_data)
