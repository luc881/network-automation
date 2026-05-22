# cisco/practica4/limpiar_dispositivos.py
"""
Limpieza — regresa dispositivos a estado de fábrica.
Borra startup-config, vlan.dat (switches) y reinicia.

IMPORTANTE: usar al FINAL de la práctica para dejar los equipos limpios.

Uso:
    poetry run python -m network_automation.cisco.practica4.limpiar_dispositivos
"""

import time
from netmiko import ConnectHandler
from network_automation.config.devices import SW_LAB

# ── Dispositivos a limpiar ────────────────────────────────────────────────────
# Descomenta cada dispositivo cuando lo conectes al cable de consola.

DISPOSITIVOS = [
    # ── SW1 ──────────────────────────────────────────────────────────────────
    {
        "conn":   SW_LAB,
        "nombre": "SW1",
        "tipo":   "switch",
    },

    # ── SW2 (descomentar en laboratorio) ─────────────────────────────────────
    # {
    #     "conn":   SW_LAB,
    #     "nombre": "SW2",
    #     "tipo":   "switch",
    # },

    # ── R1 (descomentar en laboratorio) ──────────────────────────────────────
    # {
    #     "conn":   SW_LAB,
    #     "nombre": "R1",
    #     "tipo":   "router",
    # },
]


def limpiar_dispositivo(conn_params: dict, nombre: str, tipo: str) -> None:
    params = {**conn_params, "global_delay_factor": 2, "fast_cli": False}

    print(f"\n[*] Limpiando {nombre}...")

    with ConnectHandler(**params) as net_connect:
        net_connect.write_channel("\r\n")
        time.sleep(1)
        net_connect.enable()

        # Borrar startup-config
        net_connect.write_channel("erase startup-config\r\n")
        time.sleep(1)
        net_connect.write_channel("\r\n")
        time.sleep(2)

        # Borrar vlan.dat solo en switches
        if tipo == "switch":
            net_connect.write_channel("delete flash:vlan.dat\r\n")
            time.sleep(1)
            net_connect.write_channel("\r\n")  # confirmar filename
            time.sleep(1)
            net_connect.write_channel("\r\n")  # confirmar delete
            time.sleep(2)

        # Reiniciar sin guardar
        net_connect.write_channel("reload\r\n")
        time.sleep(1)
        net_connect.write_channel("\r\n")  # no guardar cambios
        time.sleep(1)

        print(f"[+] {nombre} limpiado — reiniciando ✓")
        print(f"    Espera ~2 min a que vuelva como 'Switch>'")


def main():
    print("=" * 50)
    print("  LIMPIEZA — Regresar dispositivos a fábrica")
    print("=" * 50)
    print("\n⚠️  Esto borrará TODA la configuración.")

    confirmacion = input("¿Continuar? (si/no): ").strip().lower()
    if confirmacion != "si":
        print("Cancelado.")
        return

    for dispositivo in DISPOSITIVOS:
        try:
            limpiar_dispositivo(
                conn_params=dispositivo["conn"],
                nombre=dispositivo["nombre"],
                tipo=dispositivo["tipo"],
            )

            if len(DISPOSITIVOS) > 1:
                input("\n  → Conecta el siguiente dispositivo y presiona Enter...")

        except Exception as e:
            print(f"[!] Error en {dispositivo['nombre']}: {e}")

    print("\n[✓] Limpieza completada.")
    print("    Los dispositivos reiniciarán en ~2 minutos.")


if __name__ == "__main__":
    main()
