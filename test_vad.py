#!/usr/bin/env python3
"""
Test Voice Activity Detection
"""

import sys
import time
import numpy as np
from pathlib import Path

# Dodaj src do ścieżki
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_simple_vad():
    """Test SimpleVAD"""
    print("🎙️ Test Simple VAD")
    print("=" * 40)
    
    try:
        from voice_activity_detector import SimpleVAD
        
        # Stwórz VAD
        vad = SimpleVAD(
            sample_rate=16000,
            energy_threshold=0.01,
            min_speech_frames=2,
            min_silence_frames=3
        )
        
        print("✅ SimpleVAD utworzony")
        
        # Test z ciszą (zero)
        silence = np.zeros(1024)
        is_speech, analysis = vad.process_chunk(silence)
        print(f"🔇 Cisza: {is_speech} (energy: {analysis['energy']:.4f})")
        
        # Test z szumem (noise)
        noise = np.random.normal(0, 0.1, 1024)
        is_speech, analysis = vad.process_chunk(noise)
        print(f"📢 Szum: {is_speech} (energy: {analysis['energy']:.4f})")
        
        # Test z tonem (symulacja mowy)
        t = np.linspace(0, 1024/16000, 1024)
        tone = 0.3 * np.sin(2 * np.pi * 440 * t)  # Ton 440Hz
        is_speech, analysis = vad.process_chunk(tone)
        print(f"🎵 Ton: {is_speech} (energy: {analysis['energy']:.4f})")
        
        # Test ciągu ramek
        print("\n🔄 Test ciągu ramek:")
        for i in range(10):
            if i < 3:
                frame = np.zeros(1024)  # Cisza
                label = "🔇"
            elif i < 7:
                frame = 0.2 * np.random.normal(0, 1, 1024)  # "Mowa"
                label = "🎤"
            else:
                frame = np.zeros(1024)  # Cisza
                label = "🔇"
            
            is_speech, analysis = vad.process_chunk(frame)
            print(f"{label} Frame {i}: {is_speech} (speech_frames: {analysis['speech_frames']})")
        
        # Statystyki
        stats = vad.get_statistics()
        print(f"\n📊 Statystyki VAD: {stats}")
        
        return True
        
    except Exception as e:
        print(f"❌ Błąd SimpleVAD: {e}")
        return False

def test_webrtc_vad():
    """Test WebRTC VAD"""
    print("\n🌐 Test WebRTC VAD")
    print("=" * 40)
    
    try:
        from voice_activity_detector import WebRTCVAD, VADMode
        
        # Test z różnymi trybami
        for mode in [VADMode.PERMISSIVE, VADMode.NORMAL, VADMode.AGGRESSIVE]:
            print(f"\n🎚️ Test mode: {mode.name}")
            
            vad = WebRTCVAD(sample_rate=16000, mode=mode)
            
            # Test ramek
            silence = np.zeros(480)  # 30ms @ 16kHz
            noise = np.random.normal(0, 0.1, 480)
            tone = 0.3 * np.sin(2 * np.pi * 440 * np.linspace(0, 0.03, 480))
            
            print(f"   🔇 Cisza: {vad.is_speech(silence)}")
            print(f"   📢 Szum: {vad.is_speech(noise)}")
            print(f"   🎵 Ton: {vad.is_speech(tone)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Błąd WebRTC VAD: {e}")
        return False

def test_vad_with_audio_capture():
    """Test VAD z AudioCapture"""
    print("\n🎤 Test VAD + AudioCapture")
    print("=" * 40)
    
    try:
        # Test importów
        from voice_activity_detector import SimpleVAD
        from audio_capture import AudioCapture
        
        print("✅ Importy OK")
        
        # Stwórz obiekty
        vad = SimpleVAD(sample_rate=16000)
        capture = AudioCapture(sample_rate=16000, chunk_size=1024)
        
        print("✅ Obiekty utworzone")
        print("💡 W rzeczywistym użyciu:")
        print("   1. capture.start_recording()")
        print("   2. chunk = capture.get_audio_chunk()")
        print("   3. is_speech, analysis = vad.process_chunk(chunk)")
        print("   4. if is_speech: process_for_STT(chunk)")
        
        return True
        
    except Exception as e:
        print(f"❌ Błąd integracji: {e}")
        return False

def main():
    """Główna funkcja testów"""
    print("🧪 Test Voice Activity Detection")
    print("=" * 50)
    
    tests = [
        ("Simple VAD", test_simple_vad),
        ("WebRTC VAD", test_webrtc_vad),
        ("VAD + AudioCapture", test_vad_with_audio_capture)
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
    print("\n📋 PODSUMOWANIE")
    print("=" * 30)
    
    passed = 0
    for test_name, result in results:
        if result:
            print(f"✅ {test_name}")
            passed += 1
        else:
            print(f"❌ {test_name}")
    
    print(f"\n🎯 Wyniki: {passed}/{len(results)} testów OK")
    
    if passed == len(results):
        print("🎉 VAD gotowy do użycia!")
        return True
    else:
        print("⚠️ Niektóre testy nie przeszły")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
