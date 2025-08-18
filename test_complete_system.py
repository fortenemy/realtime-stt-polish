#!/usr/bin/env python3
"""
Kompletny test systemu Real-time STT Polish
Complete system test for Real-time STT Polish

Autor: AI Assistant
Data: 2025-01-18
"""

import sys
import time
import tempfile
import json
from pathlib import Path
from typing import List, Dict, Any

# Dodaj src do ścieżki
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_all_components():
    """Test wszystkich komponentów systemu"""
    print("🧪 Test wszystkich komponentów")
    print("=" * 50)
    
    components_results = {}
    
    # Test AudioCapture
    try:
        from audio_capture import AudioCapture
        capture = AudioCapture()
        components_results["AudioCapture"] = True
        print("✅ AudioCapture - OK")
    except Exception as e:
        components_results["AudioCapture"] = False
        print(f"❌ AudioCapture - {e}")
    
    # Test VAD
    try:
        from voice_activity_detector import SimpleVAD, WebRTCVAD, VADMode
        vad = SimpleVAD()
        components_results["VAD"] = True
        print("✅ Voice Activity Detection - OK")
    except Exception as e:
        components_results["VAD"] = False
        print(f"❌ VAD - {e}")
    
    # Test STT Engine
    try:
        from stt_engine import WhisperSTTEngine, PolishOptimizedSTT
        # Nie ładuj modelu, tylko test klasy
        engine = WhisperSTTEngine(model_name="tiny")
        components_results["STT_Engine"] = True
        print("✅ STT Engine - OK")
    except Exception as e:
        components_results["STT_Engine"] = False
        print(f"❌ STT Engine - {e}")
    
    # Test Pipeline
    try:
        from realtime_pipeline import RealtimeSTTPipeline, SpeechSegment
        pipeline = RealtimeSTTPipeline(enable_stt=False)  # Bez STT dla testu
        components_results["Pipeline"] = True
        print("✅ RealtimePipeline - OK")
    except Exception as e:
        components_results["Pipeline"] = False
        print(f"❌ Pipeline - {e}")
    
    # Test Performance Optimizer
    try:
        from performance_optimizer import PerformanceOptimizer, MemoryManager
        optimizer = PerformanceOptimizer(enable_monitoring=False)
        components_results["Performance"] = True
        print("✅ Performance Optimizer - OK")
    except Exception as e:
        components_results["Performance"] = False
        print(f"❌ Performance Optimizer - {e}")
    
    # Test Export Manager
    try:
        from export_manager import ExportManager
        exporter = ExportManager()
        components_results["Export"] = True
        print("✅ Export Manager - OK")
    except Exception as e:
        components_results["Export"] = False
        print(f"❌ Export Manager - {e}")
    
    # Test GUI Application
    try:
        from gui_application import STTGuiApplication
        # Nie tworzymy instancji GUI w teście
        components_results["GUI"] = True
        print("✅ GUI Application - OK")
    except Exception as e:
        components_results["GUI"] = False
        print(f"❌ GUI Application - {e}")
    
    return components_results

def test_export_functionality():
    """Test funkcjonalności eksportu"""
    print("\n📤 Test funkcjonalności eksportu")
    print("=" * 40)
    
    try:
        from export_manager import ExportManager
        from realtime_pipeline import SpeechSegment
        from stt_engine import TranscriptionResult
        
        # Stwórz testowe segmenty
        test_segments = []
        
        for i in range(3):
            # Stwórz fake transcription
            transcription = TranscriptionResult(
                text=f"To jest testowy segment numer {i+1}.",
                language="pl",
                confidence=0.95 - i*0.1,
                processing_time=0.1 + i*0.05,
                segments=[],
                model_used="test"
            )
            
            # Stwórz segment
            segment = SpeechSegment(
                audio_data=None,  # Nie potrzebujemy audio dla testu eksportu
                start_time=float(i * 3),
                end_time=float(i * 3 + 2),
                confidence=0.95,
                sample_rate=16000,
                transcription=transcription
            )
            
            test_segments.append(segment)
        
        # Test eksportu
        exporter = ExportManager()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Test różnych formatów
            formats_to_test = ["txt", "json", "csv", "srt", "vtt", "xml"]
            results = {}
            
            for fmt in formats_to_test:
                output_file = temp_path / f"test.{fmt}"
                success = exporter.export_transcription(
                    test_segments, str(output_file), fmt
                )
                results[fmt] = success
                
                if success:
                    # Sprawdź czy plik został utworzony
                    if output_file.exists() and output_file.stat().st_size > 0:
                        print(f"✅ Export {fmt} - OK ({output_file.stat().st_size} bytes)")
                    else:
                        print(f"❌ Export {fmt} - plik pusty")
                        results[fmt] = False
                else:
                    print(f"❌ Export {fmt} - błąd")
            
            # Test batch export
            batch_results = exporter.batch_export(
                test_segments, str(temp_path), ["txt", "json", "csv"]
            )
            
            print(f"📦 Batch export: {sum(batch_results.values())}/{len(batch_results)} formatów")
            
            return all(results.values())
        
    except Exception as e:
        print(f"❌ Export test failed: {e}")
        return False

def test_performance_monitoring():
    """Test monitoringu wydajności"""
    print("\n📊 Test monitoringu wydajności")
    print("=" * 40)
    
    try:
        from performance_optimizer import PerformanceOptimizer
        
        optimizer = PerformanceOptimizer(
            enable_monitoring=True,
            monitoring_interval=0.1  # Szybki test
        )
        
        # Uruchom monitoring na krótko
        optimizer.start_monitoring()
        time.sleep(0.5)  # Pół sekundy monitoringu
        
        # Sprawdź metryki
        current_metrics = optimizer.get_current_metrics()
        if current_metrics:
            print(f"✅ CPU: {current_metrics.cpu_percent:.1f}%")
            print(f"✅ Memory: {current_metrics.memory_percent:.1f}%")
            print(f"✅ Threads: {current_metrics.active_threads}")
            
            # Test rekomendacji
            recommendations = optimizer.get_optimization_recommendations()
            print(f"✅ Recommendations: {len(recommendations)} items")
            
            # Test raportu
            report = optimizer.generate_performance_report()
            print(f"✅ Performance report generated")
            
        optimizer.stop_monitoring()
        
        return current_metrics is not None
        
    except Exception as e:
        print(f"❌ Performance monitoring test failed: {e}")
        return False

def test_configuration_system():
    """Test systemu konfiguracji"""
    print("\n⚙️ Test systemu konfiguracji")
    print("=" * 40)
    
    try:
        # Test konfiguracji main aplikacji
        test_config = {
            "model": "base",
            "language": "pl",
            "vad_mode": "normal",
            "min_segment_duration": 1.0,
            "silence_timeout": 2.0,
            "enable_stt": True,
            "use_polish_optimization": True
        }
        
        # Test zapisu i odczytu
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_config, f)
            config_path = f.name
        
        # Odczytaj konfigurację
        with open(config_path, 'r') as f:
            loaded_config = json.load(f)
        
        # Sprawdź czy konfiguracja jest identyczna
        if loaded_config == test_config:
            print("✅ Configuration save/load - OK")
            
            # Test walidacji konfiguracji
            required_keys = ["model", "language", "vad_mode"]
            valid_config = all(key in loaded_config for key in required_keys)
            
            if valid_config:
                print("✅ Configuration validation - OK")
                return True
            else:
                print("❌ Configuration validation - missing keys")
                return False
        else:
            print("❌ Configuration save/load - mismatch")
            return False
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False
    finally:
        # Cleanup
        try:
            Path(config_path).unlink()
        except:
            pass

def test_integration_readiness():
    """Test gotowości do pełnej integracji"""
    print("\n🔗 Test gotowości integracji")
    print("=" * 40)
    
    integration_checks = []
    
    # Check 1: Wszystkie moduły importowalne
    try:
        modules = [
            "audio_capture", "voice_activity_detector", "stt_engine",
            "realtime_pipeline", "performance_optimizer", "export_manager",
            "gui_application"
        ]
        
        for module in modules:
            __import__(module)
        
        print("✅ All modules importable")
        integration_checks.append(True)
    except Exception as e:
        print(f"❌ Module import failed: {e}")
        integration_checks.append(False)
    
    # Check 2: Pipeline może być utworzony
    try:
        from realtime_pipeline import RealtimeSTTPipeline
        pipeline = RealtimeSTTPipeline(enable_stt=False)
        print("✅ Pipeline creation")
        integration_checks.append(True)
    except Exception as e:
        print(f"❌ Pipeline creation failed: {e}")
        integration_checks.append(False)
    
    # Check 3: Export manager funkcjonalny
    try:
        from export_manager import ExportManager
        exporter = ExportManager()
        formats = exporter.get_supported_formats()
        if len(formats) >= 5:
            print(f"✅ Export manager ({len(formats)} formats)")
            integration_checks.append(True)
        else:
            print(f"❌ Export manager insufficient formats")
            integration_checks.append(False)
    except Exception as e:
        print(f"❌ Export manager failed: {e}")
        integration_checks.append(False)
    
    # Check 4: Performance monitoring
    try:
        from performance_optimizer import PerformanceOptimizer
        optimizer = PerformanceOptimizer(enable_monitoring=False)
        metrics = optimizer.collect_metrics()
        if metrics.cpu_percent >= 0:
            print("✅ Performance monitoring")
            integration_checks.append(True)
        else:
            print("❌ Performance monitoring invalid")
            integration_checks.append(False)
    except Exception as e:
        print(f"❌ Performance monitoring failed: {e}")
        integration_checks.append(False)
    
    success_rate = sum(integration_checks) / len(integration_checks)
    print(f"\n📊 Integration readiness: {success_rate:.1%}")
    
    return success_rate >= 0.8

def test_system_requirements():
    """Test wymagań systemowych"""
    print("\n💻 Test wymagań systemowych")
    print("=" * 40)
    
    requirements_met = []
    
    # Python version
    if sys.version_info >= (3, 8):
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")
        requirements_met.append(True)
    else:
        print(f"❌ Python {sys.version_info.major}.{sys.version_info.minor} (wymagany 3.8+)")
        requirements_met.append(False)
    
    # Required packages
    required_packages = [
        ("numpy", "1.20.0"),
        ("sounddevice", "0.4.0"),
        ("psutil", "5.0.0")
    ]
    
    for package, min_version in required_packages:
        try:
            module = __import__(package)
            version = getattr(module, "__version__", "unknown")
            print(f"✅ {package} {version}")
            requirements_met.append(True)
        except ImportError:
            print(f"❌ {package} missing")
            requirements_met.append(False)
    
    # Optional packages (for full functionality)
    optional_packages = [
        ("whisper", "OpenAI Whisper"),
        ("torch", "PyTorch"),
        ("tkinter", "GUI support")
    ]
    
    print("\n📦 Optional packages:")
    for package, description in optional_packages:
        try:
            __import__(package)
            print(f"✅ {package} ({description})")
        except ImportError:
            print(f"⚠️ {package} missing ({description})")
    
    # System resources
    try:
        import psutil
        memory_gb = psutil.virtual_memory().total / 1024**3
        cpu_count = psutil.cpu_count()
        
        print(f"\n💾 RAM: {memory_gb:.1f}GB")
        print(f"🖥️ CPU cores: {cpu_count}")
        
        if memory_gb >= 4:
            print("✅ Sufficient RAM")
            requirements_met.append(True)
        else:
            print("⚠️ Low RAM (4GB+ recommended)")
            requirements_met.append(False)
        
        if cpu_count >= 2:
            print("✅ Sufficient CPU cores")
            requirements_met.append(True)
        else:
            print("⚠️ Low CPU cores (2+ recommended)")
            requirements_met.append(False)
            
    except Exception as e:
        print(f"❌ System resource check failed: {e}")
        requirements_met.append(False)
    
    return all(requirements_met)

def generate_system_report():
    """Wygeneruj raport systemu"""
    print("\n📋 Generowanie raportu systemu")
    print("=" * 40)
    
    report = {
        "timestamp": time.time(),
        "test_results": {},
        "system_info": {},
        "recommendations": []
    }
    
    # Uruchom wszystkie testy
    tests = [
        ("Components", test_all_components),
        ("Export", test_export_functionality),
        ("Performance", test_performance_monitoring),
        ("Configuration", test_configuration_system),
        ("Integration", test_integration_readiness),
        ("Requirements", test_system_requirements)
    ]
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            report["test_results"][test_name] = result
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            report["test_results"][test_name] = False
    
    # System info
    try:
        import platform
        import psutil
        
        report["system_info"] = {
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "platform": platform.platform(),
            "cpu_count": psutil.cpu_count(),
            "memory_gb": psutil.virtual_memory().total / 1024**3,
            "architecture": platform.architecture()[0]
        }
    except Exception as e:
        report["system_info"]["error"] = str(e)
    
    # Recommendations
    passed_tests = sum(report["test_results"].values())
    total_tests = len(report["test_results"])
    
    if passed_tests == total_tests:
        report["recommendations"].append("🎉 System jest w pełni gotowy do użycia!")
        report["recommendations"].append("Możesz uruchomić: python main.py --mode demo")
    else:
        report["recommendations"].append("⚠️ Niektóre komponenty wymagają naprawy")
        
        if not report["test_results"].get("Requirements", True):
            report["recommendations"].append("Zainstaluj brakujące dependencies")
        
        if not report["test_results"].get("Components", True):
            report["recommendations"].append("Sprawdź importy modułów")
        
        if not report["test_results"].get("Integration", True):
            report["recommendations"].append("Napraw błędy integracji")
    
    # Zapisz raport
    try:
        report_path = "system_test_report.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Raport zapisany: {report_path}")
    except Exception as e:
        print(f"❌ Nie można zapisać raportu: {e}")
    
    return report

def main():
    """Główna funkcja testów"""
    print("🧪 Real-time STT Polish - Kompletny Test Systemu")
    print("=" * 60)
    print("🎤 Testowanie wszystkich komponentów systemu...")
    print()
    
    # Wygeneruj raport
    report = generate_system_report()
    
    # Podsumowanie
    print("\n" + "=" * 60)
    print("📊 PODSUMOWANIE TESTÓW SYSTEMU")
    print("=" * 60)
    
    passed = sum(report["test_results"].values())
    total = len(report["test_results"])
    
    for test_name, result in report["test_results"].items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 Wyniki: {passed}/{total} testów przeszło ({passed/total:.1%})")
    
    # Rekomendacje
    print("\n💡 REKOMENDACJE:")
    for rec in report["recommendations"]:
        print(f"   {rec}")
    
    if passed == total:
        print("\n🎉 SYSTEM W PEŁNI FUNKCJONALNY!")
        print("🚀 Real-time Speech-to-Text Polish gotowy do użycia!")
        print("\n📋 Następne kroki:")
        print("   1. python main.py --mode demo")
        print("   2. python gui_launcher.py")
        print("   3. python install_whisper_dependencies.py (jeśli Whisper nie jest zainstalowany)")
        return True
    else:
        print("\n⚠️ System wymaga poprawek przed użyciem")
        print("📋 Sprawdź błędy powyżej i napraw problemy")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n👋 Test przerwany przez użytkownika")
        sys.exit(0)
