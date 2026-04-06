#!/bin/bash
# stop.sh - Stop the Fin FastAPI application by PID and port

# 1. Kill by PID file if exists
if [ -f fin.pid ]; then
    PID=$(cat fin.pid)
    echo "Stopping Fin from PID file (PID: $PID)..."
    kill $PID 2>/dev/null
    rm fin.pid
fi

# 2. Aggressive kill by port 8000 (uvicorn)
echo "Ensuring all processes on port 8000 are terminated..."
PIDS_PORT=$(ps -ef | grep "uvicorn" | grep "8000" | grep -v "grep" | awk '{print $2}')

if [ -n "$PIDS_PORT" ]; then
    for P in $PIDS_PORT; do
        echo "Killing zombie process: $P"
        kill -9 $P 2>/dev/null
    done
fi

# 3. Final cleanup via pkill as safety net
pkill -9 -f "uvicorn src.main:app" 2>/dev/null

echo "Fin cleanup complete. Port 8000 should be free."
