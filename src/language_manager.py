
# src/language_manager.py
import json
import os
from typing import Dict, Any

class LanguageManager:
    def __init__(self, lang_dir: str = "web_interface/translations"):
        self.lang_dir = lang_dir
        self.current_language = "en"
        self.translations = {}
        self.available_languages = self.discover_languages()
        self.load_language("en")
    
    def discover_languages(self) -> Dict[str, str]:
        """Available languages discover karein"""
        languages = {
            "en": "English 🇺🇸",
            "hi": "हिंदी 🇮🇳", 
            "es": "Español 🇪🇸",
            "fr": "Français 🇫🇷",
            "ar": "العربية 🇦🇪",
            "zh": "中文 🇨🇳",
            "pt": "Português 🇵🇹",
            "de": "Deutsch 🇩🇪"
        }
        
        # Check if translation files exist
        available = {}
        for lang_code, lang_name in languages.items():
            lang_file = os.path.join(self.lang_dir, f"{lang_code}.json")
            if os.path.exists(lang_file):
                available[lang_code] = lang_name
            else:
                print(f"Warning: Translation file not found for {lang_name}")
        
        return available
    
    def load_language(self, lang_code: str) -> bool:
        """Selected language load karein"""
        try:
            lang_file = os.path.join(self.lang_dir, f"{lang_code}.json")
            if os.path.exists(lang_file):
                with open(lang_file, 'r', encoding='utf-8') as f:
                    self.translations = json.load(f)
                self.current_language = lang_code
                print(f"✅ Language loaded: {self.available_languages.get(lang_code, lang_code)}")
                return True
            else:
                print(f"❌ Language file not found: {lang_file}")
                return False
        except Exception as e:
            print(f"❌ Language load error: {e}")
            return False
    
    def get_text(self, key: str, default: str = None) -> str:
        """Text translation get karein"""
        return self.translations.get(key, default or key)
    
    def set_language(self, lang_code: str) -> bool:
        """User selected language set karein"""
        if lang_code in self.available_languages:
            return self.load_language(lang_code)
        else:
            print(f"❌ Language not available: {lang_code}")
            return False
    
    def get_available_languages(self) -> Dict[str, str]:
        """Available languages return karein"""
        return self.available_languages
    
    def get_current_language(self) -> str:
        """Current language code return karein"""
        return self.current_language
    
    def get_language_name(self, lang_code: str) -> str:
        """Language name get karein code se"""
        return self.available_languages.get(lang_code, lang_code)
    
    def translate_dict(self, data_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Dictionary ki values translate karein"""
        translated = {}
        for key, value in data_dict.items():
            if isinstance(value, str):
                translated[key] = self.get_text(value, value)
            else:
                translated[key] = value
        return translated
    
    def get_rtl_languages(self) -> list:
        """RTL (Right-to-Left) languages ki list return karein"""
        return ['ar', 'he']  # Arabic, Hebrew

    def is_rtl(self, lang_code: str = None) -> bool:
        """Check karein ke language RTL hai ya nahi"""
        code = lang_code or self.current_language
        return code in self.get_rtl_languages()

# Test function
if __name__ == "__main__":
    lm = LanguageManager()
    print("Available Languages:")
    for code, name in lm.available_languages.items():
        print(f"  {code}: {name}")
    
    print(f"\nCurrent Language: {lm.current_language}")
    print(f"Sample Text: {lm.get_text('app_title')}")
    
    # Test Hindi
    lm.set_language("hi")
    print(f"\nHindi Text: {lm.get_text('app_title')}")
