"""
Run from the dxskytap root directory (../)

$ python -m rts.save_and_configuration_as_template
"""

from dxskytap import Skytap
from dxskytap.configurations import Configuration
import unittest
import time
import sys


class DeleteConfiguration(unittest.TestCase):
    def setUp(self):
        self.root = Skytap()
        self.configurations = self.root.configurations()

    def test_deleteConfiguration(self):
        print('in test_deleteConfiguration(%s)' % (self))
        configurationName = sys.argv[1]
        self.assertTrue(len(configurationName) > 0, "Name of configuration must be passed in")
        
        """ Delete the existing configuration """
        print("Delete the configuration")
        configs = self.configurations.get_by_name(configurationName)
        if len(configs) > 0:
            for config in configs:
                print("Deleting configuration %s" % (config))
                config.delete()

def suite():
    suite = unittest.TestSuite()
    suite.addTest(DeleteConfiguration('test_deleteConfiguration'))
    return suite

if __name__ == '__main__':
    unittest.main(argv=[sys.argv[0]])
