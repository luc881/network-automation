# cisco/practica4/configurar_dispositivos.py
"""
Fase 1 — Configuración inicial via consola serial.
Conecta secuencialmente a cada dispositivo y aplica config base.

IMPORTANTE: conectar de a un dispositivo a la vez al cable serial.
            Descomentar cada dispositivo cuando esté físicamente conectado.

Uso:
    poetry run python -m network_automation.cisco.practica4.configurar_dispositivos
"""

import time
from netmiko import ConnectHandler
from network_automation.config.devices import SW_LAB

# ── Dispositivos a configurar ─────────────────────────────────────────────────
# Descomenta cada dispositivo cuando lo conectes al cable de consola.

DISPOSITIVOS = [
    # ── SW1 / SW-CASA (prueba en casa) ───────────────────────────────────────
    {
        "conn":     SW_LAB,
        "hostname": "SW1",
        "ip":       "192.168.1.11",
        "mascara":  "255.255.255.0",
        "gateway":  "192.168.1.1",
        "tipo":     "switch",
    },

    ── SW2 (descomentar en laboratorio) ─────────────────────────────────────
    {
        "conn":     SW_LAB,
        "hostname": "SW2",
        "ip":       "192.168.1.12",
        "mascara":  "255.255.255.0",
        "gateway":  "192.168.1.1",
        "tipo":     "switch",
    },

    ── R1 (descomentar en laboratorio) ──────────────────────────────────────
    {
        "conn":     SW_LAB,
        "hostname": "R1",
        "ip":       "192.168.1.1",
        "mascara":  "255.255.255.0",
        "gateway":  None,            # el router no necesita default-gateway
        "tipo":     "router",
    },
]


def configurar_switch(conn_params: dict, hostname: str, ip: str,
                      mascara: str, gateway: str) -> None:
    commands = [
        f"hostname {hostname}",
        "enable secret ClaseCCNA",
        "username admin privilege 15 secret Cisco123",
        "interface vlan 1",
        f" ip address {ip} {mascara}",
        " no shutdown",
        "exit",
        f"ip default-gateway {gateway}",
        "line vty 0 4",
        " login local",
        " transport input telnet",
        "exit",
    ]

    params = {**conn_params, "global_delay_factor": 2, "fast_cli": False}

    print(f"\n[*] Conectando a {hostname} por consola serial...")

    with ConnectHandler(**params) as net_connect:
        net_connect.write_channel("\r\n")
        time.sleep(1)
        net_connect.enable()
        output = net_connect.send_config_set(commands)
        print(output)
        save = net_connect.send_command(
            "write memory",
            expect_string=r"\[OK\]|Building configuration",
            read_timeout=30,
        )
        print(save)
        print(f"[+] {hostname} configurado y guardado ✓")


def configurar_router(conn_params: dict, hostname: str, ip: str,
                      mascara: str) -> None:
    commands = [
        f"hostname {hostname}",
        "enable secret ClaseCCNA",
        "username admin privilege 15 secret Cisco123",
        "interface FastEthernet0/0",
        f" ip address {ip} {mascara}",
        " no shutdown",
        "exit",
        "line vty 0 4",
        " login local",
        " transport input telnet",
        "exit",
    ]

    params = {**conn_params, "global_delay_factor": 2, "fast_cli": False}

    print(f"\n[*] Conectando a {hostname} por consola serial...")

    with ConnectHandler(**params) as net_connect:
        net_connect.write_channel("\r\n")
        time.sleep(1)
        net_connect.enable()
        output = net_connect.send_config_set(commands)
        print(output)
        save = net_connect.send_command(
            "write memory",
            expect_string=r"\[OK\]|Building configuration",
            read_timeout=30,
        )
        print(save)
        print(f"[+] {hostname} configurado y guardado ✓")


def main():
    print("=" * 50)
    print("  FASE 1 — Configuración inicial por consola")
    print("=" * 50)

    for dispositivo in DISPOSITIVOS:
        try:
            if dispositivo["tipo"] == "switch":
                configurar_switch(
                    conn_params=dispositivo["conn"],
                    hostname=dispositivo["hostname"],
                    ip=dispositivo["ip"],
                    mascara=dispositivo["mascara"],
                    gateway=dispositivo["gateway"],
                )
            else:
                configurar_router(
                    conn_params=dispositivo["conn"],
                    hostname=dispositivo["hostname"],
                    ip=dispositivo["ip"],
                    mascara=dispositivo["mascara"],
                )

            if len(DISPOSITIVOS) > 1:
                input("\n  → Conecta el siguiente dispositivo y presiona Enter...")

        except Exception as e:
            print(f"[!] Error en {dispositivo['hostname']}: {e}")

    print("\n[✓] Fase 1 completada.")
    print("    Conecta todos los dispositivos a la red")
    print("    y ejecuta backup_configs.py")


if __name__ == "__main__":
    main()
