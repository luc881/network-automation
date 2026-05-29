# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python-based Cisco network device automation for two university courses:
- **Diseño y Administración de Redes** (`novenoadmredes/`)
- **Redes de Área Amplia** (`wan/`)

Uses **Netmiko** for Telnet/Serial connectivity and **tftpy** for TFTP-based config backups. Targets both a PNetLab virtual environment and a physical Cisco Catalyst 2950.

## Development Environment

- **OS:** Windows 11 — use PowerShell syntax only, never bash/Linux commands
- **Python:** 3.11.9 managed via Poetry (src layout)
- **Package management:** `poetry add <package>` only — never `pip install`
- **Run scripts:** `poetry run python -m network_automation.<module>`

## Commands

```powershell
# Install dependencies
poetry install

# Run a module (pattern for all scripts)
poetry run python -m network_automation.cisco.novenoadmredes.practica3.configurar_syslog_eem

# View project structure
tree src /F
```

There are no tests beyond the placeholder `tests/__init__.py` and no linting configuration.

## Module Structure

```
src/network_automation/
├── config/
│   └── devices.py                    # Single source of truth for all device connections
└── cisco/
    ├── novenoadmredes/                # 9no — Diseño y Administración de Redes
    │   └── practica3/                 # Syslog + EEM Applets
    ├── wan/                           # 8vo — Redes de Área Amplia
    └── legacy/                        # Old scripts (port_security, practica2_3, practica4)
```

Each file starts with a comment declaring its module path:
```python
# network_automation/cisco/novenoadmredes/practica3/configurar_syslog_eem.py
```

## Lab Environments

### PNetLab (virtual — current focus)

VMware Workstation Pro with IOL images. Key IPs:

| Device  | Interface | IP                 |
|---------|-----------|--------------------|
| Windows | VMnet8    | 192.168.241.1/24   |
| R1      | e0/0      | 192.168.241.100/24 |
| SW1     | VLAN 1    | 192.168.241.101/24 |
| R1      | e0/1      | 10.0.12.1/24       |
| SW2     | VLAN 1    | 10.0.12.2/24       |

SW2 requires a persistent static route on Windows to be reachable:
```powershell
route add 10.0.12.0 mask 255.255.255.0 192.168.241.100 -p
```

IOL interfaces are named `e0/0`, `e0/1`, etc. — **not** `Fa0/x` or `Gi0/x`.

### Physical Lab (Cisco Catalyst 2950)

- Interfaces: `FastEthernet` (`Fa0/x`) — no GigabitEthernet
- IOS 12.1: use `show mac-address-table` (with hyphen, not `show mac address-table`)
- Serial access via cable OIKWAN → COM3, 9600 baud

## Device Definitions (`src/network_automation/config/devices.py`)

All scripts import from here — change IPs and credentials only in this file.

```python
R1  = {"device_type": "cisco_ios_telnet", "host": "192.168.241.100", "username": "admin", "password": "Cisco123", "secret": "ClaseCCNA", "port": 23, "timeout": 15}
SW1 = {"device_type": "cisco_ios_telnet", "host": "192.168.241.101", "username": "admin", "password": "Cisco123", "secret": "ClaseCCNA", "port": 23, "timeout": 15}
SW2 = {"device_type": "cisco_ios_telnet", "host": "10.0.12.2",       "username": "admin", "password": "Cisco123", "secret": "ClaseCCNA", "port": 23, "timeout": 15}

SW_LAB = {"device_type": "cisco_ios_serial", "serial_settings": {"port": "COM3", "baudrate": 9600}, "secret": "ClaseCCNA"}

SYSLOG_SERVER_IP = "192.168.241.1"
```

## Key Netmiko Patterns

- Use `send_command_timing()` (not `send_command()`) when IOS prompts for additional input mid-command (e.g., TFTP IP, filename). Pass `strip_prompt=False, strip_command=False` to capture full output.
- Use `send_config_set()` for configuration mode commands.
- Include explicit `time.sleep()` delays after commands that trigger IOS prompts or require device processing time.
- All connections: `ConnectHandler(**device_dict)` imported from `config.devices`.

## Conventions

- Commits follow Conventional Commits: `feat:`, `fix:`, `docs:`, `refactor:`
- Do not use `telnetlib` — Netmiko abstracts all Telnet/Serial transport.
