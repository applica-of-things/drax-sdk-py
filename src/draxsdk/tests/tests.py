import os
import unittest
import json 

from draxsdk import drax
from draxsdk.backend import draxClient

class TestCaseClient(unittest.TestCase):

    def test_getProjectById(self):
        fp = open(os.path.dirname(os.path.abspath(__file__)) + '/config.json')
        config = json.load(fp)
        params = {
            'host': None,
            'port': None,
            'vhost': None,
        }
        params['config'] = config
        client = draxClient.DraxClient(params)       
        projectJson = client.getProjectById("trv-18443")
        print(projectJson)
        assert True

if __name__ == '__main__':
    # all tests
    testSuite = unittest.TestSuite()
    testSuite.addTest(TestCaseClient("test_getProjectById"))
    unittest.TextTestRunner().run(testSuite)