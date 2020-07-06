const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const path = require('path');
const EventHubReader = require('./scripts/event-hub-reader.js');
const fetch = require("node-fetch");

// HostName=FoodSafetyHub.azure-devices.net;SharedAccessKeyName=service;SharedAccessKey=W3fy/ruVogLuAQPgwZpWfMSCSUHSOUQtHT1umuGPOYM=
//const iotHubConnectionString = process.env.IotHubConnectionString;
const iotHubConnectionString = "HostName=FoodSafetyHub.azure-devices.net;SharedAccessKeyName=service;SharedAccessKey=W3fy/ruVogLuAQPgwZpWfMSCSUHSOUQtHT1umuGPOYM=";

// aksconsumer
//const eventHubConsumerGroup = process.env.EventHubConsumerGroup;
const eventHubConsumerGroup = "aksconsumer";

// http://52.186.36.71:80/api/QuorumTransactionService
//const apiEndpoint = process.env.ApiEndpoint;
const apiEndpoint = "http://52.186.36.71:80/api/QuorumTransactionService";

console.log(`iotHubConnectionString is ${iotHubConnectionString}`);
console.log(`eventHubConsumerGroup is ${eventHubConsumerGroup}`);

// Redirect requests to the public subdirectory to the root
const app = express();
app.use(express.static(path.join(__dirname, 'public')));
app.use((req, res /* , next */) => {
  res.redirect('/');
});

const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

wss.broadcast = (data) => {
  wss.clients.forEach((client) => {
    if (client.readyState === WebSocket.OPEN) {
      try {
        console.log(`Broadcasting data ${data}`);
        client.send(data);
      } catch (e) {
        console.error(e);
      }
    }
  });
};

server.listen(process.env.PORT || '3000', () => {
  console.log('Listening on %d.', server.address().port);
});

const eventHubReader = new EventHubReader(iotHubConnectionString, eventHubConsumerGroup);

async function postData(url = '', data = {}) {
  // Default options are marked with *
  const response = await fetch(url, {
    method: 'POST', // *GET, POST, PUT, DELETE, etc.
    mode: 'cors', // no-cors, *cors, same-origin
    cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
    credentials: 'same-origin', // include, *same-origin, omit
    headers: {
      'Content-Type': 'application/json'
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    redirect: 'follow', // manual, *follow, error
    referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
    body: JSON.stringify(data) // body data type must match "Content-Type" header
  });
  return response.json(); // parses JSON response into native JavaScript objects
}

let sendCounter = 0;

(async () => {
  await eventHubReader.startReadMessage((message, date, deviceId) => {
    try {
      const payload = {
        IotData: message,
        MessageDate: date || Date.now().toISOString(),
        DeviceId: deviceId,
      };

      wss.broadcast(JSON.stringify(payload));
      
      if (deviceId === "simulator-micya") {
        sendCounter = sendCounter + 1;
        let apiPayload = {
          "contractAddress" : "0xBC5FB78512b79CF2fbE6a8041be36BD473E4ECdc",
          "functionName" : "SetRecord",
          "inputParams" : [
            "sensor1",
            55,
            48,
            "05/31/2020 12:37AM"
          ]
        };

        console.log(`Message from simulator with a value of ${apiPayload}`);

        if (sendCounter == 20) { 
          console.log(`Calling the api with an endpoint of ${apiEndpoint}`);
          postData(apiEndpoint, apiPayload)
                .then(data => {
                  console.log(data); // JSON data parsed by `response.json()` call
                });
          sendCounter = 0;
        }
      }

    } catch (err) {
      console.error('Error broadcasting: [%s] from [%s].', err, message);
    }
  });
})().catch();