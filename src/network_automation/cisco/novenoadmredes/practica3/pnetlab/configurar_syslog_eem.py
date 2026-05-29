# network_automation/cisco/novenoadmredes/practica3/pnetlab/configurar_syslog_eem.py
# Orquestador: configura los 3 dispositivos en secuencia.
# Para configurar un solo dispositivo corre el script individual en configDisp/.

from netmiko import ConnectHandler

from network_automation.cisco.novenoadmredes.practica3.pnetlab.devices import R1, SW1, SW2
from network_automation.cisco.novenoadmredes.practica3.pnetlab.configDisp import r1, sw1, sw2


def main():
    tareas = [
        ("R1",  R1,  r1.configurar),
        ("SW1", SW1, sw1.configurar),
        ("SW2", SW2, sw2.configurar),
    ]

    exitosos = []
    fallidos = []

    for nombre, params, configurar in tareas:
        print(f"\n{'═' * 50}")
        print(f"  Configurando {nombre} ({params['host']})")
        print('═' * 50)
        try:
            with ConnectHandler(**params) as conn:
                conn.enable()
                configurar(conn)
            exitosos.append(nombre)
            print(f"\n[OK] {nombre} configurado correctamente.")
        except Exception as e:
            fallidos.append(nombre)
            print(f"\n[ERROR] {nombre}: {e}")

    print(f"\n{'═' * 50}")
    print("  RESUMEN DE CONFIGURACION")
    print('═' * 50)
    print(f"  Correctos : {', '.join(exitosos) if exitosos else 'ninguno'}")
    print(f"  Fallidos  : {', '.join(fallidos) if fallidos else 'ninguno'}")


if __name__ == "__main__":
    main()
