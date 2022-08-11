import json
import time
from datetime import datetime
import sys  
# setting path
sys.path.append('../draxsdk')
sys.path.append('../draxsdk/consumer')
sys.path.append('../draxsdk/consumer/listeners')

import draxsdk.drax as drax
from draxsdk.backend import draxClient
from draxsdk.consumer.listeners import htsensor, rele, trv

fp = open('draxsdk/example/config.json')
config = json.load(fp)

params = {
    'host': None,
    'port': None,
    'vhost': None,
}
params['config'] = config

def main():
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

    _drax.start()

    # Come mai?? requests.exceptions.HTTPError: 415 Client Error: Unsupported Media Type for url
    # _drax.handshake(node)

    state = {'dato': '23', 'battery': '78'}

    _drax.setState(3839, 'mqtt:gateway-test:nodo-01-python-test', state, False)
    
    # test listState
    dt_obj = datetime.strptime('5.8.2022 09:38:42,76', '%d.%m.%Y %H:%M:%S,%f')
    fromTime = int(dt_obj.timestamp() * 1000)
    toTime = int(time.time()*1000)
    states = _drax.listStates('node-sdk-development-65447', 3839, fromTime, toTime)
    print(str(states))

    _drax.addConfigurationListener("configurations/hmip", listeners)
    
    #await _drax.stop()

if __name__ == "__main__":
    main()