import asyncio
from backend import draxClient
from consumer import amqpDraxBroker


class Drax:
  
  def __init__(self, params):
    self.draxBroker = amqpDraxBroker.AmqpDraxBroker(params)
    self.draxClient = draxClient.DraxClient(params)

  async def start(self):
    await self.draxBroker.start()

  async def stop(self):
    await self.draxBroker.stop()

  async def setState(self, nodeId, urn, state, cryptographyDisabled = False):
    await self.draxBroker.setState(nodeId, urn, state, cryptographyDisabled)

  async def handshake(self, node):
    await self.draxClient.handshake(node)

  async def addConfigurationListener(self, topic, listeners = []):
    await self.draxBroker.addConfigurationListener(topic, listeners)
