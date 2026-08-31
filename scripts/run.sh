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