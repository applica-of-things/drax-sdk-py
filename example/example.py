import json
import asyncio
import time

import sys  
# setting path
sys.path.append('../drax-sdk-py')
sys.path.append('../drax-sdk-py/consumer')
sys.path.append('../drax-sdk-py/consumer/listeners')

import drax
from backend import draxClient
from consumer.listeners import htsensor, rele, trv

fp = open('example/config.json')
config = json.load(fp)

params = {
    'host': None,
    'port': None,
    'vhost': None,
}
params['config'] = config

async def main():
    trv_ = trv.Trv(params['config']['project']['id'])
    rele_ = rele.Rele(params['config']['project']['id'])
    htsensor_ = htsensor.HTSensor(params['config']['project']['id'])
    listeners = [trv_, rele_, htsensor_]
    # listeners = [trv_]

    _drax  = drax.Drax(params)

    node = {
        'urn': 'mqtt:gateway-test:nodo-01-python-test',
        'supportedTypes': ["nodo-drax-sdk-test"],
        'configurationPublishTopic': 'configurations/hmip',
        'statePublishTopic': 'states/hmip',
        'initialState': dict(),
        'name': 'nodo-1-test-python'
    }

    await _drax.start()

    await _drax.handshake(node)

    state = {'dato': '23', 'battery': '78'}

    await _drax.setState(3839, 'mqtt:gateway-test:nodo-01-python-test', state, False)

    await _drax.addConfigurationListener("configurations/hmip", listeners)
    
    await _drax.stop()

asyncio.run(main())
