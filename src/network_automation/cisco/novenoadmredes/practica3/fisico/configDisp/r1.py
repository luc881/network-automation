# network_automation/cisco/novenoadmredes/practica3/fisico/configDisp/r1.py
# Router Cisco 2900 series, IOS 15.x — interfaces GigabitEthernet, EEM soportado

from netmiko import ConnectHandler

from network_automation.cisco.novenoadmredes.practica3.fisico.devices import R1, SYSLOG_SERVER_IP


def _seccion(titulo):
    print(f"\n{'─' * 50}")
    print(f"  {titulo}")
    print('─' * 50)


def configurar(conn):
    # Interfaces GigabitEthernet (2900 series)
    conn.send_config_set([
        "interface GigabitEthernet0/0",
        " ip address 192.168.1.100 255.255.255.0",
        " no shutdown",
        "interface GigabitEthernet0/1",
        " ip address 10.0.12.1 255.255.255.0",
        " no shutdown",
    ])

    # Syslog centralizado
    conn.send_config_set([
        "service timestamps log datetime msec",
        "logging on",
        f"logging host {SYSLOG_SERVER_IP}",
        "logging trap informational",
        "logging facility local7",
        "logging source-interface GigabitEthernet0/0",
    ])

    # EEM Applet: detecta interfaz GigabitEthernet que cae
    conn.send_config_set([
        "event manager applet INTERFAZ_CAIDA",
        ' event syslog pattern ".*UPDOWN.*GigabitEthernet.*down.*"',
        ' action 1.0 syslog priority critical msg "ALERTA: Interfaz GigabitEthernet caida detectada"',
        "exit",
    ])

    # EEM Applet: detecta login exitoso
    conn.send_config_set([
        "event manager applet LOGIN_DETECTADO",
        ' event syslog pattern ".*LOGIN_SUCCESS.*"',
        ' action 1.0 syslog priority warning msg "AVISO: Login exitoso detectado en el dispositivo"',
        "exit",
    ])

    # EEM Applet: detecta que la configuracion fue guardada
    conn.send_config_set([
        "event manager applet CONFIG_GUARDADA",
        ' event syslog pattern ".*SYS-5-CONFIG_I.*"',
        ' action 1.0 syslog priority warning msg "AVISO: Configuracion guardada en el dispositivo"',
        "exit",
    ])

    # EEM Applet: heartbeat cada 5 minutos
    conn.send_config_set([
        "event manager applet HEARTBEAT",
        " event timer watchdog time 300",
        ' action 1.0 syslog priority informational msg "INFO: Sistema activo - heartbeat 300s"',
        "exit",
    ])

    # Verificacion
    _seccion("R1 — show ip interface brief")
    print(conn.send_command("show ip interface brief"))

    _seccion("R1 — show logging")
    print(conn.send_command("show logging"))

    _seccion("R1 — show event manager policy registered")
    print(conn.send_command("show event manager policy registered"))


def main():
    print("Configurando R1 fisico (192.168.1.100)...")
    try:
        with ConnectHandler(**R1) as conn:
            conn.enable()
            configurar(conn)
        print("\n[OK] R1 configurado correctamente.")
    except Exception as e:
        print(f"\n[ERROR] R1: {e}")


if __name__ == "__main__":
    main()
