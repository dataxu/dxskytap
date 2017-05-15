"""
Run from the dxskytap root directory (../)

$ python -m unit_tests.templates_test
"""

from dxskytap import Skytap
from dxskytap.templates import Template
import unittest

class TestTemplates(unittest.TestCase):
    def setUp(self):
        self.root = Skytap()
    
    def test_getAllTemplates(self):
        templates = self.root.templates()
        self.assertTrue(isinstance(templates.alldata(), list), "Templates.alldata didn't return a list")
        for i in templates.alldata():
            self.assertTrue(isinstance(i, dict), "Templates.alldata didn't return a list of dict %s" % (i))

    def test_doesntExistLookup(self):
        result = self.root.templates()['1234']
        self.assertTrue(result is None, "Lookup incorrectly returned result %s" % (result))

    def test_getOneTemplate(self):
        result = self.root.templates().values()[0]
        self.assertTrue(isinstance(result, Template), "Lookup didn't return a template")
        self.assertTrue(isinstance(result.alldata(), dict), "Template.alldata didn't return a dict")

    def test_lookupTemplateByName(self):
        resultList = self.root.templates().get_by_name('CentOS 6.3 x64')
        self.assertTrue(len(resultList) == 2,"Found %s templates instead of the expected 1." % (len(resultList)))
        self.assertTrue(isinstance(resultList[0], Template), "Lookup didn't return a template")
        self.assertTrue(isinstance(resultList[0].alldata(), dict), "Template.alldata didn't return a dict")

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestTemplates('test_getAllTemplates'))
    suite.addTest(TestTemplates('test_doesntExistLookup'))
    suite.addTest(TestTemplates('test_getOneTemplate'))
    suite.addTest(TestTemplates('test_lookupTemplateByName'))
    return suite
