from consumer.listeners.listener import Listener

class Rele(Listener):

    def __init__(self, bindingKey=None):
        super().__init__(bindingKey)

    def callback(self, ch, method, properties, body):
        print("Rele: ")
        print("binding key: ", self.bindingKey)
        print("message body: ", body)
        #f = open("rele.txt", "a")
        #str_ = "Rele: binding key: " + str(self.bindingKey) + " message body: " + str(body)
        #f.write(str_)
    