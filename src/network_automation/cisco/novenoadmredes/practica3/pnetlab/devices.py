# network_automation/cisco/novenoadmredes/practica3/devices.py

R1 = {
    "device_type": "cisco_ios_telnet",
    "host": "192.168.241.100",
    "username": "admin",
    "password": "Cisco123",
    "secret": "ClaseCCNA",
    "port": 23,
    "timeout": 15,
}

SW1 = {
    "device_type": "cisco_ios_telnet",
    "host": "192.168.241.101",
    "username": "admin",
    "password": "Cisco123",
    "secret": "ClaseCCNA",
    "port": 23,
    "timeout": 60,  # ← sube de 15 a 60
    "session_timeout": 60,
}

SW2 = {
    "device_type": "cisco_ios_telnet",
    "host": "10.0.12.2",
    "username": "admin",
    "password": "Cisco123",
    "secret": "ClaseCCNA",
    "port": 23,
    "timeout": 15,
}

SYSLOG_SERVER_IP = "192.168.241.1"
