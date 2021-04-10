## OTA Client and Server

The project requirements:

1. ESP32 based OTA Client

2. Flask based OTA Server
3. OTA Client check for firmware update 
4. OTA Client update the firmware to latest available firmware

### OTA Server:

- OTA Server is developed on Flask framework
- Firmware are managed by Platforms.json file
- Firmwares are stored in bin folder
- Basic Authorization is required
- The available APIs are: 
  1. list [GET]: Get the list of available versions of firmware
  2. latest [GET]: Get the latest firmware version available
  3. update [GET]: get the firmware file with specified version in the request



### OTA Client:

- OTA Client is developed on ESP32
- Arduino Framework is used
- Environment: Platformio VS Code

