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

from dxskytap.connect import SkytapException

class RestBase(object):

    def __init__(self, connect, resource, initial_data=None, is_full=False,
        can_refresh=True):
        """
        Constructor
        
        Parameters
            connect - the Connect object used to send/receive Skytap REST
                requests
            resource - the relative URI to the resource represented by this
                object
            initial_data - 
            is_full - this flag
        """
        self._connect = connect
        self._resource = resource
        self.data = initial_data
        self._is_full = is_full
        self._can_refresh = can_refresh
        
    def alldata(self):
        if not self._is_full:
            self.refresh()
        return self.data
    
    def refresh(self):
        if(self._can_refresh):
            self.data = self._connect.get(self._resource)
            self._is_full = True


class RestObject(RestBase):
    
    def __init__(self, connect, resource, initial_data=None, can_delete=True,
        is_full=False, can_refresh=True, parent=None, parent_attr=None):

        RestBase.__init__(self, connect, resource, initial_data, is_full,
            can_refresh)
        self._active = True
        self._can_delete = can_delete
        self._parent = parent
        self._parent_attr = parent_attr
    
    def set_attribute(self, attr_name, attr_value):
        if(self._parent_attr is not None):
            attr_name = '%s[%s]' % (self._parent_attr, attr_name)
        args = {attr_name:attr_value}
        self.data = self._connect.put(self._resource, args)

    def delete(self):
        if(self._can_delete):
            self._active = False
            self._connect.delete(self._resource)
        else:
            raise SkytapException("delete is not supported "
                "on this object.")
    
    def refresh(self):
        if(self._can_refresh):
            if(self._parent is not None):
                self._parent.refresh()
                self.data = self._parent.alldata()[self._parent_attr]
            else:
                self.data = self._connect.get(self._resource)
        self._is_full = True
        
    def is_active(self):
        return self._active

class RestMap(RestBase):
    
    def __init__(self, connect, resource, new_func, name_field='name'):
        RestBase.__init__(self, connect, resource)
        self._new_func = new_func
        self._name_field = name_field
    
    def __getitem__(self, uid):
        for item in self.alldata():
            if(item['id'] == uid):
                return self._new_func(self._connect, item)
        return None
   
    def __contains__(self, elem):
        return elem.uid in self.alldata()
    
    def __setitem__(self, elem):
        raise TypeError('object is immutable') 
   
    def __delitem__(self, elem):
        raise TypeError('object is immutable')

    def __len__(self):
        return len(self.alldata())
    
    def __nonzero__(self):
        return bool(self.alldata())
    
    def iteritems(self):
        for item in self.alldata():
            yield (item['id'], self._new_func(self._connect, item))
    
    def itervalues(self):
        for item in self.alldata():
            yield self._new_func(self._connect, item)

    def iterkeys(self):
        for item in self.alldata():
            yield item['id']

    def __iter__(self):
        return self.iterkeys()
    
    def keys(self):
        return list(self.iterkeys())
              
    def items(self):
        return list(self.iteritems())

    def values(self):
        return list(self.itervalues())

    def get_by_name(self, name):
        """
        This type of search, according to the SkyTap API documentation,
        will return a list and only return id, url, and name. So we
        have a second call to make with the URL to get all the details.
        """
        result = []
        for item in self.alldata():
            if(item[self._name_field] == name):
                obj = self._new_func(self._connect, item)
                result.append(obj)
        return result

class RestAttribute(object):
    "A descriptor used to get/set attributes in the REST API"
    
    __slot__ = ['_attr_name', '_readonly', '_getfunc', '_setfunc']
    
    def __init__(self, attr_name, readonly=False, getfunc=None, setfunc=None):
        self._attr_name = attr_name
        self._readonly = readonly
        self._getfunc = getfunc
        self._setfunc = setfunc
    
    @classmethod
    def _fire_inactive(cls, obj):
        """
        Fire an AttributeError if a method is called on an inactive
        object
        """
        if(not obj.is_active()):
            raise AttributeError, "method called on inactive rest object"
        
    def __get__(self, obj, cls=None):
        if(obj is None):
            return None
        
        if(not obj.is_active()):
            return None
        if(self._attr_name in obj.data):
            val = obj.data[self._attr_name]
        else:
            val = obj.alldata().get(self._attr_name)
        if(self._getfunc is None):
            return val
        else:
            return self._getfunc(val)
    
    def __set__(self, obj, val):
        self._fire_inactive(obj)
        if(not obj.is_active()):
            return None
        if(self._readonly == False):
            if(self._setfunc is None):
                obj.set_attribute(self._attr_name, str(val))
            else:
                obj.set_attribute(self._attr_name, self._setfunc(val))
        else:
            raise AttributeError, "attribute %s is readonly" % (
                self._attr_name)
        
    def __delete__(self, obj):
        self._fire_inactive(obj)
        if(self._readonly == False):
            obj.set_attribute(self._attr_name, '')
        else:
            raise AttributeError, "attribute %s is readonly" % (
                self._attr_name)

class RestBoolAttribute(RestAttribute):
    
    def __init__(self, attr_name, readonly=False):
        RestAttribute.__init__(self, attr_name, readonly, 
                lambda val: str(val).lower() == 'true',
                lambda val: str(val).lower())
