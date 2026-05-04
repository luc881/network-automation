# cisco/port_security/recover_port.py
# Recovers a port from err-disabled state caused by port security violation.

from netmiko import ConnectHandler
from network_automation.config.devices import SW_LAB

INTERFACE = "Gi1/0/1"

COMMANDS = [
    f"interface {INTERFACE}",
    "shutdown",
    "no shutdown",
    "end",
]


def main():
    print("Connecting to switch...")
    try:
        with ConnectHandler(**SW_LAB) as conn:
            conn.enable()
            print(f"Recovering {INTERFACE} from err-disabled...")
            output = conn.send_config_set(COMMANDS)
            print(output)
            print(f"✅  Port {INTERFACE} recovered and active")
    except Exception as e:
        print(f"❌  Error: {e}")


if __name__ == "__main__":
    main()
