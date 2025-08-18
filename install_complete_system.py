#!/usr/bin/env python3
"""
Complete System Installer for Real-time STT Polish
Kompletny installer systemu Real-time STT Polski

Autor: AI Assistant
Data: 2025-01-18
"""

import subprocess
import sys
import os
import platform
import importlib.util
from pathlib import Path

def print_banner():
    """Wyświetl banner instalatora"""
    print("🚀 Real-time Speech-to-Text Polish - Kompletny Installer")
    print("=" * 60)
    print("🎤 Automatyczna instalacja wszystkich komponentów systemu")
    print("🔧 Konfiguracja środowiska dla optymalnej wydajności")
    print()

def check_python_version():
    """Sprawdź wersję Python"""
    print("🐍 Sprawdzanie wersji Python...")
    
    version = sys.version_info
    print(f"   Python {version.major}.{version.minor}.{version.micro}")
    
    if version < (3, 8):
        print("❌ Wymagany Python 3.8 lub nowszy!")
        print("💡 Pobierz najnowszą wersję z https://python.org")
        return False
    elif version < (3, 9):
        print("⚠️ Python 3.9+ zalecany dla lepszej wydajności")
    
    print("✅ Wersja Python OK")
    return True

def install_package(package, description="", quiet=True):
    """Zainstaluj pakiet przez pip"""
    print(f"📦 Instalowanie {package}...")
    if description:
        print(f"   {description}")
    
    try:
        cmd = [sys.executable, "-m", "pip", "install", package, "--upgrade"]
        if quiet:
            cmd.append("--quiet")
        
        subprocess.check_call(cmd)
        print(f"✅ {package} zainstalowany pomyślnie")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Błąd instalacji {package}: {e}")
        return False

def install_basic_dependencies():
    """Zainstaluj podstawowe dependencies"""
    print("\n📦 Instalacja podstawowych bibliotek...")
    
    basic_packages = [
        ("numpy>=1.24.0", "Numerical computing"),
        ("sounddevice>=0.4.6", "Audio input/output"),
        ("scipy>=1.10.0", "Scientific computing"),
        ("colorama>=0.4.6", "Colored terminal output"),
        ("tqdm>=4.65.0", "Progress bars"),
        ("psutil>=5.9.0", "System monitoring"),
        ("webrtcvad>=2.0.10", "Voice Activity Detection"),
        ("pyaudio>=0.2.11", "Audio processing"),
        ("pydub>=0.25.1", "Audio manipulation")
    ]
    
    results = []
    for package, description in basic_packages:
        result = install_package(package, description)
        results.append((package.split(">=")[0], result))
    
    successful = sum(1 for _, success in results if success)
    print(f"\n📊 Podstawowe pakiety: {successful}/{len(results)} zainstalowane")
    
    return successful >= len(results) * 0.8  # 80% success rate

def install_pytorch():
    """Zainstaluj PyTorch z odpowiednią konfiguracją"""
    print("\n🔥 Instalacja PyTorch...")
    
    # Sprawdź czy już zainstalowany
    try:
        import torch
        print(f"✅ PyTorch już zainstalowany: {torch.__version__}")
        if torch.cuda.is_available():
            print(f"🚀 CUDA dostępne: {torch.cuda.get_device_name(0)}")
        return True
    except ImportError:
        pass
    
    # Określ platformę i zainstaluj odpowiednią wersję
    system = platform.system().lower()
    
    if system == "windows":
        print("🪟 Wykryto Windows - sprawdzanie GPU...")
        try:
            result = subprocess.run(["nvidia-smi"], capture_output=True)
            if result.returncode == 0:
                print("🚀 NVIDIA GPU wykryte - instaluję CUDA version")
                torch_cmd = "torch torchaudio --index-url https://download.pytorch.org/whl/cu118"
            else:
                print("💻 Brak NVIDIA GPU - instaluję CPU version")
                torch_cmd = "torch torchaudio --index-url https://download.pytorch.org/whl/cpu"
        except:
            print("💻 Nie można wykryć GPU - instaluję CPU version")
            torch_cmd = "torch torchaudio"
    else:
        print(f"🐧 Wykryto {system} - instaluję uniwersalną wersję")
        torch_cmd = "torch torchaudio"
    
    return install_package(torch_cmd, "Deep learning framework")

def install_whisper():
    """Zainstaluj OpenAI Whisper"""
    print("\n🎤 Instalacja OpenAI Whisper...")
    
    try:
        import whisper
        print(f"✅ Whisper już zainstalowany")
        return True
    except ImportError:
        pass
    
    return install_package("openai-whisper>=20231117", "OpenAI Speech Recognition")

def install_optional_packages():
    """Zainstaluj opcjonalne pakiety"""
    print("\n🔧 Instalacja opcjonalnych pakietów...")
    
    optional_packages = [
        ("python-docx>=0.8.11", "Microsoft Word export"),
        ("matplotlib>=3.5.0", "Plotting and visualization"),
        ("librosa>=0.9.0", "Advanced audio processing"),
        ("pytest>=7.0.0", "Testing framework"),
        ("black>=23.0.0", "Code formatting"),
        ("flake8>=6.0.0", "Code linting")
    ]
    
    results = []
    for package, description in optional_packages:
        result = install_package(package, description)
        results.append((package.split(">=")[0], result))
    
    successful = sum(1 for _, success in results if success)
    print(f"\n📊 Opcjonalne pakiety: {successful}/{len(results)} zainstalowane")
    
    return True  # Optional packages nie blokują instalacji

def test_installation():
    """Przetestuj instalację"""
    print("\n🧪 Testowanie instalacji...")
    
    # Test podstawowych importów
    tests = [
        ("numpy", "NumPy"),
        ("sounddevice", "SoundDevice"),
        ("scipy", "SciPy"),
        ("colorama", "Colorama"),
        ("psutil", "Psutil"),
        ("torch", "PyTorch"),
        ("whisper", "OpenAI Whisper")
    ]
    
    results = []
    for module, name in tests:
        try:
            __import__(module)
            print(f"✅ {name} - OK")
            results.append(True)
        except ImportError:
            print(f"⚠️ {name} - Not available")
            results.append(False)
    
    # Test naszych modułów
    print("\n🔧 Testowanie modułów systemu...")
    
    # Dodaj src do ścieżki
    sys.path.insert(0, str(Path(__file__).parent / "src"))
    
    our_modules = [
        ("audio_capture", "AudioCapture"),
        ("voice_activity_detector", "Voice Activity Detection"),
        ("stt_engine", "STT Engine"),
        ("realtime_pipeline", "RealtimePipeline"),
        ("performance_optimizer", "Performance Optimizer"),
        ("export_manager", "Export Manager"),
        ("gui_application", "GUI Application")
    ]
    
    for module, name in our_modules:
        try:
            __import__(module)
            print(f"✅ {name} - OK")
            results.append(True)
        except ImportError as e:
            print(f"❌ {name} - Error: {e}")
            results.append(False)
    
    success_rate = sum(results) / len(results)
    print(f"\n📊 Sukces testów: {success_rate:.1%}")
    
    return success_rate >= 0.8

def download_whisper_model():
    """Pobierz domyślny model Whisper"""
    print("\n📥 Pobieranie modelu Whisper...")
    
    try:
        import whisper
        
        print("📦 Pobieranie modelu 'base' (może potrwać kilka minut)...")
        model = whisper.load_model("base")
        print("✅ Model 'base' pobrany pomyślnie")
        
        # Test modelu
        print("🧪 Test modelu...")
        import numpy as np
        
        # Test z ciszą
        audio = np.zeros(16000, dtype=np.float32)
        result = model.transcribe(audio, language="pl")
        print(f"✅ Test modelu zakończony: '{result['text']}'")
        
        return True
        
    except Exception as e:
        print(f"❌ Błąd pobierania modelu: {e}")
        return False

def create_desktop_shortcuts():
    """Stwórz skróty na pulpicie"""
    print("\n🖥️ Tworzenie skrótów...")
    
    try:
        desktop_path = Path.home() / "Desktop"
        if not desktop_path.exists():
            desktop_path = Path.home() / "Pulpit"  # Polish Windows
        
        if desktop_path.exists():
            # Skrót do GUI
            gui_script = f"""@echo off
cd /d "{Path(__file__).parent}"
python gui_launcher.py
pause"""
            
            gui_shortcut = desktop_path / "Real-time STT GUI.bat"
            with open(gui_shortcut, 'w', encoding='utf-8') as f:
                f.write(gui_script)
            
            # Skrót do CLI
            cli_script = f"""@echo off
cd /d "{Path(__file__).parent}"
python main.py --mode demo
pause"""
            
            cli_shortcut = desktop_path / "Real-time STT Demo.bat"
            with open(cli_shortcut, 'w', encoding='utf-8') as f:
                f.write(cli_script)
            
            print("✅ Skróty utworzone na pulpicie")
            return True
        else:
            print("⚠️ Nie można znaleźć pulpitu")
            return False
            
    except Exception as e:
        print(f"❌ Błąd tworzenia skrótów: {e}")
        return False

def create_start_scripts():
    """Stwórz skrypty startowe"""
    print("\n📝 Tworzenie skrytów startowych...")
    
    try:
        # Główny skrypt startowy
        start_script = """@echo off
title Real-time Speech-to-Text Polish
echo.
echo 🎤 Real-time Speech-to-Text Polish
echo ================================
echo.
echo Wybierz opcję:
echo 1. GUI Application
echo 2. Command Line Demo
echo 3. Audio Test
echo 4. Complete System Test
echo 5. Install Whisper Dependencies
echo.
set /p choice="Wybór (1-5): "

if "%choice%"=="1" (
    python gui_launcher.py
) else if "%choice%"=="2" (
    python main.py --mode demo
) else if "%choice%"=="3" (
    python main.py --mode audio-test
) else if "%choice%"=="4" (
    python test_complete_system.py
) else if "%choice%"=="5" (
    python install_whisper_dependencies.py
) else (
    echo Nieprawidłowy wybór
)

pause"""
        
        with open("start.bat", 'w', encoding='utf-8') as f:
            f.write(start_script)
        
        print("✅ Skrypt start.bat utworzony")
        return True
        
    except Exception as e:
        print(f"❌ Błąd tworzenia skryptów: {e}")
        return False

def show_installation_summary():
    """Pokaż podsumowanie instalacji"""
    print("\n" + "=" * 60)
    print("🎉 INSTALACJA ZAKOŃCZONA!")
    print("=" * 60)
    
    print("\n🚀 Real-time Speech-to-Text Polish jest gotowy!")
    
    print("\n📋 Dostępne opcje uruchomienia:")
    print("   🎨 GUI:           python gui_launcher.py")
    print("   🎤 Demo CLI:      python main.py --mode demo")
    print("   🧪 Test audio:    python main.py --mode audio-test")
    print("   📊 Test systemu:  python test_complete_system.py")
    print("   ⚙️ Łatwy start:   start.bat")
    
    print("\n💡 Pierwsze uruchomienie:")
    print("   1. Uruchom test systemu: python test_complete_system.py")
    print("   2. Jeśli wszystko OK, uruchom GUI: python gui_launcher.py")
    print("   3. Lub demo CLI: python main.py --mode demo")
    
    print("\n🎯 Funkcjonalności:")
    print("   ✅ Real-time transkrypcja z mikrofonu")
    print("   ✅ Zaawansowana detekcja aktywności głosowej")
    print("   ✅ Optymalizacje dla języka polskiego")
    print("   ✅ Eksport do wielu formatów (TXT, JSON, SRT, etc.)")
    print("   ✅ Monitoring wydajności systemu")
    print("   ✅ Graficzny interfejs użytkownika")
    
    print("\n📖 Dokumentacja:")
    print("   README.md - Główna dokumentacja (EN)")
    print("   docs/README_PL.md - Dokumentacja polska")
    print("   logs/ - Logi rozwoju projektu")
    
    print("\n🆘 Pomoc:")
    print("   - Jeśli masz problemy, uruchom: python test_complete_system.py")
    print("   - Sprawdź logi w folderze logs/")
    print("   - GitHub: https://github.com/fortenemy/realtime-stt-polish")

def main():
    """Główna funkcja instalatora"""
    print_banner()
    
    # Sprawdź Python
    if not check_python_version():
        input("Press Enter to exit...")
        return False
    
    print("\n🚀 Rozpoczynam instalację systemu...")
    print("⏱️ To może potrwać 5-15 minut (zależy od połączenia)")
    
    # Pytaj o zgodę
    response = input("\nKontynuować pełną instalację? (y/N): ").lower()
    if response != 'y':
        print("❌ Instalacja anulowana")
        return False
    
    # Kroki instalacji
    steps = [
        ("Podstawowe biblioteki", install_basic_dependencies),
        ("PyTorch", install_pytorch),
        ("OpenAI Whisper", install_whisper),
        ("Opcjonalne pakiety", install_optional_packages),
        ("Test instalacji", test_installation),
        ("Model Whisper", download_whisper_model),
        ("Skróty pulpitu", create_desktop_shortcuts),
        ("Skrypty startowe", create_start_scripts)
    ]
    
    results = []
    for step_name, step_func in steps:
        print(f"\n🔄 {step_name}...")
        try:
            result = step_func()
            results.append((step_name, result))
            
            if result:
                print(f"✅ {step_name} - zakończone pomyślnie")
            else:
                print(f"⚠️ {step_name} - problemy (nie krytyczne)")
                
        except Exception as e:
            print(f"💥 {step_name} - błąd: {e}")
            results.append((step_name, False))
    
    # Podsumowanie
    successful = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"\n📊 Instalacja: {successful}/{total} kroków zakończonych sukcesem")
    
    if successful >= total - 2:  # Allow 2 failures
        show_installation_summary()
        return True
    else:
        print("\n⚠️ Instalacja częściowo nieudana")
        print("🔧 Sprawdź błędy powyżej i spróbuj ponownie")
        
        print("\n💡 Możesz też zainstalować ręcznie:")
        print("   pip install -r requirements.txt")
        print("   python install_whisper_dependencies.py")
        
        return False

if __name__ == "__main__":
    try:
        success = main()
        input(f"\nPress Enter to exit...")
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n👋 Instalacja przerwana przez użytkownika")
        sys.exit(0)
