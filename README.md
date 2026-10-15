# Remote Door Bot

Remote Door Bot is a modular software and embedded project for requesting door operations through a Bale bot and coordinating those requests with an Arduino Due controller.

> **Status:** Development project. Do not expose this system to the public internet or use it to control a real access point until authentication, transport security, authorization, failure handling, and hardware behavior have been reviewed and tested.

## Architecture

```text
Authorized Bale user
        |
        v
Bale Bot API <---- HTTPS webhook ---- Flask application
                                      |
                                      v
                                Command handlers
                                      |
                                      v
                              Arduino network client
                                      |
                                      v
                              Arduino Due controller
                               |              |
                            Ethernet        CC1101
                                              |
                                      Compatible RF device
```

The Flask application handles webhook updates and application logic. The Arduino Due is responsible for the embedded/network side of the system and interfaces with the RF hardware. The launcher starts the Python application and, when available, the Arduino serial monitor and SSH tunnel.

## Repository layout

```text
remote_door_bot/
├── Python_program/
│   ├── app.py
│   ├── configs/
│   │   ├── config_editor.py
│   │   ├── config_loader.py
│   │   ├── general_config.py
│   │   └── path.py
│   ├── core/
│   ├── database/
│   ├── handlers/
│   ├── network/
│   ├── protocols/
│   ├── tests/
│   ├── utils/
├── firmware/
│   └── due/
├── runtime/
│   ├── app.log
│   ├── tunnel.log
│   ├── tunnel_url.txt
│   └── arduino/monitor.log
├── scripts/
│   ├── run.py
│   ├── run.sh
│   └── platform/
│       ├── linux.py
│       └── windows.py
├── requirements.txt
└── README.md
```

`Python_program` is the Python application's working directory and import root. The launcher deliberately runs application subprocesses with this directory as their current working directory. Configuration and runtime paths should be resolved from the source file or from this working directory—not from assumptions about where the shell was opened.

## Requirements

- Python 3.11 or a compatible version supported by the pinned dependencies.
- Dependencies from `requirements.txt`, including Rich for the colored launcher console.
- OpenSSH client if you want the optional `localhost.run` tunnel.
- PlatformIO CLI and `pyserial` if you want the Arduino serial monitor and automatic reset.
- Arduino Due and the appropriate network/RF hardware for hardware testing.

## Setup

Run commands from the repository root.

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe scripts\run.py
```

If the virtual environment already exists, skip the creation command. The launcher checks the repository-level `.venv`, then `Python_program/.venv`, and finally uses the interpreter that started the launcher.

### Linux

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/run.py
```

The launcher can also be invoked with `python scripts/run.py` when the intended environment is already active.

## First run and configuration

If `Python_program/settings.json` does not exist, the launcher calls `configs.config_loader.load_configs()`. The configuration editor asks for:

- Flask port
- Number of doors
- Flask host
- Debug mode
- Root administrator's Bale user ID
- Bale bot token

The configuration file is written to `Python_program/settings.json`. This path is resolved absolutely by `configs/path.py`, so it does not depend on the shell's current directory.

`settings.json` contains a bot token and must remain private. Do not commit it, paste it into issues, or include it in public archives. If a token has been exposed, revoke it and create a replacement through the bot platform.

## Launcher behavior

`python scripts/run.py` is the cross-platform entry point. It:

1. Initializes launcher logging.
2. Ensures the runtime directories exist and prepares the launcher logs.
3. Runs first-time configuration when required.
4. Reads the Flask port from `configs.general_config`.
5. Attempts to locate an Arduino Due through PlatformIO and starts a serial monitor when found.
6. Attempts to reset the Due through the serial port when the platform adapter supports it.
7. Starts an SSH reverse tunnel through `localhost.run` and waits for a URL.
8. Starts the Flask application.
9. Stops child processes it started when the launcher exits or receives Ctrl+C.

Runtime output is written under `runtime/`, including `app.log`, `tunnel.log`, `tunnel_url.txt`, and `arduino/monitor.log`. The tunnel is optional in concept but the current launcher treats tunnel startup failure as a startup failure; verify this behavior before relying on local-only operation.

## Important paths

- Settings: `Python_program/settings.json`
- Main application: `Python_program/app.py`
- General application configuration: `Python_program/configs/general_config.py`
- Settings path definition: `Python_program/configs/path.py`
- Launcher: `scripts/run.py`
- Arduino firmware: `firmware/due/`
- Runtime logs: `runtime/`

## Testing and troubleshooting

- **Configuration import errors:** confirm imports use the `Python_program` directory as the import root. Application modules should use imports such as `from configs.path import SETTINGS_PATH` or package-relative imports such as `from .path import SETTINGS_PATH`; do not import through a machine-specific repository name like `remote_door_bot.Python_program`.
- **Configuration is not created:** run the launcher from the repository root and inspect the full traceback. Confirm that the virtual environment has the project dependencies installed.
- **Arduino monitor is disabled:** check the USB cable, device permissions, PlatformIO installation, and whether the board appears in `pio device list`.
- **Tunnel does not start:** confirm that `ssh` is available and inspect `runtime/tunnel.log`.
- **Port is busy:** choose an unused TCP port during first-time configuration.

## Security and deployment notes

The reverse tunnel may make the Flask endpoint reachable from the public internet. A tunnel is not an authentication mechanism. Before production use, validate every command against an authenticated user and an explicit authorization policy, protect credentials, avoid debug mode, use secure transport, and test recovery from network and hardware failures. Do not rely on a hidden URL as access control.

## Development

Python tests are located in `Python_program/tests/`. Firmware sources and PlatformIO configuration are under `firmware/due/`. Test hardware-specific behavior on the actual board; successful Python tests do not prove that a physical door or RF protocol will behave safely.

## Launcher console

The launcher uses Rich for a styled startup banner, colored log levels, and readable tracebacks on Windows and Linux. Install dependencies with `pip install -r requirements.txt`. If Rich is missing, it falls back to plain text. Runtime log files remain plain text.
