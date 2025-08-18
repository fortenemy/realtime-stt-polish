#!/usr/bin/env python3
"""
Skrypt instalacji zależności dla Real-time STT
"""

import subprocess
import sys
import importlib.util

def check_package(package_name):
    """Sprawdź czy pakiet jest zainstalowany"""
    spec = importlib.util.find_spec(package_name)
    return spec is not None

def install_package(package):
    """Zainstaluj pakiet przez pip"""
    print(f"📦 Instalowanie {package}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} zainstalowany pomyślnie")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Błąd instalacji {package}: {e}")
        return False

def main():
    """Główna funkcja instalacji"""
    print("🚀 Instalacja zależności Real-time STT")
    print("=" * 40)
    
    # Lista podstawowych pakietów (etap 1)
    basic_packages = [
        "numpy>=1.24.0",
        "sounddevice>=0.4.6", 
        "colorama>=0.4.6",
        "tqdm>=4.65.0"
    ]
    
    print("📋 Etap 1: Podstawowe biblioteki")
    for package in basic_packages:
        if not install_package(package):
            print(f"⚠️ Nie udało się zainstalować {package}")
            return False
    
    print("\n✅ Etap 1 zakończony pomyślnie!")
    
    # Test importów
    print("\n🧪 Test importów...")
    test_imports = ["numpy", "sounddevice", "colorama", "tqdm"]
    
    for module in test_imports:
        try:
            __import__(module)
            print(f"✅ {module} - OK")
        except ImportError as e:
            print(f"❌ {module} - BŁĄD: {e}")
            return False
    
    print("\n🎉 Wszystkie podstawowe zależności zainstalowane!")
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
