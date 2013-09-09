"""
Run from the dxskytap root directory (../)

$ python -m test.tunnels_test
"""

from dxskytap import Skytap
from dxskytap.tunnels import Tunnel
import unittest
import time

class TestTunnels(unittest.TestCase):
    def setUp(self):
        self.root = Skytap()
        self.configurations = self.root.configurations()
        template = self.root.templates()['286541']
        self.configuration1 = template.create_configuration()
        self.configuration1.wait_for()
        self.configuration1.name = "Source Config"
        self.configuration2 = template.create_configuration()
        self.configuration2.wait_for()
        self.configuration2.name = "Target Config"
        
    def tearDown(self):
        self.configuration1.delete()
        self.configuration2.delete()
        
    def test_createAndDeleteTunnel(self):
        self.assertTrue(len(self.configurations) > 0, "No configurations for this user")
        inVar = False
        n1 = self.configuration1.networks().values()[0]
        n2 = self.configuration2.networks().values()[0]
        n2.subnet_addr = '10.0.1.0'
        n2.tunnelable = True
        n2.refresh()
        time.sleep(30)
        r = n1.create_tunnel(n2.uid)
        n1.refresh()
        tunnels = n1.tunnels()
        self.assertTrue(len(tunnels) > 0, "No tunnels for this configuration")
        for r in tunnels:
            self.assertTrue(isinstance(r, Tunnel), "Didn't traverse any tunnels")
            inVar = True
        self.assertTrue(inVar, "Didn't traverse any tunnels")
    

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestTunnels('test_createAndDeleteTunnel'))   
    return suite

if __name__ == '__main__':
    unittest.main()
