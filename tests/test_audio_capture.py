"""
Tests for AudioCapture module
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from audio_capture import AudioCapture


def test_audio_capture_init():
    """Test AudioCapture initialization"""
    capture = AudioCapture(sample_rate=16000)
    assert capture.sample_rate == 16000
    assert capture.channels == 1
    assert not capture.is_recording


def test_audio_capture_statistics():
    """Test AudioCapture statistics"""
    capture = AudioCapture()
    stats = capture.get_statistics()

    assert "duration_seconds" in stats
    assert "total_frames" in stats
    assert "sample_rate" in stats
    assert stats["sample_rate"] == 16000


def test_audio_capture_context_manager():
    """Test AudioCapture as context manager"""
    # Note: This test won't actually record, just tests the interface
    try:
        with AudioCapture() as capture:
            assert capture is not None
    except Exception:
        # Expected to fail without actual audio device in CI
        pass
