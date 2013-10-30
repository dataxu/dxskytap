
from dxskytap import Skytap
import unittest

class TestData(unittest.TestCase):

    def test_configurationsLevel1(self):
        data = configurations.alldata()
        self.assertTrue(isinstance(data, list), "Configurations.alldata didn't return a list")
        for i in data:
            self.assertTrue(isinstance(i, dict), "Configurations.alldata didn't return a list of dict %s" % (i))

    def test_templatesLevel1(self):
        templates = root.templates()
        data = templates.alldata()
        self.assertTrue(isinstance(data, list), "Templates.alldata didn't return a list")
        for i in data:
            self.assertTrue(isinstance(i, dict), "Templates.alldata didn't return a list of dict %s" % (i))

    def test_usersLevel1(self):
        users = root.users()
        data = users.alldata()
        self.assertTrue(isinstance(data, list), "Users.alldata didn't return a list")
        for i in data:
            self.assertTrue(isinstance(i, dict), "Users.alldata didn't return a list of dict %s" % (i))

    def test_vpnsLevel1(self):
        vpns = root.vpns()
        data = vpns.alldata()
        self.assertTrue(isinstance(data, list), "Vpns.alldata didn't return a list")
        for i in data:
            self.assertTrue(isinstance(i, dict), "Vpns.alldata didn't return a list of dict %s" % (i))
        
    def test_assetsLevel1(self):
        assets = root.assets()
        data = assets.alldata()
        self.assertTrue(isinstance(data, list), "Assets.alldata didn't return a list")
        for i in data:
            self.assertTrue(isinstance(i, dict), "Assets.alldata didn't return a list of dict %s" % (i))


    def test_configurationLevel2(self):
        data = config.alldata()
        self.assertTrue(isinstance(data, dict), "Configuration.alldata didn't return a dict")
        
    def test_templateLevel2(self):
        template = root.templates().values()[0]
        data = template.alldata()
        self.assertTrue(isinstance(data, dict), "Template.alldata didn't return a dict")

    def test_userLevel2(self):
        user = root.users().values()[0]
        data = user.alldata()
        self.assertTrue(isinstance(data, dict), "User.alldata didn't return a dict")

    def test_vpnLevel2(self):
        vpn = root.vpns().values()[0]
        data = vpn.alldata()
        self.assertTrue(isinstance(data, dict), "Vpn.alldata didn't return a dict")
        
    def test_assetLevel2(self):
        asset = root.assets().values()[0]
        data = asset.alldata()
        self.assertTrue(isinstance(data, dict), "Asset.alldata didn't return a dict %s" % (data))

    def test_vmsLevel3(self):
        vms = config.vms()
        data = vms.alldata()
        self.assertTrue(isinstance(data, list), "Vms.alldata didn't return a list")
        for i in data:
            self.assertTrue(isinstance(i, dict), "Vms.alldata didn't return a list of dict %s" % (i))
        
    def test_vmLevel4(self):
        vm = config.vms().values()[0]
        data = vm.alldata()
        self.assertTrue(isinstance(data, dict), "Vm.alldata didn't return a dict")
        
    def test_interfacesLevel5(self):
        vm = config.vms().values()[0]
        interfaces = vm.interfaces()
        data = interfaces.alldata()
        self.assertTrue(isinstance(data, list), "Interfaces.alldata didn't return a list")
        for i in data:
            self.assertTrue(isinstance(i, dict), "Interfaces.alldata didn't return a list of dict %s" % (i))
    
    def test_interfaceLevel6(self):
        vm = config.vms().values()[0]
        interface = vm.interfaces().values()[0]
        data = interface.alldata()
        self.assertTrue(isinstance(data, dict), "Interface.alldata didn't return a dict")

def setUpModule():
    global root, configurations, config
    root = Skytap()
    """configurations = Configurations(username, password)"""
    configurations = root.configurations()
    template = root.templates()['294385']
    config = template.create_configuration()
    config.wait_for()
    config.name = 'test config'

def tearDownModule():
    result_list = configurations.get_by_name('test config')
    if(len(result_list) == 1):
        result_list[0].delete()

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
