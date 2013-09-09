
import unittest
import test.configurations_test
import test.data_test
import test.templates_test
import test.tunnels_test
import test.vms_test

def suite():
    suites = []
    suites.append(test.configurations_test.suite())
    suites.append(test.data_test.suite())
    suites.append(test.templates_test.suite())
    suites.append(test.tunnels_test.suite())
    suites.append(test.vms_test.suite())
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
    
