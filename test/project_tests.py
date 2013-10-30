from dxskytap import Skytap
from dxskytap.projects import Project
from dxskytap.templates import Template
from dxskytap.configurations import Configuration
import unittest
import time

class TestProjects(unittest.TestCase):
    def setUp(self):
        self.root = Skytap()
        template = self.root.templates()['294385']
        self.assertTrue(template is not None, "Unable to get template 294385")
        self.config = template.create_configuration()
        self.config.wait_for()
        self.template = self.config.create_template()
        self.template.wait_for()

    def test_createDeleteProject(self):
        new_project = self.root.projects().create_project('test_project_1')
        self.assertTrue(isinstance(new_project, Project))
        new_project.delete()

    def test_assignTemplate(self):
        new_project = self.root.projects().create_project('test_project_2')
        self.template.add_to_project(new_project)
        templates = new_project.templates()
        temp = filter(lambda x: x.uid == self.template.uid, templates)
        self.assertEquals(len(temp), 1)
        self.assertTrue(isinstance(temp[0], Template))
        new_project.delete()

    def test_assignConfiguration(self):
        new_project = self.root.projects().create_project('test_project_3')
        self.config.add_to_project(new_project)
        configurations = new_project.configurations()
        temp = filter(lambda x: x.uid == self.config.uid, configurations)
        self.assertEquals(len(temp), 1)
        self.assertTrue(isinstance(temp[0], Configuration))
        new_project.delete()

    def tearDown(self):
        self.config.delete()
        self.template.delete()

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestProjects('test_createDeleteProject'))
    suite.addTest(TestProjects('test_assignTemplate'))
    suite.addTest(TestProjects('test_assignConfiguration'))
    return suite

if __name__ == '__main__':
    unittest.main()
