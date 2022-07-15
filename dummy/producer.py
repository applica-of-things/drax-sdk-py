import pika

# connection: specify different broker message address
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost')) 
channel = connection.channel()

# create a queue called 'hello'
channel.queue_declare(queue='hello')

# publishing by an exchange the message "Hello World!"
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')

print(" [x] Sent 'Hello World!'")

connection.close()