
from dxskytap import Skytap
import unittest

class TestData(unittest.TestCase):
    def setUp(self):
        self.root = Skytap()
        """configurations = Configurations(username, password)"""
        self.configurations = self.root.configurations()

    def test_configurationsLevel1(self):
        configurations = self.root.configurations()
        data = configurations.alldata()
        self.assertIsInstance(data, list, "Configurations.alldata didn't return a list")
        for i in data:
            self.assertIsInstance(i, dict, "Configurations.alldata didn't return a list of dict {}".format(i))

    def test_templatesLevel1(self):
        templates = self.root.templates()
        data = templates.alldata()
        self.assertIsInstance(data, list, "Templates.alldata didn't return a list")
        for i in data:
            self.assertIsInstance(i, dict, "Templates.alldata didn't return a list of dict {}".format(i))

    def test_usersLevel1(self):
        users = self.root.users()
        data = users.alldata()
        self.assertIsInstance(data, list, "Users.alldata didn't return a list")
        for i in data:
            self.assertIsInstance(i, dict, "Users.alldata didn't return a list of dict {}".format(i))

    def test_vpnsLevel1(self):
        vpns = self.root.vpns()
        data = vpns.alldata()
        self.assertIsInstance(data, list, "Vpns.alldata didn't return a list")
        for i in data:
            self.assertIsInstance(i, dict, "Vpns.alldata didn't return a list of dict {}".format(i))
        
    def test_assetsLevel1(self):
        assets = self.root.assets()
        data = assets.alldata()
        self.assertIsInstance(data, list, "Assets.alldata didn't return a list")
        for i in data:
            self.assertIsInstance(i, dict, "Assets.alldata didn't return a list of dict {}".format(i))


    def test_configurationLevel2(self):
        configuration = self.root.configurations().values()[0]
        data = configuration.alldata()
        self.assertIsInstance(data, dict, "Configuration.alldata didn't return a dict")
        
    def test_templateLevel2(self):
        template = self.root.templates().values()[0]
        data = template.alldata()
        self.assertIsInstance(data, dict, "Template.alldata didn't return a dict")

    def test_userLevel2(self):
        user = self.root.users().values()[0]
        data = user.alldata()
        self.assertIsInstance(data, dict, "User.alldata didn't return a dict")

    def test_vpnLevel2(self):
        vpn = self.root.vpns().values()[0]
        data = vpn.alldata()
        self.assertIsInstance(data, dict, "Vpn.alldata didn't return a dict")
        
    def test_assetLevel2(self):
        asset = self.root.assets().values()[0]
        data = asset.alldata()
        self.assertIsInstance(data, dict, "Asset.alldata didn't return a dict {}".format(data))

    def test_vmsLevel3(self):
        vms = self.root.configurations().values()[0].vms()
        data = vms.alldata()
        self.assertIsInstance(data, list, "Vms.alldata didn't return a list")
        for i in data:
            self.assertIsInstance(i, dict, "Vms.alldata didn't return a list of dict {}".format(i))
        
    def test_vmLevel4(self):
        vm = self.root.configurations().values()[0].vms().values()[0]
        data = vm.alldata()
        self.assertIsInstance(data, dict, "Vm.alldata didn't return a dict")
        
    def test_interfacesLevel5(self):
        vm = self.root.configurations().values()[0].vms().values()[0]
        interfaces = vm.interfaces()
        data = interfaces.alldata()
        self.assertIsInstance(data, list, "Interfaces.alldata didn't return a list")
        for i in data:
            self.assertIsInstance(i, dict, "Interfaces.alldata didn't return a list of dict {}".format(i))
    
    def test_interfaceLevel6(self):
        vm = self.root.configurations().values()[0].vms().values()[0]
        interface = vm.interfaces().values()[0]
        data = interface.alldata()
        self.assertIsInstance(data, dict, "Interface.alldata didn't return a dict")

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestData('test_configurationsLevel1'))
    suite.addTest(TestData('test_templatesLevel1'))
    suite.addTest(TestData('test_usersLevel1'))
    suite.addTest(TestData('test_vpnsLevel1'))
    suite.addTest(TestData('test_assetsLevel1'))
    suite.addTest(TestData('test_configurationLevel2'))
    suite.addTest(TestData('test_templateLevel2'))
    suite.addTest(TestData('test_userLevel2'))
    suite.addTest(TestData('test_vpnLevel2'))
    suite.addTest(TestData('test_assetLevel2'))
    suite.addTest(TestData('test_vmsLevel3'))
    suite.addTest(TestData('test_vmLevel4'))
    suite.addTest(TestData('test_interfacesLevel5'))
    suite.addTest(TestData('test_interfacesLevel5'))
    return suite
