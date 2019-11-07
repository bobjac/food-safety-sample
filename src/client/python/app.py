#!/usr/bin/env python

import random
import time
import sys
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue
import config as config
import Adafruit_DHT
import re
import yaml
from telemetry import Telemetry

# HTTP options
# Because it can poll "after 9 seconds" polls will happen effectively
# at ~10 seconds.
# Note that for scalabilty, the default value of minimumPollingTime
# is 25 minutes. For more information, see:
# https://azure.microsoft.com/documentation/articles/iot-hub-devguide/#messaging
TIMEOUT = 241000
MINIMUM_POLLING_TIME = 9

# messageTimeout - the maximum time in milliseconds until a message times out.
# The timeout period starts at IoTHubClient.send_event_async.
# By default, messages do not expire.
MESSAGE_TIMEOUT = 10000

RECEIVE_CONTEXT = 0
MESSAGE_COUNT = 0
MESSAGE_SWITCH = True
TWIN_CONTEXT = 0
SEND_REPORTED_STATE_CONTEXT = 0
METHOD_CONTEXT = 0
TEMPERATURE_ALERT = 30.0

# global counters
RECEIVE_CALLBACKS = 0
SEND_CALLBACKS = 0
BLOB_CALLBACKS = 0
TWIN_CALLBACKS = 0
SEND_REPORTED_STATE_CALLBACKS = 0
METHOD_CALLBACKS = 0
EVENT_SUCCESS = "success"
EVENT_FAILED = "failed"

# chose HTTP, AMQP or MQTT as transport protocol
PROTOCOL = IoTHubTransportProvider.MQTT

# String containing Hostname, Device Id & Device Key in the format:
# "HostName=<host_name>;DeviceId=<device_id>;SharedAccessKey=<device_key>"
telemetry = Telemetry()

def is_correct_connection_string():
    m = re.search("HostName=.*;DeviceId=.*;", CONNECTION_STRING)
    if m:
        return True
    else:
        return False

def send_temp_and_humidity(sensor, pin):

    try:
        client = iothub_client_init()
        
        if client.protocol == IoTHubTransportProvider.MQTT:
            print ( "IoTHubClient is reporting state" )
            reported_state = "{\"newState\":\"standBy\"}"
            client.send_reported_state(reported_state, len(reported_state), send_reported_state_callback, SEND_REPORTED_STATE_CONTEXT)
    
        telemetry.send_telemetry_data(parse_iot_hub_name(), EVENT_SUCCESS, "IoT hub connection is established")

        while True:
            global MESSAGE_COUNT,MESSAGE_SWITCH
            if MESSAGE_SWITCH:
                # Try to grab a sensor reading.  Use the read_retry method which will retry up
                # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
                humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

                # Un-comment the line below to convert the temperature to Fahrenheit.
                temperature = temperature * 9/5.0 + 32

                # Note that sometimes you won't get a reading and
                # the results will be null (because Linux can't
                # guarantee the timing of calls to read the sensor).
                # If this happens try again!
                if humidity is not None and temperature is not None:
                    print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
                else:
                    print('Failed to get reading. Try again!')
                    sys.exit(1)
                
                # send a few messages every minute
                print ( "IoTHubClient sending %d messages" % MESSAGE_COUNT )

                msg_txt_formatted = MSG_TXT % (
                    temperature,
                    humidity)
                print (msg_txt_formatted)
                message = IoTHubMessage(msg_txt_formatted)
                # optional: assign ids
                message.message_id = "message_%d" % MESSAGE_COUNT
                message.correlation_id = "correlation_%d" % MESSAGE_COUNT
                # optional: assign properties
                prop_map = message.properties()
                prop_map.add("temperatureAlert", "true" if temperature > TEMPERATURE_ALERT else "false")

                client.send_event_async(message, send_confirmation_callback, MESSAGE_COUNT)
                print ( "IoTHubClient.send_event_async accepted message [%d] for transmission to IoT Hub." % MESSAGE_COUNT )

                status = client.get_send_status()
                print ( "Send status: %s" % status )
                MESSAGE_COUNT += 1
            time.sleep(config.MESSAGE_TIMESPAN / 1000.0)
    except IoTHubError as iothub_error:
        print ( "Unexpected error %s from IoTHub" % iothub_error )
        telemetry.send_telemetry_data(parse_iot_hub_name(), EVENT_FAILED, "Unexpected error %s from IoTHub" % iothub_error)
        return
    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

def receive_message_callback(message, counter):
    global RECEIVE_CALLBACKS
    message_buffer = message.get_bytearray()
    size = len(message_buffer)
    print ( "Received Message [%d]:" % counter )
    print ( "    Data: <<<%s>>> & Size=%d" % (message_buffer[:size].decode("utf-8"), size) )
    map_properties = message.properties()
    key_value_pair = map_properties.get_internals()
    print ( "    Properties: %s" % key_value_pair )
    counter += 1
    RECEIVE_CALLBACKS += 1
    print ( "    Total calls received: %d" % RECEIVE_CALLBACKS )
    return IoTHubMessageDispositionResult.ACCEPTED


def send_confirmation_callback(message, result, user_context):
    global SEND_CALLBACKS
    print ( "Confirmation[%d] received for message with result = %s" % (user_context, result) )
    map_properties = message.properties()
    print ( "    message_id: %s" % message.message_id )
    print ( "    correlation_id: %s" % message.correlation_id )
    key_value_pair = map_properties.get_internals()
    print ( "    Properties: %s" % key_value_pair )
    SEND_CALLBACKS += 1
    print ( "    Total calls confirmed: %d" % SEND_CALLBACKS )
    # led_blink()


def device_twin_callback(update_state, payload, user_context):
    global TWIN_CALLBACKS
    print ( "\nTwin callback called with:\nupdateStatus = %s\npayload = %s\ncontext = %s" % (update_state, payload, user_context) )
    TWIN_CALLBACKS += 1
    print ( "Total calls confirmed: %d\n" % TWIN_CALLBACKS )


def send_reported_state_callback(status_code, user_context):
    global SEND_REPORTED_STATE_CALLBACKS
    print ( "Confirmation for reported state received with:\nstatus_code = [%d]\ncontext = %s" % (status_code, user_context) )
    SEND_REPORTED_STATE_CALLBACKS += 1
    print ( "    Total calls confirmed: %d" % SEND_REPORTED_STATE_CALLBACKS )


def device_method_callback(method_name, payload, user_context):
    global METHOD_CALLBACKS,MESSAGE_SWITCH
    print ( "\nMethod callback called with:\nmethodName = %s\npayload = %s\ncontext = %s" % (method_name, payload, user_context) )
    METHOD_CALLBACKS += 1
    print ( "Total calls confirmed: %d\n" % METHOD_CALLBACKS )
    device_method_return_value = DeviceMethodReturnValue()
    device_method_return_value.response = "{ \"Response\": \"This is the response from the device\" }"
    device_method_return_value.status = 200
    if method_name == "start":
        MESSAGE_SWITCH = True
        print ( "Start sending message\n" )
        device_method_return_value.response = "{ \"Response\": \"Successfully started\" }"
        return device_method_return_value
    if method_name == "stop":
        MESSAGE_SWITCH = False
        print ( "Stop sending message\n" )
        device_method_return_value.response = "{ \"Response\": \"Successfully stopped\" }"
        return device_method_return_value
    return device_method_return_value


def blob_upload_conf_callback(result, user_context):
    global BLOB_CALLBACKS
    print ( "Blob upload confirmation[%d] received for message with result = %s" % (user_context, result) )
    BLOB_CALLBACKS += 1
    print ( "    Total calls confirmed: %d" % BLOB_CALLBACKS )

def iothub_client_init():
    # prepare iothub client
    client = IoTHubClient(CONNECTION_STRING, PROTOCOL)
    client.set_option("product_info", "HappyPath_RaspberryPi-Python")
    if client.protocol == IoTHubTransportProvider.HTTP:
        client.set_option("timeout", TIMEOUT)
        client.set_option("MinimumPollingTime", MINIMUM_POLLING_TIME)
    # set the time until a message times out
    client.set_option("messageTimeout", MESSAGE_TIMEOUT)
    # to enable MQTT logging set to 1
    if client.protocol == IoTHubTransportProvider.MQTT:
        client.set_option("logtrace", 0)
    client.set_message_callback(
        receive_message_callback, RECEIVE_CONTEXT)
    if client.protocol == IoTHubTransportProvider.MQTT or client.protocol == IoTHubTransportProvider.MQTT_WS:
        client.set_device_twin_callback(
            device_twin_callback, TWIN_CONTEXT)
        client.set_device_method_callback(
            device_method_callback, METHOD_CONTEXT)
    return client

def print_last_message_time(client):
    try:
        last_message = client.get_last_message_receive_time()
        print ( "Last Message: %s" % time.asctime(time.localtime(last_message)) )
        print ( "Actual time : %s" % time.asctime() )
    except IoTHubClientError as iothub_client_error:
        if iothub_client_error.args[0].result == IoTHubClientResult.INDEFINITE_TIME:
            print ( "No message received" )
        else:
            print ( iothub_client_error )

def get_connection_string():
    connection_string = ""

    with open("config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.BaseLoader)
    
    if 'iothub' in cfg:
        connection_string = cfg['iothub']['connectionstring']
    else:
        if len(sys.argv) == 4:
            connection_string = sys.argv[3]

    print('The connection string is ' + connection_string)
    return connection_string

def get_message_timespan():
    timespan = 1000
    with open("config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.BaseLoader)
    
    if 'other' in cfg:
        timespan = cfg['other']['messagetimespan']
    return timespan

MESSAGE_TIMESPAN = get_message_timespan()

#def led_blink():
#    GPIO.output(config.GPIO_PIN_ADDRESS, GPIO.HIGH)
#    time.sleep(config.BLINK_TIMESPAN / 1000.0)
#    GPIO.output(config.GPIO_PIN_ADDRESS, GPIO.LOW)

def usage():
    print ( "Usage: iothub_client_sample.py -p <protocol> -c <connectionstring>" )
    print ( "    protocol        : <amqp, amqp_ws, http, mqtt, mqtt_ws>" )
    print ( "    connectionstring: <HostName=<host_name>;DeviceId=<device_id>;SharedAccessKey=<device_key>>" )

def parse_iot_hub_name():
    m = re.search("HostName=(.*?)\.", CONNECTION_STRING)
    return m.group(1)

CONNECTION_STRING = get_connection_string()

if not is_correct_connection_string():
    print ( "Device connection string is not correct." )
    telemetry.send_telemetry_data(None, EVENT_FAILED, "Device connection string is not correct.")
    sys.exit(0)

MSG_TXT = "{\"deviceId\": \"Raspberry Pi - Python\",\"temperature\": %f,\"humidity\": %f}"

if __name__ == "__main__":
    print ( "\nPython %s" % sys.version )
    print ( "IoT Hub Client for Python" )
    # Parse command line parameters.
    sensor_args = { '11': Adafruit_DHT.DHT11,
                    '22': Adafruit_DHT.DHT22,
                    '2302': Adafruit_DHT.AM2302 }

    if len(sys.argv) < 2:
        print ( "You need to provide the device connection string as command line arguments." )
        telemetry.send_telemetry_data(None, EVENT_FAILED, "Device connection string is not provided")
        sys.exit(0)

    sensor = 0
    pin = 0
    if len(sys.argv) >= 3 and sys.argv[1] in sensor_args:
        sensor = sensor_args[sys.argv[1]]
        pin = sys.argv[2]
    else:
        print('Usage: sudo ./Adafruit_DHT.py [11|22|2302] <GPIO pin number>')
        print('Example: sudo ./Adafruit_DHT.py <connection string> 2302 4 - Read from an AM2302 connected to GPIO pin #4')
        sys.exit(1)

    send_temp_and_humidity(sensor, pin)



