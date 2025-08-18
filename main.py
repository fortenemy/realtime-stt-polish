#!/usr/bin/env python3
"""
Real-time Speech-to-Text dla języka polskiego
Real-time Speech-to-Text for Polish language

Główna aplikacja / Main application

Autor: AI Assistant
Data: 2025-01-18
Wersja: 1.0.0
"""

import sys
import os
import argparse
import logging
import signal
from pathlib import Path

# Główny folder projektu
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

# Konfiguracja loggingu
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def signal_handler(signum, frame):
    """Obsługa sygnału przerwania"""
    print("\n👋 Przerwanie przez użytkownika")
    sys.exit(0)

def check_dependencies():
    """Sprawdź dostępność dependencies"""
    missing = []
    
    try:
        import numpy
        logger.info(f"✅ NumPy: {numpy.__version__}")
    except ImportError:
        missing.append("numpy")
    
    try:
        import sounddevice
        logger.info("✅ SoundDevice: OK")
    except ImportError:
        missing.append("sounddevice")
    
    try:
        import whisper
        logger.info("✅ OpenAI Whisper: OK")
    except ImportError:
        logger.warning("⚠️ OpenAI Whisper nie zainstalowany")
        missing.append("openai-whisper")
    
    if missing:
        print("❌ Brakujące dependencies:")
        for dep in missing:
            print(f"   - {dep}")
        print("\n💡 Zainstaluj:")
        print("   python install_whisper_dependencies.py")
        return False
    
    return True

def run_demo_mode():
    """Uruchom tryb demo"""
    print("🎤 Real-time STT - Tryb Demo")
    print("=" * 40)
    
    try:
        from realtime_pipeline import RealtimeSTTPipeline
        
        # Stwórz pipeline
        pipeline = RealtimeSTTPipeline(
            sample_rate=16000,
            enable_stt=True,
            stt_model="base",  # Średni model dla demo
            use_polish_optimization=True,
            min_segment_duration=1.0,
            silence_timeout=2.0
        )
        
        # Callback dla segmentów mowy
        def on_speech_detected(segment):
            print(f"\n🎤 Wykryto mowę ({segment.duration:.1f}s)")
            if segment.transcription:
                print(f"📝 Tekst: '{segment.text}'")
                print(f"🎯 Pewność: {segment.transcription.confidence:.2f}")
                print(f"⏱️ Czas: {segment.transcription.processing_time:.2f}s")
            else:
                print("⚠️ Brak transkrypcji")
        
        pipeline.set_speech_callback(on_speech_detected)
        
        print("\n🚀 Uruchamiam pipeline...")
        if not pipeline.load_stt_model():
            print("❌ Nie można załadować modelu STT")
            return False
        
        print("✅ Pipeline gotowy!")
        print("\n💬 Mów do mikrofonu (Ctrl+C aby zakończyć)")
        print("📊 Statystyki będą wyświetlane na żywo")
        
        with pipeline:
            try:
                while True:
                    import time
                    time.sleep(1)
                    
                    # Wyświetl statystyki co 10 sekund
                    stats = pipeline.get_statistics()
                    if stats['pipeline']['runtime_seconds'] > 0 and \
                       int(stats['pipeline']['runtime_seconds']) % 10 == 0:
                        print(f"\n📊 Statystyki: "
                              f"{stats['pipeline']['total_segments']} segmentów, "
                              f"{stats['pipeline']['runtime_seconds']:.0f}s")
                        
            except KeyboardInterrupt:
                print("\n👋 Zatrzymywanie...")
        
        print("✅ Pipeline zatrzymany")
        return True
        
    except ImportError as e:
        print(f"❌ Brak dependencies: {e}")
        print("💡 Uruchom: python install_whisper_dependencies.py")
        return False
    except Exception as e:
        print(f"❌ Błąd demo: {e}")
        return False

def run_test_mode():
    """Uruchom tryb testowy"""
    print("🧪 Real-time STT - Tryb Testowy")
    print("=" * 40)
    
    try:
        # Uruchom test integracji
        print("🔄 Uruchamiam test kompletnej integracji...")
        
        import subprocess
        result = subprocess.run([
            sys.executable, "test_complete_integration.py"
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("Stderr:", result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Błąd testów: {e}")
        return False

def run_audio_test():
    """Test systemu audio"""
    print("🎵 Test systemu audio")
    print("=" * 30)
    
    try:
        from audio_capture import AudioCapture
        
        capture = AudioCapture()
        capture.list_devices()
        
        print("\n🎤 Test nagrywania (3 sekundy)...")
        print("💬 Powiedz coś...")
        
        capture.start_recording()
        import time
        time.sleep(3)
        capture.stop_recording()
        
        stats = capture.get_statistics()
        print(f"📊 Statystyki: {stats}")
        
        if stats['total_frames'] > 0:
            print("✅ System audio działa!")
            return True
        else:
            print("❌ Brak sygnału audio")
            return False
        
    except Exception as e:
        print(f"❌ Błąd testu audio: {e}")
        return False

def main():
    """Główna funkcja aplikacji"""
    # Obsługa sygnału przerwania
    signal.signal(signal.SIGINT, signal_handler)
    
    parser = argparse.ArgumentParser(
        description="Real-time Speech-to-Text dla języka polskiego"
    )
    parser.add_argument(
        "--mode", 
        choices=["demo", "test", "audio-test"],
        default="demo",
        help="Tryb uruchomienia (default: demo)"
    )
    parser.add_argument(
        "--model",
        choices=["tiny", "base", "small", "medium", "large"],
        default="base",
        help="Model Whisper do użycia (default: base)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Włącz szczegółowe logi"
    )
    parser.add_argument(
        "--no-stt",
        action="store_true", 
        help="Wyłącz STT (tylko audio + VAD)"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.info("🔍 Verbose mode enabled")
    
    print("🎤 Real-time Speech-to-Text - Polski")
    print("=" * 50)
    print(f"📅 Wersja: 1.0.0")
    print(f"🔧 Tryb: {args.mode}")
    print(f"🤖 Model: {args.model}")
    
    # Sprawdź dependencies (poza trybem audio-test)
    if args.mode != "audio-test":
        if not check_dependencies():
            return False
    
    # Uruchom odpowiedni tryb
    if args.mode == "demo":
        success = run_demo_mode()
    elif args.mode == "test":
        success = run_test_mode()
    elif args.mode == "audio-test":
        success = run_audio_test()
    else:
        print(f"❌ Nieznany tryb: {args.mode}")
        return False
    
    if success:
        print("\n🎉 Aplikacja zakończona pomyślnie!")
    else:
        print("\n❌ Aplikacja zakończona z błędami")
    
    return success

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n👋 Przerwane przez użytkownika")
        sys.exit(0)
    except Exception as e:
        logger.error(f"💥 Nieoczekiwany błąd: {e}")
        sys.exit(1)
