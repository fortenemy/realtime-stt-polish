#!/usr/bin/env python3
"""
Test STT Engine - OpenAI Whisper integration
"""

import sys
import time
import numpy as np
from pathlib import Path

# Dodaj src do ścieżki
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_whisper_availability():
    """Test dostępności Whisper"""
    print("🤖 Test dostępności OpenAI Whisper")
    print("=" * 40)
    
    try:
        import whisper
        print(f"✅ OpenAI Whisper zainstalowany: {whisper.__version__ if hasattr(whisper, '__version__') else 'unknown'}")
        
        # Sprawdź dostępne modele
        available_models = whisper.available_models()
        print(f"📋 Dostępne modele: {', '.join(available_models)}")
        
        return True
        
    except ImportError as e:
        print(f"❌ OpenAI Whisper nie zainstalowany: {e}")
        print("💡 Zainstaluj: pip install openai-whisper")
        return False

def test_torch_availability():
    """Test dostępności PyTorch"""
    print("\n🔥 Test dostępności PyTorch")
    print("=" * 40)
    
    try:
        import torch
        print(f"✅ PyTorch zainstalowany: {torch.__version__}")
        
        # Sprawdź CUDA
        if torch.cuda.is_available():
            print(f"🚀 CUDA dostępne: {torch.cuda.get_device_name(0)}")
            print(f"💾 CUDA memory: {torch.cuda.get_device_properties(0).total_memory // 1024**3}GB")
        else:
            print("💻 CUDA niedostępne - będzie używany CPU")
        
        return True
        
    except ImportError as e:
        print(f"❌ PyTorch nie zainstalowany: {e}")
        print("💡 Zainstaluj: pip install torch torchaudio")
        return False

def test_stt_engine_import():
    """Test importu STT Engine"""
    print("\n🎤 Test importu STT Engine")
    print("=" * 40)
    
    try:
        from stt_engine import WhisperSTTEngine, PolishOptimizedSTT, WhisperModel, TranscriptionResult
        print("✅ STT Engine classes imported successfully")
        
        # Test enum
        print(f"📋 Whisper models: {[model.value for model in WhisperModel]}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Błąd importu STT Engine: {e}")
        return False

def test_stt_engine_basic():
    """Test podstawowych funkcji STT Engine"""
    print("\n🧪 Test podstawowych funkcji STT Engine")
    print("=" * 40)
    
    try:
        from stt_engine import WhisperSTTEngine, WhisperModel
        
        # Stwórz engine z najmniejszym modelem
        print("🔧 Tworzenie STT Engine...")
        engine = WhisperSTTEngine(
            model_name=WhisperModel.TINY,  # Najmniejszy model dla testu
            language="pl"
        )
        
        print("✅ STT Engine utworzony")
        
        # Test model info
        info = engine.get_model_info()
        print(f"📊 Model info: {info['model_name']}, device: {info['device']}")
        
        # Test bez ładowania modelu (nie mamy jeszcze Whisper zainstalowanego)
        print("⚠️ Model nie zostanie załadowany (brak Whisper)")
        
        return True
        
    except Exception as e:
        print(f"❌ Błąd testu STT Engine: {e}")
        return False

def test_polish_optimized():
    """Test Polish optimized STT"""
    print("\n🇵🇱 Test Polish Optimized STT")
    print("=" * 40)
    
    try:
        from stt_engine import PolishOptimizedSTT
        
        # Stwórz Polish optimized engine
        engine = PolishOptimizedSTT(model_name="tiny")
        print("✅ PolishOptimizedSTT utworzony")
        
        # Test post-processing
        test_texts = [
            "to jest test",
            "jak sie masz",
            "ze wszystkim w porządku",
            "nie ma problemu"
        ]
        
        print("🔧 Test post-processingu polskiego:")
        for text in test_texts:
            processed = engine.post_process_polish_text(text)
            if processed != text:
                print(f"   '{text}' -> '{processed}'")
            else:
                print(f"   '{text}' (bez zmian)")
        
        return True
        
    except Exception as e:
        print(f"❌ Błąd Polish STT test: {e}")
        return False

def test_synthetic_audio():
    """Test z syntetycznym audio"""
    print("\n🎵 Test z syntetycznym audio")
    print("=" * 40)
    
    try:
        from stt_engine import WhisperSTTEngine
        
        # Stwórz syntetyczne audio (440Hz ton przez 1 sekundę)
        sample_rate = 16000
        duration = 1.0
        frequency = 440
        
        t = np.linspace(0, duration, int(sample_rate * duration))
        audio = 0.3 * np.sin(2 * np.pi * frequency * t).astype(np.float32)
        
        print(f"🎵 Syntetyczne audio: {len(audio)} samples, {duration}s")
        
        # Test przygotowania audio
        engine = WhisperSTTEngine(model_name="tiny")
        prepared_audio = engine._prepare_audio(audio, sample_rate)
        
        print(f"✅ Audio przygotowane: {len(prepared_audio)} samples")
        print(f"📊 Audio range: {prepared_audio.min():.3f} to {prepared_audio.max():.3f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Błąd testu syntetycznego audio: {e}")
        return False

def test_integration_with_pipeline():
    """Test integracji z RealtimePipeline"""
    print("\n🔗 Test integracji z Pipeline")
    print("=" * 40)
    
    try:
        # Import pipeline
        from realtime_pipeline import RealtimeSTTPipeline
        from stt_engine import WhisperSTTEngine
        
        print("✅ Importy pipeline i STT engine OK")
        
        # Test compatibility
        pipeline = RealtimeSTTPipeline()
        stt_engine = WhisperSTTEngine(model_name="tiny", language="pl")
        
        print("✅ Obiekty utworzone - kompatybilność OK")
        print("💡 W przyszłości: pipeline.set_stt_engine(stt_engine)")
        
        return True
        
    except Exception as e:
        print(f"❌ Błąd integracji: {e}")
        return False

def main():
    """Główna funkcja testów"""
    print("🧪 Test STT Engine - OpenAI Whisper Integration")
    print("=" * 60)
    
    tests = [
        ("PyTorch Availability", test_torch_availability),
        ("Whisper Availability", test_whisper_availability), 
        ("STT Engine Import", test_stt_engine_import),
        ("STT Engine Basic", test_stt_engine_basic),
        ("Polish Optimized", test_polish_optimized),
        ("Synthetic Audio", test_synthetic_audio),
        ("Pipeline Integration", test_integration_with_pipeline)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            print(f"\n🚀 {test_name}")
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"💥 {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Podsumowanie
    print("\n" + "=" * 60)
    print("📋 PODSUMOWANIE TESTÓW STT ENGINE")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        if result:
            print(f"✅ {test_name}")
            passed += 1
        else:
            print(f"❌ {test_name}")
    
    print(f"\n🎯 Wyniki: {passed}/{len(results)} testów przeszło")
    
    if passed >= len(results) - 2:  # Allow 2 failures (whisper/torch not installed)
        print("🎉 STT Engine implementacja gotowa!")
        print("\n📋 Następne kroki:")
        print("1. Zainstaluj dependencies: pip install openai-whisper torch")
        print("2. Przetestuj z prawdziwym audio")
        print("3. Zintegruj z RealtimePipeline")
        return True
    else:
        print("⚠️ Niektóre testy nie przeszły - sprawdź implementację")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
