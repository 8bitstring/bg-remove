#!/usr/bin/env bash

# Automatically move to the directory where this script is located
cd "$(dirname "$0")" || exit 1

# Colors for friendly output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

clear
echo -e "${BLUE}======================================================${NC}"
echo -e "${BLUE}       🖼️  Local Image Background Remover (macOS)     ${NC}"
echo -e "${BLUE}======================================================${NC}"
echo ""

# 1. Detect Python 3
PYTHON_BIN=""
if command -v python3 &> /dev/null; then
    PYTHON_BIN="python3"
elif command -v python &> /dev/null && python --version 2>&1 | grep -q "Python 3"; then
    PYTHON_BIN="python"
fi

# If Python 3 is missing, try to install via Homebrew or Xcode CLT
if [ -z "$PYTHON_BIN" ]; then
    echo -e "${YELLOW}[!] Python 3 was not detected on your Mac.${NC}"
    echo -e "Attempting automatic installation..."
    
    if command -v brew &> /dev/null; then
        echo -e "${BLUE}Installing Python via Homebrew...${NC}"
        brew install python
        PYTHON_BIN="python3"
    else
        echo -e "${YELLOW}Requesting Apple Command Line Developer Tools (includes Python 3)...${NC}"
        xcode-select --install 2>/dev/null
        echo ""
        echo -e "${YELLOW}Please complete the software installation dialog on your screen,${NC}"
        echo -e "${YELLOW}then double-click this script again when finished.${NC}"
        read -p "Press Return to exit..."
        exit 1
    fi
fi

echo -e "${GREEN}[OK] Using Python:${NC} $($PYTHON_BIN --version)"

# 2. Check if Virtual Environment exists and is working
SETUP_NEEDED=false

if [ ! -d ".venv" ]; then
    SETUP_NEEDED=true
elif [ ! -f ".venv/bin/python" ] || [ ! -f ".venv/bin/rembg" ]; then
    echo -e "${YELLOW}[!] Incomplete environment detected. Re-installing...${NC}"
    rm -rf .venv
    SETUP_NEEDED=true
fi

# 3. Perform automatic first-time setup
if [ "$SETUP_NEEDED" = true ]; then
    echo ""
    echo -e "${BLUE}------------------------------------------------------${NC}"
    echo -e "${YELLOW}  ⏳ First-time setup in progress...${NC}"
    echo -e "  This only happens once and takes about 1-2 minutes."
    echo -e "  Everything is set up locally and privately on your Mac."
    echo -e "${BLUE}------------------------------------------------------${NC}"
    echo ""

    echo -e "${BLUE}Step 1/3:${NC} Creating isolated environment..."
    $PYTHON_BIN -m venv .venv || {
        echo -e "${RED}[ERROR] Failed to create virtual environment.${NC}"
        read -p "Press Return to exit..."
        exit 1
    }

    echo -e "${BLUE}Step 2/3:${NC} Installing background removal tools..."
    source .venv/bin/activate
    python -m pip install --upgrade pip --quiet
    python -m pip install -r requirements.txt --quiet || {
        echo -e "${RED}[ERROR] Failed to install packages. Please check your internet connection.${NC}"
        read -p "Press Return to exit..."
        exit 1
    }

    echo -e "${BLUE}Step 3/3:${NC} Pre-downloading AI model for offline use..."
    python -m rembg d u2net

    echo ""
    echo -e "${GREEN}======================================================${NC}"
    echo -e "${GREEN}  ✓ Setup successfully completed!                     ${NC}"
    echo -e "${GREEN}======================================================${NC}"
    echo ""
else
    source .venv/bin/activate
fi

# 4. Launch the application
echo -e "${BLUE}Starting Background Remover Web UI...${NC}"
echo -e "Your web browser will open automatically in a moment."
echo -e "To stop the tool, simply close this Terminal window."
echo ""

python app.py

# Keep window open if app exits
read -p "Application closed. Press Return to exit..."
