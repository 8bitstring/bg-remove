#!/bin/bash
cd "$(dirname "$0")"

echo "==================================================="
echo " Starting Local Background Remover Web UI (macOS)  "
echo "==================================================="

if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Running setup first..."
    bash setup_mac.sh
fi

source .venv/bin/activate
python3 app.py
