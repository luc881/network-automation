# cisco/mac_flooding/verify_cam_table.py
# Monitors the CAM table in real time during a MAC flooding attack.
# Run this while macof is running in Kali to watch the table fill up.

import time
from netmiko import ConnectHandler
from network_automation.config.devices import SW_LAB

INTERVAL_SECONDS = 3   # how often to poll the switch
MAX_CAPACITY     = 16360  # 2960X CAM table size


def parse_dynamic_count(output: str) -> int:
    for line in output.splitlines():
        if "Dynamic Address Count" in line:
            return int(line.split(":")[1].strip())
    return 0


def main():
    print("Connecting to switch — monitoring CAM table (Ctrl+C to stop)...
")
    try:
        with ConnectHandler(**SW_LAB) as conn:
            conn.enable()
            while True:
                output = conn.send_command("show mac address-table count")
                count  = parse_dynamic_count(output)
                pct    = (count / MAX_CAPACITY) * 100
                bar    = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))

                status = "⚠️  TABLE FULL — switch in hub mode!" if count >= MAX_CAPACITY else ""
                print(f"CAM entries: {count:>6} / {MAX_CAPACITY}  [{bar}] {pct:5.1f}%  {status}")

                if count >= MAX_CAPACITY:
                    print("
🔴 Attack successful — CAM table saturated.")
                    break

                time.sleep(INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("
Monitoring stopped.")
    except Exception as e:
        print(f"❌  Error: {e}")


if __name__ == "__main__":
    main()
