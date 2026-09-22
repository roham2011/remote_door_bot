#!/bin/bash

# ============================================================
# Bale Bot launcher
# ============================================================

set -u

# ------------------------------------------------------------
# Project directory
# ------------------------------------------------------------

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

cd "$PROJECT_DIR" || exit 1


# ------------------------------------------------------------
# Runtime directory
# ------------------------------------------------------------

mkdir -p runtime


# ------------------------------------------------------------
# Python virtual environment
# ------------------------------------------------------------

source .venv/bin/activate


# ------------------------------------------------------------
# Startup message
# ------------------------------------------------------------

echo "================================================"
echo "Starting Bale Bot"
echo "================================================"


# ------------------------------------------------------------
# Application log
# ------------------------------------------------------------

echo "==================================================================================================================================" > runtime/app.log
echo "                                                        IN THE NAME OF GOD                                                        " >> runtime/app.log
echo "==================================================================================================================================" >> runtime/app.log


# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

echo "Checking configuration..."

if [ ! -f "settings.json" ]; then
    echo "No configuration file found."
    echo "Starting first-time configuration..."
    echo ""

    python -c "
from config.config_loader import load_configs
load_configs('settings.json')
"

    if [ $? -ne 0 ]; then
        echo "Configuration failed."
        exit 1
    fi

    echo ""
    echo "Configuration completed."
else
    echo "Configuration file found."
fi


# ------------------------------------------------------------
# Read application port
# ------------------------------------------------------------

PORT=$(python -c "
from config.config import APP_PORT
print(APP_PORT)
")

if [ $? -ne 0 ] || [ -z "$PORT" ]; then
    echo "Failed to read application port."
    exit 1
fi

echo "Flask port: $PORT"


# ------------------------------------------------------------
# Arduino serial monitor
# ------------------------------------------------------------

ARDUINO_MONITOR_PID=""
ARDUINO_LOG="runtime/arduino/monitor.log"
ARDUINO_SEPARATOR="=================================================================================================================================="

start_arduino_monitor() {
    if ! command -v pio >/dev/null 2>&1; then
        echo "PlatformIO CLI not found. Arduino monitor disabled."
        return 0
    fi

    local arduino_port

    arduino_port=$(pio device list --json-output 2>/dev/null | python -c '
import json
import sys

try:
    devices = json.load(sys.stdin)
except (json.JSONDecodeError, TypeError):
    sys.exit(0)

for device in devices:
    hwid = str(device.get("hwid", "")).lower()
    description = str(device.get("description", "")).lower()
    port = device.get("port", "")

    if ("2341:003d" in hwid or "2341:003e" in hwid
            or "arduino due" in description):
        if port:
            print(port)
            break
'
)

    if [ -z "$arduino_port" ]; then
        echo "Arduino Due not connected. Arduino monitor disabled."
        return 0
    fi

    mkdir -p runtime/arduino

    printf '%s\n' "$ARDUINO_SEPARATOR" > "$ARDUINO_LOG"
    printf '%*s%s%*s\n' \
        54 "" \
        "ARDUINO SERIAL MONITOR" \
        54 "" \
        >> "$ARDUINO_LOG"
    printf '%s\n' "$ARDUINO_SEPARATOR" >> "$ARDUINO_LOG"

    echo "Arduino Due detected on: $arduino_port"
    echo "Starting PlatformIO serial monitor..."

    TERM=dumb \
    NO_COLOR=1 \
    CLICOLOR=0 \
    script -qefc \
        "pio device monitor \
            --port '$arduino_port' \
            --baud 115200 \
            --quiet \
            --raw" \
        /dev/null \
        </dev/null \
        >> "$ARDUINO_LOG" 2>&1 &

    ARDUINO_MONITOR_PID=$!

    sleep 1

    echo "Resetting Arduino Due..."

    python - "$arduino_port" <<'PY'
import sys
import time
import serial

port = sys.argv[1]

with serial.Serial(port, 1200) as ser:
    ser.dtr = False
    time.sleep(0.1)
    ser.dtr = True
    time.sleep(0.1)

time.sleep(2)
PY

    echo "Arduino Due reset completed."
}

finish_arduino_monitor() {
    if [ -n "$ARDUINO_MONITOR_PID" ] &&
       kill -0 "$ARDUINO_MONITOR_PID" 2>/dev/null
    then
        kill "$ARDUINO_MONITOR_PID" 2>/dev/null || true
    fi

    {
        printf '\n'
        printf '%s\n' "$ARDUINO_SEPARATOR"
        printf '%*s\n' 78 "ARDUINO MONITOR FINISHED"
        printf '%*s\n' 84 "Finished : $(date '+%Y-%m-%d %H:%M:%S')"
        printf '%s\n' "$ARDUINO_SEPARATOR"
    } >> "$ARDUINO_LOG"
}

start_arduino_monitor

trap 'finish_arduino_monitor; exit 130' INT TERM

# ------------------------------------------------------------
# Remove old tunnel data
# ------------------------------------------------------------

rm -f runtime/tunnel.log
rm -f runtime/tunnel_url.txt


# ------------------------------------------------------------
# Start SSH tunnel
# ------------------------------------------------------------

echo "================================================"
echo "Creating SSH Tunnel"
echo "================================================"

# Kill previous localhost.run tunnels
pkill -f "ssh.*localhost.run" 2>/dev/null || true

ssh \
    -o ServerAliveInterval=60 \
    -o StrictHostKeyChecking=no \
    -R 80:localhost:"$PORT" \
    nokey@localhost.run \
    > runtime/tunnel.log 2>&1 &

TUNNEL_PID=$!


# ------------------------------------------------------------
# Wait for tunnel URL
# ------------------------------------------------------------

echo "Waiting for tunnel..."

while true
do

    if grep -qE "https://[a-zA-Z0-9]+\.lhr\.life" runtime/tunnel.log
    then

        URL=$(grep -oE "https://[a-zA-Z0-9]+\.lhr\.life" \
            runtime/tunnel.log | head -n 1)

        echo "$URL" > runtime/tunnel_url.txt

        echo ""
        echo "Tunnel URL:"
        echo "$URL"

        break
    fi


    # Check whether SSH process is still alive

    if ! kill -0 "$TUNNEL_PID" 2>/dev/null
    then
        echo ""
        echo "SSH tunnel stopped unexpectedly."
        echo ""
        cat runtime/tunnel.log

        exit 1
    fi

    sleep 1

done


# ------------------------------------------------------------
# Start Flask application
# ------------------------------------------------------------

echo "================================================"
echo "Bale Bot is running"
echo "================================================"

python -u app.py >> runtime/app.log 2>&1