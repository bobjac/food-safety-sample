const Client = require('azure-iot-device').Client;
const Message = require('azure-iot-device').Message;
const Protocol = require('azure-iot-device-mqtt').Mqtt;

const sensor = require('node-dht-sensor');


var connectionString = 'Your Connection String' //


sendMessage = function(){

    sensor.read(22, 4, function(err, temperature, humidity) {
        if (!err) {
            console.log('temp: ' + temperature.toFixed(1) + '°C, ' +
                'humidity: ' + humidity.toFixed(1) + '%');
            var content = JSON.stringify({
            messageId: messageId++,
            deviceId: 'JennyPiSensor',
            temperature: temperature.toFixed(1),
            humidity: humidity.toFixed(1),
            time:new Date()
            });
    
            var message = new Message(content);
            console.log('Sending message: ' + content);
            client.sendEvent(message, (err) => {
            if (err) {
                console.error('Failed to send message to Azure IoT Hub');
            } else {
                console.log('Message sent to Azure IoT Hub');
            }
            setTimeout(sendMessage, 500);
            });
        }
        else{console.log('error while reading sensor');}
    });
};

receiveMessageCallback = function(msg) {
    var message = msg.getData().toString('utf-8');
    client.complete(msg, () => {
      console.log('Receive message: ' + message);
    });
  }


var client = Client.fromConnectionString(connectionString, Protocol);
messageId =0;
client.open((err) => {
    if (err) {
      console.error('[IoT hub Client] Connect error: ' + err.message);
      return;
    }
    client.on('disconnect',function(){
        client.removeAllListeners();
        console.log('client disconnected');
    });
    client.on('message', receiveMessageCallback);
    sendMessage();
});
