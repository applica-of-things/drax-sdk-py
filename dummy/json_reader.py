import json
import numpy as np

#fp = open('example/config.json')
#data = json.load(fp)
#print(data)

# base64 to numpy array
body = b'{"nodeId":3839,"timestamp":1657882251549,"urn":"mqtt:gateway-test:nodo-01-python-test","configuration":"bTnqqz7uNKp2OR9iqRH0oGfkByh/HiCB0u5AGdX+mM0=","cryptographyDisabled":false}'
body_json = json.loads(body)
print(body_json['cryptographyDisabled'], " ", body_json['configuration'])
if body_json['cryptographyDisabled'] == False:
    conf_base64 = body_json['configuration']
    signedData = np.frombuffer(conf_base64.encode('ascii'), dtype=np.uint8)
    print(signedData)
