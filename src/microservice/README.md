# Web-app node IoT Hub Data Visualization

This repo contains code for a web application, which can read temperature and humidity data from IoT Hub and show the real-time data in a line chart on the web page.

## Sign in to the Azure portal

## Create and configure your IoT hub

1. [Create](https://portal.azure.com/#create/Microsoft.IotHub), or [select an existing](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.Devices%2FIotHubs), IoT hub.

1. Select the **Settings | Shared access policies** menu item, open the **service** policy, and copy a connection string to be used in later steps.

1. Select **Settings | Built-in endpoints | Events**, add a new consumer group (e.g. "monitoring"), and then change focus to save it. Note the name to be used in later steps.

## Send device data

## Run the visualization website

For a quick start, it is recommended to run the site locally, but you may also deploy it to Azure. Follow the corresponding option below.

### Inspect the code

Server.js is a service-side script that initializes the web socket and event hub wrapper class, and provides a callback to the event hub for incoming messages to broadcast them to the web socket.

Scripts/event-hub-reader.js is a service-side script that connects to the IoT hub's event hub using the specified connection string and consumer group, extracts the DeviceId and EnqueuedTimeUtc from metadata, and then relays message using the provided callback method.

Public/js/chart-device-data.js is a client-side script that listens on the web socket, keeps track of each DeviceId, and stores the the last 50 points of incoming device data. It then binds the selected device data to the chart object.

Public/index.html handles the UI layout for the web page, and references the necessary scripts for client-side logic.

### Run locally

1. To pass parameters to the website, you may use environment variables or parameters.
    - Open a command prompt or PowerShell terminal and set the environment variables **IotHubConnectionString** and **EventHubConsumerGroup**.

        > Syntax for Windows command prompt is `set key=value`, PowerShell is `$env:key="value"`, and Linux shell is `export key="value"`.

    - Or, if you are debugging with [VS Code](https://code.visualstudio.com/docs/nodejs/nodejs-debugging), you can edit the launch.json file and add these values in the env property.

        ```json
        "env": {
            "NODE_ENV": "local",
            "IotHubConnectionString": "<your iot hub connection string>",
            "EventHubConsumerGroup": "<your consumer group name>"
        }
        ```

1. In the same directory as package.json, run `npm install` to download and install referenced packages.

1. Run the website one of the following ways:
    - From the command-line use `npm start`
    - In VS Code, press F5 to start debugging

1. Watch for console output from the website.

1. If you are debugging, you may set breakpoints in any of the server-side scripts and step through the code to watch the code work.

1. Open a browser to <http://localhost:3000>.


