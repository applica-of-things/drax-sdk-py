import json

from draxsdk.backend import draxClient
from draxsdk.consumer import amqpDraxBroker
from draxsdk.model.parameters import DraxProjectParameters, DraxServerConfig
from draxsdk.consumer.listeners.listener import Listener


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
  """This is a class representation of Drax platform which must be used by third part 
  application for accessing Drax IoT functionalities and services. 
  
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
    """Start the drax instance: it connects Drax SDK to Drax AMQP message Broker.
    """
    self.draxBroker.start()   
  
  def stop(self):
    """Stop the drax instance: it disconnects Drax SDK from Drax AMQP message Broker.
    """
    self.draxBroker.stop()    
  
  def setState(self, nodeId: int, urn: str, state: dict, cryptographyDisabled = False):
    """This method is called by the node or the gateway, which the node is connected
    to, in order to comunicate its state to Drax Cloud platform.
    Source: IoT node / gateway
    Comunication protocol: AMQP queue selected on a specific topic 
    Destination (intermediate): Drax Message Broker
    Destination (final): Drax Cloud platform
    This function is used by sensors.

    :param nodeId: IoT node identifier (sender)
    :type nodeId: int
    :param urn: URN 
    :type urn: str
    :param state: state to be sent to Drax cloud
    :type state: dict
    :param cryptographyDisabled: flag to control ECDH cryptografy on data, defaults to False
    :type cryptographyDisabled: bool, optional
    """
    self.draxBroker.setState(nodeId, urn, state, cryptographyDisabled)

  def setConfiguration(self, nodeId: int, urn: str, configuration: dict, cryptographyDisabled = False):
    """This method is called by Drax Cloud platform to send a configuration (command)
    to one node part of Drax Iot network.
    The communication is not direct, but it uses AMQP Drax Message Broker.
    Source: Drax Cloud platform
    Comunication protocol: AMQP queue selected on a specific topic 
    Destination (intermediate): Drax Message Broker
    Destination (final): IoT node
    This function can be called by third part application or internal Drax module to send a configuration command to
    an IoT node of the network.

    :param nodeId: IoT node identifier (receiver)
    :type nodeId: int
    :param urn: URN 
    :type urn: str
    :param configuration: configuration to be sent to the node
    :type configuration: dict
    :param cryptographyDisabled: flag to control ECDH cryptografy on data, defaults to False
    :type cryptographyDisabled: bool, optional
    """
    self.draxBroker.setConfiguration(nodeId, urn, configuration, cryptographyDisabled)    
  
  def handshake(self, node: dict):
    """@TBC

    :param node: _description_
    :type node: dict
    """
    self.draxClient.handshake(node)   
  
  def addConfigurationListener(self, topic:str, listeners: list[Listener]):
    """This method is called to attach a configuration listener to an IoT node.
      The listener will be listening to a specific topic on a queue of the AMQP Drax Message 
      Broker.
      The queue is set to buffer configuration messages coming from Drax Cloud platform
      or third part application and directed to the node.
      It is possibile to attach more that one listener for a single topic.
      
      This function can be called on a device (node, i.e. sensor or gateway)
      that will be waiting for configuration commands waiting on AMQP Drax Message Broker
      queue coming from Drax Cloud platforma .

      :param topic: topic to be listening to
      :type topic: str
      :param listeners: list of Listeners objects
      :type listeners: ListenersList, [Listener]
      """
    
    self.draxBroker.addConfigurationListener(topic, listeners)

  def listStates(self, projectId: str, nodeId: int, fromTimeMillis: int, toTimeMillis: int)->dict:
    """This method can be called by a third part application or internal Drax module to Drax Cloud platform 
    in order to get the states of a single node part of a project (selected by their IDs)
    relative to a time interval set by timestamps limits expressed in millisecs.
    The communication is direct, it uses an HTTPs POST request to Drax Cloud platform REST API service.
    Source: Application (third-part) or internal Drax module
    Comunication protocol: HTTPs 
    Destination (final): Drax Cloud platform (REST API service)

    :param projectId: Project Identifier 
    :type projectId: str
    :param nodeId: IoT node identifier
    :type nodeId: int
    :param fromTimeMillis: initial time (millis)
    :type fromTimeMillis: int
    :param toTimeMillis: final time (millis)
    :type toTimeMillis: int
    :return: dict of node's states in time interval
    :rtype: dict
    """
    return self.draxClient.listStates(projectId, nodeId, fromTimeMillis, toTimeMillis)

  def listNodesStates(self, projectId: str, nodeIds: list[int], fromTimeMillis: int, toTimeMillis: int):
    """This method can be called by a third part application to Drax Cloud platform 
    in order to get the states of multiple nodes part of a project (selected by their IDs)
    relative to a time interval set by timestamps limits expressed in millisecs.
    The communication is direct, it uses an HTTPs POST request to Drax Cloud platform REST API service.
    Source: Application (third-part) or internal Drax module
    Comunication protocol: HTTPs 
    Destination (final): Drax Cloud platform (REST API service)

    :param projectId: Project Identifier 
    :type projectId: str
    :param nodeIds: list of IoT nodes' identifiers
    :type nodeIds: list[int]
    :param fromTimeMillis: initial time (millis)
    :type fromTimeMillis: int
    :param toTimeMillis: final time (millis)
    :type toTimeMillis: int
    :return: dict of nodes' states in time interval
    :rtype: dict
    """
    return self.draxClient.listNodesStates(projectId, nodeIds, fromTimeMillis, toTimeMillis)
  
  def getNodeById(self, nodeId: int)->dict:
    """Returns node information given its code ID, making an HTTP GET Rest call to DraxCloud.
        The client must have been initialized with project ApiKey and ApiSecret in request headers.
        
        :param nodeId: project unique code ID
        :type nodeId: int
        :return: node information
        :rtype: dict
    """
    return self.draxClient.getNodeById(nodeId)
  
  def listNodes(self, projectId: int, keyword='', pagingState='')->dict:
    """Returns information about all nodes part of a project, making an HTTP GET Rest call to DraxCloud.
        The client must have been initialized with project ApiKey and ApiSecret in request headers.
        
        :param projectId: project unique code ID
        :type projectId: str
        :return: dict of nodes information (JSON format)
        :rtype: dict
    """
    return self.draxClient.listNodes(projectId, keyword, pagingState)
  
  def addStateListener(self, topic: str, listeners: list[Listener]):
    """Add a node state listener in order to get information published by nodes in a queue
    defined by a specific topic on AMQP Drax Message Broker.
    The queue is set to buffer state messages coming from IoT nodes and directed to Drax Cloud platform.
    It is possibile to attach more that one listener for a single topic.
    This function can be called from a third part application or internal Drax module 
    that will be waiting for stated sent by nodes.
    It returns nothing; it start the receiver service.
    
    :param topic: Topic where the node publishes the message
    :type topic: str
    :param listeners: list of listeners objects waiting for node's message
    :type listeners: Listener[]
    """
    self.draxBroker.addStateListener(topic, listeners)