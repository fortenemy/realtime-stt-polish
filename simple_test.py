#!/usr/bin/env python3
"""
Prosty test AudioCapture bez dodatkowych zależności
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test podstawowych importów"""
    print("🧪 Test importów...")
    
    try:
        import numpy as np
        print("✅ NumPy:", np.__version__)
    except ImportError as e:
        print("❌ NumPy nie zainstalowany:", e)
        return False
    
    try:
        import sounddevice as sd
        print("✅ SoundDevice zainstalowany")
        
        # Test urządzeń
        devices = sd.query_devices()
        print(f"📱 Znaleziono {len(devices)} urządzeń audio")
        
        return True
    except ImportError as e:
        print("❌ SoundDevice nie zainstalowany:", e)
        return False
    except Exception as e:
        print("⚠️ Błąd SoundDevice:", e)
        return False

def test_audio_capture_import():
    """Test importu AudioCapture"""
    print("\n🎤 Test AudioCapture...")
    
    # Dodaj src do ścieżki
    sys.path.insert(0, str(Path(__file__).parent / "src"))
    
    try:
        from audio_capture import AudioCapture
        print("✅ AudioCapture zaimportowany")
        
        # Test tworzenia obiektu
        capture = AudioCapture()
        print("✅ AudioCapture obiekt utworzony")
        
        # Test metod
        stats = capture.get_statistics()
        print(f"✅ Statystyki: {stats}")
        
        return True
        
    except Exception as e:
        print(f"❌ Błąd AudioCapture: {e}")
        return False

def main():
    """Główna funkcja"""
    print("🚀 Prosty test Real-time STT")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_audio_capture_import
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"💥 Test błąd: {e}")
            results.append(False)
    
    passed = sum(results)
    total = len(results)
    
    print(f"\n📊 Wyniki: {passed}/{total}")
    
    if passed == total:
        print("🎉 Wszystko działa!")
        return True
    else:
        print("⚠️ Niektóre testy nie przeszły")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
