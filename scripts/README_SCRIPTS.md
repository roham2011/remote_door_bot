# Cross-platform launcher

`scripts/run.py` is the repository-level entry point for Windows and Linux. The OS-specific implementations are in `scripts/platform/windows.py` and `scripts/platform/linux.py`.

## Run it

Run from the repository root:

**Windows PowerShell**

```powershell
.\.venv\Scripts\python.exe scripts\run.py
```

**Linux**

```bash
.venv/bin/python scripts/run.py
```

If `.venv` is already activated, `python scripts/run.py` is sufficient. The launcher selects the repository `.venv` first, then `Python_program/.venv`, and falls back to the interpreter used to start the launcher.

## Directory contract

```text
repository/
├── scripts/
│   ├── run.py
│   └── platform/
│       ├── __init__.py
│       ├── linux.py
│       └── windows.py
├── Python_program/
│   ├── app.py
│   ├── settings.json       # generated on first run; contains secrets
│   ├── configs/
└── firmware/
    └── due/
```

The launcher sets `cwd=Python_program` when it runs application configuration checks and starts `app.py`. Consequently, `configs`, `protocols`, `database`, and other application directories are top-level imports within that working directory. Avoid imports through a repository-specific package name such as `remote_door_bot.Python_program`.

`configs/path.py` resolves `settings.json` from its own file location. This avoids a path changing unexpectedly when the program is started from another shell directory.

## Logs

- `runtime/app.log`: application output and startup banner.
- `runtime/tunnel.log`: SSH tunnel output.
- `runtime/tunnel_url.txt`: detected public URL.
- `runtime/arduino/monitor.log`: Arduino serial monitor output.

The launcher resets the application and tunnel logs when it starts. On Windows, it opens a separate classic Command Prompt window. On Linux, it uses the first available terminal emulator from `x-terminal-emulator`, GNOME Terminal, Konsole, Xfce Terminal, or xterm. If none is available, it runs in the current terminal. The Arduino monitor log is also opened in overwrite mode when a monitor starts.

## Optional integrations

- **Arduino monitoring:** install PlatformIO CLI and `pyserial` in the interpreter environment used by the launcher, connect the Due, and verify that `pio device list --json-output` detects it.
- **Public tunnel:** install the OpenSSH client and ensure `ssh` can connect to `localhost.run`. Tunnel startup currently has a timeout and a failed tunnel can stop startup.
- **Serial reset:** the adapters attempt a 1200-baud DTR reset. Board/driver behavior varies by operating system, so verify it on the actual hardware.

## Configuration flow

When `Python_program/settings.json` is missing, `run.py` launches:

```python
from configs.config_loader import load_configs
load_configs()
```

The loader calls `edit_config()` on `FileNotFoundError`; the editor collects the required values and writes the settings file. The function takes no arguments. If this flow fails, inspect the first traceback above the launcher's generic `Configuration setup failed` message.

## Safety notes

The SSH reverse tunnel can expose the Flask application outside the local machine. Do not treat the tunnel URL as authentication. Before deployment, enforce authorization for each command, keep the bot token private, disable debug mode, and verify that invalid or unauthorized requests cannot operate hardware.

## Console appearance

The launcher uses [Rich](https://github.com/Textualize/rich) for a framed startup banner, colored log levels, readable timestamps, and formatted tracebacks. Rich is installed with the project's `requirements.txt`. If it is unavailable, the launcher falls back to plain-text logging instead of refusing to start. ANSI styling is used only for terminal output; the application, tunnel, and Arduino log files remain ordinary text.
