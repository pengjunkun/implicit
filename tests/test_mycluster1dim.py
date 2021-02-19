from unittest import TestCase

from examples.mycluster1dim import ClusterFounder
class TestClusterFounder(TestCase):
    # file_url="C:\\Users\\lenovo\\work\\project\\sugarJar\\simu\\data\\"
    file_url="C:\\Users\\HP\\work\\project\\SugarJar\\simu\\data\\"
    clusterFounder=ClusterFounder(file_url+"1h_frequency.csv")
    def test_get_freq(self):
        self.assertEqual(6057,self.clusterFounder.getFreq('14'))
        self.assertEqual(5650,self.clusterFounder.getFreq('36'))

    def test_get_position_test_value(self):
        x=99
        top10=[(10,'14',91.1)]
        self.clusterFounder.posTable={'14':100}
        self.assertEqual(901,self.clusterFounder.getPositionTestValue(top10,x))

        self.clusterFounder.posTable.update({'1':89})
        top10.append((20,'1',80.2))
        self.assertEqual(2305,self.clusterFounder.getPositionTestValue(top10,x))

    def test_get_position(self):
        # test the first one
        self.assertEqual(100,self.clusterFounder.getPosition('14',None))

