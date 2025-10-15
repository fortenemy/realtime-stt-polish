"""
Speech-to-Text Engine using OpenAI Whisper
Optimized for Polish language real-time processing

Autor: AI Assistant
Data: 2025-01-18
"""

import whisper
import numpy as np
import torch
import logging
import time
from typing import Optional, Dict, Any, List, Union
from dataclasses import dataclass
from enum import Enum
import threading
import queue

# Konfiguracja loggingu
logger = logging.getLogger(__name__)

class WhisperModel(Enum):
    """Dostępne modele Whisper"""
    TINY = "tiny"
    BASE = "base" 
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    LARGE_V2 = "large-v2"
    LARGE_V3 = "large-v3"

@dataclass
class TranscriptionResult:
    """Wynik transkrypcji"""
    text: str
    language: str
    confidence: float
    processing_time: float
    segments: List[Dict[str, Any]]
    model_used: str
    
    @property
    def words_per_minute(self) -> float:
        """Oblicz słowa na minutę"""
        if self.processing_time <= 0:
            return 0
        word_count = len(self.text.split())
        return (word_count / self.processing_time) * 60

class WhisperSTTEngine:
    """
    Silnik Speech-to-Text oparty na OpenAI Whisper
    Zoptymalizowany dla języka polskiego
    """
    
    def __init__(
        self,
        model_name: Union[WhisperModel, str] = WhisperModel.MEDIUM,
        device: Optional[str] = None,
        language: str = "pl",
        beam_size: int = 5,
        best_of: int = 5,
        temperature: float = 0.0,
        patience: float = 1.0,
        length_penalty: float = 1.0,
        suppress_tokens: str = "-1",
        initial_prompt: Optional[str] = None,
        condition_on_previous_text: bool = True,
        fp16: bool = True,
        compression_ratio_threshold: float = 2.4,
        logprob_threshold: float = -1.0,
        no_speech_threshold: float = 0.6
    ):
        """
        Inicjalizacja Whisper STT Engine
        
        Args:
            model_name: Nazwa modelu Whisper (tiny, base, small, medium, large)
            device: Device do używania ('cpu', 'cuda', None=auto)
            language: Kod języka (domyślnie 'pl' dla polskiego)
            beam_size: Rozmiar beam search
            best_of: Liczba kandydatów do wyboru
            temperature: Temperature dla sampling (0.0 = deterministyczny)
            patience: Patience factor dla beam search
            length_penalty: Penalty dla długości sekwencji
            suppress_tokens: Tokeny do tłumienia
            initial_prompt: Początkowy prompt dla kontekstu
            condition_on_previous_text: Czy używać poprzedniego tekstu jako kontekst
            fp16: Czy używać half precision (szybsze, mniej pamięci)
            compression_ratio_threshold: Próg dla wykrywania powtórzeń
            logprob_threshold: Próg prawdopodobieństwa
            no_speech_threshold: Próg dla wykrywania braku mowy
        """
        self.model_name = model_name.value if isinstance(model_name, WhisperModel) else model_name
        self.language = language
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        
        # Parametry dekodowania
        self.decode_options = {
            "language": language,
            "beam_size": beam_size,
            "best_of": best_of,
            "temperature": temperature,
            "patience": patience,
            "length_penalty": length_penalty,
            "suppress_tokens": suppress_tokens,
            "initial_prompt": initial_prompt,
            "condition_on_previous_text": condition_on_previous_text,
            "fp16": fp16,
            "compression_ratio_threshold": compression_ratio_threshold,
            "logprob_threshold": logprob_threshold,
            "no_speech_threshold": no_speech_threshold
        }
        
        # Model i stan
        self.model = None
        self.is_loaded = False
        self.previous_text = ""
        
        # Statystyki
        self.total_transcriptions = 0
        self.total_processing_time = 0
        self.model_load_time = 0
        
        logger.info(f"🤖 WhisperSTTEngine inicjalizowany: model={self.model_name}, "
                   f"device={self.device}, language={language}")
    
    def load_model(self) -> bool:
        """
        Załaduj model Whisper
        
        Returns:
            True jeśli załadowanie się powiodło
        """
        if self.is_loaded:
            logger.info("✅ Model już załadowany")
            return True
        
        try:
            start_time = time.time()
            logger.info(f"📥 Ładowanie modelu Whisper: {self.model_name}")
            
            # Załaduj model z konfiguracją
            self.model = whisper.load_model(
                self.model_name,
                device=self.device
            )
            
            self.model_load_time = time.time() - start_time
            self.is_loaded = True
            
            logger.info(f"✅ Model załadowany w {self.model_load_time:.2f}s")
            logger.info(f"📊 Model info: {self.model_name} na {self.device}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Błąd ładowania modelu: {e}")
            self.is_loaded = False
            return False
    
    def transcribe_audio(
        self,
        audio_data: np.ndarray,
        sample_rate: int = 16000
    ) -> Optional[TranscriptionResult]:
        """
        Transkrybuj audio na tekst
        
        Args:
            audio_data: Dane audio jako numpy array
            sample_rate: Częstotliwość próbkowania
            
        Returns:
            TranscriptionResult lub None w przypadku błędu
        """
        if not self.is_loaded:
            if not self.load_model():
                return None
        
        try:
            start_time = time.time()
            
            # Przygotuj audio
            audio = self._prepare_audio(audio_data, sample_rate)
            
            # Użyj poprzedniego tekstu jako prompt jeśli dostępny
            decode_options = self.decode_options.copy()
            if self.previous_text and decode_options.get("condition_on_previous_text", True):
                decode_options["initial_prompt"] = self.previous_text[-200:]  # Ostatnie 200 znaków
            
            # Transkrypcja
            result = self.model.transcribe(
                audio,
                **decode_options
            )
            
            processing_time = time.time() - start_time
            
            # Przygotuj wynik
            transcription_result = TranscriptionResult(
                text=result["text"].strip(),
                language=result["language"],
                confidence=self._calculate_confidence(result),
                processing_time=processing_time,
                segments=result.get("segments", []),
                model_used=self.model_name
            )
            
            # Aktualizuj statystyki
            self.total_transcriptions += 1
            self.total_processing_time += processing_time
            
            # Zachowaj tekst dla kontekstu
            if transcription_result.text:
                self.previous_text = transcription_result.text
            
            logger.debug(f"🎤 Transkrypcja: '{transcription_result.text}' "
                        f"({processing_time:.2f}s, conf={transcription_result.confidence:.2f})")
            
            return transcription_result
            
        except Exception as e:
            logger.error(f"❌ Błąd transkrypcji: {e}")
            return None
    
    def _prepare_audio(self, audio_data: np.ndarray, sample_rate: int) -> np.ndarray:
        """
        Przygotuj audio dla Whisper
        
        Args:
            audio_data: Surowe dane audio
            sample_rate: Częstotliwość próbkowania
            
        Returns:
            Przygotowane audio dla Whisper
        """
        # Whisper oczekuje 16kHz mono float32
        audio = audio_data.astype(np.float32)
        
        # Flatten jeśli stereo
        if len(audio.shape) > 1:
            audio = audio.flatten()
        
        # Resample jeśli potrzeba (Whisper używa 16kHz)
        if sample_rate != 16000:
            # Prosty resampling - w produkcji użyj librosa.resample
            audio = self._simple_resample(audio, sample_rate, 16000)
        
        # Normalizacja
        if audio.max() > 1.0 or audio.min() < -1.0:
            audio = audio / max(abs(audio.max()), abs(audio.min()))
        
        # Whisper wymaga minimum 0.1s audio
        min_samples = int(0.1 * 16000)
        if len(audio) < min_samples:
            audio = np.pad(audio, (0, min_samples - len(audio)))
        
        return audio
    
    def _simple_resample(self, audio: np.ndarray, orig_sr: int, target_sr: int) -> np.ndarray:
        """
        Prosty resampling audio
        
        Args:
            audio: Audio do resample
            orig_sr: Oryginalna częstotliwość
            target_sr: Docelowa częstotliwość
            
        Returns:
            Resampled audio
        """
        if orig_sr == target_sr:
            return audio
        
        # Prosty linear interpolation resampling
        ratio = target_sr / orig_sr
        new_length = int(len(audio) * ratio)
        
        # Linear interpolation
        old_indices = np.linspace(0, len(audio) - 1, new_length)
        new_audio = np.interp(old_indices, np.arange(len(audio)), audio)
        
        return new_audio.astype(np.float32)
    
    def _calculate_confidence(self, result: Dict[str, Any]) -> float:
        """
        Oblicz wskaźnik pewności transkrypcji
        
        Args:
            result: Wynik Whisper
            
        Returns:
            Confidence score 0-1
        """
        try:
            # Użyj średniego logprob z segmentów
            segments = result.get("segments", [])
            if not segments:
                return 0.5  # Domyślna wartość
            
            logprobs = []
            for segment in segments:
                if "avg_logprob" in segment:
                    logprobs.append(segment["avg_logprob"])
                elif "tokens" in segment:
                    # Fallback - użyj liczby tokenów jako proxy
                    logprobs.append(-0.1 * len(segment["tokens"]))
            
            if logprobs:
                avg_logprob = np.mean(logprobs)
                # Konwertuj logprob na confidence (0-1)
                confidence = max(0.0, min(1.0, (avg_logprob + 2.0) / 2.0))
                return confidence
            
            return 0.5
            
        except Exception as e:
            logger.warning(f"⚠️ Błąd obliczania confidence: {e}")
            return 0.5
    
    def get_model_info(self) -> Dict[str, Any]:
        """Pobierz informacje o modelu"""
        return {
            "model_name": self.model_name,
            "device": self.device,
            "language": self.language,
            "is_loaded": self.is_loaded,
            "load_time": self.model_load_time,
            "total_transcriptions": self.total_transcriptions,
            "avg_processing_time": (
                self.total_processing_time / max(self.total_transcriptions, 1)
            ),
            "decode_options": self.decode_options
        }
    
    def get_supported_languages(self) -> List[str]:
        """Pobierz listę obsługiwanych języków"""
        if not self.is_loaded:
            self.load_model()
        
        if self.model:
            return list(whisper.tokenizer.LANGUAGES.values())
        return []
    
    def clear_context(self):
        """Wyczyść kontekst poprzedniego tekstu"""
        self.previous_text = ""
        logger.info("🧹 Kontekst tekstowy wyczyszczony")
    
    def set_language(self, language: str):
        """
        Ustaw język transkrypcji
        
        Args:
            language: Kod języka (np. 'pl', 'en')
        """
        self.language = language
        self.decode_options["language"] = language
        logger.info(f"🌐 Język ustawiony na: {language}")
    
    def unload_model(self):
        """Zwolnij model z pamięci"""
        if self.model is not None:
            del self.model
            self.model = None
            self.is_loaded = False
            
            # Wyczyść cache GPU jeśli używane
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            
            logger.info("🗑️ Model Whisper zwolniony z pamięci")
    
    def __enter__(self):
        """Context manager entry"""
        self.load_model()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.unload_model()


class PolishOptimizedSTT(WhisperSTTEngine):
    """
    Whisper STT Engine zoptymalizowany specjalnie dla języka polskiego
    """
    
    def __init__(self, **kwargs):
        """
        Inicjalizacja z optymalizacjami dla polskiego
        """
        # Optymalne ustawienia dla polskiego
        polish_defaults = {
            "language": "pl",
            "initial_prompt": "To jest nagranie w języku polskim. ",
            "beam_size": 5,
            "best_of": 5,
            "temperature": 0.0,
            "patience": 1.0,
            "no_speech_threshold": 0.5  # Niższy próg dla polskiego
        }
        
        # Merge z user settings
        for key, value in polish_defaults.items():
            kwargs.setdefault(key, value)
        
        super().__init__(**kwargs)
        
        # Polskie stopwords i frazy
        self.polish_common_words = {
            "tak", "nie", "jest", "to", "na", "w", "z", "się", "że", "do", "i", "a", "o",
            "ale", "jego", "jej", "ich", "my", "wy", "oni", "one", "jak", "co", "gdy",
            "gdzie", "dlaczego", "który", "która", "które", "bardzo", "może", "może być"
        }
        
        logger.info("🇵🇱 PolishOptimizedSTT zainicjalizowany z optymalizacjami dla polskiego")
    
    def post_process_polish_text(self, text: str) -> str:
        """
        Post-processing specyficzny dla polskiego języka
        
        Args:
            text: Surowy tekst z Whisper
            
        Returns:
            Przetworzony tekst
        """
        if not text:
            return text
        
        # Podstawowe poprawki dla polskiego
        corrections = {
            # Częste błędy Whisper dla polskiego (brak polskich znaków)
            " sie ": " się ",   # się
            " ze ": " że ",     # że (tylko jeśli poprzedzone spacją)
            "ze ": "że ",       # że na początku
        }
        
        processed_text = text
        
        # Zastosuj podstawowe korekty
        for wrong, correct in corrections.items():
            if wrong in processed_text.lower():
                # Zachowaj oryginalne wielkości liter
                processed_text = processed_text.replace(wrong, correct)
        
        # Kapitalizacja pierwszej litery
        if processed_text:
            processed_text = processed_text[0].upper() + processed_text[1:]
        
        return processed_text.strip()
    
    def transcribe_audio(self, audio_data: np.ndarray, sample_rate: int = 16000) -> Optional[TranscriptionResult]:
        """
        Transkrypcja z post-processingiem dla polskiego
        """
        result = super().transcribe_audio(audio_data, sample_rate)
        
        if result and result.text:
            # Zastosuj post-processing dla polskiego
            original_text = result.text
            processed_text = self.post_process_polish_text(original_text)
            
            # Utwórz nowy wynik z przetworzonym tekstem
            result = TranscriptionResult(
                text=processed_text,
                language=result.language,
                confidence=result.confidence,
                processing_time=result.processing_time,
                segments=result.segments,
                model_used=result.model_used
            )
            
            if processed_text != original_text:
                logger.debug(f"🇵🇱 Polish post-processing: '{original_text}' -> '{processed_text}'")
        
        return result
