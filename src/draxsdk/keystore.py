class Keystore:
    
    _instance = None
    draxPublicKey = ""
    nodesKeys = dict()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Keystore, cls).__new__(cls)
        return cls._instance

    def addConfigurationParams(self, draxPublicKey, nodesKeys=None):
        self.draxPublicKey = draxPublicKey
        if nodesKeys != None:
            self.nodesKeys = nodesKeys
    
    def getPrivateKey(self, nodeId: int):
        if not self.nodesKeys:
            raise "Node pk not found" 
        result = list(filter(lambda item: item['nodeId']==str(nodeId), self.nodesKeys))
        if len(result) > 0 and 'privateKey' in result[0].keys():
            return result[0]['privateKey']
        else: 
            raise "Node pk not found"

