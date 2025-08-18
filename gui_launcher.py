#!/usr/bin/env python3
"""
GUI Launcher for Real-time Speech-to-Text Polish
Launcher GUI dla Real-time Speech-to-Text Polski

Autor: AI Assistant
Data: 2025-01-18
"""

import sys
import os
from pathlib import Path

# Dodaj src do ścieżki
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

def check_gui_dependencies():
    """Sprawdź dependencies dla GUI"""
    missing = []
    
    try:
        import tkinter
    except ImportError:
        missing.append("tkinter")
    
    try:
        import numpy
    except ImportError:
        missing.append("numpy")
    
    try:
        import sounddevice
    except ImportError:
        missing.append("sounddevice")
    
    if missing:
        print("❌ Brakujące dependencies dla GUI:")
        for dep in missing:
            print(f"   - {dep}")
        print("\n💡 Zainstaluj:")
        if "tkinter" in missing:
            print("   - Windows: Tkinter jest w Python, sprawdź instalację")
            print("   - Linux: sudo apt-get install python3-tk")
            print("   - macOS: Tkinter jest w Python")
        print("   - python install_whisper_dependencies.py")
        return False
    
    return True

def main():
    """Główna funkcja launchera"""
    print("🎨 Real-time STT Polish - GUI Launcher")
    print("=" * 45)
    
    # Sprawdź dependencies
    if not check_gui_dependencies():
        input("Press Enter to exit...")
        return False
    
    try:
        # Import i uruchom GUI
        from src.gui_application import STTGuiApplication
        
        print("🚀 Uruchamianie GUI aplikacji...")
        app = STTGuiApplication()
        app.run()
        
        return True
        
    except ImportError as e:
        print(f"❌ Błąd importu GUI: {e}")
        print("💡 Sprawdź czy wszystkie pliki są na miejscu")
        return False
    
    except Exception as e:
        print(f"❌ Błąd GUI aplikacji: {e}")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n👋 Przerwane przez użytkownika")
        sys.exit(0)
