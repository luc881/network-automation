# config/devices.py
# Connection settings for all lab devices.
# Update the serial port to match your OIKWAN cable.

SW_LAB = {
    "device_type": "cisco_ios_serial",
    "serial_settings": {
        "port": "/dev/tty.usbserial-A9ATYFK6",  # <-- update this
        "baudrate": 9600,
        "data_bits": 8,
        "parity": "N",
        "stop_bits": 1,
    },
    "secret": "",       # enable password (leave empty if none)
    "verbose": False,
}
