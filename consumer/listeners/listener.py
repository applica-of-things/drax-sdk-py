class Listener:

    bindingKey = None

    def __init__(self, bindingKey=None):
        self.bindingKey = bindingKey

    def getBindingKey(self):
        return self.bindingKey

    def callback(self, ch, method, properties, body):
        pass