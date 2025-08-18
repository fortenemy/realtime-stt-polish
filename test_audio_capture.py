#!/usr/bin/env python3
"""
Test modułu AudioCapture
Audio Capture Module Test

Autor: AI Assistant
Data: 2025-01-18
"""

import sys
import time
import numpy as np
from pathlib import Path

# Dodaj src do ścieżki
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from audio_capture import AudioCapture
    import sounddevice as sd
    from colorama import init, Fore, Style
    init()  # Inicjalizacja colorama dla Windows
except ImportError as e:
    print(f"❌ Błąd importu: {e}")
    print("💡 Uruchom: python install_dependencies.py")
    sys.exit(1)

def test_audio_devices():
    """Test dostępnych urządzeń audio"""
    print(f"{Fore.CYAN}📱 Test urządzeń audio{Style.RESET_ALL}")
    print("=" * 50)
    
    try:
        devices = sd.query_devices()
        print(f"Znaleziono {len(devices)} urządzeń audio:")
        
        for i, device in enumerate(devices):
            device_type = "🎤" if device['max_input_channels'] > 0 else "🔊"
            print(f"{device_type} [{i}] {device['name']} - {device['max_input_channels']}ch in, {device['max_output_channels']}ch out")
        
        # Sprawdź domyślne urządzenia
        default_input = sd.default.device[0]
        default_output = sd.default.device[1]
        
        print(f"\n🎤 Domyślne wejście: {default_input}")
        print(f"🔊 Domyślne wyjście: {default_output}")
        
        return True
        
    except Exception as e:
        print(f"❌ Błąd testu urządzeń: {e}")
        return False

def test_audio_capture_basic():
    """Podstawowy test AudioCapture"""
    print(f"\n{Fore.GREEN}🎤 Test podstawowy AudioCapture{Style.RESET_ALL}")
    print("=" * 50)
    
    try:
        # Stwórz obiekt AudioCapture
        capture = AudioCapture(
            sample_rate=16000,
            chunk_size=1024,
            buffer_size=10
        )
        
        print("✅ AudioCapture utworzony pomyślnie")
        
        # Wyświetl statystyki początkowe
        stats = capture.get_statistics()
        print(f"📊 Statystyki początkowe: {stats}")
        
        return True
        
    except Exception as e:
        print(f"❌ Błąd testu podstawowego: {e}")
        return False

def test_audio_recording():
    """Test nagrywania audio"""
    print(f"\n{Fore.YELLOW}🎙️ Test nagrywania audio{Style.RESET_ALL}")
    print("=" * 50)
    
    try:
        capture = AudioCapture(
            sample_rate=16000,
            chunk_size=1024,
            buffer_size=50
        )
        
        print("🎤 Rozpoczynam nagrywanie na 3 sekundy...")
        print("💬 Powiedz coś do mikrofonu!")
        
        # Rozpocznij nagrywanie
        capture.start_recording()
        
        # Zbieraj audio przez 3 sekundy
        start_time = time.time()
        audio_levels = []
        chunks_received = 0
        
        while time.time() - start_time < 3.0:
            chunk = capture.get_audio_chunk(timeout=0.1)
            if chunk is not None:
                chunks_received += 1
                # Oblicz poziom audio
                level = capture.get_audio_level(chunk.flatten())
                audio_levels.append(level)
                
                # Wyświetl prosty wskaźnik poziomu
                if level > -40:  # Próg dla wykrycia dźwięku
                    print("🔊", end="", flush=True)
                else:
                    print(".", end="", flush=True)
        
        print()  # Nowa linia
        
        # Zatrzymaj nagrywanie
        capture.stop_recording()
        
        # Wyświetl statystyki
        stats = capture.get_statistics()
        print(f"\n📊 Statystyki nagrywania:")
        print(f"   • Czas trwania: {stats['duration_seconds']:.2f}s")
        print(f"   • Całkowite ramki: {stats['total_frames']}")
        print(f"   • Pominięte ramki: {stats['dropped_frames']}")
        print(f"   • Współczynnik strat: {stats['drop_rate']:.2%}")
        print(f"   • Chunks otrzymane: {chunks_received}")
        
        if audio_levels:
            avg_level = np.mean([l for l in audio_levels if l > -np.inf])
            max_level = max([l for l in audio_levels if l > -np.inf], default=-np.inf)
            print(f"   • Średni poziom audio: {avg_level:.1f} dB")
            print(f"   • Maksymalny poziom: {max_level:.1f} dB")
        
        if chunks_received > 0:
            print("✅ Test nagrywania zakończony pomyślnie!")
            return True
        else:
            print("⚠️ Nie otrzymano żadnych chunków audio")
            return False
            
    except Exception as e:
        print(f"❌ Błąd testu nagrywania: {e}")
        return False

def test_audio_buffer_management():
    """Test zarządzania buforem"""
    print(f"\n{Fore.MAGENTA}🗂️ Test zarządzania buforem{Style.RESET_ALL}")
    print("=" * 50)
    
    try:
        # Mały bufor do testowania przepełnienia
        capture = AudioCapture(
            sample_rate=16000,
            chunk_size=512,
            buffer_size=5  # Mały bufor
        )
        
        capture.start_recording()
        
        # Pozwól buforowi się zapełnić
        time.sleep(1.0)
        
        # Sprawdź statystyki
        stats = capture.get_statistics()
        print(f"📊 Statystyki bufora:")
        print(f"   • Rozmiar kolejki: {stats['queue_size']}")
        print(f"   • Pominięte ramki: {stats['dropped_frames']}")
        
        # Wyczyść bufor
        capture.clear_buffer()
        
        time.sleep(0.5)
        stats_after_clear = capture.get_statistics()
        print(f"   • Rozmiar kolejki po czyszczeniu: {stats_after_clear['queue_size']}")
        
        capture.stop_recording()
        
        print("✅ Test zarządzania buforem zakończony!")
        return True
        
    except Exception as e:
        print(f"❌ Błąd testu bufora: {e}")
        return False

def main():
    """Główna funkcja testów"""
    print(f"{Fore.CYAN}🧪 Test AudioCapture - Real-time STT{Style.RESET_ALL}")
    print("=" * 60)
    
    tests = [
        ("Urządzenia Audio", test_audio_devices),
        ("AudioCapture Basic", test_audio_capture_basic),
        ("Nagrywanie Audio", test_audio_recording),
        ("Zarządzanie Buforem", test_audio_buffer_management)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            print(f"\n🚀 Uruchamiam: {test_name}")
            result = test_func()
            results.append((test_name, result))
            
            if result:
                print(f"✅ {test_name}: SUKCES")
            else:
                print(f"❌ {test_name}: NIEPOWODZENIE")
                
        except KeyboardInterrupt:
            print(f"\n⏹️ Test przerwany przez użytkownika")
            break
        except Exception as e:
            print(f"💥 {test_name}: BŁĄD - {e}")
            results.append((test_name, False))
    
    # Podsumowanie
    print(f"\n{Fore.CYAN}📋 PODSUMOWANIE TESTÓW{Style.RESET_ALL}")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = f"{Fore.GREEN}✅ PASS" if result else f"{Fore.RED}❌ FAIL"
        print(f"{status}{Style.RESET_ALL} {test_name}")
    
    print(f"\n🎯 Wyniki: {passed}/{total} testów zakończonych sukcesem")
    
    if passed == total:
        print(f"{Fore.GREEN}🎉 Wszystkie testy przeszły! AudioCapture gotowy!{Style.RESET_ALL}")
        return True
    else:
        print(f"{Fore.YELLOW}⚠️ Niektóre testy nie poszły. Sprawdź konfigurację.{Style.RESET_ALL}")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}👋 Test przerwany przez użytkownika{Style.RESET_ALL}")
        sys.exit(0)
