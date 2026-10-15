# Cross-platform launcher

`scripts/run.py` is the repository-level entry point for Windows and Linux. It starts the Bale bot using Long Polling instead of an SSH reverse tunnel and webhook. OS-specific implementations remain in `scripts/platform/windows.py` and `scripts/platform/linux.py`.

## Run it

Run from the repository root.

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
│   ├── long_polling.py
│   ├── app.py
│   ├── settings.json
│   ├── configs/
│   ├── database/
│   ├── core/
│   └── protocols/
├── runtime/
└── firmware/
    └── due/
```

`settings.json` is generated during initial configuration and contains sensitive values, including the bot token. Do not commit it to version control.

The launcher uses `cwd=Python_program` when running application configuration checks and starting `long_polling.py`. Consequently, `configs`, `protocols`, `database`, and other application directories are top-level imports within that working directory. Avoid imports through a repository-specific package name such as `remote_door_bot.Python_program`.

`configs/path.py` resolves application paths relative to its own file location, preventing configuration paths from unexpectedly changing when the program is launched from another working directory.

## Logs

- `runtime/app.log`: application and Long Polling output.
- `runtime/arduino/monitor.log`: Arduino serial monitor output.

The launcher resets `runtime/app.log` when it starts. The Arduino monitor log is opened in overwrite mode when a monitor starts.

On Windows, the launcher opens a separate classic Command Prompt window. On Linux, it uses the first available terminal emulator from `x-terminal-emulator`, GNOME Terminal, Konsole, Xfce Terminal, or xterm. If none is available, it runs in the current terminal.

## Optional integrations

**Arduino monitoring:** Install PlatformIO CLI and `pyserial` in the interpreter environment used by the launcher. Connect the Arduino Due and verify that `pio device list --json-output` detects it. The serial monitor is optional; the bot can run without a detected board.

**Long Polling:** The launcher runs `Python_program/long_polling.py`. The script disables the bot's webhook before polling for updates from the Bale API. Keep the process running to receive messages. Do not run another instance of the same bot using webhook or Long Polling simultaneously, because competing update consumers can cause conflicts.

**Serial reset:** The platform adapters may attempt a 1200-baud DTR reset. Board and driver behavior varies by operating system, so verify it on the actual hardware.

## Configuration flow

When `Python_program/settings.json` is missing, `run.py` launches the configuration loader:

```python
from configs.config_loader import load_configs
load_configs()
```

The loader handles missing configuration by calling `edit_config()`, which collects the required values and writes the settings file. The function takes no arguments.

If configuration fails, inspect the first traceback above the launcher's generic configuration error message.

## Safety notes

Keep the Bale bot token private and out of version control. Validate user authorization for every door-control command, disable debug mode in production, and ensure that unauthorized or malformed requests cannot operate the hardware.

Long Polling removes the need for a public webhook URL or SSH reverse tunnel, but it does not replace authentication or authorization. The bot must still validate incoming users and commands before controlling physical doors.

## Console appearance

The launcher uses [Rich](https://github.com/Textualize/rich) for a framed startup banner, colored log levels, readable timestamps, and formatted tracebacks. Rich is installed through the project's `requirements.txt`. If Rich is unavailable, the launcher falls back to plain-text logging rather than refusing to start.

ANSI styling is used only for terminal output. Application and Arduino log files remain ordinary text.