# src/web_server.py
from flask import Flask, render_template, jsonify, request
import json
import threading
from typing import Dict, Any

class WebServer:
    def __init__(self, host='0.0.0.0', port=5000):
        self.app = Flask(__name__, 
                        template_folder='../web_interface',
                        static_folder='../web_interface')
        self.host = host
        self.port = port
        self.ai_fixer = None
        self.language_manager = None
        
        self.setup_routes()
        self.load_dependencies()
    
    def load_dependencies(self):
        """Dependencies load karein background mein"""
        def load():
            try:
                from ai_bluetooth_fix import AIBluetoothFixer
                from language_manager import LanguageManager
                
                self.ai_fixer = AIBluetoothFixer()
                self.language_manager = LanguageManager()
                print("✅ Web server dependencies loaded successfully")
            except Exception as e:
                print(f"❌ Dependency load error: {e}")
        
        threading.Thread(target=load, daemon=True).start()
    
    def setup_routes(self):
        """Web routes setup karein"""
        
        @self.app.route('/')
        def index():
            return render_template('index.html')
        
        @self.app.route('/api/devices', methods=['GET'])
        def get_devices():
            try:
                if self.ai_fixer:
                    devices = self.ai_fixer.scan_devices()
                    return jsonify({
                        "success": True,
                        "devices": devices,
                        "count": len(devices)
                    })
                else:
                    return jsonify({
                        "success": False,
                        "error": "AI system not ready"
                    }), 503
            except Exception as e:
                return jsonify({
                    "success": False,
                    "error": str(e)
                }), 500
        
        @self.app.route('/api/diagnose', methods=['POST'])
        def diagnose_device():
            try:
                data = request.json
                device_info = data.get('device', {})
                
                if self.ai_fixer:
                    diagnosis = self.ai_fixer.diagnose_device(device_info)
                    return jsonify({
                        "success": True,
                        "diagnosis": diagnosis
                    })
                else:
                    return jsonify({
                        "success": False,
                        "error": "AI system not ready"
                    }), 503
                    
            except Exception as e:
                return jsonify({
                    "success": False,
                    "error": str(e)
                }), 500
        
        @self.app.route('/api/fix', methods=['POST'])
        def apply_fix():
            try:
                data = request.json
                fix_action = data.get('fix_action')
                device_info = data.get('device', {})
                
                if self.ai_fixer:
                    result = self.ai_fixer.apply_fix(fix_action, device_info)
                    return jsonify({
                        "success": True,
                        "result": result
                    })
                else:
                    return jsonify({
                        "success": False, 
                        "error": "AI system not ready"
                    }), 503
                    
            except Exception as e:
                return jsonify({
                    "success": False,
                    "error": str(e)
                }), 500
        
        @self.app.route('/api/languages', methods=['GET'])
        def get_languages():
            try:
                if self.language_manager:
                    languages = self.language_manager.get_available_languages()
                    return jsonify({
                        "success": True,
                        "languages": languages,
                        "current": self.language_manager.get_current_language()
                    })
                else:
                    return jsonify({
                        "success": False,
                        "error": "Language system not ready"
                    }), 503
            except Exception as e:
                return jsonify({
                    "success": False,
                    "error": str(e)
                }), 500
        
        @self.app.route('/api/translations/<lang_code>', methods=['GET'])
        def get_translations(lang_code):
            try:
                if self.language_manager:
                    success = self.language_manager.set_language(lang_code)
                    if success:
                        translations = self.language_manager.translations
                        return jsonify({
                            "success": True,
                            "language": lang_code,
                            "translations": translations,
                            "is_rtl": self.language_manager.is_rtl(lang_code)
                        })
                    else:
                        return jsonify({
                            "success": False,
                            "error": f"Language {lang_code} not available"
                        }), 404
                else:
                    return jsonify({
                        "success": False,
                        "error": "Language system not ready"
                    }), 503
            except Exception as e:
                return jsonify({
                    "success": False,
                    "error": str(e)
                }), 500
        
        @self.app.route('/api/status', methods=['GET'])
        def get_status():
            """System status return karein"""
            status = {
                "ai_system": self.ai_fixer is not None,
                "language_system": self.language_manager is not None,
                "available_languages": self.language_manager.get_available_languages() if self.language_manager else {},
                "current_language": self.language_manager.get_current_language() if self.language_manager else "en"
            }
            return jsonify(status)
    
    def run(self):
        """Web server run karein"""
        print(f"🌐 Starting Bluetooth AI Fix Master Web Server...")
        print(f"📍 Server running on: http://{self.host}:{self.port}")
        print(f"📱 Web Interface: http://{self.host}:{self.port}/")
        print(f"🔧 API Status: http://{self.host}:{self.port}/api/status")
        print("\nPress Ctrl+C to stop the server")
        
        try:
            self.app.run(
                host=self.host,
                port=self.port,
                debug=False,
                threaded=True
            )
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user")
        except Exception as e:
            print(f"❌ Server error: {e}")

if __name__ == "__main__":
    server = WebServer()
    server.run()
