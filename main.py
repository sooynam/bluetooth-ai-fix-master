# main.py
#!/usr/bin/env python3
"""
Bluetooth AI Fix Master - Main Application
AI-powered Bluetooth problem solver with multi-language support
"""

import sys
import os
import argparse

def main():
    parser = argparse.ArgumentParser(description="Bluetooth AI Fix Master")
    parser.add_argument('--gui', action='store_true', help='Start GUI interface')
    parser.add_argument('--web', action='store_true', help='Start web server')
    parser.add_argument('--cli', action='store_true', help='Command line interface')
    parser.add_argument('--language', type=str, default='en', help='Set language')
    parser.add_argument('--scan', action='store_true', help='Scan for devices')
    
    args = parser.parse_args()
    
    try:
        if args.gui:
            print("🚀 Starting GUI Interface...")
            from src.gui_interface import BluetoothAIGUI
            app = BluetoothAIGUI()
            app.run()
            
        elif args.web:
            print("🌐 Starting Web Server...")
            from src.web_server import WebServer
            server = WebServer()
            server.run()
            
        elif args.cli or args.scan:
            print("💻 Starting CLI Mode...")
            from src.ai_bluetooth_fix import AIBluetoothFixer
            ai_fixer = AIBluetoothFixer()
            
            if args.scan:
                devices = ai_fixer.scan_devices()
                print(f"📱 Found {len(devices)} devices:")
                for device in devices:
                    print(f"  • {device['name']} - {device['mac_address']}")
                    
        else:
            # Default to GUI
            print("🚀 Starting Bluetooth AI Fix Master...")
            from src.gui_interface import BluetoothAIGUI
            app = BluetoothAIGUI()
            app.run()
            
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
