"""
Voice Activity Detection (VAD) - Detekcja aktywności głosowej
Real-time Voice Activity Detection Module

Autor: AI Assistant
Data: 2025-01-18
"""

import numpy as np
import logging
from typing import Optional, List, Tuple
from enum import Enum

# Konfiguracja loggingu
logger = logging.getLogger(__name__)

class VADMode(Enum):
    """Tryby agresywności VAD"""
    VERY_AGGRESSIVE = 3  # Bardzo agresywny (mało false positives)
    AGGRESSIVE = 2       # Agresywny
    NORMAL = 1          # Normalny
    PERMISSIVE = 0      # Permisywny (mało false negatives)

class SimpleVAD:
    """
    Prosta implementacja Voice Activity Detection
    Oparta na analizie energii i crossing rate
    """
    
    def __init__(
        self,
        sample_rate: int = 16000,
        frame_duration_ms: int = 30,
        energy_threshold: float = 0.01,
        zcr_threshold: float = 0.1,
        min_speech_frames: int = 3,
        min_silence_frames: int = 5
    ):
        """
        Inicjalizacja SimpleVAD
        
        Args:
            sample_rate: Częstotliwość próbkowania
            frame_duration_ms: Długość ramki w ms
            energy_threshold: Próg energii dla detekcji mowy
            zcr_threshold: Próg zero crossing rate
            min_speech_frames: Min. ramek dla potwierdzenia mowy
            min_silence_frames: Min. ramek dla potwierdzenia ciszy
        """
        self.sample_rate = sample_rate
        self.frame_duration_ms = frame_duration_ms
        self.frame_size = int(sample_rate * frame_duration_ms / 1000)
        
        self.energy_threshold = energy_threshold
        self.zcr_threshold = zcr_threshold
        self.min_speech_frames = min_speech_frames
        self.min_silence_frames = min_silence_frames
        
        # Stan wewnętrzny
        self.is_speech = False
        self.speech_frame_count = 0
        self.silence_frame_count = 0
        
        # Historia dla stabilizacji
        self.energy_history = []
        self.zcr_history = []
        self.decision_history = []
        self.history_size = 10
        
        logger.info(f"🎙️ SimpleVAD zainicjalizowany: frame={frame_duration_ms}ms, "
                   f"energy_thr={energy_threshold}, zcr_thr={zcr_threshold}")
    
    def calculate_energy(self, audio_frame: np.ndarray) -> float:
        """
        Oblicz energię ramki audio
        
        Args:
            audio_frame: Ramka audio
            
        Returns:
            Energia znormalizowana (0-1)
        """
        if len(audio_frame) == 0:
            return 0.0
        
        # RMS energy
        rms = np.sqrt(np.mean(audio_frame ** 2))
        
        # Normalizacja logarytmiczna
        if rms > 0:
            energy = min(1.0, rms * 10)  # Skalowanie
        else:
            energy = 0.0
        
        return energy
    
    def calculate_zero_crossing_rate(self, audio_frame: np.ndarray) -> float:
        """
        Oblicz zero crossing rate
        
        Args:
            audio_frame: Ramka audio
            
        Returns:
            ZCR znormalizowany (0-1)
        """
        if len(audio_frame) < 2:
            return 0.0
        
        # Policz przejścia przez zero
        zero_crossings = np.sum(np.abs(np.diff(np.sign(audio_frame))))
        
        # Normalizacja przez długość ramki
        zcr = zero_crossings / (2 * len(audio_frame))
        
        return zcr
    
    def analyze_frame(self, audio_frame: np.ndarray) -> dict:
        """
        Analizuj pojedynczą ramkę audio
        
        Args:
            audio_frame: Ramka audio
            
        Returns:
            Słownik z wynikami analizy
        """
        energy = self.calculate_energy(audio_frame)
        zcr = self.calculate_zero_crossing_rate(audio_frame)
        
        # Dodaj do historii
        self.energy_history.append(energy)
        self.zcr_history.append(zcr)
        
        # Ogranicz historię
        if len(self.energy_history) > self.history_size:
            self.energy_history.pop(0)
            self.zcr_history.pop(0)
        
        # Średnie z historii dla stabilizacji
        avg_energy = np.mean(self.energy_history)
        avg_zcr = np.mean(self.zcr_history)
        
        return {
            'energy': energy,
            'zcr': zcr,
            'avg_energy': avg_energy,
            'avg_zcr': avg_zcr,
            'frame_size': len(audio_frame)
        }
    
    def is_speech_frame(self, analysis: dict) -> bool:
        """
        Określ czy ramka zawiera mowę
        
        Args:
            analysis: Wyniki analizy ramki
            
        Returns:
            True jeśli mowa, False jeśli cisza
        """
        energy = analysis['avg_energy']
        zcr = analysis['avg_zcr']
        
        # Logika decyzyjna
        speech_indicators = 0
        
        # Test energii
        if energy > self.energy_threshold:
            speech_indicators += 1
        
        # Test ZCR (mowa ma średni ZCR, szum ma wysoki lub niski)
        if 0.02 < zcr < 0.4:  # Typowy zakres dla mowy
            speech_indicators += 1
        
        # Decyzja: przynajmniej jeden wskaźnik musi być pozytywny
        return speech_indicators >= 1
    
    def update_state(self, is_current_speech: bool) -> bool:
        """
        Aktualizuj stan VAD z hysterezą
        
        Args:
            is_current_speech: Czy aktualna ramka to mowa
            
        Returns:
            Stabilny stan mowy (po hysterzie)
        """
        if is_current_speech:
            self.speech_frame_count += 1
            self.silence_frame_count = 0
            
            # Przejście do mowy
            if not self.is_speech and self.speech_frame_count >= self.min_speech_frames:
                self.is_speech = True
                logger.debug("🎤 VAD: Start mowy")
        else:
            self.silence_frame_count += 1
            self.speech_frame_count = 0
            
            # Przejście do ciszy
            if self.is_speech and self.silence_frame_count >= self.min_silence_frames:
                self.is_speech = False
                logger.debug("🔇 VAD: Koniec mowy")
        
        return self.is_speech
    
    def process_chunk(self, audio_chunk: np.ndarray) -> Tuple[bool, dict]:
        """
        Przetwórz chunk audio i zwróć decyzję VAD
        
        Args:
            audio_chunk: Chunk audio do analizy
            
        Returns:
            Tuple (is_speech, analysis_details)
        """
        # Upewnij się że chunk ma właściwy format
        if len(audio_chunk.shape) > 1:
            audio_chunk = audio_chunk.flatten()
        
        # Analizuj ramkę
        analysis = self.analyze_frame(audio_chunk)
        
        # Sprawdź czy to mowa
        is_current_speech = self.is_speech_frame(analysis)
        
        # Aktualizuj stan z hysterezą
        stable_speech = self.update_state(is_current_speech)
        
        # Dodaj do analizy
        analysis.update({
            'is_current_speech': is_current_speech,
            'is_stable_speech': stable_speech,
            'speech_frames': self.speech_frame_count,
            'silence_frames': self.silence_frame_count
        })
        
        return stable_speech, analysis
    
    def get_statistics(self) -> dict:
        """Pobierz statystyki VAD"""
        return {
            'current_state': 'speech' if self.is_speech else 'silence',
            'speech_frame_count': self.speech_frame_count,
            'silence_frame_count': self.silence_frame_count,
            'energy_threshold': self.energy_threshold,
            'zcr_threshold': self.zcr_threshold,
            'avg_energy': np.mean(self.energy_history) if self.energy_history else 0,
            'avg_zcr': np.mean(self.zcr_history) if self.zcr_history else 0
        }
    
    def reset(self):
        """Reset stanu VAD"""
        self.is_speech = False
        self.speech_frame_count = 0
        self.silence_frame_count = 0
        self.energy_history.clear()
        self.zcr_history.clear()
        self.decision_history.clear()
        
        logger.info("🔄 VAD zresetowany")


class WebRTCVAD:
    """
    Wrapper dla WebRTC VAD (gdy dostępny)
    Fallback do SimpleVAD jeśli WebRTC nie jest dostępne
    """
    
    def __init__(
        self,
        sample_rate: int = 16000,
        mode: VADMode = VADMode.NORMAL
    ):
        """
        Inicjalizacja WebRTC VAD
        
        Args:
            sample_rate: Częstotliwość próbkowania (8k, 16k, 32k, 48k)
            mode: Agresywność VAD
        """
        self.sample_rate = sample_rate
        self.mode = mode
        self.webrtc_vad = None
        self.fallback_vad = None
        
        # Spróbuj załadować WebRTC VAD
        try:
            import webrtcvad
            self.webrtc_vad = webrtcvad.Vad(mode.value)
            logger.info(f"✅ WebRTC VAD zainicjalizowany (mode={mode.name})")
        except ImportError:
            logger.warning("⚠️ WebRTC VAD niedostępny, używam SimpleVAD")
            self.fallback_vad = SimpleVAD(sample_rate=sample_rate)
    
    def is_speech(self, audio_frame: np.ndarray) -> bool:
        """
        Sprawdź czy ramka zawiera mowę
        
        Args:
            audio_frame: Ramka audio (16-bit PCM)
            
        Returns:
            True jeśli mowa
        """
        if self.webrtc_vad is not None:
            # WebRTC VAD wymaga 16-bit PCM
            if audio_frame.dtype != np.int16:
                # Konwertuj float32 -> int16
                audio_int16 = (audio_frame * 32767).astype(np.int16)
            else:
                audio_int16 = audio_frame
            
            # WebRTC VAD wymaga określonych długości ramek
            frame_duration = len(audio_int16) / self.sample_rate
            if frame_duration not in [0.01, 0.02, 0.03]:  # 10ms, 20ms, 30ms
                # Użyj fallback
                if self.fallback_vad is None:
                    self.fallback_vad = SimpleVAD(sample_rate=self.sample_rate)
                is_speech, _ = self.fallback_vad.process_chunk(audio_frame)
                return is_speech
            
            try:
                return self.webrtc_vad.is_speech(audio_int16.tobytes(), self.sample_rate)
            except Exception as e:
                logger.warning(f"WebRTC VAD error: {e}, using fallback")
                if self.fallback_vad is None:
                    self.fallback_vad = SimpleVAD(sample_rate=self.sample_rate)
                is_speech, _ = self.fallback_vad.process_chunk(audio_frame)
                return is_speech
        else:
            # Użyj SimpleVAD
            is_speech, _ = self.fallback_vad.process_chunk(audio_frame)
            return is_speech
