# config/devices.py
# Connection settings for all lab devices.
# Update the serial port to match your OIKWAN cable.

SW_LAB = {
    "device_type": "cisco_ios_serial",
    "serial_settings": {
        "port": "/dev/cu.usbserial-A9ATYFK6",
        "baudrate": 9600,
        "bytesize": 8,       # antes: data_bits
        "parity": "N",
        "stopbits": 1,       # antes: stop_bits
    },
    "secret": "",
    "verbose": False,
}