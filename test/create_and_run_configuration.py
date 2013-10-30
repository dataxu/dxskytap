"""
Run from the dxskytap root directory (../)

$ python -m rts.create_and_run_configurations
"""

from dxskytap import Skytap
from dxskytap.configurations import Configuration
from dxskytap.templates import Template
import unittest
import time
import sys


class CreateAndRunConfiguration(unittest.TestCase):
    def setUp(self):
        print("CreateAndRunConfiguration setUp")
        self.root = Skytap()
        self.configurations = self.root.configurations()
        self.templates = self.root.templates()

    def test_createAndRunConfiguration(self):
        print('in test_createAndRunConfiguration(%s)' % (self))
        template_name = sys.argv[1]
        self.assertTrue(len(template_name) > 1, "Template name must be passed in")
        print("Template name '%s'" % (template_name))
        driver_name = sys.argv[2]
        self.assertTrue(len(driver_name) > 1, "Test driver name must be passed in")
        print("Test driver name '%s'" % (driver_name))
        user_name = sys.argv[3]
        if len(user_name) > 1:
            configuration_name = user_name + ' ' + template_name
        else:
            configuration_name = template_name
        print("Configuration name '%s'" % (configuration_name))
            
        """ Delete the existing configuration """
        print("Delete the existing configuration")
        configs = self.configurations.get_by_name(configuration_name)
        if len(configs) > 0:
            for config in configs:
                print("Deleting configuration %s" % (config))
                config.delete()
        
        """ Create configuration from template """
        print("Creating configuration '%s' from template '%s'" % (configuration_name, template_name))
        self.templates.refresh()
        templates = self.templates.get_by_name(template_name)
        self.assertTrue(templates is not None, "Unable to get template %s" % (template_name))
        self.assertTrue(len(templates) == 1, "Should only be one '%s' template. Found %s template(s)" % (template_name, len(templates)))
        config = templates[0].create_configuration()
        self.assertTrue(config is not None, "Unable to create new configuration")
        config.name = configuration_name

        """ Run the configuration """
        print("Run the configuration")
        iterations = 0
        time.sleep(30)
        config.runstate = 'running'
        while ((config.runstate != 'running') & (iterations < 10)):
            print("'%s' %s. Sleep for 30 seconds" % (configuration_name, config.runstate))
            time.sleep(30)
            self.configurations.refresh()
            config = self.configurations.get_by_name(configuration_name)[0]
            iterations += 1
        self.assertTrue(config.runstate == 'running', "Configuration did not transition to running.")
        
        """ Allow hosts more time to start up """
        time.sleep(60)
        
        """ Connect the test driver and test client configurations """
        print("Connect the test driver to the configuration")
        driver_config = self.configurations.get_by_name(driver_name)[0]
        driver_network = driver_config.networks().values()[0]
        network = config.networks().values()[0]
        driver_network.create_tunnel(network.uid)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(CreateAndRunConfiguration('test_createAndRunConfiguration'))
    return suite

if __name__ == '__main__':
    unittest.main(argv=[sys.argv[0]])
