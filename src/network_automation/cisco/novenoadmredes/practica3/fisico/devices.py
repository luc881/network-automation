# network_automation/cisco/novenoadmredes/practica3/fisico/devices.py
# Ajusta las IPs segun la asignacion del laboratorio presencial

R1 = {
    "device_type": "cisco_ios_telnet",
    "host": "192.168.1.100",
    "username": "admin",
    "password": "Cisco123",
    "secret": "ClaseCCNA",
    "port": 23,
    "timeout": 60,
}

SW1 = {
    "device_type": "cisco_ios_telnet",
    "host": "192.168.1.101",
    "username": "admin",
    "password": "Cisco123",
    "secret": "ClaseCCNA",
    "port": 23,
    "timeout": 60,
}

SW2 = {
    "device_type": "cisco_ios_telnet",
    "host": "10.0.12.2",
    "username": "admin",
    "password": "Cisco123",
    "secret": "ClaseCCNA",
    "port": 23,
    "timeout": 60,
}

SYSLOG_SERVER_IP = "192.168.1.1"  # IP de Windows en el laboratorio presencial
