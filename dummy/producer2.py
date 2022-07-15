import sys

import pika

# connection: specify different broker message address
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost')) 
channel = connection.channel()

# create a queue called 'hello'
channel.queue_declare(queue='hello')

message = ''.join(sys.argv[1:]) or "Hello World"
# publishing by an exchange the message "Hello World!"
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=message)

print(" [x] Sent %r" % message)

connection.close()