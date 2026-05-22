# config/devices.py

# ── Conexión por consola serial (cable OIKWAN) ────────────────────────────────
SW_LAB = {
    "device_type": "cisco_ios_serial",
    "serial_settings": {
        "port":     "/dev/ttyUSB0",
        "baudrate": 9600,
        "bytesize": 8,        # ← era data_bits (nombre pyserial)
        "parity":   "N",
        "stopbits": 1,        # ← era stop_bits (nombre pyserial)
    },
    "secret": "ClaseCCNA",
    "verbose": False,
}

# ── Conexión por Telnet ───────────────────────────────────────────────────────
TFTP_SERVER_IP = "192.168.1.100"

SW1 = {
    "device_type": "cisco_ios_telnet",
    "host":        "192.168.1.11",
    "username":    "admin",
    "password":    "Cisco123",
    "secret":      "ClaseCCNA",
    "port":        23,
    "verbose":     False,
}

SW2 = {
    "device_type": "cisco_ios_telnet",
    "host":        "192.168.1.12",
    "username":    "admin",
    "password":    "Cisco123",
    "secret":      "ClaseCCNA",
    "port":        23,
    "verbose":     False,
}

R1 = {
    "device_type": "cisco_ios_telnet",
    "host":        "192.168.1.1",
    "username":    "admin",
    "password":    "Cisco123",
    "secret":      "ClaseCCNA",
    "port":        23,
    "verbose":     False,
}
