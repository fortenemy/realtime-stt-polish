"""
Tests for Voice Activity Detection module
"""

import pytest
import numpy as np
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from voice_activity_detector import SimpleVAD, VADMode


def test_simple_vad_init():
    """Test SimpleVAD initialization"""
    vad = SimpleVAD(sample_rate=16000)
    assert vad.sample_rate == 16000
    assert not vad.is_speech


def test_simple_vad_energy_calculation():
    """Test energy calculation"""
    vad = SimpleVAD()

    # Silent audio
    silent_audio = np.zeros(1024, dtype=np.float32)
    energy = vad.calculate_energy(silent_audio)
    assert energy == 0.0

    # Loud audio
    loud_audio = np.ones(1024, dtype=np.float32) * 0.5
    energy = vad.calculate_energy(loud_audio)
    assert energy > 0.0


def test_simple_vad_process_chunk():
    """Test chunk processing"""
    vad = SimpleVAD()

    # Process silent chunk
    silent_audio = np.zeros(1024, dtype=np.float32)
    is_speech, analysis = vad.process_chunk(silent_audio)

    assert isinstance(is_speech, bool)
    assert "energy" in analysis
    assert "zcr" in analysis


def test_simple_vad_statistics():
    """Test VAD statistics"""
    vad = SimpleVAD()
    stats = vad.get_statistics()

    assert "current_state" in stats
    assert "energy_threshold" in stats
    assert "zcr_threshold" in stats
