"""
Tests for STT Engine module
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from stt_engine import WhisperSTTEngine, PolishOptimizedSTT, WhisperModel


def test_whisper_model_enum():
    """Test WhisperModel enum"""
    assert WhisperModel.TINY.value == "tiny"
    assert WhisperModel.BASE.value == "base"
    assert WhisperModel.MEDIUM.value == "medium"


def test_whisper_stt_init():
    """Test WhisperSTTEngine initialization"""
    engine = WhisperSTTEngine(model_name="tiny", device="cpu")

    assert engine.model_name == "tiny"
    assert engine.language == "pl"
    assert not engine.is_loaded


def test_polish_optimized_stt_init():
    """Test PolishOptimizedSTT initialization"""
    engine = PolishOptimizedSTT(model_name="tiny")

    assert engine.model_name == "tiny"
    assert engine.language == "pl"
    assert "tak" in engine.polish_common_words


def test_polish_post_processing():
    """Test Polish text post-processing"""
    engine = PolishOptimizedSTT(model_name="tiny")

    # Test corrections
    result = engine.post_process_polish_text("to jest sie")
    assert "się" in result

    # Test capitalization
    result = engine.post_process_polish_text("test")
    assert result[0].isupper()


def test_stt_engine_info():
    """Test STT engine info"""
    engine = WhisperSTTEngine(model_name="tiny")
    info = engine.get_model_info()

    assert "model_name" in info
    assert "device" in info
    assert "language" in info
    assert info["model_name"] == "tiny"
