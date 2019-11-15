from SimulatedDevice import SimulatedDevice

# The device connection string to authenticate the device with your IoT hub.
# Using the Azure CLI:
# az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table
CONNECTION_STRING = "{Your IoT hub device connection string}"

if __name__ == '__main__':
    print ("Press Ctrl-C to exit")
    device = SimulatedDevice(CONNECTION_STRING)
    device.send_device_to_cloud_messages()
