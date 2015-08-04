"""
This file use the reflection capabilities of python to 
dynamically call all public noarg methods, and attribute 
getters for object types that can be reached from an
instance of dxskytap.Skytap.

This test is just looking for exceptions and errors
in the basic tree traversal process.
"""

from dxskytap import Skytap
import inspect
import re
try:
    import Queue as queue
except ImportError:
    import queue

import logging

ignoreAttrs = ['delete', '_newFunc','create_template','create_configuration',
    'attach_vpn','detach']
#'__doc__', '__init__', '__delattr__', '__format__',
#'__class__', '__module__', '__repr__', '__str__',
#'__dict__', '__getattribute__', '__getitem__',
#'__new__', '__setattr__', '_newFunc','__hash__',
#'__reduce__', '__reduce_ex__', '__sizeof__',
#'__subclasshook__', '__add__', '__contains__',
#'__delitem__', '__delslice__' ]

ignoreTypes = ['str', 'list', 'dict', 'bool', 'int', 'float', 'unicode', 'NoneType', 'Connect', 'Http']

pattern = re.compile('_.+')

def handleObject(obj, path, objs, exploredTypes):
    n = type(obj).__name__
    if(n in ['generator','tuple', 'list']):
        for o in obj:
            obj = o
    t = type(obj).__name__
    if(not (t in exploredTypes)):
        exploredTypes.append(t)
        objs.put((obj, "%s.%s" % (path, n)))
        return "NEW " + t
    else:
        return t
        
def handleFunction(func, path, objs, exploredTypes, logger):
    try:
        spec = inspect.getargspec(func)
    except TypeError:
        return "NotCalled"
    args = spec[0]
    if len(args) == 1 and args[0] == 'self':
        logger.info("CALL: %s()" % func.__name__)
        return handleObject(func(), path, objs, exploredTypes)
    else:
        return "NotCalled"
        
            
def testAPI():
    obj = Skytap()
    objs = queue.Queue()
    objs.put((obj, ""))
    exploredTypes = ignoreTypes[:]
    logger = logging.getLogger('dxskytap.test')
    while not objs.empty():
        (o, p) = objs.get()
        logger.info(" **********************************")
        logger.info(" * OBJECT: %s" % (type(o).__name__))
        logger.info(" **********************************")
        for attr in dir(o):
            if not pattern.match(attr) and not attr in ignoreAttrs:
                v = getattr(o, attr, None)

                if callable(v):
                    handleFunction(v, p, objs, exploredTypes, logger)
                else:
                    logger.info("GET: %s" % attr)
                    handleObject(v, p, objs, exploredTypes)
