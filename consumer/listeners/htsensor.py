from consumer.listeners.listener import Listener

class HTSensor(Listener):

    def __init__(self, bindingKey=None):
        super().__init__(bindingKey)

    def callback(self, ch, method, properties, body):
        print("HTSensor: ")
        print("binding key: ", self.bindingKey)
        print("message body: ", body)

    
    