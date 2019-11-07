using System;

namespace simulated_device
{
    class Program
    {
        // The device connection string to authenticate the device with your IoT hub.
        // Using the Azure CLI:
        // az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyDotnetDevice --output table
        private readonly static string connectionString = "{Your device connection string here}";

        static void Main(string[] args)
        {
            Console.WriteLine("Ctrl-C to exit.\n");

            SimulatedDevice device = new SimulatedDevice(connectionString);
            device.SendDeviceToCloudMessagesAsync();
            Console.ReadLine();
        }
    }
}
