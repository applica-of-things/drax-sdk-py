import asyncio
import json
from matplotlib.font_manager import json_load
import numpy as np
import base64 

import pika

from drax_ecdh_py import crypto

import keystore

class AmqpDraxBroker:

    def __init__(self, params):
        self.params = params
        self.connection = None
        self.channel = None
        self.ks = keystore.Keystore()
        self.ks.addConfig(self.params['config'])
    
    async def start(self):
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
        except:
            print("Cannot start DraxBroker")

    async def stop(self):
        try:
            await self.connection.close()
            print("Drax connection correctly closed")
        except:
            print("DraxBroker close channel error")

    async def setState(self, nodeId, urn, state, cryptographyDisabled = False):
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

    async def addConfigurationListener(self, topic, listeners = []):
        
        # set the exchange, if not set before
        self.channel.exchange_declare(exchange=topic, exchange_type='topic', durable=True)
        
        # for each listener, set the queue, bind the queue to the exchange 
        # set the callback function, set basic consume and start consuming
        ret = self.channel.queue_declare('', exclusive=True)
            
        queue_name = ret.method.queue
            
        self.channel.queue_bind(exchange=topic, queue=queue_name, 
            routing_key='node-sdk-development-65447.configurations.hmip')
        
        for listener in listeners:
                    
            def callback(ch, method, properties, body):
                body_json = self._decrypt(body)
                listener.callback(ch, method, properties, body_json)
            
            self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)
        
            print(' [*] Waiting for messages. To exit press CTRL+C')
            await self.channel.start_consuming()

#    addConfigurationListener(topic, listeners = []){
#        var projectTopic = this.params.config.project.id + "." + topic.replace(/\//g, ".")
#        console.log("Consuming topic: ", projectTopic)
#        var exchange = 'amq.topic';
#        var _q = null
#
#        this.channel.assertQueue('', {exclusive: true}, (error, q) => {
#            if (error) {
#                throw error
#            }
#            
#            console.log(' [*] Waiting for logs. To exit press CTRL+C')
#            
#            this.channel.bindQueue(q.queue, exchange, projectTopic);
#            this.channel.consume(q.queue, (msg) => {
#
#                console.log(" [x] %s:'%s'", msg.fields.routingKey, msg.content);
#                
#                if (JSON.parse(msg.content).cryptographyDisabled){
#                    var response = JSON.parse(msg.content)
#                    response.configuration = JSON.parse(Buffer.from(JSON.parse(msg.content).configuration, "base64"));
#                    listeners.forEach(listener => {
#                        if (_.isFunction(listener.configuration)){
#                            listener.configuration(response)
#                        }
#                    })
#                } else {
#                    var signed_data = Buffer.from(JSON.parse(msg.content).configuration, "base64");
#                    var payloadEncripted = []
#                    for (var i = 0; i < signed_data.length; i++) {
#                        payloadEncripted.push(signed_data[i]);
#                    }
#    
#                    var received_data = new Buffer.alloc(signed_data.length);
#                    try{
#                        var privateKey = new Keystore().instance().getPrivateKey(JSON.parse(msg.content).nodeId).privateKey;
#                        var publicKey = new Keystore().instance().getCloudPublicKey();
#        
#                        var original_len = crypto_unsign(privateKey, publicKey, payloadEncripted, payloadEncripted.length, received_data);
#                        var response = JSON.parse(msg.content)
#                        response.configuration = JSON.parse(received_data.slice(0, original_len))
#                        
#                        listeners.forEach(listener => {
#                            if (_.isFunction(listener.configuration)){
#                                listener.configuration(response)
#                            }
#                        })
#                    }catch(e) {
#                        console.log(e)
#                    }
#                }
#            }, {
#                    noAck: true
#                }
#            )
#        })
#        
#    }
#}
#
#module.exports = AmqpDraxBroker