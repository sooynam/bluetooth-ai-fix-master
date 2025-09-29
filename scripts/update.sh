#!/bin/bash
# scripts/update.sh

echo ""
echo "🔄 Updating Bluetooth AI Fix Master..."
echo "==========================================="

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Check if virtual environment exists
if [ ! -d "bluetooth-ai-env" ]; then
    echo "❌ Virtual environment not found. Please run install.sh first."
    exit 1
fi

# Activate virtual environment
source bluetooth-ai-env/bin/activate

# Update from git (if this is a git repository)
if [ -d ".git" ]; then
    print_status "Checking for updates from repository..."
    git pull origin main
fi

# Update Python dependencies
print_status "Updating Python dependencies..."
pip install --upgrade -r requirements.txt

# Update device database
print_status "Updating device database..."
python3 -c "
from src.device_database import DeviceDatabase
db = DeviceDatabase()
print('Device database updated with', len(db.devices.get('devices', {})), 'companies')
"

print_success "Update completed successfully!"
echo ""
echo "🚀 You can now run the application with:"
echo "   source bluetooth-ai-env/bin/activate"
echo "   python3 main.py --gui"
echo ""
