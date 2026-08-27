#!/bin/bash

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

cd "$PROJECT_DIR" || exit 1

mkdir -p runtime

source .venv/bin/activate

echo "================================================"
echo  Starting Bale Bot
echo "================================================"

# over write app.log 
echo "==================================================================================================================================" > runtime/app.log
echo "                                                        IN THE NAME OF GOD                                                        " >> runtime/app.log
echo "==================================================================================================================================" >> runtime/app.log
PORT=$(python -c "from core.config import APP_PORT; print(APP_PORT)")

echo "================================================"
echo "Creating SSH Tunne"
echo "================================================"

rm -f runtime/tunnel.log
rm -f runtime/tunnel_url.txt

ssh \
    -o ServerAliveInterval=60 \
    -o StrictHostKeyChecking=no \
    -R 80:localhost:$PORT \
    nokey@localhost.run \
    > runtime/tunnel.log 2>&1 &

TUNNEL_PID=$!

echo "Waiting for tunnel..."

while true
do
    if grep -q "https://.*\.lhr\.life" runtime/tunnel.log
    then
        URL=$(grep -o "https://[a-zA-Z0-9]*\.lhr\.life" runtime/tunnel.log | head -n 1)

        echo "$URL" > runtime/tunnel_url.txt

        echo "Tunnel URL:"
        echo "$URL"

        break
    fi

    if ! kill -0 "$TUNNEL_PID" 2>/dev/null
    then
        echo "SSH tunnel stopped unexpectedly."
        cat runtime/tunnel.log
        exit 1
    fi

    sleep 1
done

echo "================================================"
echo "Bale Bot is running"
echo "================================================"

python -u app.py >> runtime/app.log 2>&1