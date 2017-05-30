from dxskytap import Skytap
import unittest
import datetime
class TestReports(unittest.TestCase):
    def setUp(self):
        self.root = Skytap()
        self.reports = self.root.reports()

    def test_generateReadReport(self):
        midnight = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        sdate = midnight - datetime.timedelta(days=2)
        edate = midnight - datetime.timedelta(days=1)
        rpt = self.reports.generate_usage_report(sdate, edate, region='US-East', group_by='user', aggregate_by='day')
        rpt.wait_for(30, 30)
        reader = rpt.get_reader()
        count = 0
        maxlen = 0
        for line in reader:
            if len(line) > maxlen:
                maxlen = len(line)
            count  = count + 1
        self.assertGreater(count, 0, 'Report contains zero rows')
        self.assertGreater(maxlen, 0, 'Report rows all blank')

    def tearDown(self):
        pass

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestProjects('test_generateReadReport'))
    return suite

if __name__ == '__main__':
    unittest.main()
