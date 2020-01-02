using System;

namespace simulated_device
{
    class Program
    {
        // The device connection string to authenticate the device with your IoT hub.
        // Using the Azure CLI:
        // az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyDotnetDevice --output table
        private readonly static string connectionString = "HostName=bobjacfoodsafety.azure-devices.net;DeviceId=MyDotnetDevice;SharedAccessKey=YJRbHoN4xE12tz7cpNZ3m7FF10LKlGUiVSvCEFA8t9Y=";

        static void Main(string[] args)
        {
            Console.WriteLine("Ctrl-C to exit.\n");

            SimulatedDevice device = new SimulatedDevice(connectionString);
            device.SendDeviceToCloudMessagesAsync();
            Console.ReadLine();
        }
    }
}
