"""
Run from the dxskytap root directory (../)

$ python -m rts.save_and_configuration_as_template
"""

from dxskytap import Skytap
from dxskytap.configurations import Configuration
from dxskytap.templates import Template
import unittest
import time
import sys


class SaveConfigurationAsTemplate(unittest.TestCase):
    def setUp(self):
        self.root = Skytap()
        self.configurations = self.root.configurations()
        self.templates = self.root.templates()

    def test_saveConfigurationAsTemplate(self):
        print('in saveConfigurationAsTemplate(%s)' % (self))
        configurationName = sys.argv[1]
        self.assertTrue(len(configurationName) > 1, "Configuration name must be passed in")
        templateName = configurationName + " - Running Components"
        
        """ Delete the template """
        print("Delete the template")
        templates = self.templates.get_by_name(templateName)
        if len(templates) > 0:
            for template in templates:
                print("Deleting template %s" % (template))
                template.delete()
        
        """ Save the existing configuration as a template """
        print("Save the existing configuration as a template")
        self.configurations.refresh()
        configs = self.configurations.get_by_name(configurationName)
        self.assertTrue(len(configs) == 1, "Should only be one '%s' configuration. Found {1} configuration(s)" % (configurationName, len(configs)))
        config = configs[0]
        template = config.createTemplate()
        self.assertTrue(template is not None, "Unable to create new template")
        template.name = templateName
        self.templates.refresh()
        templates = self.templates.get_by_name(templateName)
        self.assertTrue(len(templates) == 1, "Should only be one '%s' template. Found {1} template(s)" % (templateName, len(templates)))

        """ Wait for the configuration to not be busy """
        print("Wait for the configuration to not be busy")
        iterations = 0
        self.configurations.refresh()
        config = self.configurations.getByName(configurationName)[0]
        while ((config.runstate == 'busy') & (iterations < 10)):
            print("'%s' %s. Sleep for 30 seconds" % (configurationName, config.runstate))
            time.sleep(30)
            self.configurations.refresh()
            config = self.configurations.getByName(configurationName)[0]
            iterations += 1

def suite():
    suite = unittest.TestSuite()
    suite.addTest(SaveConfigurationAsTemplate('test_saveConfigurationAsTemplate'))
    return suite

if __name__ == '__main__':
    unittest.main(argv=[sys.argv[0]])
