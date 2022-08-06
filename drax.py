import asyncio
from backend import draxClient
from consumer import amqpDraxBroker


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

  def handshake(self, node):
    self.draxClient.handshake(node)

  def addConfigurationListener(self, topic, listeners = []):
    self.draxBroker.addConfigurationListener(topic, listeners)
    
  def listStates(self, projectId, nodeId, fromTime, toTime):
    return self.draxClient.listStates(projectId, nodeId, fromTime, toTime)
