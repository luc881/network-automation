# config/devices.py

# ── Conexión por consola serial (cable OIKWAN) ────────────────────────────────
SW_LAB = {
    "device_type": "cisco_ios_serial",
    "serial_settings": {
        "port":     "/dev/ttyUSB0",
        "baudrate": 9600,
        "bytesize": 8,
        "parity":   "N",
        "stopbits": 1,
    },
    "secret": "ClaseCCNA",
    "verbose": False,
}

# ── Conexión por Telnet ───────────────────────────────────────────────────────
TFTP_SERVER_IP = "192.168.54.100"   # ← IP de tu laptop en el lab

SW1 = {
    "device_type": "cisco_ios_telnet",
    "host":        "192.168.54.201",
    "username":    "admin",
    "password":    "Cisco123",
    "secret":      "ClaseCCNA",
    "port":        23,
    "verbose":     False,
}

SW2 = {
    "device_type": "cisco_ios_telnet",
    "host":        "192.168.54.202",
    "username":    "admin",
    "password":    "Cisco123",
    "secret":      "ClaseCCNA",
    "port":        23,
    "verbose":     False,
}

R1 = {
    "device_type": "cisco_ios_telnet",
    "host":        "192.168.54.203",
    "username":    "admin",
    "password":    "Cisco123",
    "secret":      "ClaseCCNA",
    "port":        23,
    "verbose":     False,
}
