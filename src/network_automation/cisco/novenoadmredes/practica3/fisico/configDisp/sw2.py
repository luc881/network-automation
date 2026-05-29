# network_automation/cisco/novenoadmredes/practica3/fisico/configDisp/sw2.py
# Catalyst 2950, IOS 12.1 — sin EEM, interfaces FastEthernet

from netmiko import ConnectHandler

from network_automation.cisco.novenoadmredes.practica3.fisico.devices import SW2, SYSLOG_SERVER_IP


def _seccion(titulo):
    print(f"\n{'─' * 50}")
    print(f"  {titulo}")
    print('─' * 50)


def configurar(conn):
    # VLAN 1 SVI y gateway
    conn.send_config_set([
        "interface vlan 1",
        " ip address 10.0.12.2 255.255.255.0",
        " no shutdown",
        "ip default-gateway 10.0.12.1",
    ])

    # Syslog basico (IOS 12.1 no soporta source-interface en switches)
    conn.send_config_set([
        "service timestamps log datetime msec",
        "logging on",
        f"logging host {SYSLOG_SERVER_IP}",
        "logging trap informational",
    ])

    # Guardar configuracion y verificar
    conn.send_command("write memory")
    _seccion("SW2 — show interface vlan 1")
    print(conn.send_command("show interface vlan 1"))

    _seccion("SW2 — show logging")
    print(conn.send_command("show logging"))

    _seccion("SW2 — show mac-address-table")
    print(conn.send_command("show mac-address-table"))


def main():
    print("Configurando SW2 fisico (10.0.12.2)...")
    try:
        with ConnectHandler(**SW2) as conn:
            conn.enable()
            configurar(conn)
        print("\n[OK] SW2 configurado correctamente.")
    except Exception as e:
        print(f"\n[ERROR] SW2: {e}")


if __name__ == "__main__":
    main()
