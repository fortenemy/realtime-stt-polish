#!/usr/bin/env python3
"""
Test środowiska i podstawowych funkcjonalności
"""

import sys
import platform
from pathlib import Path

def test_python_version():
    """Test wersji Python"""
    print("🐍 Python Environment Test")
    print(f"Version: {sys.version}")
    print(f"Platform: {platform.system()} {platform.release()}")
    
    if sys.version_info < (3, 8):
        print("❌ Wymagany Python 3.8+")
        return False
    else:
        print("✅ Python version OK")
        return True

def test_audio_devices():
    """Test dostępności urządzeń audio"""
    try:
        import sounddevice as sd
        print("\n🎤 Audio Devices Test")
        devices = sd.query_devices()
        print(f"Found {len(devices)} audio devices")
        
        # Znajdź domyślne urządzenie wejściowe
        default_input = sd.default.device[0]
        if default_input is not None:
            print(f"✅ Default input device: {default_input}")
            return True
        else:
            print("❌ No default input device found")
            return False
            
    except Exception as e:
        print(f"❌ Audio test failed: {e}")
        return False

def test_numpy():
    """Test NumPy"""
    try:
        import numpy as np
        print("\n🔢 NumPy Test")
        test_array = np.array([1, 2, 3, 4, 5])
        print(f"✅ NumPy {np.__version__} - Array test OK: {test_array}")
        return True
    except Exception as e:
        print(f"❌ NumPy test failed: {e}")
        return False

def test_project_structure():
    """Test struktury projektu"""
    print("\n📁 Project Structure Test")
    
    required_files = [
        "main.py",
        "requirements.txt", 
        "src/__init__.py",
        "src/audio_capture.py"
    ]
    
    all_ok = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ Missing: {file_path}")
            all_ok = False
    
    return all_ok

def main():
    """Główna funkcja testów"""
    print("🧪 Real-time STT - Environment Test")
    print("=" * 40)
    
    tests = [
        ("Python Version", test_python_version),
        ("Project Structure", test_project_structure),
        ("NumPy", test_numpy),
        ("Audio Devices", test_audio_devices)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    print("\n📊 Test Summary")
    print("-" * 30)
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! Environment ready!")
        return True
    else:
        print("⚠️ Some tests failed. Check configuration.")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
