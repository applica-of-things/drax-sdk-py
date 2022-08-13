import os
import unittest
import datetime, time 

from draxsdk import drax
from draxsdk.backend import draxClient
from draxsdk.model.parameters import DraxProjectParameters

class TestCaseClient(unittest.TestCase):

    def test_getProjectById(self):
        projectId = "trv-18443"
        configFilePath = os.path.dirname(os.path.abspath(__file__)) + '/config.json'
        draxServerConfig = drax.loadConfigFromFile(configFilePath)
        client = draxClient.DraxClient(
            draxServerConfig.serviceUrl, 
            draxServerConfig.draxApiKey, 
            draxServerConfig.draxApiSecret
            ) 
        try:      
            projectJson = client.getProjectById(projectId)
            print(projectJson)
            assert True
        except Exception as ex:
            print(ex)
            assert False
            
    def test_listNodesStates(self):
        # get project Information at first
        projectId = "trv-18443"
        configFilePath = os.path.dirname(os.path.abspath(__file__)) + '/config.json'
        draxServerConfig = drax.loadConfigFromFile(configFilePath)
        client = draxClient.DraxClient(
            draxServerConfig.serviceUrl, 
            draxServerConfig.draxApiKey, 
            draxServerConfig.draxApiSecret
            ) 
        try:      
            projectInfo = client.getProjectById(projectId)
            #projectInfo = json.loads(projectJson)
            # initialize Drax with project parameters
            draxProjectParams = DraxProjectParameters(
                projectId, projectInfo['apiKey'], projectInfo['apiSecret'], 
                draxServerConfig
                )
            _drax = drax.Drax(draxProjectParams)
            _drax.start()
            
            # list states from one or multiple nodes
            nodesIds = [3950, 3951]
            dt_obj = datetime.datetime.strptime('12.8.2022 14:30:42,76', '%d.%m.%Y %H:%M:%S,%f')
            fromTimeMillis = int(dt_obj.timestamp() * 1000)
            dt_obj = datetime.datetime.strptime('12.8.2022 14:40:42,76', '%d.%m.%Y %H:%M:%S,%f')
            toTimeMillis = int(dt_obj.timestamp() * 1000)
            #toTimeMillis = int(time.time()*1000) #to now
            statesResponse = _drax.listNodesStates(projectId, nodesIds, fromTimeMillis, toTimeMillis)
            print(statesResponse)
    
            _drax.stop()
            assert True
        except Exception as ex:
            print(ex)
            assert False

    def test_setConfiguration(self):
        pass
    
    def test_setState(self):
        pass
    
if __name__ == '__main__':
    # all tests
    testSuite = unittest.TestSuite()
    testSuite.addTest(TestCaseClient("test_getProjectById"))
    testSuite.addTest(TestCaseClient("test_listNodesStates"))
    testSuite.addTest(TestCaseClient("test_setConfiguration"))
    testSuite.addTest(TestCaseClient("test_setState"))
    unittest.TextTestRunner().run(testSuite)