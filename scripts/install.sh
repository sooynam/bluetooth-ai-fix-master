#!/bin/bash
# scripts/install.sh

echo ""
echo "🚀 Installing Bluetooth AI Fix Master..."
echo "==========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    print_warning "It's recommended to run this script as a regular user, not as root."
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check Python installation
print_status "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python3 not found!"
    print_status "Installing Python3..."
    
    if command -v apt &> /dev/null; then
        # Ubuntu/Debian
        sudo apt update
        sudo apt install python3 python3-pip python3-venv -y
    elif command -v yum &> /dev/null; then
        # CentOS/RHEL
        sudo yum install python3 python3-pip -y
    elif command -v pacman &> /dev/null; then
        # Arch Linux
        sudo pacman -S python python-pip
    elif command -v brew &> /dev/null; then
        # macOS
        brew install python3
    else
        print_error "Cannot automatically install Python3. Please install it manually."
        exit 1
    fi
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
print_success "Python $PYTHON_VERSION found"

# Create virtual environment
print_status "Creating virtual environment..."
if [ -d "bluetooth-ai-env" ]; then
    print_warning "Virtual environment already exists. Removing old one..."
    rm -rf bluetooth-ai-env
fi

python3 -m venv bluetooth-ai-env

if [ $? -ne 0 ]; then
    print_error "Failed to create virtual environment"
    exit 1
fi

print_success "Virtual environment created"

# Activate virtual environment
print_status "Activating virtual environment..."
source bluetooth-ai-env/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    print_error "Failed to install Python dependencies"
    exit 1
fi

print_success "Python dependencies installed"

# Install system dependencies
print_status "Installing system dependencies..."

if command -v apt &> /dev/null; then
    # Ubuntu/Debian
    print_status "Installing Bluetooth tools for Ubuntu/Debian..."
    sudo apt update
    sudo apt install bluetooth bluez bluez-tools rfkill -y
    
elif command -v yum &> /dev/null; then
    # CentOS/RHEL
    print_status "Installing Bluetooth tools for CentOS/RHEL..."
    sudo yum install bluez bluez-tools rfkill -y
    
elif command -v pacman &> /dev/null; then
    # Arch Linux
    print_status "Installing Bluetooth tools for Arch Linux..."
    sudo pacman -S bluez bluez-utils rfkill
    
elif command -v brew &> /dev/null; then
    # macOS
    print_status "macOS detected - Bluetooth tools should be available"
else
    print_warning "Unknown package manager - Bluetooth tools may need manual installation"
fi

# Create necessary directories
print_status "Creating directories..."
mkdir -p data
mkdir -p logs
mkdir -p web_interface/assets
mkdir -p web_interface/translations

# Set permissions for scripts
print_status "Setting script permissions..."
chmod +x scripts/*.sh
chmod +x src/*.py

# Initialize device database
print_status "Initializing device database..."
python3 -c "
from src.device_database import DeviceDatabase
db = DeviceDatabase()
print('✅ Device database initialized with', len(db.devices.get('devices', {})), 'companies')
"

# Create desktop shortcut (Linux)
if command -v gnome-session &> /dev/null || [ "$XDG_CURRENT_DESKTOP" != "" ]; then
    print_status "Creating desktop shortcut..."
    cat > ~/Desktop/bluetooth-ai-fix.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Bluetooth AI Fix Master
Comment=AI-Powered Bluetooth Problem Solver
Exec=$(pwd)/bluetooth-ai-env/bin/python3 $(pwd)/main.py --gui
Icon=$(pwd)/web_interface/assets/icons/app_icon.png
Terminal=false
Categories=Utility;
EOF
    chmod +x ~/Desktop/bluetooth-ai-fix.desktop
fi

# Test the installation
print_status "Testing installation..."
python3 -c "
try:
    from src.ai_bluetooth_fix import AIBluetoothFixer
    from src.gui_interface import BluetoothAIGUI
    from src.web_server import WebServer
    print('✅ All modules imported successfully')
except Exception as e:
    print('❌ Import error:', e)
"

echo ""
echo "==========================================="
print_success "Installation completed successfully!"
echo ""
echo "🎯 Quick Start Guide:"
echo ""
echo "1. Start the application:"
echo "   source bluetooth-ai-env/bin/activate"
echo "   python3 main.py --gui"
echo ""
echo "2. Or start web interface:"
echo "   python3 main.py --web"
echo "   Then open: http://localhost:5000"
echo ""
echo "3. Command line usage:"
echo "   python3 main.py --scan    # Scan devices"
echo "   python3 main.py --cli     # CLI mode"
echo ""
echo "🔧 Additional Commands:"
echo "   ./scripts/update.sh       # Update application"
echo "   ./scripts/deploy_website.sh # Deploy to web"
echo ""
echo "📖 Documentation:"
echo "   Check docs/ folder for user manual and troubleshooting"
echo ""
echo "==========================================="
echo ""
