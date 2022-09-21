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
      params['draxServer']['port'],
      params['nodesKeys']
      )

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
  
  def getNodeById(self, nodeId: int):
    """Returns node information given its code ID, making an HTTP GET Rest call to DraxCloud.
        The client must have been initialized with project ApiKey and ApiSecret in request headers.
        :param nodeId: project unique code ID
        :type nodeId: int
        :return: node information in JSON format
        :rtype: str
    """
    return self.draxClient.getNodeById(nodeId)
  
  def listNodes(self, projectId: int, keyword='', pagingState=''):
    """Returns information about all nodes part of a project, making an HTTP GET Rest call to DraxCloud.
        The client must have been initialized with project ApiKey and ApiSecret in request headers.
        :param projectId: project unique code ID
        :type projectId: str
        :return: nodes information in JSON format
        :rtype: str
    """
    return self.draxClient.listNodes(projectId, keyword, pagingState)
  
  def addStateListener(self, topic: str, listeners):
    """Add a node state listener in order to get information published by nodes in queue.
    It returns nothing; it start the receiver service.

    :param topic: Topic where the node publishes the message
    :type topic: str
    :param listeners: list of listeners objects waiting for node's message
    :type listeners: Listener[]
    :return: None
    :rtype: -
    """
    self.draxBroker.addStateListener(topic, listeners)