#!/bin/bash
set -e

cd "$(dirname "$0")"

echo "=========================================="
echo " Setting up Background Remover on macOS"
echo "=========================================="

# Check for python3
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH."
    echo "Please install Python 3 (e.g., via brew install python@3.10 or from python.org)."
    exit 1
fi

echo "[1/3] Creating virtual environment (.venv)..."
python3 -m venv .venv

echo "[2/3] Installing dependencies..."
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "[3/3] Pre-downloading default u2net model..."
rembg d u2net

echo ""
echo "=========================================="
echo " Setup complete! To start the Web UI run:"
echo " ./start_web_ui.command"
echo "=========================================="
