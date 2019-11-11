import random
import time

# The sample connects to a device-specific MQTT endpoint on your IoT Hub.
from azure.iot.device import IoTHubDeviceClient, Message

# Define the JSON message to send to IoT Hub.
TEMPERATURE = 20.0
HUMIDITY = 60
MSG_TXT = '{{"temperature": {temperature},"humidity": {humidity}}}'

class SimulatedDevice:

    
    def __init__(self, connection_string):
        self.device = IoTHubDeviceClient.create_from_connection_string(connection_string)

    def send_device_to_cloud_messages(self):
        try:
            while True:
                # Build the message with simulated telemetry values.
                temperature = TEMPERATURE + (random.random() * 15)
                humidity = HUMIDITY + (random.random() * 20)
                msg_txt_formatted = MSG_TXT.format(temperature=temperature, humidity=humidity)
                message = Message(msg_txt_formatted)

                # Add a custom application property to the message.
                # An IoT hub can filter on these properties without access to the message body.
                if temperature > 30:
                    message.custom_properties["temperatureAlert"] = "true"
                else:
                    message.custom_properties["temperatureAlert"] = "false"

                # Send the message.
                print( "Sending message: {}".format(message) )
                self.device.send_message(message)
                print ( "Message successfully sent" )
                time.sleep(1)
        
        except KeyboardInterrupt:
            print("Simulator stopped")
