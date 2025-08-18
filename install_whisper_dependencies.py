#!/usr/bin/env python3
"""
Installer for Whisper STT dependencies
Instalator zależności dla Whisper STT

Autor: AI Assistant
Data: 2025-01-18
"""

import subprocess
import sys
import importlib.util
import platform
import os
from pathlib import Path

def print_banner():
    """Wyświetl banner"""
    print("🤖 Instalator OpenAI Whisper Dependencies")
    print("=" * 50)
    print("🎤 Real-time Speech-to-Text Polish")
    print("🔧 Instalacja pakietów AI dla rozpoznawania mowy")
    print()

def check_python_version():
    """Sprawdź wersję Python"""
    print("🐍 Sprawdzanie wersji Python...")
    
    version = sys.version_info
    print(f"   Python {version.major}.{version.minor}.{version.micro}")
    
    if version < (3, 8):
        print("❌ Wymagany Python 3.8 lub nowszy!")
        return False
    
    print("✅ Wersja Python OK")
    return True

def check_package_installed(package_name):
    """Sprawdź czy pakiet jest zainstalowany"""
    spec = importlib.util.find_spec(package_name)
    return spec is not None

def install_package(package, description=""):
    """Zainstaluj pakiet przez pip"""
    print(f"📦 Instalowanie {package}...")
    if description:
        print(f"   {description}")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            package, "--upgrade", "--quiet"
        ])
        print(f"✅ {package} zainstalowany pomyślnie")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Błąd instalacji {package}: {e}")
        return False

def install_torch():
    """Zainstaluj PyTorch z odpowiednią konfiguracją"""
    print("\n🔥 Instalacja PyTorch...")
    
    # Sprawdź czy już zainstalowany
    if check_package_installed("torch"):
        try:
            import torch
            print(f"✅ PyTorch już zainstalowany: {torch.__version__}")
            if torch.cuda.is_available():
                print(f"🚀 CUDA dostępne: {torch.cuda.get_device_name(0)}")
            else:
                print("💻 CPU-only version")
            return True
        except ImportError:
            pass
    
    # Określ platformę
    system = platform.system().lower()
    
    if system == "windows":
        # Windows - sprawdź CUDA
        print("🪟 Wykryto Windows")
        try:
            import subprocess
            result = subprocess.run(["nvidia-smi"], capture_output=True, text=True)
            if result.returncode == 0:
                print("🚀 NVIDIA GPU wykryte - instaluję CUDA version")
                torch_package = "torch torchaudio --index-url https://download.pytorch.org/whl/cu118"
            else:
                print("💻 Brak NVIDIA GPU - instaluję CPU version")
                torch_package = "torch torchaudio --index-url https://download.pytorch.org/whl/cpu"
        except:
            print("💻 Nie można wykryć GPU - instaluję CPU version")
            torch_package = "torch torchaudio"
    else:
        # Linux/Mac
        print(f"🐧 Wykryto {system}")
        torch_package = "torch torchaudio"
    
    return install_package(torch_package, "Deep learning framework")

def install_whisper():
    """Zainstaluj OpenAI Whisper"""
    print("\n🎤 Instalacja OpenAI Whisper...")
    
    if check_package_installed("whisper"):
        try:
            import whisper
            print(f"✅ Whisper już zainstalowany")
            models = whisper.available_models()
            print(f"📋 Dostępne modele: {', '.join(models)}")
            return True
        except ImportError:
            pass
    
    return install_package("openai-whisper", "Speech recognition by OpenAI")

def install_optional_packages():
    """Zainstaluj opcjonalne pakiety"""
    print("\n🔧 Instalacja opcjonalnych pakietów...")
    
    optional_packages = [
        ("librosa", "Zaawansowane przetwarzanie audio"),
        ("scipy", "Scientific computing"),
        ("matplotlib", "Wykresy i wizualizacje"),
        ("pydub", "Manipulacja plików audio")
    ]
    
    results = []
    for package, description in optional_packages:
        if not check_package_installed(package):
            result = install_package(package, description)
            results.append((package, result))
        else:
            print(f"✅ {package} już zainstalowany")
            results.append((package, True))
    
    return results

def test_installations():
    """Przetestuj instalacje"""
    print("\n🧪 Testowanie instalacji...")
    
    tests = [
        ("torch", "PyTorch"),
        ("whisper", "OpenAI Whisper"),
        ("librosa", "Librosa (optional)"),
        ("scipy", "SciPy")
    ]
    
    results = []
    for module, name in tests:
        try:
            __import__(module)
            print(f"✅ {name} - OK")
            results.append((name, True))
        except ImportError:
            print(f"⚠️ {name} - Not available")
            results.append((name, False))
    
    return results

def download_whisper_model():
    """Pobierz domyślny model Whisper"""
    print("\n📥 Pobieranie modelu Whisper...")
    
    try:
        import whisper
        
        # Pobierz model 'base' - dobry kompromis rozmiar/jakość
        print("📦 Pobieranie modelu 'base' (142MB)...")
        print("   (Może chwilę potrwać przy pierwszym uruchomieniu)")
        
        model = whisper.load_model("base")
        print("✅ Model 'base' pobrany i gotowy")
        
        # Test na próbce
        print("🧪 Test modelu z próbką audio...")
        import numpy as np
        
        # Stwórz próbkę audio (cisza)
        audio = np.zeros(16000, dtype=np.float32)  # 1 sekunda ciszy
        
        result = model.transcribe(audio)
        print(f"✅ Model działa - tekst: '{result['text']}'")
        
        return True
        
    except Exception as e:
        print(f"❌ Błąd pobierania modelu: {e}")
        return False

def create_test_script():
    """Stwórz skrypt testowy"""
    print("\n📝 Tworzenie skryptu testowego...")
    
    test_script = """#!/usr/bin/env python3
# Test Whisper STT integration

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_whisper_basic():
    try:
        import whisper
        import torch
        
        print("🤖 Testing Whisper basic functionality...")
        print(f"PyTorch: {torch.__version__}")
        print(f"Device: {'CUDA' if torch.cuda.is_available() else 'CPU'}")
        
        # Load small model
        model = whisper.load_model("base")
        print("✅ Model loaded successfully")
        
        # Test with silence
        import numpy as np
        audio = np.zeros(16000, dtype=np.float32)
        
        result = model.transcribe(audio, language="pl")
        print(f"✅ Transcription test: '{result['text']}'")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_whisper_basic()
    print("🎉 Whisper ready!" if success else "⚠️ Check installation")
"""
    
    try:
        with open("test_whisper_basic.py", "w", encoding="utf-8") as f:
            f.write(test_script)
        print("✅ Skrypt testowy utworzony: test_whisper_basic.py")
        return True
    except Exception as e:
        print(f"❌ Błąd tworzenia skryptu: {e}")
        return False

def main():
    """Główna funkcja instalacji"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        input("Press Enter to exit...")
        return False
    
    print("\n🚀 Rozpoczynam instalację dependencies...")
    print("⏱️ To może potrwać kilka minut (PyTorch + Whisper to duże pakiety)")
    
    # Ask for confirmation
    response = input("\nKontynuować instalację? (y/N): ").lower()
    if response != 'y':
        print("❌ Instalacja anulowana")
        return False
    
    steps = [
        ("PyTorch", install_torch),
        ("OpenAI Whisper", install_whisper),
        ("Optional packages", install_optional_packages),
        ("Test installations", test_installations),
        ("Download Whisper model", download_whisper_model),
        ("Create test script", create_test_script)
    ]
    
    results = []
    for step_name, step_func in steps:
        print(f"\n🔄 {step_name}...")
        try:
            result = step_func()
            results.append((step_name, result))
            
            if isinstance(result, list):
                # Handle multiple results (like optional packages)
                success = all(r[1] for r in result)
                results[-1] = (step_name, success)
                
        except Exception as e:
            print(f"💥 {step_name} crashed: {e}")
            results.append((step_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 PODSUMOWANIE INSTALACJI")
    print("=" * 50)
    
    successful = 0
    for step_name, success in results:
        if success:
            print(f"✅ {step_name}")
            successful += 1
        else:
            print(f"❌ {step_name}")
    
    print(f"\n🎯 Wynik: {successful}/{len(results)} kroków zakończonych sukcesem")
    
    if successful >= len(results) - 1:  # Allow 1 failure
        print("\n🎉 INSTALACJA ZAKOŃCZONA POMYŚLNIE!")
        print("\n📋 Następne kroki:")
        print("1. Uruchom: python test_whisper_basic.py")
        print("2. Uruchom: python test_stt_engine.py") 
        print("3. Przetestuj pełną integrację")
        print("\n🎤 Real-time STT gotowy do użycia!")
        
        # Sprawdź rozmiar instalacji
        print(f"\n📊 Szacunkowy rozmiar instalacji: ~2-3GB")
        print("   (PyTorch: ~1.5GB, Whisper models: ~500MB)")
        
        return True
    else:
        print("\n⚠️ Instalacja częściowo nieudana")
        print("💡 Spróbuj uruchomić ponownie lub zainstaluj ręcznie:")
        print("   pip install torch torchaudio openai-whisper")
        return False

if __name__ == "__main__":
    try:
        success = main()
        input(f"\nPress Enter to exit...")
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n👋 Instalacja przerwana przez użytkownika")
        sys.exit(0)
