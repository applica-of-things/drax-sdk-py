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
        
    def listStates(self, projectId, nodeId, fromTime, toTime):
        try:
            params = {"projectId": projectId, "from": fromTime, "to": toTime}
            response = requests.get(
                self.serviceUrl + '/nodes/' + str(nodeId) + "/states", 
                params=params, 
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except RequestException:
            raise RequestException()