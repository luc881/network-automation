# cisco/port_security/status_port_security.py
# Shows port security status, CAM table count, and violation log messages.

from netmiko import ConnectHandler
from network_automation.config.devices import SW_LAB

INTERFACE = "Gi0/1"

# Syslog keywords to filter — captures violation + err-disable events
LOG_FILTER = "PORT_SECURITY|psecure|ERR_DISABLE"


def parse_violation_status(ps_output: str) -> tuple[bool, str]:
    """
    Returns (is_err_disabled, violation_count) from port-security output.
    """
    err_disabled = "err-disabled" in ps_output.lower()
    violation_count = "0"
    for line in ps_output.splitlines():
        if "Security Violation Count" in line:
            violation_count = line.split(":")[-1].strip()
    return err_disabled, violation_count


def main():
    print("Connecting to switch...")
    try:
        with ConnectHandler(**SW_LAB) as conn:
            conn.enable()

            ps_status = conn.send_command(
                f"show port-security interface {INTERFACE}"
            )
            cam_count = conn.send_command(
                "show mac address-table count"
            )
            port_status = conn.send_command(
                "show interfaces status"
            )

            violation_logs = conn.send_command(
                f"show logging | include {INTERFACE}|{LOG_FILTER}"
            )

            # ── Detect err-disabled state ──────────────────────────────
            is_err_disabled, violation_count = parse_violation_status(ps_status)

            if is_err_disabled:
                print(f"\n⚠️  ALERTA: {INTERFACE} está en estado ERR-DISABLED")
                print(f"   Violaciones registradas: {violation_count}")

            # ── Secciones de salida ────────────────────────────────────
            print("\n─── PORT SECURITY STATUS ───────────────────────")
            print(ps_status)

            print("\n─── CAM TABLE COUNT ────────────────────────────")
            print(cam_count)

            print("\n─── INTERFACE STATUS ───────────────────────────")
            print(port_status)

            print("\n─── VIOLATION LOG MESSAGES ─────────────────────")
            if violation_logs.strip():
                print(violation_logs)
            else:
                print("  ✅  Sin mensajes de violación en el log.")

    except Exception as e:
        print(f"❌  Error: {e}")


if __name__ == "__main__":
    main()