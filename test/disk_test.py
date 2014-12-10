"""
Run from the dxskytap root directory (../)

$ python -m test.disk_test
"""

from dxskytap import Skytap
from dxskytap.configurations import Configuration
import unittest
import time


class TestDisk(unittest.TestCase):
    def setUp(self):
        self.root = Skytap()
        """configurations = Configurations(username, password)"""
        self.configurations = self.root.configurations()
        template = self.root.templates()['294385']
        self.assertTrue(template is not None, "Unable to get template 294385")

    def test_createNewDisk(self):
        template = self.root.templates()['294385']
        self.assertTrue(template is not None, "Unable to get template 294385")
        config1 = template.create_configuration()
        config1.wait_for()
        vm1 = config1.vms().values()[0]
        self.assertEqual(len(vm1.hardware().disks()), 1,
            "Expected only 1 initial disk in vm")
        vm1.hardware().addDisk(8192)
        config1.wait_for()
        vm1.refresh()
        self.assertEqual(len(vm1.hardware().disks()), 2,
            "Expected 2 disks in vm")
        config1.delete()

    def test_DeleteDisk(self):
        template = self.root.templates()['294385']
        self.assertTrue(template is not None, "Unable to get template 294385")
        config1 = template.create_configuration()
        config1.wait_for()
        vm1 = config1.vms().values()[0]
        self.assertEqual(len(vm1.hardware().disks()), 1,
            "Expected only 1 initial disk in vm")
        vm1.hardware().addDisk(8192)
        config1.wait_for()
        vm1.refresh()
        self.assertEqual(len(vm1.hardware().disks()), 2,
            "Expected 2 disks in vm")
        vm1.hardware().disks()[1].delete()
        config1.wait_for()
        vm1.refresh()
        self.assertEqual(len(vm1.hardware().disks()), 1,
            "Expected 1 disks in vm")
        config1.delete()

    def tearDown(self):
        pass

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestDisk('test_createNewDisk'))
    suite.addTest(TestDisk('test_DeleteDisk'))
    return suite

if __name__ == '__main__':
    unittest.main()
