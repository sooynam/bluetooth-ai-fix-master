# src/device_database.py
import json
import os
from typing import Dict, List, Any

class DeviceDatabase:
    def __init__(self, db_path: str = "data/device_database.json"):
        self.db_path = db_path
        self.devices = self.load_database()
    
    def load_database(self) -> Dict[str, Any]:
        """Device database load karein"""
        default_db = {
            "devices": {
                "Sony": {
                    "WH-1000XM4": {
                        "mac_prefix": "04:5F",
                        "common_issues": ["connection_drop", "audio_quality", "battery_drain", "touch_controls"],
                        "recommended_fixes": ["reset_connection", "update_firmware", "battery_calibration", "clean_earcups"],
                        "auto_connect": True,
                        "ai_optimization": "high",
                        "device_type": "headphones",
                        "specs": {
                            "battery_life": "30 hours",
                            "noise_canceling": True,
                            "voice_assistant": True
                        }
                    },
                    "WF-1000XM4": {
                        "mac_prefix": "04:5F", 
                        "common_issues": ["pairing", "battery", "fit_issues", "charging_case"],
                        "recommended_fixes": ["reset_pairing", "case_cleaning", "ear_tip_replacement"],
                        "auto_connect": True,
                        "ai_optimization": "high",
                        "device_type": "earbuds"
                    }
                },
                "Apple": {
                    "AirPods Pro": {
                        "mac_prefix": "DC:56",
                        "common_issues": ["connectivity", "sound_balance", "mic_issues", "spatial_audio"],
                        "recommended_fixes": ["reconnect_sequence", "audio_balance", "mic_test", "reset_spatial"],
                        "auto_connect": True,
                        "ai_optimization": "high",
                        "device_type": "earbuds"
                    },
                    "AirPods Max": {
                        "mac_prefix": "DC:56",
                        "common_issues": ["anc_issues", "battery_drain", "comfort", "case_charging"],
                        "recommended_fixes": ["reset_anc", "battery_recalibration", "adjust_fit"],
                        "auto_connect": True,
                        "ai_optimization": "high",
                        "device_type": "headphones"
                    }
                },
                "Samsung": {
                    "Galaxy Buds Pro": {
                        "mac_prefix": "64:5A",
                        "common_issues": ["connection_stability", "ambient_sound", "touch_controls", "battery"],
                        "recommended_fixes": ["reset_gear_app", "update_software", "clean_buds"],
                        "auto_connect": True,
                        "ai_optimization": "medium",
                        "device_type": "earbuds"
                    }
                },
                "Logitech": {
                    "MX Keys": {
                        "mac_prefix": "70:B3", 
                        "common_issues": ["pairing_mode", "battery_indicator", "multi_device"],
                        "recommended_fixes": ["reset_pairing", "recharge_battery", "reconnect_all_devices"],
                        "auto_connect": True,
                        "ai_optimization": "medium",
                        "device_type": "keyboard"
                    },
                    "MX Master 3": {
                        "mac_prefix": "70:B3",
                        "common_issues": ["scroll_wheel", "gesture_buttons", "battery_life"],
                        "recommended_fixes": ["reset_mouse", "update_options_software", "recalibrate"],
                        "auto_connect": True,
                        "ai_optimization": "medium",
                        "device_type": "mouse"
                    }
                }
            },
            "issue_patterns": {
                "connection_drop": {
                    "description": "Frequent disconnections or unstable connection",
                    "severity": "high",
                    "common_causes": ["interference", "low_battery", "driver_issues", "distance"]
                },
                "audio_quality": {
                    "description": "Poor sound quality, crackling, or no audio",
                    "severity": "medium", 
                    "common_causes": ["codec_mismatch", "audio_settings", "hardware_issue"]
                },
                "battery_drain": {
                    "description": "Battery drains faster than expected",
                    "severity": "medium",
                    "common_causes": ["battery_age", "firmware_bug", "excessive_usage"]
                }
            }
        }
        
        try:
            if os.path.exists(self.db_path):
                with open(self.db_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Create directory if not exists
                os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
                # Save default database
                with open(self.db_path, 'w', encoding='utf-8') as f:
                    json.dump(default_db, f, indent=2)
                return default_db
        except Exception as e:
            print(f"Database load error: {e}")
            return default_db
    
    def get_device_info(self, mac_address: str, device_name: str = "") -> Dict[str, Any]:
        """Device information get karein MAC address ya name se"""
        # MAC prefix se search karein
        mac_prefix = mac_address.replace(':', '')[:4].upper()
        
        for company, models in self.devices.get("devices", {}).items():
            for model, info in models.items():
                if info.get("mac_prefix", "").replace(':', '') == mac_prefix:
                    return {
                        "company": company,
                        "model": model,
                        "device_type": info.get("device_type", "unknown"),
                        **info
                    }
        
        # Name se search karein agar MAC match na ho
        if device_name:
            device_lower = device_name.lower()
            for company, models in self.devices.get("devices", {}).items():
                for model, info in models.items():
                    if model.lower() in device_lower:
                        return {
                            "company": company, 
                            "model": model,
                            "device_type": info.get("device_type", "unknown"),
                            **info
                        }
        
        # Default device info agar kuch na mile
        return {
            "company": "Unknown",
            "model": "Generic Bluetooth Device", 
            "device_type": "unknown",
            "common_issues": ["connection_drop", "audio_quality", "pairing"],
            "recommended_fixes": ["reset_bluetooth", "reconnect_device", "update_drivers"],
            "ai_optimization": "low"
        }
    
    def get_common_issues(self, device_type: str) -> List[str]:
        """Common issues get karein device type ke hisaab se"""
        issue_map = {
            "headphones": ["audio_quality", "connection_drop", "battery_drain", "comfort"],
            "earbuds": ["connection_drop", "battery_life", "fit_issues", "charging_case"],
            "speaker": ["audio_quality", "connection_range", "battery", "volume_issues"],
            "keyboard": ["pairing_mode", "battery_indicator", "key_response"],
            "mouse": ["cursor_movement", "battery_life", "scroll_wheel"],
            "wearable": ["connection_stability", "battery_drain", "sync_issues"]
        }
        
        return issue_map.get(device_type, ["connection_drop", "audio_quality"])
    
    def get_recommended_fixes(self, device_info: Dict[str, Any], issue_type: str) -> List[str]:
        """Recommended fixes get karein device aur issue ke hisaab se"""
        device_fixes = device_info.get("recommended_fixes", [])
        issue_patterns = self.devices.get("issue_patterns", {})
        
        # Device-specific fixes
        fixes = device_fixes.copy()
        
        # Issue-specific fixes add karein
        if issue_type in issue_patterns:
            common_causes = issue_patterns[issue_type].get("common_causes", [])
            for cause in common_causes:
                if cause == "driver_issues" and "update_drivers" not in fixes:
                    fixes.append("update_drivers")
                elif cause == "interference" and "check_interference" not in fixes:
                    fixes.append("check_interference")
                elif cause == "low_battery" and "check_battery" not in fixes:
                    fixes.append("check_battery")
        
        return fixes[:5]  # Maximum 5 fixes return karein
    
    def add_custom_device(self, device_data: Dict[str, Any]) -> bool:
        """Custom device add karein database mein"""
        try:
            company = device_data.get("company", "Custom")
            model = device_data.get("model", "Device")
            
            if "devices" not in self.devices:
                self.devices["devices"] = {}
            
            if company not in self.devices["devices"]:
                self.devices["devices"][company] = {}
            
            self.devices["devices"][company][model] = {
                "mac_prefix": device_data.get("mac_prefix", "00:00"),
                "common_issues": device_data.get("common_issues", []),
                "recommended_fixes": device_data.get("recommended_fixes", []),
                "device_type": device_data.get("device_type", "unknown"),
                "ai_optimization": device_data.get("ai_optimization", "low")
            }
            
            # Save updated database
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump(self.devices, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Add device error: {e}")
            return False
    
    def search_devices(self, query: str) -> List[Dict[str, Any]]:
        """Devices search karein query se"""
        results = []
        query_lower = query.lower()
        
        for company, models in self.devices.get("devices", {}).items():
            for model, info in models.items():
                if (query_lower in company.lower() or 
                    query_lower in model.lower() or
                    query_lower in info.get("device_type", "").lower()):
                    
                    results.append({
                        "company": company,
                        "model": model,
                        "device_type": info.get("device_type", "unknown"),
                        "common_issues": info.get("common_issues", []),
                        "mac_prefix": info.get("mac_prefix", "")
                    })
        
        return results

if __name__ == "__main__":
    db = DeviceDatabase()
    print("Device Database Loaded Successfully!")
    print(f"Companies: {list(db.devices.get('devices', {}).keys())}")
    
    # Test device lookup
    test_mac = "04:5F:01:02:03"
    device_info = db.get_device_info(test_mac, "Sony WH-1000XM4")
    print(f"\nDevice Info for {test_mac}:")
    print(f"Company: {device_info['company']}")
    print(f"Model: {device_info['model']}")
    print(f"Type: {device_info['device_type']}")
    print(f"Common Issues: {device_info['common_issues']}")
