#!/usr/bin/env python
import sys
import json

import pika

fp = open('example/config.json')
config = json.load(fp)

params = {
    'host': None,
    'port': None,
    'vhost': None,
}
params['config'] = config

host = "35.205.187.28"
port = 5672
password = params['config']['project']['apiSecret']
user = params['config']['project']['apiKey']
vhost = params['vhost'] if params['vhost'] is not None else "/"
projectId = params['config']['project']['id']
credentials = pika.PlainCredentials(user, password)

connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=host, port=port, 
                    virtual_host=vhost, credentials=credentials)
            ) 
channel = connection.channel()

channel.exchange_declare(exchange='amq.topic', exchange_type='topic', durable=True)

result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

binding_keys = ['node-sdk-development-65447.configurations.hmip']

for binding_key in binding_keys:
    channel.queue_bind(
        exchange='amq.topic', queue=queue_name, routing_key=binding_key)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()