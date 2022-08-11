import json
import time
from datetime import datetime
import sys  
# setting path
sys.path.append('../draxsdk')
sys.path.append('../draxsdk/consumer')
sys.path.append('../draxsdk/consumer/listeners')


from draxsdk import drax
from draxsdk.backend import draxClient
from draxsdk.consumer.listeners import htsensor, rele, trv

fp = open('src/draxsdk/example/config_trv.json')
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
    _drax.start()

    # set configuration
    configuration = {'targetTemperature': '22.5'}
    _drax.setConfiguration(3950, 'trv:3014F711A0001F9D89A98A50:00201D89A8EC80', configuration, False)
    
    # list states from one or multiple nodes
    dt_obj = datetime.strptime('11.8.2022 14:30:42,76', '%d.%m.%Y %H:%M:%S,%f')
    fromTime = int(dt_obj.timestamp() * 1000)
    toTime = int(time.time()*1000)
    statesResponse = _drax.listNodesStates('trv-18443', [3950, 3951], fromTime, toTime)
    print(statesResponse)
    
if __name__ == "__main__":
    main()