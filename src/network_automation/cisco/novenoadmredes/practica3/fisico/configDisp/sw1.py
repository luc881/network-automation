# network_automation/cisco/novenoadmredes/practica3/fisico/configDisp/sw1.py
# Catalyst 2950, IOS 12.1 — sin EEM, interfaces FastEthernet

from netmiko import ConnectHandler

from network_automation.cisco.novenoadmredes.practica3.fisico.devices import SW1, SYSLOG_SERVER_IP


def _seccion(titulo):
    print(f"\n{'─' * 50}")
    print(f"  {titulo}")
    print('─' * 50)


def configurar(conn):
    # VLAN 1 SVI y gateway
    conn.send_config_set([
        "interface vlan 1",
        " ip address 192.168.1.101 255.255.255.0",
        " no shutdown",
        "ip default-gateway 192.168.1.100",
    ])

    # Syslog basico (IOS 12.1 no soporta source-interface en switches)
    conn.send_config_set([
        "service timestamps log datetime msec",
        "logging on",
        f"logging host {SYSLOG_SERVER_IP}",
        "logging trap informational",
    ])

    # Verificacion — IOS 12.1 usa guion en mac-address-table
    _seccion("SW1 — show interface vlan 1")
    print(conn.send_command("show interface vlan 1"))

    _seccion("SW1 — show logging")
    print(conn.send_command("show logging"))

    _seccion("SW1 — show mac-address-table")
    print(conn.send_command("show mac-address-table"))


def main():
    print("Configurando SW1 fisico (192.168.1.101)...")
    try:
        with ConnectHandler(**SW1) as conn:
            conn.enable()
            configurar(conn)
        print("\n[OK] SW1 configurado correctamente.")
    except Exception as e:
        print(f"\n[ERROR] SW1: {e}")


if __name__ == "__main__":
    main()
