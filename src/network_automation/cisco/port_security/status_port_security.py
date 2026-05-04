# cisco/port_security/status_port_security.py
# Shows port security status and CAM table count.

from netmiko import ConnectHandler
from network_automation.config.devices import SW_LAB

INTERFACE = "Gi1/0/1"


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

            print("\n─── PORT SECURITY STATUS ───────────────────────")
            print(ps_status)
            print("\n─── CAM TABLE COUNT ────────────────────────────")
            print(cam_count)
            print("\n─── INTERFACE STATUS ───────────────────────────")
            print(port_status)

    except Exception as e:
        print(f"❌  Error: {e}")


if __name__ == "__main__":
    main()
