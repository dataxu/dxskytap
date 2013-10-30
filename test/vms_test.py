"""
Run from the dxskytap root directory (../)

$ python -m test.configurations_test
"""

from dxskytap import Skytap
import unittest
import time

class TestVMs(unittest.TestCase):
    def setUp(self):
        self.root = Skytap()
        """configurations = Configurations(username, password)"""
        template = self.root.templates()['294385']
        self.assertTrue(template is not None, "Unable to get template 294385")
        self.config = template.create_configuration()
        self.config.wait_for()

    def test_vms_exist(self):
        vms = self.config.vms().values()
        self.assertTrue(len(vms) > 0, "Configuration has no VMs")

    def test_vm_labels(self):
        vm = self.config.vms().values()[0]
        labels = vm.labels()
        label_count = len(labels.values())
        labels.create_label('my_text', 'ApplicationTag')
        vm.refresh()
        labels = vm.labels()
        self.assertEqual(len(labels.values()), label_count + 1, "Wrong number of labels after creating a new label")

    def test_vm_notes(self):
        vm = self.config.vms().values()[0]
        notes = vm.notes()
        note_count = len(notes.values())
        notes.create_note('my_note')
        vm.refresh()
        notes = vm.notes()
        self.assertEqual(len(notes.values()), note_count + 1, "Wrong number of notes after creating a new label")

    def tearDown(self):
        self.config.delete()

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestVMs('test_vms_exist'))
    suite.addTest(TestVMs('test_vm_labels'))
    suite.addTest(TestVMs('test_vm_notes'))
    return suite

if __name__ == '__main__':
    unittest.main()
