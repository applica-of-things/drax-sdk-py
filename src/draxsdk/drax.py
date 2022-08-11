from draxsdk.backend import draxClient
from draxsdk.consumer import amqpDraxBroker

class Drax:
  
  def __init__(self, params):
    self.draxBroker = amqpDraxBroker.AmqpDraxBroker(params)
    self.draxClient = draxClient.DraxClient(params)

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
