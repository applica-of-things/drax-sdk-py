class DraxServerConfig:
    """This class represents all configuration settings of Drax Server to be loaded from 
    JSON configuration file. Use the utility function to load from file and create the obj.
    :param host: IP address of messagge broker (i.e.: RabbitMQ server)
    :type host: str
    :param vhost: Virtual host of message broker, defaults to '/'
    :type vhost: str, optional
    :param draxApiKey: Drax security api key to be added in headers requests sent to Drax cloud
    :type draxApiKey: str
    :param draxApiSecret: Drax security api secret to be added in headers requests sent to Drax cloud
    :type draxApiSecret: str
    :param serviceUrl: Drax cloud Rest APIs Service Url
    :type serviceUrl: str
    :param port: port number of message broker (i.e. Rabbit MQ), defaults to 5672
    :type port: int, optional
    :param draxPublicKey: Drax cloud server public key
    :type draxPublicKey: str
    """  
    host = ""
    port = ""
    vhost = ""
    serviceUrl = ""
    draxPublicKey = ""
    draxApiKey = ""
    draxApiSecret = ""
    nodesKeys = dict()
    
    def __init__(self, host:str, draxApiKey:str, draxApiSecret:str, serviceUrl:str, draxPublicKey:str, vhost='/', port=5672, nodesKeys={}):      
        self.host = host
        self.port = port
        self.vhost = vhost
        self.draxApiKey = draxApiKey
        self.draxApiSecret = draxApiSecret
        self.serviceUrl = serviceUrl
        self.draxPublicKey = draxPublicKey
        self.nodesKeys = nodesKeys
    
class DraxProjectParameters:    
    """This class represents all the setting parameters for Drax class.
    It contains all Drax Server configuration setting, plus project parameters
    :param projectId: project unique code ID
    :type projectId: str
    :param projectApiKey: project security api key to be added in headers requests sent to Drax cloud
    :type projectApiKey: str
    :param projectApiSecret: project security api secret to be added in headers requests sent to Drax cloud
    :type projectApiSecret: str
    :param draxServerConfig: Drax Server Configuration parameters
    :type draxServerConfig: <DraxServerConfig>
    """  
    draxServerConfig = None
    projectId = ""
    projectApiKey = ""
    projectApiSecret = ""
    
    def __init__(self, projectId: str, projectApiKey: str, projectApiSecret:str, draxServerConfig: DraxServerConfig):      
        self.projectId = projectId
        self.projectApiKey = projectApiKey
        self.projectApiSecret = projectApiSecret
        self.draxServerConfig = draxServerConfig
        
        
        
    
    