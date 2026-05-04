# cisco/port_security/disable_port_security.py
# Disables port security and clears the CAM table.

from netmiko import ConnectHandler
from network_automation.config.devices import SW_LAB

INTERFACE = "Gi1/0/1"

COMMANDS = [
    f"interface {INTERFACE}",
    "no switchport port-security mac-address sticky",
    "no switchport port-security",
    "shutdown",
    "no shutdown",
    "end",
    "clear mac address-table dynamic",
    "write memory",
]


def main():
    print("Connecting to switch...")
    try:
        with ConnectHandler(**SW_LAB) as conn:
            conn.enable()
            print(f"Disabling Port Security on {INTERFACE}...")
            output = conn.send_config_set(COMMANDS)
            print(output)
            print("✅  Port Security disabled and CAM table cleared")
    except Exception as e:
        print(f"❌  Error: {e}")


if __name__ == "__main__":
    main()
