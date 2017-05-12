"""
Run from the dxskytap root directory (../)

$ python -m test.configurations_test
"""

from dxskytap import Skytap
from dxskytap.configurations import Configuration
import unittest
import time


class TestConfigurations(unittest.TestCase):
    def setUp(self):
        self.root = Skytap()
        """configurations = Configurations(username, password)"""
        self.configurations = self.root.configurations()
        self.template = self.root.templates()['294385']
        self.assertTrue(self.template is not None, "Unable to get template 294385")

    def test_lookupNotExist(self):
        result_list = self.configurations['123456']
        self.assertTrue(result_list is None, "Lookup of config that doesn't exist should return None")

    def test_getAllConfigurations(self):
        config = self.template.create_configuration()
        config.wait_for()
        config.name = 'test config'
        self.assertTrue(len(self.configurations) > 0, "No configurations for this user")
        inVar = False
        for r in self.configurations.values():
            self.assertTrue(isinstance(r, Configuration), "Didn't traverse any configurations")
            inVar = True
        self.assertTrue(inVar, "Didn't traverse any configurations")
    
    def test_getConfigurationByName(self):
        config = self.template.create_configuration()
        config.wait_for()
        config.name = 'test config'
        result_list = self.configurations.get_by_name('test config')
        self.assertTrue(len(result_list) == 1, "Received %s configs from lookup of 'test config'" % (len(result_list)))
        count = 0
        for r in result_list:
            self.assertTrue(isinstance(r, Configuration), "Item is not a configuration")
            count += 1
        self.assertTrue(count == 1, "Didn't traverse any configurations")
    
    def test_startConfiguration(self):
        self.assertTrue(self.template is not None, "Unable to get template 294385")
        config1 = self.template.create_configuration()
        config1.wait_for() 
        newState = 'running'
        config1.name = 'test_config'
        config1.runstate = newState
        self.assertTrue( config1.runstate != newState, "Verify state doesn't change immediately")
        config1.wait_for()
        config2 = self.configurations[config1.uid]
        self.assertTrue(config2.runstate == newState, "Configuration state not changed to %s" % (newState))

    def test_createAndDeleteConfiguration(self):
        template = self.root.templates()['294385']
        self.assertTrue(template is not None, "Unable to get template 294385")
        config = template.create_configuration()
        config.name = 'test_config'
        uid = config.uid
        self.assertTrue(config is not None, "Unable to create new config")
        c1 = self.configurations[uid]
        self.assertTrue(c1 is not None and c1.uid == uid, "Unable to find config for delete test")
        try:
            c1.delete()
        except ValueError:
            time.sleep(30)
            c1.delete()
        time.sleep(60)
        self.configurations.refresh()
        c2 = self.configurations[uid]
        self.assertTrue(c2 is None, "Deleted config is still searchable")

    def test_createConfigurationAndMergeTemplate(self):
        template = self.root.templates()['294385']
        self.assertTrue(template is not None, "Unable to get template 294385")
        config = template.create_configuration()
        self.assertEqual(len(config.vms().values()), 1, "Config doesn't have right number of vms before merging template in")
        self.assertTrue(config is not None, "Unable to create new config")
        config.wait_for()
        config.name = 'test_config'
        config.merge_template(template.uid)
        config.wait_for()
        self.assertEqual(len(config.vms().values()), 2, "Config doesn't have right number of vms after merging template in")

    def tearDown(self):
        result_list = self.configurations.get_by_name('test config')
        if(len(result_list) == 1):
            try:
                result_list[0].delete()
            except ValueError:
                time.sleep(30)
                result_list[0].delete()

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestConfigurations('test_lookupNotExist'))
    suite.addTest(TestConfigurations('test_getAllConfigurations'))
    suite.addTest(TestConfigurations('test_getConfigurationByName'))
    suite.addTest(TestConfigurations('test_startConfiguration'))
    suite.addTest(TestConfigurations('test_createAndDeleteConfiguration'))
    suite.addTest(TestConfigurations('test_createConfigurationAndMergeTemplate'))
    return suite

if __name__ == '__main__':
    unittest.main()
