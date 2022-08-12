import json
import requests

from requests import RequestException

class DraxClient:

    def __init__(self, params):
        self.params = params
        self.serviceUrl = 'https://draxcloud.com/core'
        self.headers = {
                "drax-api-secret": self.params['config']['project']['apiSecret'],
                "drax-api-key": self.params['config']['project']['apiKey']
        }

    def handshake(self, node):
        try:
            payload = {
                'urn': node['urn'],
                'projectId': self.params['config']['project']['id'],
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
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except RequestException:
            raise RequestException()
        
    def listStates(self, projectId: str, nodeId: int, fromTimeMillis: int, toTimeMillis: int):
        print("hello")
        try:
            params = {"projectId": projectId, "from": fromTimeMillis, "to": toTimeMillis}
            response = requests.get(
                self.serviceUrl + '/nodes/' + str(nodeId) + "/states", 
                params=params, 
                headers=self.headers
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
        try:
            response = requests.get(
                self.serviceUrl + '/projects/' + str(projectId), 
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except RequestException:
            raise RequestException()