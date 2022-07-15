from http import client
import aiohttp


class DraxClient:

    def __init__(self, params):
        self.params = params
        self.serviceUrl = 'https://draxcloud.com/core'

    async def handshake(self, node):
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
            headers = {
                "drax-api-secret": self.params['config']['project']['apiSecret'],
                "drax-api-key": self.params['config']['project']['apiKey']
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(self.serviceUrl + '/handshake', 
                    json=payload, headers=headers) as response:
                    responseBody = await response.text()
                    #print(responseBody)
                    response.raise_for_status()
                    return response
        except IOError:
            raise IOError