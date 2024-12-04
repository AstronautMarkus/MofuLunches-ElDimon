<div align="center">

# MofuLunches-ElDimon 

<img src="https://raw.githubusercontent.com/AstronautMarkus/MofuLunches-Web/refs/heads/dev/mofulunches-web/app/static/img/icon.png" alt="MofuLunches-logo" width="120">

</div>

This daemon is a crucial component of the [MofuLunches platform](https://github.com/topics/mofulunches), specifically for [MofuLunches Totem](https://github.com/AstronautMarkus/MofuLunches-Totem), a student project designed to manage and serve core API services for the totem, mobile app, and admin web portal. The daemon listens to RFID data from an Arduino device connected via USB, processes it, and outputs it in JSON format for integration with the MofuLunches backend system.

## Overview

This project is a daemon that listens to RFID data from an Arduino device connected via USB. It reads the data, processes it, and outputs it in JSON format.

> Note:
> This daemon is specifically designed to work on Linux systems. It relies on Linux-specific device paths (`/dev/ttyUSB*` and `/dev/ttyACM*`) to detect connected Arduino devices. As such, it will not function correctly on Windows or macOS systems. Ensure you are running a compatible Linux distribution before using this daemon.
<img src="https://www.clipartmax.com/png/full/277-2771263_cirno-shrug-discord-emoji-shrug-emote-discord.png" width=50px>




## Features

- Automatically detects connected Arduino devices.
- Reads and processes RFID data.
- Outputs data in JSON format for easy integration with other systems.
- Handles connection errors and retries automatically.

## Ports

The daemon scans for Arduino devices connected to `/dev/ttyUSB*` and `/dev/ttyACM*` ports. It selects the first available port for communication.

## JSON System

The daemon outputs various status messages and data in JSON format. Below are some examples:

### Connection Attempt
```json
{
  "code": 10,
  "message": "Attempting to connect to /dev/ttyUSB0"
}
```

### Successful Connection
```json
{
  "code": 20,
  "message": "Working correctly on /dev/ttyUSB0"
}
```

### Data Received
```json
{
  "code": 30,
  "data": 12345
}
```

### Errors
- **Connection Error**:
    ```json
    {
      "code": 10,
      "message": "Connection error on /dev/ttyUSB0. Attempting to reconnect: [Error Message]"
    }
    ```

- **Decoding Error**:
    ```json
    {
      "code": 40,
      "message": "Warning: Decoding error - [Error Message]"
    }
    ```

- **Unexpected Error**:
    ```json
    {
      "code": 60,
      "message": "Unexpected error: [Error Message]"
    }
    ```

## Usage

1. Ensure Python with virtualenv is installed on your system.

2. Install the `pyserial` package if not already installed:
    ```bash
    pip install pyserial
    ```
3. Run the script:
    ```bash
    python ElDimon.py
    ```
4. The daemon will detect the Arduino device and start listening for RFID data.

## Troubleshooting

- **No Arduino Device Detected**:
    - Ensure the Arduino is properly connected to the USB port.
    - Check if the device is listed under `/dev/ttyUSB*` or `/dev/ttyACM*`.

- **Decoding Errors**:
    - Verify the data sent by the Arduino is in the expected format.

## Contributing

Feel free to fork this repository and contribute to improve the daemon. Pull requests are welcome!

## Compiling the Daemon

If you need to compile the daemon into a standalone executable, you can use `pyinstaller`. Follow these steps:

1. Ensure `pyinstaller` is installed on your system:

    ```bash
    pip install pyinstaller
    ```
2. Compile the daemon using the following command:

    ```bash
    pyinstaller --noconfirm --onefile --console ElDimon.py -n <eldimon>
    ```
   Replace `<eldimon>` with the desired name for the executable.

This will generate a standalone executable in the `dist` directory.

