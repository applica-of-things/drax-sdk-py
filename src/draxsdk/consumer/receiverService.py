import threading
import json 
import numpy as np
import base64

import pika

from drax_ecdh_py import crypto

class ReceiverService (threading.Thread):
   
    def __init__(self, channel, projectId, topic, keystore, listeners = []):
        threading.Thread.__init__(self)
        self.listeners = listeners
        self.topic = topic
        self.channel = channel
        self.projectId = projectId
        self.ks = keystore
   
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

    def run(self):
        # set the exchange, if not set before
        self.channel.exchange_declare(exchange="amq.topic", exchange_type='topic', durable=True)
        
        # for each listener, set the queue, bind the queue to the exchange 
        # set the callback function, set basic consume and start consuming
        ret = self.channel.queue_declare('', exclusive=True)
            
        queue_name = ret.method.queue
            
        bindingKey = self.projectId + '.' + self.topic.replace("/", ".")
        self.channel.queue_bind(exchange='amq.topic', queue=queue_name, routing_key=bindingKey)
                    
        def callback(ch, method, properties, body):
            body_json = self._decrypt(body)
            for listener in self.listeners:
                listener.callback(ch, method, properties, body_json)
            
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, 
            auto_ack=False)
    
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

