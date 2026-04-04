#!/bin/bash
# start.sh - Start the Fin FastAPI application in the background

echo "Starting WealthQuest - 8-Bit Financial Tracker..."

# Check if already running
if [ -f fin.pid ]; then
    PID=$(cat fin.pid)
    if ps -p $PID > /dev/null; then
        echo "Fin is already running with PID $PID"
        exit 1
    else
        rm fin.pid
    fi
fi

# Run uvicorn in the background
# We use python3 -m uvicorn to ensure the local src package is in the path
nohup python3 -m uvicorn src.main:app --host 0.0.0.0 --port 8000 > fin.log 2>&1 &

# Save PID
echo $! > fin.pid

echo "Fin is now running in the background."
echo "PID: $(cat fin.pid)"
echo "Local access: http://localhost:8000"
echo "Logs: tail -f fin.log"
