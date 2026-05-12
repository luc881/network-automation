# cisco/port_security/enable_port_security.py
# Enables port security on a given interface.

from netmiko import ConnectHandler
from network_automation.config.devices import SW_LAB

INTERFACE = "Gi0/1"
MAX_MACS  = 5

COMMANDS = [
    f"interface {INTERFACE}",
    "switchport mode access",
    "switchport port-security",
    f"switchport port-security maximum {MAX_MACS}",
    "switchport port-security violation shutdown",
    "switchport port-security mac-address sticky",
    "end",
    "write memory",
]


def main():
    print(f"Connecting to switch...")
    try:
        with ConnectHandler(**SW_LAB) as conn:
            conn.enable()
            print(f"Enabling Port Security on {INTERFACE}...")
            output = conn.send_config_set(COMMANDS)
            print(output)
            print(f"✅  Port Security enabled on {INTERFACE}")
    except Exception as e:
        print(f"❌  Error: {e}")


if __name__ == "__main__":
    main()
