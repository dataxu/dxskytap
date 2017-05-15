
import unittest
import unit_tests.configurations_test
import unit_tests.data_test
import unit_tests.templates_test
import unit_tests.tunnels_test
import unit_tests.vms_test
import unit_tests.disk_test

def suite():
    suites = []
    suites.append(unit_tests.configurations_test.suite())
    suites.append(unit_tests.data_test.suite())
    suites.append(unit_tests.templates_test.suite())
    suites.append(unit_tests.tunnels_test.suite())
    suites.append(unit_tests.vms_test.suite())
    suites.append(unit_tests.disk_test.suite())
    suite = unittest.TestSuite(suites)
    return suite

"""
This function is need for Eclipse PyDev plugin.
Eclipse unittest will not run the suite without
this function.
"""
def load_tests(loader, tests, pattern):
    return suite()

if __name__ == '__main__':
    unittest.main(defaultTest="suite")
    
