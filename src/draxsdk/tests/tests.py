import os, sys
import unittest
import datetime, time 

try:
    from draxsdk import drax
except:
    print("using local draxsdk source...")
    sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/../..")
    from draxsdk import drax

from draxsdk.backend import draxClient
from draxsdk.consumer.listeners.htsensor import HTSensor
from draxsdk.consumer.listeners.rele import Rele
from draxsdk.consumer.listeners.trv import Trv
from draxsdk.consumer.listeners.stateListener import StateListener
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
            nodesIds = [4298, 4295]
            dt_obj = datetime.datetime.strptime('12.11.2022 14:30:42,76', '%d.%m.%Y %H:%M:%S,%f')
            fromTimeMillis = int(dt_obj.timestamp() * 1000)
            dt_obj = datetime.datetime.strptime('15.11.2022 14:40:42,76', '%d.%m.%Y %H:%M:%S,%f')
            toTimeMillis = int(dt_obj.timestamp() * 1000)
            statesResponse = _drax.listNodesStates(projectId, nodesIds, fromTimeMillis, toTimeMillis)

            _drax.stop()
            assert True
        except Exception as ex:
            print(ex)
            assert False

    def test_setConfiguration(self):
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
            # initialize Drax with project parameters
            draxProjectParams = DraxProjectParameters(
                projectId, projectInfo['apiKey'], projectInfo['apiSecret'], 
                draxServerConfig
                )
            _drax = drax.Drax(draxProjectParams)
            _drax.start()
            
            # set configuration
            nodeId = 3950
            #urn = 'trv:3014F711A0001F9D89A98A50:00201D89A8EC80' #TODO: get it from DB with rest call
            configuration = {'targetTemperature': '21.5'}
            _drax.setConfiguration(nodeId, "", configuration, False)
    
            _drax.stop()
            assert True
        except Exception as ex:
            print(ex)
            assert False
    
    def _setState(self, projectId: str, nodeId: int, state: dict()):
        # get project Information at first
        configFilePath = os.path.dirname(os.path.abspath(__file__)) + '/config.json'
        draxServerConfig = drax.loadConfigFromFile(configFilePath)
        client = draxClient.DraxClient(
            draxServerConfig.serviceUrl, 
            draxServerConfig.draxApiKey, 
            draxServerConfig.draxApiSecret
            ) 
        try:      
            projectInfo = client.getProjectById(projectId)
            # initialize Drax with project parameters
            draxProjectParams = DraxProjectParameters(
                projectId, projectInfo['apiKey'], projectInfo['apiSecret'], 
                draxServerConfig
                )
            _drax = drax.Drax(draxProjectParams)
            _drax.start()
            
            # set state
            #urn = 'mqtt:gateway-test:nodo-01-python-test' #TODO: get it from DB with rest call
            _drax.setState(nodeId, None, state, False)
    
            _drax.stop()
            assert True
        except Exception as ex:
            print(ex)
            assert False
    
    def test_setState(self):
        state = {'dato': '22205', 'battery': '10'}
        #node-sdk-development-65447
        self._setState("drax-simu-project-82327", 3839, state)
        
        state = {'internalTemperature': '25.5', 'externalTemperature': '10.5',
                'timestamp':'1662657117864'}
        self._setState("drax-simu-project-82327", 4348, state)
        assert True
                   
    def test_addConfigurationListener(self):
        # get project Information at first
        projectId = "node-sdk-development-65447"
        nodeId = 3839
        configFilePath = os.path.dirname(os.path.abspath(__file__)) + '/config.json'
        draxServerConfig = drax.loadConfigFromFile(configFilePath)
        client = draxClient.DraxClient(
            draxServerConfig.serviceUrl, 
            draxServerConfig.draxApiKey, 
            draxServerConfig.draxApiSecret
            ) 
        try:      
            projectInfo = client.getProjectById(projectId)
            # initialize Drax with project parameters
            draxProjectParams = DraxProjectParameters(
                projectId, projectInfo['apiKey'], projectInfo['apiSecret'], 
                draxServerConfig
                )
            _drax = drax.Drax(draxProjectParams)
            _drax.start()
            
            # set listeners
            trv_ = Trv(projectId)
            rele_ = Rele(projectId)
            htsensor_ = HTSensor(projectId)
            listeners = [trv_, rele_, htsensor_]
            
            # get node topic
            nodeInfo = _drax.getNodeById(nodeId)
            # add configuration listener
            _drax.addConfigurationListener(
                nodeInfo['configurationPublishTopic'], 
                listeners
                )
    
            #_drax.stop() # don't close connection to drax
            assert True
        except Exception as ex:
            print(ex)
            assert False

    def test_listNodes(self):
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
            # initialize Drax with project parameters
            draxProjectParams = DraxProjectParameters(
                projectId, projectInfo['apiKey'], projectInfo['apiSecret'], 
                draxServerConfig
                )
            _drax = drax.Drax(draxProjectParams)
            _drax.start()
            
            # get nodes
            nodesInfo = _drax.listNodes(projectId)
            print(nodesInfo['results'][0])
            
            _drax.stop()
            assert True
        except Exception as ex:
            print(ex)
            assert False

    def test_addStateListener(self):
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
            # initialize Drax with project parameters
            draxProjectParams = DraxProjectParameters(
                projectId, projectInfo['apiKey'], projectInfo['apiSecret'], 
                draxServerConfig
                )
            _drax = drax.Drax(draxProjectParams)
            _drax.start()
            
            # set listeners
            trv_ = Trv(projectId)
            rele_ = Rele(projectId)
            htsensor_ = HTSensor(projectId)
            stateListener_ = StateListener(projectId)
            listeners = [stateListener_]
            
            # add configuration listener
            _drax.addStateListener(
                "mqtt/states/thermovalve", 
                listeners
                )
    
            #_drax.stop() # don't close connection to drax
            assert True
        except Exception as ex:
            print(ex)
            assert False

    def test_listConfigurations(self):
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
            nodesId = 4295
            dt_obj = datetime.datetime.strptime('1.11.2020 06:00:00,00', '%d.%m.%Y %H:%M:%S,%f')
            fromTimeMillis = int(dt_obj.timestamp() * 1000)
            dt_obj = datetime.datetime.strptime('1.11.2022 07:00:00,00', '%d.%m.%Y %H:%M:%S,%f')
            toTimeMillis = int(dt_obj.timestamp() * 1000)
            #toTimeMillis = int(time.time()*1000) #to now
            response = _drax.listConfigurations(projectId, nodesId, None, None)
            print(response)
    
            _drax.stop()
            assert True
        except Exception as ex:
            print(ex)
            assert False

if __name__ == '__main__':
    # all tests
    testSuite = unittest.TestSuite()
    testSuite.addTest(TestCaseClient("test_getProjectById"))
    testSuite.addTest(TestCaseClient("test_listNodesStates"))
    testSuite.addTest(TestCaseClient("test_setConfiguration"))
    testSuite.addTest(TestCaseClient("test_setState"))
    testSuite.addTest(TestCaseClient("test_addConfigurationListener"))
    testSuite.addTest(TestCaseClient("test_listNodes"))
    testSuite.addTest(TestCaseClient("test_addStateListener"))
    testSuite.addTest(TestCaseClient("test_listConfigurations"))
    unittest.TextTestRunner().run(testSuite)