# cisco/port_security/status_port_security.py
# Shows port security status and CAM table count.

from netmiko import ConnectHandler
from network_automation.config.devices import SW_LAB


def main():
    print("Connecting to switch...")
    try:
        with ConnectHandler(**SW_LAB) as conn:
            conn.enable()

            cam_count = conn.send_command(
                "show mac address-table count"
            )

            print("\n─── CAM TABLE COUNT ────────────────────────────")
            print(cam_count)

    except Exception as e:
        print(f"❌  Error: {e}")


if __name__ == "__main__":
    main()
