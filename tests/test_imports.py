"""
Basic import tests to verify all modules can be imported
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def test_import_audio_capture():
    """Test importing audio_capture module"""
    import audio_capture

    assert hasattr(audio_capture, "AudioCapture")


def test_import_vad():
    """Test importing voice_activity_detector module"""
    import voice_activity_detector

    assert hasattr(voice_activity_detector, "SimpleVAD")
    assert hasattr(voice_activity_detector, "VADMode")


def test_import_stt_engine():
    """Test importing stt_engine module"""
    import stt_engine

    assert hasattr(stt_engine, "WhisperSTTEngine")
    assert hasattr(stt_engine, "PolishOptimizedSTT")


def test_import_pipeline():
    """Test importing realtime_pipeline module"""
    import realtime_pipeline

    assert hasattr(realtime_pipeline, "RealtimeSTTPipeline")


def test_import_performance():
    """Test importing performance_optimizer module"""
    import performance_optimizer

    assert hasattr(performance_optimizer, "PerformanceOptimizer")


def test_import_export():
    """Test importing export_manager module"""
    import export_manager

    assert hasattr(export_manager, "ExportManager")


def test_import_gui():
    """Test importing gui_application module"""
    import gui_application

    assert hasattr(gui_application, "STTGuiApplication")
