class Keystore:
    
    _instance = None
    config = dict()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Keystore, cls).__new__(cls)
        return cls._instance

    def addConfig(self, config):
        self.config = config
    
    def getPrivateKey(self, nodeId):
        if 'keys' not in self.config.keys():
            raise "NodeId not found in config.json" 
        result = list(filter(lambda item: item['nodeId']==str(nodeId), self.config['keys']))
        if len(result) > 0 and 'privateKey' in result[0].keys():
            return result[0]['privateKey']
        else: 
            raise "NodeId not found in config.json"
        
    def getCloudPublicKey(self):
        if 'draxPublicKey' not in self.config.keys():
            raise "Public Key not found in config.json"
        pubKey = self.config['draxPublicKey']
        if pubKey is not None:
            return pubKey
        else:
            raise "Public Key not found in config.json"

