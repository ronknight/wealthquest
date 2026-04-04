#!/bin/bash
# stop.sh - Stop the Fin FastAPI application

if [ -f fin.pid ]; then
    PID=$(cat fin.pid)
    echo "Stopping Fin (PID: $PID)..."
    kill $PID
    
    # Wait for process to exit
    while ps -p $PID > /dev/null; do 
        sleep 1
    done
    
    rm fin.pid
    echo "Fin stopped successfully."
else
    echo "fin.pid not found. Attempting to stop via process name..."
    pkill -f "uvicorn src.main:app"
    echo "Stop command issued."
fi
