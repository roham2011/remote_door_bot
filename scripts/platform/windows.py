from __future__ import annotations

import json
import shutil
import subprocess
import time
from pathlib import Path
from typing import TextIO


class WindowsAdapter:
    name = "Windows"

    def find_arduino_port(self) -> str | None:
        pio = shutil.which("pio") or shutil.which("platformio")
        if not pio:
            return None
        result = subprocess.run([pio, "device", "list", "--json-output"], capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            return None
        try:
            devices = json.loads(result.stdout)
        except json.JSONDecodeError:
            return None
        for device in devices:
            hwid = str(device.get("hwid", "")).lower()
            description = str(device.get("description", "")).lower()
            if "2341:003d" in hwid or "2341:003e" in hwid or "arduino due" in description:
                return device.get("port") or None
        return None

    def start_arduino_monitor(self, port: str, log_path: Path, processes: list, log_handles: list[TextIO]) -> None:
        pio = shutil.which("pio") or shutil.which("platformio")
        if not pio:
            return
        log_path.parent.mkdir(parents=True, exist_ok=True)
        handle = log_path.open("w", encoding="utf-8", buffering=1)
        log_handles.append(handle)
        separator = "=" * 110
        handle.write(f"{separator}\n{'ARDUINO SERIAL MONITOR':^110}\n{separator}\n")
        process = subprocess.Popen(
            [pio, "device", "monitor", "--port", port, "--baud", "115200", "--quiet", "--raw"],
            stdin=subprocess.DEVNULL, stdout=handle, stderr=subprocess.STDOUT,
        )
        processes.append(process)
        time.sleep(1)
        try:
            import serial
            with serial.Serial(port, 1200) as connection:
                connection.dtr = False
                time.sleep(0.1)
                connection.dtr = True
                time.sleep(0.1)
            time.sleep(2)
        except Exception as exc:
            handle.write(f"\n[launcher] Automatic reset failed: {exc}\n")

    def start_tunnel(self, port: int, log_handle: TextIO) -> subprocess.Popen:
        ssh = shutil.which("ssh")
        if not ssh:
            raise FileNotFoundError("OpenSSH client (ssh.exe) was not found. Enable/install OpenSSH Client in Windows.")
        return subprocess.Popen(
            [ssh, "-o", "ServerAliveInterval=60", "-o", "StrictHostKeyChecking=accept-new",
             "-R", f"80:localhost:{port}", "nokey@localhost.run"],
            stdin=subprocess.DEVNULL, stdout=log_handle, stderr=subprocess.STDOUT,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
