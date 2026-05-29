# cisco/practica4/backup_configs.py
"""
Fase 2 — Backup de running-config via TFTP.
Maneja los prompts interactivos de Cisco IOS.

Uso:
    poetry run python -m network_automation.cisco.practica4.backup_configs
"""

import threading
import time
from pathlib import Path
from netmiko import ConnectHandler
import tftpy

from network_automation.config.devices import SW1, SW2, R1, TFTP_SERVER_IP

DISPOSITIVOS = {
    "SW1": SW1,
    # "SW2": SW2,
    # "R1":  R1,
}

BACKUP_DIR = Path("backups")
TFTP_PORT  = 69


def iniciar_servidor_tftp(directorio: Path, puerto: int) -> None:
    server = tftpy.TftpServer(str(directorio))
    thread = threading.Thread(
        target=server.listen,
        kwargs={"listenip": "0.0.0.0", "listenport": puerto},
        daemon=True,
    )
    thread.start()
    print(f"[+] Servidor TFTP escuchando en {TFTP_SERVER_IP}:{puerto}")


def backup_via_tftp(nombre: str, conn_params: dict,
                    tftp_ip: str, tftp_port: int) -> None:
    filename = f"{nombre}_backup.cfg"

    print(f"\n[*] Conectando a {nombre} ({conn_params['host']}) via Telnet...")

    with ConnectHandler(**conn_params) as net_connect:
        net_connect.enable()

        # Paso 1 — iniciar comando
        net_connect.write_channel("copy running-config tftp\r\n")
        time.sleep(2)

        # Paso 2 — responder IP del servidor TFTP
        output = net_connect.read_channel()
        print(f"    {output.strip()}")
        net_connect.write_channel(f"{tftp_ip}\r\n")
        time.sleep(2)

        # Paso 3 — responder nombre del archivo
        output = net_connect.read_channel()
        print(f"    {output.strip()}")
        net_connect.write_channel(f"{filename}\r\n")
        time.sleep(5)  # esperar transferencia

        # Leer resultado final
        output = net_connect.read_channel()
        print(f"    {output.strip()}")

        if "OK" in output or "bytes copied" in output:
            print(f"[+] {nombre} → backup guardado como {filename} ✓")
        else:
            print(f"[!] {nombre} → verifica el archivo en backups/")


def main():
    print("=" * 50)
    print("  FASE 2 — Backup running-config via TFTP")
    print("=" * 50)

    BACKUP_DIR.mkdir(exist_ok=True)

    iniciar_servidor_tftp(BACKUP_DIR, TFTP_PORT)
    time.sleep(1)

    for nombre, conn_params in DISPOSITIVOS.items():
        try:
            backup_via_tftp(
                nombre=nombre,
                conn_params=conn_params,
                tftp_ip=TFTP_SERVER_IP,
                tftp_port=TFTP_PORT,
            )
        except Exception as e:
            print(f"[!] Error en {nombre}: {e}")

    time.sleep(2)
    print("\n[✓] Backups completados en carpeta backups/")
    print(f"    Archivos: {list(BACKUP_DIR.glob('*.cfg'))}")


if __name__ == "__main__":
    main()
