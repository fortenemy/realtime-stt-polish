"""
Moduł do przechwytywania audio w czasie rzeczywistym
Real-time Audio Capture Module

Autor: AI Assistant
Data: 2025-01-18
"""

import sounddevice as sd
import numpy as np
import queue
import threading
import time
from typing import Optional, Callable, List
import logging
from pathlib import Path

# Konfiguracja loggingu
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class AudioCapture:
    """Klasa do przechwytywania audio z mikrofonu w czasie rzeczywistym"""

    def __init__(
        self,
        sample_rate: int = 16000,
        channels: int = 1,
        chunk_size: int = 1024,
        device: Optional[int] = None,
        buffer_size: int = 100,
    ):
        """
        Inicjalizacja AudioCapture

        Args:
            sample_rate: Częstotliwość próbkowania (Hz) - 16kHz optymalne dla STT
            channels: Liczba kanałów audio (1=mono, 2=stereo)
            chunk_size: Rozmiar bufora w sampleach
            device: ID urządzenia audio (None = domyślne)
            buffer_size: Maksymalny rozmiar kolejki audio
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.device = device
        self.buffer_size = buffer_size

        # Kolejka audio z ograniczeniem rozmiaru
        self.audio_queue = queue.Queue(maxsize=buffer_size)
        self.is_recording = False
        self.stream = None

        # Statystyki
        self.total_frames = 0
        self.dropped_frames = 0
        self.start_time = None

        logger.info(
            f"🎤 AudioCapture zainicjalizowany: {sample_rate}Hz, {channels}ch, buffer={buffer_size}"
        )

        # Sprawdź dostępność urządzeń
        self._validate_audio_system()

    def list_devices(self):
        """Wyświetl dostępne urządzenia audio"""
        print("📱 Dostępne urządzenia audio:")
        print(sd.query_devices())

    def start_recording(self):
        """Rozpocznij nagrywanie"""
        if self.is_recording:
            logger.warning("⚠️ Nagrywanie już trwa!")
            return

        try:
            # Reset statystyk
            self.total_frames = 0
            self.dropped_frames = 0
            self.start_time = time.time()

            self.stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                callback=self._audio_callback,
                blocksize=self.chunk_size,
                device=self.device,
                dtype=np.float32,
            )

            self.stream.start()
            self.is_recording = True
            logger.info("🎤 Nagrywanie rozpoczęte")

        except Exception as e:
            logger.error(f"❌ Błąd podczas rozpoczynania nagrywania: {e}")
            raise

    def stop_recording(self):
        """Zatrzymaj nagrywanie"""
        if not self.is_recording:
            return

        self.is_recording = False
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None

        logger.info("⏹️ Nagrywanie zatrzymane")

    def _audio_callback(self, indata, frames, time, status):
        """Callback dla strumienia audio"""
        if status:
            logger.warning(f"⚠️ Audio callback status: {status}")

        self.total_frames += 1

        # Dodaj audio do kolejki
        audio_chunk = indata.copy()

        try:
            # Użyj put_nowait aby nie blokować audio callback
            self.audio_queue.put_nowait(audio_chunk)
        except queue.Full:
            # Jeśli kolejka pełna, usuń najstarszy element i dodaj nowy
            try:
                self.audio_queue.get_nowait()
                self.audio_queue.put_nowait(audio_chunk)
                self.dropped_frames += 1
            except queue.Empty:
                pass

    def get_audio_chunk(self, timeout: float = 1.0) -> Optional[np.ndarray]:
        """
        Pobierz chunk audio z kolejki

        Args:
            timeout: Timeout w sekundach

        Returns:
            Chunk audio lub None jeśli timeout
        """
        try:
            return self.audio_queue.get(timeout=timeout)
        except queue.Empty:
            return None

    def __enter__(self):
        """Context manager entry"""
        self.start_recording()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop_recording()

    def _validate_audio_system(self):
        """Sprawdź dostępność systemu audio"""
        try:
            devices = sd.query_devices()
            if len(devices) == 0:
                raise RuntimeError("Brak urządzeń audio w systemie")

            # Sprawdź domyślne urządzenie wejściowe
            default_input = sd.default.device[0]
            if default_input is None:
                logger.warning("⚠️ Brak domyślnego urządzenia wejściowego")
            else:
                device_info = sd.query_devices(default_input)
                logger.info(f"📱 Domyślny mikrofon: {device_info['name']}")

        except Exception as e:
            logger.error(f"❌ Błąd systemu audio: {e}")
            raise

    def get_audio_level(self, audio_data: np.ndarray) -> float:
        """
        Oblicz poziom audio (RMS)

        Args:
            audio_data: Dane audio

        Returns:
            Poziom audio w dB
        """
        if len(audio_data) == 0:
            return -np.inf

        rms = np.sqrt(np.mean(audio_data**2))
        if rms > 0:
            return 20 * np.log10(rms)
        else:
            return -np.inf

    def get_statistics(self) -> dict:
        """
        Pobierz statystyki nagrywania

        Returns:
            Słownik ze statystykami
        """
        if self.start_time is None:
            duration = 0
        else:
            duration = time.time() - self.start_time

        return {
            "duration_seconds": duration,
            "total_frames": self.total_frames,
            "dropped_frames": self.dropped_frames,
            "drop_rate": self.dropped_frames / max(self.total_frames, 1),
            "sample_rate": self.sample_rate,
            "is_recording": self.is_recording,
            "queue_size": self.audio_queue.qsize(),
        }

    def clear_buffer(self):
        """Wyczyść bufor audio"""
        while not self.audio_queue.empty():
            try:
                self.audio_queue.get_nowait()
            except queue.Empty:
                break
        logger.info("🧹 Bufor audio wyczyszczony")
