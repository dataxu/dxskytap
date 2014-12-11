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

class Hardware(RestObject):
    def __init__(self, connect, res, initial_data, parent):
        super(Hardware, self).__init__(connect, res, initial_data,
            is_full=True, parent=parent, parent_attr="hardware")
    
    cpus = RestAttribute("cpus")
    guest_os = RestAttribute("guestOS", readonly=True)
    max_cpus = RestAttribute("max_cpus", readonly=True)
    max_ram = RestAttribute("max_ram", readonly=True)
    min_ram = RestAttribute("min_ram", readonly=True)
    ram = RestAttribute("ram")
    svms = RestAttribute("svms", readonly=True)
    upgradable = RestAttribute("upgradable", readonly=True)
    vnc_keymap = RestAttribute("vnc_keymap", readonly=True)

    def disks(self):
        return [Disk(self._connect, self._resource, disk)
            for disk in self.alldata()['disks']]

    def addDisk(self, size):
        msg = { "hardware": { "disks":
                {"new": [ size ] }
              } }
        self._connect.put(self._resource, body=msg)

class Disk(RestObject):
    def __init__(self, connect, res, initial_data):
        super(Disk, self).__init__(connect, res, initial_data,
            is_full=True, can_refresh=False)

    controller = RestAttribute('controller', readonly=True)
    uid = RestAttribute('id', readonly=True)
    lun = RestAttribute('lun', readonly=True)
    size = RestAttribute('size', readonly=True)
    disk_type = RestAttribute('type', readonly=True)

    def delete(self):
        msg = { 'hardware': { 'disks': { 'existing': { } } } }
        msg['hardware']['disks']['existing'][self.uid] = {
            'id': self.uid,
            'size': None }
        self._connect.put(self._resource, body=msg)
        self._active = False
