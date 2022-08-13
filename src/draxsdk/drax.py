import json

from draxsdk.backend import draxClient
from draxsdk.consumer import amqpDraxBroker
from .model.parameters import DraxProjectParameters, DraxServerConfig

def loadConfigFromFile(paramsFile: str) -> DraxServerConfig:
  """Loads Drax Server configuration parameter from JSON file to DraxServerConfig object.

  :param paramsFile: path (abs or relative) to the JSON file
  :type paramsFile: str
  :return: Drax Server configuration object to be used to initialize Drax / DraxClient
  :rtype: DraxServerConfig
  """  
  fp = open(paramsFile)
  params = json.load(fp)
  return DraxServerConfig(
      params['draxServer']['host'],
      params['draxApiKey'],
      params['draxApiSecret'],
      params['draxServer']['serviceUrl'],
      params['draxPublicKey'],
      params['draxServer']['vhost'],
      params['draxServer']['port'])

class Drax:
  """This is a class representation of Drax platform which must be used client-side for
  accessing the Drax functionalities. 
  :param params: setting parameters for Drax SDK 
  :type params: class:`DraxParameters`
  """  
  
  def __init__(self, params: DraxProjectParameters):
    self.draxBroker = amqpDraxBroker.AmqpDraxBroker(params)
    self.draxClient = draxClient.DraxClient(
      params.draxServerConfig.serviceUrl, 
      params.projectApiKey, 
      params.projectApiSecret
    )  
     
  def start(self):
    self.draxBroker.start()   
  
  def stop(self):
    self.draxBroker.stop()    
  
  def setState(self, nodeId, urn, state, cryptographyDisabled = False):
    self.draxBroker.setState(nodeId, urn, state, cryptographyDisabled)

  def setConfiguration(self, nodeId: int, urn: str, configuration: dict, cryptographyDisabled = False):
    self.draxBroker.setConfiguration(nodeId, urn, configuration, cryptographyDisabled)    
  
  def handshake(self, node):
    self.draxClient.handshake(node)   
  
  def addConfigurationListener(self, topic, listeners = []):
    self.draxBroker.addConfigurationListener(topic, listeners)

  def listStates(self, projectId: str, nodeId: int, fromTimeMillis: int, toTimeMillis: int):
    return self.draxClient.listStates(projectId, nodeId, fromTimeMillis, toTimeMillis)

  def listNodesStates(self, projectId: str, nodeIds: list[int], fromTimeMillis: int, toTimeMillis: int):
    return self.draxClient.listNodesStates(projectId, nodeIds, fromTimeMillis, toTimeMillis)
  
      