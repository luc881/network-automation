# config/devices.py
# Connection settings for all lab devices.
# Update the serial port to match your OIKWAN cable.

# ── Conexión por consola (cable serial OIKWAN) ────────────────────────────────
# Usado en: prácticas de MAC flooding, password recovery, configuración inicial
SW_LAB = {
    "device_type": "cisco_ios_serial",
    "serial_settings": {
        "port": "/dev/tty.usbserial-A9ATYFK6",  # <-- actualiza con tu puerto
        "baudrate": 9600,
        "data_bits": 8,
        "parity": "N",
        "stop_bits": 1,
    },
    "secret": "",
    "verbose": False,
}

# ── Conexión por Telnet (práctica 2 y 3) ─────────────────────────────────────
# Requisito: IP de administración ya configurada en cada switch por consola.
# Busca tu IP con: ifconfig | grep "inet 192"

TFTP_SERVER_IP = "192.168.1.100"  # <-- IP de tu Mac en la red del switch

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