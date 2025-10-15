"""
Real-time Speech-to-Text Pipeline
Główny pipeline łączący wszystkie komponenty

Autor: AI Assistant
Data: 2025-01-18
"""

import threading
import queue
import time
import numpy as np
import logging
from typing import Optional, Callable, Dict, Any
from dataclasses import dataclass
from enum import Enum

from audio_capture import AudioCapture
from voice_activity_detector import SimpleVAD, WebRTCVAD, VADMode
from stt_engine import WhisperSTTEngine, PolishOptimizedSTT, TranscriptionResult

# Konfiguracja loggingu
logger = logging.getLogger(__name__)


class PipelineState(Enum):
    """Stany pipeline"""

    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    ERROR = "error"


@dataclass
class SpeechSegment:
    """Segment mowy wykryty przez pipeline"""

    audio_data: np.ndarray
    start_time: float
    end_time: float
    confidence: float
    sample_rate: int
    transcription: Optional[TranscriptionResult] = None

    @property
    def duration(self) -> float:
        """Długość segmentu w sekundach"""
        return self.end_time - self.start_time

    @property
    def num_samples(self) -> int:
        """Liczba próbek audio"""
        return len(self.audio_data)

    @property
    def text(self) -> str:
        """Tekst transkrypcji (jeśli dostępny)"""
        return self.transcription.text if self.transcription else ""


class RealtimeSTTPipeline:
    """
    Główny pipeline Real-time Speech-to-Text
    Łączy AudioCapture + VAD + STT
    """

    def __init__(
        self,
        sample_rate: int = 16000,
        chunk_size: int = 1024,
        vad_mode: VADMode = VADMode.NORMAL,
        use_webrtc_vad: bool = True,
        min_segment_duration: float = 0.5,
        max_segment_duration: float = 30.0,
        silence_timeout: float = 2.0,
        enable_stt: bool = True,
        stt_model: str = "medium",
        use_polish_optimization: bool = True,
    ):
        """
        Inicjalizacja pipeline

        Args:
            sample_rate: Częstotliwość próbkowania
            chunk_size: Rozmiar chunka audio
            vad_mode: Tryb Voice Activity Detection
            use_webrtc_vad: Czy używać WebRTC VAD
            min_segment_duration: Min. długość segmentu mowy (s)
            max_segment_duration: Max. długość segmentu mowy (s)
            silence_timeout: Timeout ciszy dla zakończenia segmentu (s)
            enable_stt: Czy włączyć transkrypcję STT
            stt_model: Model Whisper do użycia
            use_polish_optimization: Czy używać optymalizacji dla polskiego
        """
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.min_segment_duration = min_segment_duration
        self.max_segment_duration = max_segment_duration
        self.silence_timeout = silence_timeout

        # Komponenty
        self.audio_capture = AudioCapture(
            sample_rate=sample_rate, chunk_size=chunk_size, buffer_size=100
        )

        # VAD
        if use_webrtc_vad:
            self.vad = WebRTCVAD(sample_rate=sample_rate, mode=vad_mode)
        else:
            self.vad = SimpleVAD(sample_rate=sample_rate)

        # STT Engine
        self.enable_stt = enable_stt
        self.stt_engine = None
        if enable_stt:
            try:
                if use_polish_optimization:
                    self.stt_engine = PolishOptimizedSTT(
                        model_name=stt_model, language="pl"
                    )
                else:
                    self.stt_engine = WhisperSTTEngine(
                        model_name=stt_model, language="pl"
                    )
                logger.info(f"🤖 STT Engine inicjalizowany: {stt_model}")
            except ImportError:
                logger.warning("⚠️ Whisper nie zainstalowany - STT wyłączony")
                self.enable_stt = False
                self.stt_engine = None
            except Exception as e:
                logger.error(f"❌ Błąd inicjalizacji STT: {e}")
                self.enable_stt = False
                self.stt_engine = None

        # Stan pipeline
        self.state = PipelineState.STOPPED
        self.processing_thread = None
        self.speech_queue = queue.Queue()

        # Callback dla segmentów mowy
        self.speech_callback: Optional[Callable[[SpeechSegment], None]] = None

        # Bieżący segment
        self.current_segment_audio = []
        self.current_segment_start = None
        self.last_speech_time = None

        # Statystyki
        self.total_segments = 0
        self.total_audio_time = 0
        self.start_time = None

        logger.info(
            f"🚀 RealtimeSTTPipeline zainicjalizowany: "
            f"{sample_rate}Hz, chunk={chunk_size}, VAD={type(self.vad).__name__}"
        )

    def set_speech_callback(self, callback: Callable[[SpeechSegment], None]):
        """
        Ustaw callback dla segmentów mowy

        Args:
            callback: Funkcja wywoływana dla każdego segmentu mowy
        """
        self.speech_callback = callback
        logger.info("🔗 Speech callback ustawiony")

    def start(self):
        """Uruchom pipeline"""
        if self.state != PipelineState.STOPPED:
            logger.warning("⚠️ Pipeline już działa lub się uruchamia")
            return

        logger.info("🚀 Uruchamianie Real-time STT Pipeline...")
        self.state = PipelineState.STARTING

        try:
            # Uruchom audio capture
            self.audio_capture.start_recording()

            # Uruchom wątek przetwarzania
            self.processing_thread = threading.Thread(
                target=self._processing_loop, daemon=True
            )
            self.processing_thread.start()

            self.state = PipelineState.RUNNING
            self.start_time = time.time()

            logger.info("✅ Pipeline uruchomiony!")

        except Exception as e:
            logger.error(f"❌ Błąd uruchamiania pipeline: {e}")
            self.state = PipelineState.ERROR
            raise

    def stop(self):
        """Zatrzymaj pipeline"""
        if self.state not in [PipelineState.RUNNING, PipelineState.STARTING]:
            return

        logger.info("⏹️ Zatrzymywanie pipeline...")
        self.state = PipelineState.STOPPING

        # Zatrzymaj audio capture
        self.audio_capture.stop_recording()

        # Poczekaj na zakończenie wątku
        if self.processing_thread and self.processing_thread.is_alive():
            self.processing_thread.join(timeout=5.0)

        # Wyślij ostatni segment jeśli istnieje
        self._finalize_current_segment()

        self.state = PipelineState.STOPPED
        logger.info("✅ Pipeline zatrzymany")

    def _processing_loop(self):
        """Główna pętla przetwarzania audio"""
        logger.info("🔄 Processing loop started")

        while self.state == PipelineState.RUNNING:
            try:
                # Pobierz chunk audio
                audio_chunk = self.audio_capture.get_audio_chunk(timeout=0.1)
                if audio_chunk is None:
                    continue

                # Przetwórz chunk
                self._process_audio_chunk(audio_chunk)

            except Exception as e:
                logger.error(f"❌ Błąd w processing loop: {e}")
                self.state = PipelineState.ERROR
                break

        logger.info("🔄 Processing loop stopped")

    def _process_audio_chunk(self, audio_chunk: np.ndarray):
        """
        Przetwórz pojedynczy chunk audio

        Args:
            audio_chunk: Chunk audio do przetworzenia
        """
        current_time = time.time()

        # Sprawdź czy chunk zawiera mowę
        if hasattr(self.vad, "process_chunk"):
            # SimpleVAD
            is_speech, vad_analysis = self.vad.process_chunk(audio_chunk.flatten())
        else:
            # WebRTC VAD
            is_speech = self.vad.is_speech(audio_chunk.flatten())
            vad_analysis = {"is_stable_speech": is_speech}

        if is_speech:
            self._handle_speech_chunk(audio_chunk, current_time)
        else:
            self._handle_silence_chunk(current_time)

    def _handle_speech_chunk(self, audio_chunk: np.ndarray, current_time: float):
        """
        Obsłuż chunk z mową

        Args:
            audio_chunk: Chunk audio z mową
            current_time: Aktualny czas
        """
        # Rozpocznij nowy segment jeśli potrzeba
        if self.current_segment_start is None:
            self.current_segment_start = current_time
            self.current_segment_audio = []
            logger.debug("🎤 Rozpoczęcie nowego segmentu mowy")

        # Dodaj audio do bieżącego segmentu
        self.current_segment_audio.append(audio_chunk.flatten())
        self.last_speech_time = current_time

        # Sprawdź czy segment nie jest za długi
        segment_duration = current_time - self.current_segment_start
        if segment_duration >= self.max_segment_duration:
            logger.debug(f"⏱️ Segment osiągnął max długość: {segment_duration:.2f}s")
            self._finalize_current_segment()

    def _handle_silence_chunk(self, current_time: float):
        """
        Obsłuż chunk z ciszą

        Args:
            current_time: Aktualny czas
        """
        # Sprawdź czy mamy aktywny segment i czy cisza trwa wystarczająco długo
        if (
            self.current_segment_start is not None
            and self.last_speech_time is not None
            and current_time - self.last_speech_time >= self.silence_timeout
        ):

            segment_duration = self.last_speech_time - self.current_segment_start

            # Finalizuj segment jeśli ma minimalną długość
            if segment_duration >= self.min_segment_duration:
                logger.debug(f"🔇 Koniec segmentu po ciszy: {segment_duration:.2f}s")
                self._finalize_current_segment()
            else:
                logger.debug(
                    f"🗑️ Odrzucenie krótkiego segmentu: {segment_duration:.2f}s"
                )
                self._discard_current_segment()

    def _finalize_current_segment(self):
        """Finalizuj bieżący segment mowy"""
        if self.current_segment_start is None or not self.current_segment_audio:
            return

        # Połącz wszystkie chunki audio
        segment_audio = np.concatenate(self.current_segment_audio)

        # Stwórz segment
        segment = SpeechSegment(
            audio_data=segment_audio,
            start_time=self.current_segment_start,
            end_time=self.last_speech_time or time.time(),
            confidence=1.0,  # TODO: oblicz confidence
            sample_rate=self.sample_rate,
        )

        # Transkrypcja STT (jeśli włączona)
        if self.enable_stt and self.stt_engine:
            try:
                transcription = self.stt_engine.transcribe_audio(
                    segment_audio, self.sample_rate
                )
                segment.transcription = transcription

                if transcription:
                    logger.info(
                        f"🎯 Transkrypcja: '{transcription.text}' "
                        f"(conf={transcription.confidence:.2f})"
                    )
            except Exception as e:
                logger.error(f"❌ Błąd transkrypcji: {e}")
                segment.transcription = None

        # Statystyki
        self.total_segments += 1
        self.total_audio_time += segment.duration

        logger.info(
            f"🎯 Segment #{self.total_segments}: {segment.duration:.2f}s, "
            f"{len(segment_audio)} samples"
        )

        # Wyślij segment przez callback
        if self.speech_callback:
            try:
                self.speech_callback(segment)
            except Exception as e:
                logger.error(f"❌ Błąd w speech callback: {e}")

        # Dodaj do kolejki
        try:
            self.speech_queue.put_nowait(segment)
        except queue.Full:
            logger.warning("⚠️ Speech queue full, dropping segment")

        # Reset stanu
        self._reset_current_segment()

    def _discard_current_segment(self):
        """Odrzuć bieżący segment"""
        logger.debug("🗑️ Odrzucenie bieżącego segmentu")
        self._reset_current_segment()

    def _reset_current_segment(self):
        """Reset stanu bieżącego segmentu"""
        self.current_segment_start = None
        self.current_segment_audio = []
        self.last_speech_time = None

    def get_speech_segment(self, timeout: float = 1.0) -> Optional[SpeechSegment]:
        """
        Pobierz segment mowy z kolejki

        Args:
            timeout: Timeout w sekundach

        Returns:
            SpeechSegment lub None jeśli timeout
        """
        try:
            return self.speech_queue.get(timeout=timeout)
        except queue.Empty:
            return None

    def get_statistics(self) -> Dict[str, Any]:
        """Pobierz statystyki pipeline"""
        runtime = time.time() - self.start_time if self.start_time else 0

        # Statystyki audio capture
        audio_stats = self.audio_capture.get_statistics()

        # Statystyki VAD
        if hasattr(self.vad, "get_statistics"):
            vad_stats = self.vad.get_statistics()
        else:
            vad_stats = {"type": "WebRTC VAD"}

        return {
            "pipeline": {
                "state": self.state.value,
                "runtime_seconds": runtime,
                "total_segments": self.total_segments,
                "total_audio_time": self.total_audio_time,
                "segments_per_minute": (
                    (self.total_segments / (runtime / 60)) if runtime > 0 else 0
                ),
                "queue_size": self.speech_queue.qsize(),
            },
            "audio_capture": audio_stats,
            "vad": vad_stats,
        }

    def __enter__(self):
        """Context manager entry"""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop()

    def set_stt_engine(self, stt_engine):
        """
        Ustaw custom STT engine

        Args:
            stt_engine: Instancja WhisperSTTEngine lub kompatybilnego silnika
        """
        self.stt_engine = stt_engine
        self.enable_stt = stt_engine is not None
        logger.info(f"🤖 STT Engine ustawiony: {type(stt_engine).__name__}")

    def load_stt_model(self):
        """Załaduj model STT (jeśli nie jest załadowany)"""
        if self.stt_engine and hasattr(self.stt_engine, "load_model"):
            return self.stt_engine.load_model()
        return True

    def unload_stt_model(self):
        """Zwolnij model STT z pamięci"""
        if self.stt_engine and hasattr(self.stt_engine, "unload_model"):
            self.stt_engine.unload_model()
            logger.info("🗑️ STT model zwolniony z pamięci")
