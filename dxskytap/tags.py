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

class Note(RestObject):
    def __init__(self, connect, res, uid, intial_data):
        super(Note, self).__init__(connect, "%s/notes/%s" % (res, uid),
            intial_data, can_refresh=False)

    uid = RestAttribute("id", readonly=True)
    text = RestAttribute("text")
    time = RestAttribute("time", readonly=True)
    user_id = RestAttribute("user_id", readonly=True)


class Notes(RestMap):

    def __init__(self, connect, res):
        super(Notes, self).__init__(connect, "%s/notes" % (res),
            lambda conn, data: Note(conn, res, data['id'], data))
        self._base_resource = res

    def create_note(self, text):
        result = self._connect.post("%s/notes" % (self._base_resource),
            body={'text': text})
        return Note(self._connect, self._base_resource, result['id'], result)


class Label(RestObject):
    def __init__(self, connect, res, uid, intial_data):
        super(Label, self).__init__(connect, "%s/labels/%s" % (res, uid),
            intial_data)

    uid = RestAttribute("id", readonly=True)
    text = RestAttribute("text")
    label_type = RestAttribute("type")


class Labels(RestMap):

    VALID_VM_TYPES = ['VmInstance','ConfigurationTemplate']

    VALID_TAG_TYPES = ['ApplicationTag', 'BugTag', 'PurposeTag', 'DiskTag', 
       'LicenseTag', 'RegionNameTag', 'SecurityTag', 'VersionTag']

    def __init__(self, connect, res, vmtype):
        super(Labels, self).__init__(connect, "%s/labels" % (res),
            lambda conn, data: Note(conn, res, data['id'], data))
        self._base_resource = res
        self._vm_type = vmtype
        if(not vmtype in self.VALID_VM_TYPES):
            raise ValueError("Invalid value for param vmtype. Should be %s"
                % ("|".join(self.VALID_VM_TYPES)))

    def create_label(self, text, tagtype):
        if(not tagtype in self.VALID_TAG_TYPES):
            raise ValueError("Invalid value for param tagtype. Should be %s"
                % ("|".join(self.VALID_TAG_TYPES)))
        body = {
            'object_type': self._vm_type,
            'tag_type' : tagtype,
            'text': text }
        result = self._connect.post("%s/labels" % (self._base_resource),
            body=body)
        return Label(self._connect, self._base_resource, result['id'], result)


class Credential(RestObject):
    def __init__(self, connect, res, uid, intial_data):
        super(Credential, self).__init__(connect,
            "%s/credentials/%s" % (res, uid), intial_data)

    uid = RestAttribute("id", readonly=True)
    text = RestAttribute("text")


class Credentials(RestMap):

    def __init__(self, connect, res):
        super(Credentials, self).__init__(connect,
            "%s/credentials" % (res),
            lambda conn, data: Note(conn, res, data['id'], data))
        self._base_resource = res

    def create_credential(self, text):
        result = self._connect.post("%s/credentials" % (
            self._base_resource), body={'text': text})
        return Credential(self._connect, self._base_resource, result['id'],
            result)
