import json
import requests

from requests import RequestException

class DraxClient:
    serviceUrl = ""
    apiKey = ""
    apiSecrect = ""
    
    def __init__(self, serviceUrl:str, apiKey:str, apiSecret:str):  
        self.serviceUrl = serviceUrl
        self.apiKey = apiKey
        self.apiSecrect = apiSecret
        
    def _get_headers(self):
        return {
            "drax-api-key": self.apiKey,
            "drax-api-secret": self.apiSecrect
        }
        
    #TODO: refactoring this method, not working
    def handshake(self, node):
        try:
            payload = {
                'urn': node['urn'],
                'projectId': node['projectId'],
                'supportedTypes': node['supportedTypes'] if node['supportedTypes'] is not None else [],
                'configurationPublishTopic': node['configurationPublishTopic'],
                'statePublishTopic': node['statePublishTopic'],
                'initialState': node['initialState'] if node['initialState'] is not None else dict(),
                'name': node['name'],
                'extras': node['extras'] if 'extras' in node.keys() else []
            }
            response = requests.post(
                self.serviceUrl + '/handshake', 
                data=payload, 
                headers=self._get_headers()
            )
            response.raise_for_status()
            return response.json()
        except RequestException:
            raise RequestException()
        
    def listStates(self, projectId: str, nodeId: int, fromTimeMillis: int, toTimeMillis: int):
        try:
            params = {"projectId": projectId, "from": fromTimeMillis, "to": toTimeMillis}
            response = requests.get(
                self.serviceUrl + '/nodes/' + str(nodeId) + "/states", 
                params=params, 
                headers=self._get_headers()
            )
            response.raise_for_status()
            return response.json()
        except RequestException:
            raise RequestException()
        
    def listNodesStates(self, projectId: str, nodeIds: list[int], fromTimeMillis: int, toTimeMillis: int):
        try:
            response = dict()
            print("nodeIds: " + str(nodeIds))
            for nodeId in nodeIds:
                print("nodeId: " + str(nodeId))
                response[nodeId] = self.listStates(projectId, nodeId, fromTimeMillis, toTimeMillis)
            return json.dumps(response)
        except RequestException:
            raise RequestException()
    
    def getProjectById(self, projectId: str):
        """Returns project information given its code ID, making an HTTP GET Rest call to DraxCloud.
        The client must have been initialized with administrator ApiKey and ApiSecret in request headers.
        This method must be called as "administrator".
        :param projectId: project unique code ID
        :type projectId: str
        :return: project information in JSON format
        :rtype: str
        """
        try:
            response = requests.get(
                self.serviceUrl + '/projects/' + str(projectId), 
                headers=self._get_headers()
            )
            response.raise_for_status()
            return response.json()
        except RequestException:
            raise RequestException()