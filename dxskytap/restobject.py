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
            initial_data - a dictionary containing attribute/value pairs for
                this object. It can be a partial set. For instance if this
                is template object created after calling
                cloud.skytap.com/templates, the Skytap API only returns a 
                subset of the data for each template when list all the user's
                templates.
            is_full - this flag is used to determine when all the attributes
                for this object has been gathered from the Skytap API.
                When the object is first created only a subset of attribute
                values are known. A second API call to Skytap is need to get
                all data. This class performs that 2nd only when necessary.
            can_refresh - this flag indicates that the object can be directly
                referenced with a URI to the Skytap API. Objects that are 
                embedded in other object have no direct URL, and the refresh
                call will not work on these objects.
        """
        self._connect = connect
        self._resource = resource
        self.data = initial_data
        self._is_full = is_full
        self._can_refresh = can_refresh
        
    def alldata(self):
        """
        Return all of the data extracted from the Skytap REST API for this
        resource. The data is converted from its JSON format into a python
        dictionary that is returned by this method.
        """
        if not self._is_full:
            self.refresh()
        return self.data
    
    def refresh(self):
        """
        This method forces dxskytap to query the Skytap API and download
        new data for this resource.

        Note: Not all objects have a unique URL that can be called to refresh
        the data. Nested objects that can only be accessed through its parent
        object, will not be refreshed. This method is basically a NO OP for
        nested objects. Call refresh on the parent to get new data.
        """
        if(self._can_refresh):
            self.data = self._connect.get(self._resource)
            self._is_full = True


class RestObject(RestBase):
    
    def __init__(self, connect, resource, initial_data=None, can_delete=True,
        is_full=False, can_refresh=True, parent=None, parent_attr=None):
        """
        Construct a new Skytap Object that wraps REST API calls.
        Parameters
            connect - The Connect class that maintains the users session with
                      Skytap.
            resource - The relative path to this resource.
            initial_data - Before creating the object information is known
                about the Skytap resource. Information like id, name, etc ...
                are passed to the construct rather than performing a HTTP GET
                to pull the data from Skytap.
            can_delete - Not all Skytap resources support deleting. If
                can_delete is set to False, the delete() method will throw
                an Exception when called.
            is_full - If all data for an object is passed in initial_data
                then set is_full to True.
            can_refresh - Not all objects support pulling updated data
                use HTTP GET to Skytap. Set can_refresh to False for these
                resources.
            parent - A reference to the parent object. This is used when
                creating a nested object.
            parent_attr - When referring to this nested object from the 
                context of its parent, use this attribute name to get/set
                the nest object value in the parent.
        """
        super(RestObject, self).__init__(connect, resource,
            initial_data, is_full, can_refresh)
        self._active = True
        self._can_delete = can_delete
        self._parent = parent
        self._parent_attr = parent_attr
    
    def set_attribute(self, attr_name, attr_value):
        """
        When an RestAttribute has its value set this method is called
        to execute a HTTP PUT to push the updated attribute to Skytap. 
        Users of the dxskytap library should never call this method
        directly.
        Parameters
            attr_name - The name of the attribute being set.
            attr_value - The new value for the attribute.
        """
        if(self._parent_attr is not None):
            attr_name = '%s[%s]' % (self._parent_attr, attr_name)
        args = {attr_name:attr_value}
        self.data = self._connect.put(self._resource, args)

    def delete(self):
        """
        Delete this Skytap resource.
        """
        if(self._can_delete):
            self._active = False
            self._connect.delete(self._resource)
        else:
            raise SkytapException("delete is not supported "
                "on this object.")
    
    def refresh(self):
        """
        A RestObject is a snapshot of a Skytap resource that is 
        downloaded from the Skytap API. It contains the resource
        data for when it was downloaded but any changes to the 
        object are not stored in this local RestObject. To update
        the object with the latest information call this refresh
        method.
        """
        if(self._can_refresh):
            if(self._parent is not None):
                self._parent.refresh()
                self.data = self._parent.alldata()[self._parent_attr]
            else:
                self.data = self._connect.get(self._resource)
        self._is_full = True
        
    def is_active(self):
        """
        Returns active status of this Skytap resource. A resource will 
        become inactive after calling delete() on this object.
        """
        return self._active

class RestMap(RestBase):
    """
    This class wraps a set of REST API calls for a collection of objects
    that can be represented in python as a dictionary.
    """
    
    def __init__(self, connect, resource, new_func, name_field='name'):
        """
        Construct a new dictionary of name and Skytap Object pairs. Skytap
        objects are created only when the RestMap is traversed or getitem
        is called on this dict like object.
        Parameters
            connect - The Connect class that maintains the users session with
                      Skytap.
            resource - The relative path to this resource.
            new_func - This function is used to build the Skytap objects.
                The function is passed Connect class and dict of attribute
                data for the created object.
            name_field - The field in the object's attribute data to use
                as the key in the dict. This defaults to 'name'.
        """
        super(RestMap, self).__init__(connect, resource)
        self._new_func = new_func
        self._name_field = name_field
    
    def __getitem__(self, uid):
        for item in self.alldata():
            if(item['id'] == uid):
                return self._new_func(self._connect, item)
        return None
   
    def __contains__(self, elem):
        """
        Check the uid of the passed object is in the collection
        of all object ids for this collection. If the id is found,
        then the object is contained in this dictionary.
        """
        return elem.uid in self.alldata()
    
    def __setitem__(self, elem):
        """
        Replacing an object in this dictionary is not a supported 
        operation. If the dictionary supports add new elements,
        look for a create_* method on the class.
        """
        raise TypeError('object is immutable') 
   
    def __delitem__(self, elem):
        """
        Deleting an object in this dictionary is not a supported
        operation. Try using the delete method on the object itself.
        """
        raise TypeError('object is immutable')

    def __len__(self):
        """
        Return the number of items that exist in this dictionary.
        """
        return len(self.alldata())
    
    def __nonzero__(self):
        """
        Return True if this dictionary has a non-zero content.
        """
        return bool(self.alldata())
    
    def iteritems(self):
        """
        Return an iterator for traversing the key/value tuples of this
        dictionary.
        """
        for item in self.alldata():
            yield (item['id'], self._new_func(self._connect, item))
    
    def itervalues(self):
        """
        Return an iterator for traversing the values of this dictionary.
        """
        for item in self.alldata():
            yield self._new_func(self._connect, item)

    def iterkeys(self):
        """
        Return an iterator for traversing the keys of this dictionary.
        """
        for item in self.alldata():
            yield item['id']

    def __iter__(self):
        """
        The default way to iterate a dictionary is to iterate
        over the dictionary keys. This allows operations like
        'key in restmap' to work.
        """
        return self.iterkeys()
    
    def keys(self):
        """
        Return a list of all keys in the dictionary.
        """
        return list(self.iterkeys())
              
    def items(self):
        """
        Return a list of all key,value tuples in the dictionary.
        """
        return list(self.iteritems())

    def values(self):
        """
        Return a list of all values in the dictionary.
        """
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

    def get_by_id(self, uid):
        """
        The Skytap API can be used to list resources the current 
        user owns and the resources for projects the user belongs
        to. This works for most users, but admins can access all
        resources regardless of ownership/projects. The Skytap
        API for listing resources is bound to the owner/project
        constraint, so that admin can't use this class to iterate
        over all resources. However, if the admin knows the uid
        for the Skytap resource, this method can be used to
        access the Skytap object.
        """
        item = { 'id': uid }
        return self._new_func(self._connect, item)

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
            raise AttributeError("method called on inactive rest object")
        
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
            raise AttributeError("attribute %s is readonly" % (
                self._attr_name))
        
    def __delete__(self, obj):
        self._fire_inactive(obj)
        if(self._readonly == False):
            obj.set_attribute(self._attr_name, '')
        else:
            raise AttributeError("attribute %s is readonly" % (
                self._attr_name))

class RestBoolAttribute(RestAttribute):
    """
    A python descriptor used to get/set Boolean attributes in a REST API.
    """
    
    def __init__(self, attr_name, readonly=False):
        super(RestBoolAttribute, self).__init__(attr_name, readonly, 
                lambda val: str(val).lower() == 'true',
                lambda val: str(val).lower())
