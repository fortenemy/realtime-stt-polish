#!/usr/bin/env python3
"""
Quick Dependencies Installer
Szybki installer dependencies

Autor: AI Assistant
Data: 2025-01-18
"""

import subprocess
import sys

def install_package(package):
    """Zainstaluj pakiet"""
    try:
        print(f"📦 Instalowanie {package}...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            package, "--upgrade"
        ])
        print(f"✅ {package} zainstalowany!")
        return True
    except Exception as e:
        print(f"❌ Błąd instalacji {package}: {e}")
        return False

def main():
    print("🚀 Quick Dependencies Installer")
    print("=" * 40)
    
    # Podstawowe pakiety potrzebne do uruchomienia
    packages = [
        "sounddevice",
        "numpy", 
        "psutil",
        "colorama"
    ]
    
    print("📦 Instalowanie podstawowych pakietów...")
    
    results = []
    for package in packages:
        result = install_package(package)
        results.append(result)
    
    if all(results):
        print("\n✅ Wszystkie pakiety zainstalowane!")
        print("🎉 Możesz teraz uruchomić GUI!")
        print("\nUruchom ponownie: python gui_launcher.py")
    else:
        print("\n⚠️ Niektóre pakiety nie zostały zainstalowane")
        print("Spróbuj ręcznie: pip install sounddevice numpy psutil colorama")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
