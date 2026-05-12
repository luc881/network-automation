# cisco/practica2_3/configurar_switches.py
# Práctica 2: Configuración de switches vía Telnet + Port Security
# Práctica 3: Respaldo de configuración vía TFTP
#
# Uso:
#   poetry run python -m network_automation.cisco.practica2_3.configurar_switches
#
# Prerequisito — agregar tftpy al proyecto:
#   poetry add tftpy

import os
import time
import socket
import threading

import tftpy
from netmiko import ConnectHandler

from network_automation.config.devices import SW1, SW2, TFTP_SERVER_IP


# ── Parámetros de la práctica ─────────────────────────────────────────────────

# En casa: deja solo SW1. En el lab descomenta SW2.
SWITCHES = [
    {"nombre": "SW1", **SW1},
    # {"nombre": "SW2", **SW2},
]

INTERFAZ_PS  = "Fa0/1"    # Catalyst 2950 usa FastEthernet. Si tienes 2960 usa Fa0/1 también.
MAX_MACS     = 2
VIOLACION    = "shutdown"  # shutdown | restrict | protect

TFTP_PORT        = 69                    # estándar TFTP (requiere sudo en Mac)
CARPETA_BACKUPS  = "./backups"


# ── Helpers ───────────────────────────────────────────────────────────────────

def _netmiko_params(sw: dict) -> dict:
    """Retorna solo los keys que netmiko entiende (quita 'nombre')."""
    return {k: v for k, v in sw.items() if k != "nombre"}


# ── FASE 0 — Verificación de conectividad ────────────────────────────────────

def verificar_conectividad() -> bool:
    """
    Comprueba puerto Telnet (23) en cada switch antes de empezar.
    Más seguro fallar aquí que a mitad de la configuración.
    """
    print("\n[PRE] Verificando conectividad...")
    todos_ok = True

    for sw in SWITCHES:
        ip   = sw["host"]
        port = sw["port"]
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            ok = sock.connect_ex((ip, port)) == 0
            sock.close()
            estado = f"✅  {sw['nombre']} ({ip}) — puerto {port} abierto"
            if not ok:
                estado = f"❌  {sw['nombre']} ({ip}) — no responde en puerto {port}"
                print("     → Verifica IP y que Telnet esté habilitado en VTY")
                todos_ok = False
        except Exception as e:
            estado = f"❌  {sw['nombre']} ({ip}) — {e}"
            todos_ok = False
        print(f"     {estado}")

    return todos_ok


# ── FASE 1 — Configuración base ───────────────────────────────────────────────

def configurar_switch(sw: dict) -> None:
    """
    Aplica configuración básica al switch:
      - hostname
      - VLAN 1 / IP de administración
      - default gateway
      - banner MOTD
      - guarda en NVRAM

    netmiko maneja automáticamente:
      - detección de prompts (>, #, Password:)
      - entrada a modo enable con secret
      - 'configure terminal' y 'end' al usar send_config_set()
    """
    nombre = sw["nombre"]
    print(f"\n  [1] Configurando {nombre}...")

    comandos = [
        f"hostname {nombre}",
        "interface vlan 1",
        f"ip address {sw['host']} 255.255.255.0",
        "no shutdown",
        "exit",
        "ip default-gateway 192.168.1.1",
        "banner motd # Acceso restringido — solo personal autorizado #",
    ]

    with ConnectHandler(**_netmiko_params(sw)) as conn:
        conn.enable()
        conn.send_config_set(comandos)
        conn.save_config()   # write memory

    print(f"  ✅  {nombre} — configuración base OK + guardado en NVRAM")


# ── FASE 2 — Port Security ────────────────────────────────────────────────────

def configurar_port_security(sw: dict) -> None:
    """
    Configura Port Security en INTERFAZ_PS.

    Conceptos:
      maximum  → cuántas MACs distintas tolera el puerto
      sticky   → aprende MACs dinámicamente y las escribe en running-config
                 como si fueran estáticas — persisten tras reboot (write memory)
      violation shutdown → puerto pasa a err-disabled ante MAC no autorizada
                           (es el modo más seguro para laboratorio)

    Requisito: el puerto DEBE estar en modo access (no trunk).
    Port Security no aplica en puertos trunk ni en port-channels.
    """
    nombre = sw["nombre"]
    print(f"\n  [2] Port Security en {nombre} ({INTERFAZ_PS})...")

    comandos = [
        f"interface {INTERFAZ_PS}",
        "switchport mode access",
        "switchport port-security",
        f"switchport port-security maximum {MAX_MACS}",
        f"switchport port-security violation {VIOLACION}",
        "switchport port-security mac-address sticky",
        "exit",
    ]

    with ConnectHandler(**_netmiko_params(sw)) as conn:
        conn.enable()
        conn.send_config_set(comandos)
        conn.save_config()

        # Verificación inline
        estado = conn.send_command(f"show port-security interface {INTERFAZ_PS}")

    # Mostrar solo las líneas relevantes (mismo estilo que status_port_security.py)
    print(f"  ✅  {nombre} — Port Security configurado")
    for linea in estado.splitlines():
        if any(k in linea for k in ["Security Enabled", "Port Status", "Maximum", "Violation Mode", "Sticky"]):
            print(f"       {linea.strip()}")


# ── FASE 3 — Servidor TFTP + Backup ──────────────────────────────────────────

def iniciar_servidor_tftp() -> tftpy.TftpServer:
    """
    Levanta un servidor TFTP en esta Mac con tftpy.

    ¿Por qué TFTP y no HTTP/FTP?
      IOS tiene soporte nativo para TFTP desde los 90s.
      Es el protocolo estándar para mover configs entre
      dispositivos de red en una LAN confiable.
      Usa UDP:69 — sin handshake, sin autenticación.

    ¿Por qué no Railway / Vercel?
      Esas plataformas son HTTP (TCP 80/443) en internet.
      TFTP usa UDP en tu LAN local.
      Son capas de transporte y entornos completamente distintos.
    """
    os.makedirs(CARPETA_BACKUPS, exist_ok=True)

    print(f"\n  [3] Levantando servidor TFTP en {TFTP_SERVER_IP}:{TFTP_PORT}...")
    print(f"       Carpeta: {os.path.abspath(CARPETA_BACKUPS)}")

    servidor = tftpy.TftpServer(CARPETA_BACKUPS)
    hilo = threading.Thread(
        target=servidor.listen,
        kwargs={"listenip": "0.0.0.0", "listenport": TFTP_PORT},
        daemon=True,
    )
    hilo.start()
    time.sleep(1.5)
    print("  ✅  Servidor TFTP activo")
    return servidor


def respaldar_config(sw: dict) -> None:
    """
    Ordena al switch copiar su running-config al servidor TFTP.

    Comando ejecutado en el switch:
      copy running-config tftp
      → Address of remote host: <IP de tu Mac>
      → Destination filename: SW1_backup.txt

    send_command_timing() maneja prompts interactivos donde el switch
    hace preguntas en lugar de mostrar el prompt # directamente.
    """
    nombre  = sw["nombre"]
    archivo = f"{nombre}_backup.txt"
    print(f"\n  [3] Respaldando {nombre} → tftp://{TFTP_SERVER_IP}/{archivo}...")

    with ConnectHandler(**_netmiko_params(sw)) as conn:
        conn.enable()
        conn.send_command_timing("copy running-config tftp", delay_factor=2)
        conn.send_command_timing(TFTP_SERVER_IP, delay_factor=2)
        respuesta = conn.send_command_timing(archivo, delay_factor=3)

    ruta = os.path.join(CARPETA_BACKUPS, archivo)
    if os.path.exists(ruta):
        size = os.path.getsize(ruta)
        print(f"  ✅  {nombre} — backup recibido: {archivo} ({size} bytes)")
    else:
        print(f"  ⚠️   {nombre} — archivo no llegó al servidor")
        print(f"       Respuesta del switch: {respuesta[-200:].strip()}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 58)
    print("  Práctica 2 + 3 — Diseño y Administración de Redes")
    print("=" * 58)

    if not verificar_conectividad():
        print("\n❌  Corrige la conectividad antes de continuar.")
        return

    iniciar_servidor_tftp()

    resultados = []

    for sw in SWITCHES:
        nombre = sw["nombre"]
        print(f"\n{'─' * 50}")
        print(f"  {nombre} ({sw['host']})")
        print(f"{'─' * 50}")
        ok = True
        try:
            configurar_switch(sw)
            configurar_port_security(sw)
            respaldar_config(sw)
        except Exception as e:
            print(f"\n  ❌  Error en {nombre}: {e}")
            ok = False
        resultados.append((nombre, sw["host"], ok))

    print("\n" + "=" * 58)
    print("  RESUMEN")
    print("=" * 58)
    for nombre, ip, ok in resultados:
        print(f"  {'✅' if ok else '❌'}  {nombre} ({ip})")

    print(f"\n  Backups en: {os.path.abspath(CARPETA_BACKUPS)}/")
    if os.path.exists(CARPETA_BACKUPS):
        for f in sorted(os.listdir(CARPETA_BACKUPS)):
            size = os.path.getsize(os.path.join(CARPETA_BACKUPS, f))
            print(f"    📄 {f}  ({size} bytes)")
    print("=" * 58)


if __name__ == "__main__":
    main()