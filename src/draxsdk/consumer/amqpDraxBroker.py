import json
import numpy as np
import base64 

import pika

from drax_ecdh_py import crypto

from draxsdk import keystore
from draxsdk.consumer.receiverService import ReceiverService


class AmqpDraxBroker:

    def __init__(self, params):
        self.params = params
        self.connection = None
        self.channel = None
        self.ks = keystore.Keystore()
        self.ks.addConfig(self.params['config'])
    
    def start(self):
        self.host = self.params['host'] if 'host' in self.params.keys() and self.params['host'] is not None else "35.205.187.28"
        self.port = self.params['port'] if 'port' in self.params.keys() and self.params['port'] is not None else  5672
        self.password = self.params['config']['project']['apiSecret']
        self.user = self.params['config']['project']['apiKey']
        self.vhost = self.params['vhost'] if self.params['vhost'] is not None else "/"
        self.projectId = self.params['config']['project']['id']
        self.credentials = pika.PlainCredentials(self.user, self.password)

        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self.host, port=self.port, 
                    virtual_host=self.vhost, credentials=self.credentials)
            ) 
            self.channel = self.connection.channel()
            #self.channel.queue_declare(queue='')

            print("Drax Broker started on host: ", self.host, " port: ", self.port)
        except Exception as e:
            print("Cannot start DraxBroker")
            print(e)

    def stop(self):
        try:
            self.connection.close()
            print("Drax connection correctly closed")
        except Exception as e:
            print("DraxBroker close channel error")
            print(e)

    def setState(self, nodeId, urn, state, cryptographyDisabled = False):
        stateRequest = {
            'apiKey': self.params['config']['project']['apiKey'],
            'apiSecret': self.params['config']['project']['apiSecret'],
            'nodeId': nodeId,
            'urn': urn,
            'cryptographyDisabled': cryptographyDisabled
        }
        data = json.dumps(state) # state to JSON string
         
        if(cryptographyDisabled):
            stateRequest['state'] = data # @TODO: it is a str, should it be a list?
        else:
            privateKey = self.ks.getPrivateKey(nodeId)
            publicKey = self.ks.getCloudPublicKey()
            privateKey_uint8 = np.frombuffer(bytearray.fromhex(privateKey), dtype=np.uint8)
            publicKey_uint8 = np.frombuffer(bytearray.fromhex(publicKey), dtype=np.uint8)
            data_uint8 = np.frombuffer(data.encode(), dtype=np.uint8)
            signed_data = crypto.crypto_sign(privateKey_uint8, publicKey_uint8, data_uint8)

            stateRequest['state'] = signed_data.tolist() # @TODO: check draxcloud expected format
        print("State request to publish: ", stateRequest)
        
        self.channel.exchange_declare(exchange='amq.topic', exchange_type='topic', durable=True)
        self.channel.basic_publish(exchange='amq.topic',
                      routing_key='node-sdk-development-65447.requests.states',
                      body=json.dumps(stateRequest))

        print(" [x] Sent '", json.dumps(stateRequest), "'")

    def _decrypt(self, body):
        body_json = json.loads(body)
        if body_json['cryptographyDisabled'] == False:
            confBase64 = body_json['configuration']
            confBytes = confBase64.encode('ascii')
            signedData = np.frombuffer(base64.b64decode(confBytes), dtype=np.uint8)
            privateKey = self.ks.getPrivateKey(body_json['nodeId'])
            publicKey = self.ks.getCloudPublicKey()
            privateKey_uint8 = np.frombuffer(bytearray.fromhex(privateKey), dtype=np.uint8)
            publicKey_uint8 = np.frombuffer(bytearray.fromhex(publicKey), dtype=np.uint8)
            unsigned_data = crypto.crypto_unsign(privateKey_uint8, publicKey_uint8, signedData)
            unsigned_data_str = "".join(map(chr, unsigned_data))
            body_json['configuration'] = unsigned_data_str
        return body_json

    def addConfigurationListener(self, topic, listeners = []):
        receiverServiceThread = ReceiverService(self.channel, self.projectId, topic, self.ks, listeners)
        receiverServiceThread.start()