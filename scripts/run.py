from __future__ import annotations

import importlib.util
import logging
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import TextIO

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.logging import RichHandler
    RICH_AVAILABLE = True
except ImportError:
    Console = Panel = Text = RichHandler = None  # type: ignore[assignment,misc]
    RICH_AVAILABLE = False

ROOT_DIR = Path(__file__).resolve().parents[1]
APP_DIR = ROOT_DIR / "Python_program"
RUNTIME_DIR = ROOT_DIR / "runtime"
ARDUINO_LOG = RUNTIME_DIR / "arduino" / "monitor.log"
APP_LOG = RUNTIME_DIR / "app.log"
TUNNEL_LOG = RUNTIME_DIR / "tunnel.log"
TUNNEL_URL_FILE = RUNTIME_DIR / "tunnel_url.txt"
URL_PATTERN = re.compile(r"https://[a-zA-Z0-9-]+\.lhr\.life")


class Launcher:
    def __init__(self) -> None:
        self.logger = self._make_logger()
        self.adapter = self._load_platform_adapter()
        self.processes: list[subprocess.Popen] = []
        self.log_handles: list[TextIO] = []
        self.stopping = False

    @staticmethod
    def _make_logger() -> logging.Logger:
        RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
        logger = logging.getLogger("remote_door_launcher")
        logger.setLevel(logging.INFO)
        logger.handlers.clear()
        logger.propagate = False

        if RICH_AVAILABLE and RichHandler is not None:
            handler = RichHandler(
                console=Console(stderr=False),
                show_time=True,
                show_level=True,
                show_path=False,
                markup=False,
                rich_tracebacks=True,
                log_time_format="[%H:%M:%S]",
            )
            handler.setFormatter(logging.Formatter("%(message)s"))
        else:
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(
                logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", "%Y-%m-%d %H:%M:%S")
            )
        logger.addHandler(handler)
        return logger

    @staticmethod
    def show_banner() -> None:
        if not RICH_AVAILABLE or Console is None or Panel is None or Text is None:
            print("\n=== REMOTE DOOR BOT ===\nCross-platform launcher\n")
            return

        console = Console()
        title = Text("REMOTE DOOR BOT", style="bold bright_cyan", justify="center")
        subtitle = Text("Cross-platform runtime launcher", style="dim", justify="center")
        content = Text.assemble(title, "\n", subtitle)
        console.print(Panel(content, border_style="bright_blue", padding=(1, 4), expand=False))

    @staticmethod
    def _load_platform_adapter():
        # Load by file path because the requested folder name `platform` clashes
        # with Python's standard-library module named `platform`.
        scripts_dir = Path(__file__).resolve().parent
        filename = "windows.py" if os.name == "nt" else "linux.py"
        module_name = "remote_door_platform_adapter"
        module_path = scripts_dir / "platform" / filename
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Could not load platform adapter: {module_path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        adapter_class = module.WindowsAdapter if os.name == "nt" else module.LinuxAdapter
        return adapter_class()

    def _open_log(self, path: Path, *, reset: bool = False) -> TextIO:
        path.parent.mkdir(parents=True, exist_ok=True)
        handle = path.open("w" if reset else "a", encoding="utf-8", buffering=1)
        self.log_handles.append(handle)
        return handle

    def prepare_runtime(self) -> None:
        RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
        (RUNTIME_DIR / "arduino").mkdir(parents=True, exist_ok=True)
        with APP_LOG.open("w", encoding="utf-8") as log:
            line = "=" * 110
            log.write(f"{line}\n{'IN THE NAME OF GOD':^110}\n{line}\n")
        TUNNEL_LOG.write_text("", encoding="utf-8")
        TUNNEL_URL_FILE.unlink(missing_ok=True)

    def python_executable(self) -> str:
        candidates = [ROOT_DIR / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python"),
                      APP_DIR / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")]
        for candidate in candidates:
            if candidate.is_file():
                return str(candidate)
        return sys.executable

    def configure(self) -> None:
        settings = APP_DIR / "settings.json"
        python = self.python_executable()
        if settings.exists():
            self.logger.info("Configuration file found: %s", settings)
            return
        self.logger.info("No settings.json found; starting first-time configuration.")
        result = subprocess.run(
            [python, "-c", "from configs.config_loader import load_configs; load_configs()"],
            cwd=APP_DIR,
        )
        if result.returncode != 0 or not settings.exists():
            raise RuntimeError("Configuration setup failed. Check configs.config_loader and its required inputs.")
        self.logger.info("Configuration completed.")

    def read_port(self) -> int:
        result = subprocess.run(
            [self.python_executable(), "-c", "from configs.general_config import APP_PORT; print(APP_PORT)"],
            cwd=APP_DIR, capture_output=True, text=True, check=False,
        )
        if result.returncode != 0:
            raise RuntimeError("Could not import APP_PORT from configs.general_config. Check the config module path.")
        try:
            port = int(result.stdout.strip().splitlines()[-1])
        except (ValueError, IndexError) as exc:
            raise RuntimeError(f"Invalid application port output: {result.stdout!r}") from exc
        if not 1 <= port <= 65535:
            raise RuntimeError(f"Port is outside the valid TCP range: {port}")
        return port

    def start_arduino_monitor(self) -> None:
        try:
            port = self.adapter.find_arduino_port()
        except (FileNotFoundError, subprocess.SubprocessError) as exc:
            self.logger.warning("Could not check Arduino ports; monitor disabled: %s", exc)
            return
        if not port:
            self.logger.warning("Arduino Due not detected; serial monitor disabled.")
            return
        self.adapter.start_arduino_monitor(port, ARDUINO_LOG, self.processes, self.log_handles)
        self.logger.info("Arduino serial monitor started on %s", port)

    def start_tunnel(self, port: int) -> subprocess.Popen:
        handle = self._open_log(TUNNEL_LOG, reset=True)
        process = self.adapter.start_tunnel(port, handle)
        self.processes.append(process)
        self.logger.info("SSH tunnel process started; waiting for public URL...")
        deadline = time.monotonic() + 90
        while time.monotonic() < deadline:
            if process.poll() is not None:
                raise RuntimeError(f"SSH tunnel exited with code {process.returncode}. See {TUNNEL_LOG}")
            try:
                contents = TUNNEL_LOG.read_text(encoding="utf-8", errors="replace")
            except OSError:
                contents = ""
            match = URL_PATTERN.search(contents)
            if match:
                url = match.group(0)
                TUNNEL_URL_FILE.write_text(url + "\n", encoding="utf-8")
                self.logger.info("Tunnel URL: %s", url)
                return process
            time.sleep(1)
        raise TimeoutError(f"No localhost.run URL received within 90 seconds. See {TUNNEL_LOG}")

    def start_app(self) -> subprocess.Popen:
        # The app's own logger writes runtime/app.log. Redirect console output there as well.
        handle = self._open_log(APP_LOG)
        process = subprocess.Popen(
            [self.python_executable(), "-u", "app.py"], cwd=APP_DIR,
            stdin=subprocess.DEVNULL, stdout=handle, stderr=subprocess.STDOUT,
        )
        self.processes.append(process)
        return process

    def stop(self) -> None:
        if self.stopping:
            return
        self.stopping = True
        self.logger.info("Stopping child processes...")
        for process in reversed(self.processes):
            if process.poll() is None:
                process.terminate()
        for process in reversed(self.processes):
            if process.poll() is None:
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=3)
        try:
            with ARDUINO_LOG.open("a", encoding="utf-8") as log:
                log.write("\n" + "=" * 110 + "\n")
                log.write(f"{'ARDUINO MONITOR FINISHED':^110}\n")
                log.write(f"{'Finished: ' + time.strftime('%Y-%m-%d %H:%M:%S'):^110}\n")
                log.write("=" * 110 + "\n")
        except OSError:
            pass
        for handle in self.log_handles:
            try:
                handle.close()
            except OSError:
                pass

    def run(self) -> int:
        self.prepare_runtime()
        self.show_banner()
        if not RICH_AVAILABLE:
            self.logger.warning("Rich is not installed; using plain-text console output.")
        self.logger.info("Starting Remote Door Bot")
        self.logger.info("Platform: %s", self.adapter.name)
        self.configure()
        port = self.read_port()
        self.logger.info("Flask port: %s", port)
        self.start_arduino_monitor()
        self.start_tunnel(port)
        app_process = self.start_app()
        self.logger.info("Bale Bot is running. Press Ctrl+C to stop.")
        try:
            while app_process.poll() is None:
                time.sleep(0.5)
            return int(app_process.returncode or 0)
        finally:
            self.stop()


def _open_in_new_terminal() -> bool:
    """Relaunch this script in a dedicated native terminal window once."""
    if "--terminal-child" in sys.argv or os.environ.get("REMOTE_DOOR_TERMINAL_CHILD") == "1":
        return False

    script = str(Path(__file__).resolve())
    env = os.environ.copy()
    env["REMOTE_DOOR_TERMINAL_CHILD"] = "1"
    command = [sys.executable, script, "--terminal-child"]

    if os.name == "nt":
        # CREATE_NEW_CONSOLE opens a separate classic Windows console window.
        command_text = subprocess.list2cmdline(command)
        subprocess.Popen(
            [os.environ.get("COMSPEC", "cmd.exe"), "/k", command_text],
            cwd=str(ROOT_DIR), env=env,
            creationflags=getattr(subprocess, "CREATE_NEW_CONSOLE", 0),
        )
        return True

    terminals = [
        ("x-terminal-emulator", ["-e", *command]),
        ("gnome-terminal", ["--", *command]),
        ("konsole", ["-e", *command]),
        ("xfce4-terminal", ["--disable-server", "--command", subprocess.list2cmdline(command)]),
        ("xterm", ["-e", *command]),
    ]
    for executable, arguments in terminals:
        terminal = shutil.which(executable)
        if terminal:
            subprocess.Popen([terminal, *arguments], cwd=str(ROOT_DIR), env=env)
            return True

    # If no graphical terminal is installed, keep running in the current terminal.
    print("No supported terminal emulator found; running in the current terminal.", file=sys.stderr)
    return False


def main() -> int:
    try:
        if _open_in_new_terminal():
            return 0
        launcher = Launcher()
        return launcher.run()
    except KeyboardInterrupt:
        print("Interrupted before launcher initialization.", file=sys.stderr)
        return 130
    except Exception as exc:
        logger = logging.getLogger("remote_door_launcher")
        if logger.handlers:
            logger.exception("Launcher failed: %s", exc)
        else:
            print(f"Launcher failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
