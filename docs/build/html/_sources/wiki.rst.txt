Drax SDK Wiki (HowTo guide)
==========================================================================

Initializing Drax
-----------------

In case of **internal Drax module** (i.d. drax-ai), having access to Drax Admin credentials, it is possibile to initialize a drax client instance and get project information, within project credentials details, 
calling Drax platform REST API service. 
Moreover, using project credentials, the drax instance can be created.

..  code-block:: python
    
    projectId="sampleProjectId"

    #load Drax Admin credentials for internal configuration file
    draxServerConfig = drax.loadConfigFromFile(configFilePath)
    client = draxClient.DraxClient(draxServerConfig.serviceUrl, draxServerConfig.draxApiKey, draxServerConfig.draxApiSecret)

    #get project information from ID using draxClient (API REST service)
    projectInfo = client.getProjectById(projectId)

    #initialize Drax with project parameters
    draxProjectParams = DraxProjectParameters(projectId, projectInfo['apiKey'], projectInfo['apiSecret'], draxServerConfig)

    #init drax instance
    _drax = drax.Drax(draxProjectParams)
    _drax.start()

    # code here....

    _drax.stop()

Sample of **configuration file** (JSON format) for internal Drax module:

..  code-block:: JSON
    
    {
    "draxPublicKey": "bb099d6dce1a953c7c5d2380815ee02ea191b39206000000ceefb3c222b480459556ce440379cef89db0ccfc04000000",
    "draxApiKey": "XXXXXX",
    "draxApiSecret": "XXXXXX",
    "draxServer" : {
        "host" : "35.205.187.28",
        "port" : 5672,
        "vhost" : "/",
        "serviceUrl" : "https://draxcloud.com/core"
    },
    "nodesKeys" :[
        {
            "nodeId": "3839",
            "public_key": "db99316293e601b64f0cc42a69fa114ae6f772c201000000e23296ec17cc978798eaa8ccc99e85da30be50e102000000",
            "privateKey": "c85bf80bd1c484cadc7e6ab1e74145dc5018658202000000"
        },
        {
            "nodeId": "4348",
            "public_key": "0460a4febdd287f4e9a6b43f208e010b2140b67d0300000080f961adf3ef5d2878f50066790dbc4ac2a1786203000000",
            "privateKey": "50891df1beb0a9fec171c34fb801edfc683fab6e00000000"
        }
        ]
    }


In case of a **third-part application**, it must own alrady project credentials to instantiate a Drax instance.  

..  code-block:: python
    
    # sample data
    projectId = "sampleProjectId"
    projectApiKey = "euinr7899vffkd"
    projectApiSecret = "33884940fsdmfemrnegr00040frgfrrg"

    #load Drax Admin credentials for internal configuration file
    draxServerConfig = drax.loadConfigFromFile(configFilePath)

    #initialize Drax with project parameters
    draxProjectParams = DraxProjectParameters(projectId, projectApiKey, projectApiSecret, draxServerConfig)

    #init drax instance
    _drax = drax.Drax(draxProjectParams)
    _drax.start()

    # code here....

    _drax.stop()

Sample of **configuration file** (JSON format) for third-part application:

..  code-block:: JSON
    
    {
    "draxPublicKey": "bb099d6dce1a953c7c5d2380815ee02ea191b39206000000ceefb3c222b480459556ce440379cef89db0ccfc04000000",
    "draxServer" : {
        "host" : "35.205.187.28",
        "port" : 5672,
        "vhost" : "/",
        "serviceUrl" : "https://draxcloud.com/core"
    },
    "nodesKeys" :[
        {
            "nodeId": "3839",
            "public_key": "db99316293e601b64f0cc42a69fa114ae6f772c201000000e23296ec17cc978798eaa8ccc99e85da30be50e102000000",
            "privateKey": "c85bf80bd1c484cadc7e6ab1e74145dc5018658202000000"
        },
        {
            "nodeId": "4348",
            "public_key": "0460a4febdd287f4e9a6b43f208e010b2140b67d0300000080f961adf3ef5d2878f50066790dbc4ac2a1786203000000",
            "privateKey": "50891df1beb0a9fec171c34fb801edfc683fab6e00000000"
        }
        ]
    }

