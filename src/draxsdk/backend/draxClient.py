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
            params = {"projectId": projectId, "from": fromTimeMillis, "to": toTimeMillis}
            nodeIds_json = {"nodeIds": nodeIds}
            response = requests.post(
                self.serviceUrl + '/nodes/states', 
                params=params, 
                headers=self._get_headers(),
                json=nodeIds_json
            )
            response.raise_for_status()
            return response.json()
        except RequestException:
            raise RequestException()
        
    def listConfigurations(self, projectId: str, nodeId: int, fromTimeMillis: int, toTimeMillis: int, fetchSize: int):
        try:
            params = {"projectId": projectId}
            if fetchSize is not None:
                params["fetchSize"] = fetchSize
            if fromTimeMillis is not None:
                params["from"] = fromTimeMillis
            if toTimeMillis is not None:
                params["to"] = toTimeMillis
            response = requests.get(
                self.serviceUrl + '/nodes/' + str(nodeId) + "/configurations", 
                params=params, 
                headers=self._get_headers()
            )
            response.raise_for_status()
            return response.json()
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
        
    def getNodeById(self, nodeId: int):
        """Returns node information given its code ID, making an HTTP GET Rest call to DraxCloud.
        The client must have been initialized with project ApiKey and ApiSecret in request headers.
        :param nodeId: project unique code ID
        :type nodeId: int
        :return: node information in JSON format
        :rtype: str
        """
        try:
            response = requests.get(
                self.serviceUrl + '/nodes/' + str(nodeId), 
                headers=self._get_headers()
            )
            response.raise_for_status()
            return response.json()
        except RequestException:
            raise RequestException()
        
    def listNodes(self, projectId: int, keyword:str, pagingState:str):
        """Returns information about all nodes part of a project, making an HTTP GET Rest call to DraxCloud.
        The client must have been initialized with project ApiKey and ApiSecret in request headers.
        :param projectId: project unique code ID
        :type projectId: str
        :return: nodes information in JSON format
        :rtype: str
        """
        try:
            params = {'projectId': projectId}
            if not keyword.strip():
                params['keyword'] = keyword
            if not pagingState.strip():
                params['pagingState'] = pagingState
            response = requests.get(
                self.serviceUrl + '/nodes/',
                params=params, 
                headers=self._get_headers()
            )
            response.raise_for_status()
            return response.json()
        except RequestException:
            raise RequestException()