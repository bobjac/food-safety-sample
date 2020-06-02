
Subscribing to blockchain events via Blockchain Data Manager: https://docs.microsoft.com/en-us/azure/blockchain/service/data-manager-cosmosdb

Blockchain events can be subscribed to by routing through several services:

1. Blockchain service
2. Data Manager
3. Event Grid topic
4. Logic app
5. Final workflow/destination

If subscribing for reporting purposes, events can be filtered in the logic app. An example logic app is included that filters for state change events similar to the below:

    {
        "TransactionHash": "0x90563022f8f1504fbee848f673550e972e0bea77ae14a2b6f484709ad5ce3332",
        "BlockHash": "0x7b3811a0cabd3fad43b87ac04a982564932ed8937fa71a3e2af54c940a22c9a5",
        "BlockNumber": 37215,
        "ContractAddress": "0xe292477c93c5a84e02c23329875096e96d25929c",
        "EventName": "StateChanged",
        "EventValue": [
            {
                "ParameterName": "stateData",
                "ParameterType": "string",
                "ParameterValue": "HORRIBLE!!!!!!",
                "Indexed": false
            }
        ],
        "RawTopicHex": "0x8fbf346523616c015d34c71713ea41bb98008282341b0f191f578d20d7ed26e2",
        "BlockTimestamp": 1590896343,
        "ScheduleOffsetMillisec": 0,
        "MessageId": "f03a8dcd-a4a2-4636-ab92-031f0374401a",
        "MessageType": "DecodedContractEventsMsg",
        "Connection": "https://transaction-node-testmem.blockchain.azure.com:3200",
        "WatcherId": "8420e236-8be4-4728-b0eb-a9b4841f1b71",
        "BatchSize": 0,
        "SequenceNumber": 0,
        "InitMessageId": "00000000-0000-0000-0000-000000000000",
        "id": "2020-05-31T03:39:04.8740271Z",
        "_rid": "4eFpAMplGbABAAAAAAAAAA==",
        "_self": "dbs/4eFpAA==/colls/4eFpAMplGbA=/docs/4eFpAMplGbABAAAAAAAAAA==/",
        "_etag": "\"0900862f-0000-0700-0000-5ed326d80000\"",
        "_attachments": "attachments/",
        "_ts": 1590896344
    }