"""
GUI Application for Real-time Speech-to-Text Polish
Aplikacja GUI dla Real-time Speech-to-Text Polski

Autor: AI Assistant
Data: 2025-01-18
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import queue
import time
import json
import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any
import logging

# Import naszych modułów
# Dodaj src do ścieżki jeśli jeszcze nie ma
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from realtime_pipeline import RealtimeSTTPipeline, SpeechSegment
from voice_activity_detector import VADMode

# Konfiguracja loggingu
logger = logging.getLogger(__name__)

class STTGuiApplication:
    """
    Główna aplikacja GUI dla Real-time Speech-to-Text
    """
    
    def __init__(self):
        """Inicjalizacja aplikacji GUI"""
        self.root = tk.Tk()
        self.root.title("🎤 Real-time Speech-to-Text - Polski")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Stan aplikacji
        self.pipeline: Optional[RealtimeSTTPipeline] = None
        self.is_recording = False
        self.transcriptions = []
        self.stats_queue = queue.Queue()
        
        # Konfiguracja
        self.config = {
            "model": "base",
            "language": "pl",
            "vad_mode": "normal",
            "min_segment_duration": 1.0,
            "silence_timeout": 2.0,
            "auto_save": True,
            "show_confidence": True,
            "show_timing": True
        }
        
        # Ładuj konfigurację
        self.load_config()
        
        # Stwórz interface
        self.create_interface()
        
        # Uruchom aktualizację statystyk
        self.update_stats()
        
        logger.info("🎨 GUI Application initialized")
    
    def create_interface(self):
        """Stwórz główny interface"""
        # Menu bar
        self.create_menu()
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Control panel (left)
        self.create_control_panel(main_frame)
        
        # Transcription area (right)
        self.create_transcription_area(main_frame)
        
        # Status bar (bottom)
        self.create_status_bar(main_frame)
        
        # Bind events
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_menu(self):
        """Stwórz menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Plik", menu=file_menu)
        file_menu.add_command(label="Nowa sesja", command=self.new_session)
        file_menu.add_command(label="Zapisz transkrypcję...", command=self.save_transcription)
        file_menu.add_command(label="Wczytaj plik audio...", command=self.load_audio_file)
        file_menu.add_separator()
        file_menu.add_command(label="Wyjście", command=self.on_closing)
        
        # Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ustawienia", menu=settings_menu)
        settings_menu.add_command(label="Konfiguracja...", command=self.show_settings)
        settings_menu.add_command(label="Test audio...", command=self.test_audio)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Pomoc", menu=help_menu)
        help_menu.add_command(label="O programie", command=self.show_about)
        help_menu.add_command(label="Skróty klawiszowe", command=self.show_shortcuts)
    
    def create_control_panel(self, parent):
        """Stwórz panel kontrolny"""
        # Control frame
        control_frame = ttk.LabelFrame(parent, text="Kontrola", padding="10")
        control_frame.grid(row=0, column=0, rowspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Record button
        self.record_button = ttk.Button(
            control_frame, 
            text="🎤 Rozpocznij\nnagrywanie",
            command=self.toggle_recording,
            width=15
        )
        self.record_button.grid(row=0, column=0, pady=5, sticky=tk.W+tk.E)
        
        # Settings frame
        settings_frame = ttk.LabelFrame(control_frame, text="Ustawienia", padding="5")
        settings_frame.grid(row=1, column=0, pady=10, sticky=(tk.W, tk.E))
        
        # Model selection
        ttk.Label(settings_frame, text="Model:").grid(row=0, column=0, sticky=tk.W)
        self.model_var = tk.StringVar(value=self.config["model"])
        model_combo = ttk.Combobox(
            settings_frame, 
            textvariable=self.model_var,
            values=["tiny", "base", "small", "medium", "large"],
            state="readonly",
            width=12
        )
        model_combo.grid(row=0, column=1, padx=5, sticky=tk.W+tk.E)
        model_combo.bind("<<ComboboxSelected>>", self.on_model_changed)
        
        # VAD mode
        ttk.Label(settings_frame, text="VAD:").grid(row=1, column=0, sticky=tk.W)
        self.vad_var = tk.StringVar(value=self.config["vad_mode"])
        vad_combo = ttk.Combobox(
            settings_frame,
            textvariable=self.vad_var,
            values=["permissive", "normal", "aggressive", "very_aggressive"],
            state="readonly",
            width=12
        )
        vad_combo.grid(row=1, column=1, padx=5, sticky=tk.W+tk.E)
        
        # Audio level indicator
        self.create_audio_level_indicator(control_frame)
        
        # Statistics
        self.create_statistics_panel(control_frame)
    
    def create_audio_level_indicator(self, parent):
        """Stwórz wskaźnik poziomu audio"""
        level_frame = ttk.LabelFrame(parent, text="Poziom audio", padding="5")
        level_frame.grid(row=2, column=0, pady=10, sticky=(tk.W, tk.E))
        
        # Progress bar for audio level
        self.audio_level_var = tk.DoubleVar()
        self.audio_level_bar = ttk.Progressbar(
            level_frame,
            variable=self.audio_level_var,
            maximum=100,
            length=150
        )
        self.audio_level_bar.grid(row=0, column=0, pady=5)
        
        # VAD indicator
        self.vad_indicator = tk.Label(
            level_frame,
            text="🔇 Cisza",
            background="lightgray"
        )
        self.vad_indicator.grid(row=1, column=0, pady=5)
    
    def create_statistics_panel(self, parent):
        """Stwórz panel statystyk"""
        stats_frame = ttk.LabelFrame(parent, text="Statystyki", padding="5")
        stats_frame.grid(row=3, column=0, pady=10, sticky=(tk.W, tk.E))
        
        # Statistics labels
        self.stats_labels = {}
        
        stats_items = [
            ("Czas:", "session_time"),
            ("Segmenty:", "segments_count"),
            ("Słowa:", "words_count"),
            ("Średnia pewność:", "avg_confidence")
        ]
        
        for i, (label, key) in enumerate(stats_items):
            ttk.Label(stats_frame, text=label).grid(row=i, column=0, sticky=tk.W)
            self.stats_labels[key] = ttk.Label(stats_frame, text="0")
            self.stats_labels[key].grid(row=i, column=1, sticky=tk.E, padx=5)
    
    def create_transcription_area(self, parent):
        """Stwórz obszar transkrypcji"""
        # Transcription frame
        trans_frame = ttk.LabelFrame(parent, text="Transkrypcja", padding="5")
        trans_frame.grid(row=0, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        trans_frame.columnconfigure(0, weight=1)
        trans_frame.rowconfigure(0, weight=1)
        
        # Text area with scrollbar
        self.transcription_text = scrolledtext.ScrolledText(
            trans_frame,
            wrap=tk.WORD,
            width=50,
            height=20,
            font=("Arial", 11)
        )
        self.transcription_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Control buttons
        button_frame = ttk.Frame(trans_frame)
        button_frame.grid(row=1, column=0, pady=5, sticky=tk.W+tk.E)
        
        ttk.Button(button_frame, text="Wyczyść", command=self.clear_transcription).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Kopiuj", command=self.copy_transcription).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Zapisz", command=self.save_transcription).pack(side=tk.LEFT, padx=5)
        
        # Options
        self.show_confidence_var = tk.BooleanVar(value=self.config["show_confidence"])
        self.show_timing_var = tk.BooleanVar(value=self.config["show_timing"])
        
        ttk.Checkbutton(button_frame, text="Pewność", variable=self.show_confidence_var).pack(side=tk.RIGHT, padx=5)
        ttk.Checkbutton(button_frame, text="Czas", variable=self.show_timing_var).pack(side=tk.RIGHT, padx=5)
    
    def create_status_bar(self, parent):
        """Stwórz status bar"""
        self.status_bar = ttk.Label(
            parent,
            text="Gotowy do nagrywania",
            relief=tk.SUNKEN
        )
        self.status_bar.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def toggle_recording(self):
        """Przełącz nagrywanie"""
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()
    
    def start_recording(self):
        """Rozpocznij nagrywanie"""
        try:
            # Stwórz pipeline
            vad_mode_map = {
                "permissive": VADMode.PERMISSIVE,
                "normal": VADMode.NORMAL,
                "aggressive": VADMode.AGGRESSIVE,
                "very_aggressive": VADMode.VERY_AGGRESSIVE
            }
            
            self.pipeline = RealtimeSTTPipeline(
                sample_rate=16000,
                enable_stt=True,
                stt_model=self.model_var.get(),
                vad_mode=vad_mode_map[self.vad_var.get()],
                use_polish_optimization=True,
                min_segment_duration=self.config["min_segment_duration"],
                silence_timeout=self.config["silence_timeout"]
            )
            
            # Ustaw callback
            self.pipeline.set_speech_callback(self.on_speech_detected)
            
            # Rozpocznij nagrywanie
            self.update_status("Ładowanie modelu STT...")
            if not self.pipeline.load_stt_model():
                raise Exception("Nie można załadować modelu STT")
            
            self.pipeline.start()
            
            # Aktualizuj UI
            self.is_recording = True
            self.record_button.config(text="⏹️ Zatrzymaj\nnagrywanie")
            self.update_status("Nagrywanie... Mów do mikrofonu")
            
            logger.info("🎤 Recording started")
            
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie można rozpocząć nagrywania:\n{e}")
            logger.error(f"Recording start failed: {e}")
    
    def stop_recording(self):
        """Zatrzymaj nagrywanie"""
        if self.pipeline:
            self.pipeline.stop()
            self.pipeline = None
        
        self.is_recording = False
        self.record_button.config(text="🎤 Rozpocznij\nnagrywanie")
        self.update_status("Nagrywanie zatrzymane")
        self.vad_indicator.config(text="🔇 Cisza", background="lightgray")
        self.audio_level_var.set(0)
        
        logger.info("⏹️ Recording stopped")
    
    def on_speech_detected(self, segment: SpeechSegment):
        """Callback dla wykrytych segmentów mowy"""
        try:
            # Dodaj do kolejki (thread-safe)
            self.stats_queue.put(("speech", segment))
            
            # Formatuj tekst
            text_parts = []
            
            if self.show_timing_var.get():
                timestamp = time.strftime("%H:%M:%S", time.localtime(segment.start_time))
                text_parts.append(f"[{timestamp}]")
            
            if segment.transcription and segment.text:
                text_parts.append(segment.text)
                
                if self.show_confidence_var.get():
                    confidence = segment.transcription.confidence
                    text_parts.append(f"({confidence:.2f})")
            else:
                text_parts.append("[brak transkrypcji]")
            
            formatted_text = " ".join(text_parts) + "\n\n"
            
            # Dodaj do UI (thread-safe)
            self.root.after(0, self.add_transcription_text, formatted_text)
            
            # Zapisz w historii
            self.transcriptions.append(segment)
            
        except Exception as e:
            logger.error(f"Speech callback error: {e}")
    
    def add_transcription_text(self, text: str):
        """Dodaj tekst do obszaru transkrypcji"""
        self.transcription_text.insert(tk.END, text)
        self.transcription_text.see(tk.END)
        
        # Auto-save jeśli włączony
        if self.config["auto_save"]:
            self.auto_save_session()
    
    def update_stats(self):
        """Aktualizuj statystyki"""
        try:
            # Przetwórz elementy z kolejki
            while True:
                try:
                    item_type, data = self.stats_queue.get_nowait()
                    
                    if item_type == "speech":
                        self.update_speech_stats(data)
                    elif item_type == "audio_level":
                        self.update_audio_level(data)
                    elif item_type == "vad":
                        self.update_vad_indicator(data)
                        
                except queue.Empty:
                    break
            
            # Aktualizuj czas sesji
            if self.is_recording and self.pipeline:
                stats = self.pipeline.get_statistics()
                runtime = stats['pipeline']['runtime_seconds']
                self.stats_labels['session_time'].config(text=f"{runtime:.0f}s")
        
        except Exception as e:
            logger.error(f"Stats update error: {e}")
        
        # Zaplanuj następną aktualizację
        self.root.after(100, self.update_stats)
    
    def update_speech_stats(self, segment: SpeechSegment):
        """Aktualizuj statystyki mowy"""
        # Liczba segmentów
        segments_count = len(self.transcriptions)
        self.stats_labels['segments_count'].config(text=str(segments_count))
        
        # Liczba słów
        words_count = sum(len(s.text.split()) for s in self.transcriptions if s.text)
        self.stats_labels['words_count'].config(text=str(words_count))
        
        # Średnia pewność
        confidences = [s.transcription.confidence for s in self.transcriptions 
                      if s.transcription and s.transcription.confidence]
        if confidences:
            avg_confidence = sum(confidences) / len(confidences)
            self.stats_labels['avg_confidence'].config(text=f"{avg_confidence:.2f}")
    
    def update_audio_level(self, level: float):
        """Aktualizuj poziom audio"""
        # Konwertuj z dB na procenty
        level_percent = max(0, min(100, (level + 60) * 100 / 60))  # -60dB to 0dB -> 0% to 100%
        self.audio_level_var.set(level_percent)
    
    def update_vad_indicator(self, is_speech: bool):
        """Aktualizuj wskaźnik VAD"""
        if is_speech:
            self.vad_indicator.config(text="🎤 Mowa", background="lightgreen")
        else:
            self.vad_indicator.config(text="🔇 Cisza", background="lightgray")
    
    def update_status(self, message: str):
        """Aktualizuj status bar"""
        self.status_bar.config(text=message)
    
    def on_model_changed(self, event=None):
        """Obsługa zmiany modelu"""
        if self.is_recording:
            result = messagebox.askyesno(
                "Zmiana modelu",
                "Zmiana modelu wymaga restartu nagrywania. Kontynuować?"
            )
            if result:
                self.stop_recording()
                self.config["model"] = self.model_var.get()
                self.save_config()
    
    def new_session(self):
        """Nowa sesja"""
        if self.is_recording:
            self.stop_recording()
        
        self.transcriptions.clear()
        self.clear_transcription()
        self.update_status("Nowa sesja rozpoczęta")
    
    def clear_transcription(self):
        """Wyczyść obszar transkrypcji"""
        self.transcription_text.delete(1.0, tk.END)
    
    def copy_transcription(self):
        """Kopiuj transkrypcję do schowka"""
        text = self.transcription_text.get(1.0, tk.END)
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.update_status("Transkrypcja skopiowana do schowka")
    
    def save_transcription(self):
        """Zapisz transkrypcję do pliku"""
        if not self.transcriptions:
            messagebox.showwarning("Brak danych", "Brak transkrypcji do zapisania")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("JSON files", "*.json"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            try:
                if filename.endswith('.json'):
                    self.save_as_json(filename)
                else:
                    self.save_as_text(filename)
                
                self.update_status(f"Transkrypcja zapisana: {filename}")
                
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie można zapisać pliku:\n{e}")
    
    def save_as_text(self, filename: str):
        """Zapisz jako plik tekstowy"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("Real-time Speech-to-Text - Transkrypcja\n")
            f.write("=" * 50 + "\n\n")
            
            for segment in self.transcriptions:
                if segment.text:
                    timestamp = time.strftime("%H:%M:%S", time.localtime(segment.start_time))
                    f.write(f"[{timestamp}] {segment.text}\n")
                    
                    if segment.transcription:
                        f.write(f"    Pewność: {segment.transcription.confidence:.2f}\n")
                        f.write(f"    Czas przetwarzania: {segment.transcription.processing_time:.2f}s\n")
                    f.write("\n")
    
    def save_as_json(self, filename: str):
        """Zapisz jako plik JSON"""
        data = {
            "session_info": {
                "timestamp": time.time(),
                "model_used": self.model_var.get(),
                "vad_mode": self.vad_var.get(),
                "total_segments": len(self.transcriptions)
            },
            "transcriptions": []
        }
        
        for segment in self.transcriptions:
            segment_data = {
                "start_time": segment.start_time,
                "end_time": segment.end_time,
                "duration": segment.duration,
                "text": segment.text,
                "confidence": segment.transcription.confidence if segment.transcription else None,
                "processing_time": segment.transcription.processing_time if segment.transcription else None
            }
            data["transcriptions"].append(segment_data)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def auto_save_session(self):
        """Automatyczne zapisywanie sesji"""
        # Implementacja auto-save w tle
        pass
    
    def load_audio_file(self):
        """Wczytaj plik audio do przetworzenia"""
        messagebox.showinfo("Funkcja", "Przetwarzanie plików audio - w przyszłej wersji")
    
    def test_audio(self):
        """Test systemu audio"""
        def run_audio_test():
            try:
                from audio_capture import AudioCapture
                
                capture = AudioCapture()
                self.update_status("Test audio - nagrywanie 3 sekundy...")
                
                capture.start_recording()
                time.sleep(3)
                capture.stop_recording()
                
                stats = capture.get_statistics()
                
                if stats['total_frames'] > 0:
                    messagebox.showinfo(
                        "Test audio", 
                        f"Test zakończony pomyślnie!\n\n"
                        f"Ramki: {stats['total_frames']}\n"
                        f"Pominięte: {stats['dropped_frames']}\n"
                        f"Współczynnik strat: {stats['drop_rate']:.2%}"
                    )
                else:
                    messagebox.showwarning("Test audio", "Brak sygnału audio")
                
                self.update_status("Test audio zakończony")
                
            except Exception as e:
                messagebox.showerror("Błąd testu audio", str(e))
        
        threading.Thread(target=run_audio_test, daemon=True).start()
    
    def show_settings(self):
        """Pokaż okno ustawień"""
        SettingsWindow(self.root, self.config, self.on_settings_changed)
    
    def on_settings_changed(self, new_config: Dict[str, Any]):
        """Obsługa zmiany ustawień"""
        self.config.update(new_config)
        self.save_config()
        
        # Aktualizuj UI
        self.model_var.set(self.config["model"])
        self.vad_var.set(self.config["vad_mode"])
        
        self.update_status("Ustawienia zaktualizowane")
    
    def show_about(self):
        """Pokaż okno o programie"""
        about_text = """Real-time Speech-to-Text Polish v1.0.0

🎤 System rozpoznawania mowy w czasie rzeczywistym
zoptymalizowany dla języka polskiego.

Funkcjonalności:
• Real-time transkrypcja z mikrofonu
• Zaawansowana detekcja aktywności głosowej (VAD)
• Optymalizacje dla języka polskiego
• Eksport transkrypcji (TXT, JSON)
• Konfigurowalny interfejs

Technologie:
• OpenAI Whisper (silnik STT)
• WebRTC VAD
• Python + Tkinter

Autor: AI Assistant
Data: 2025-01-18
"""
        messagebox.showinfo("O programie", about_text)
    
    def show_shortcuts(self):
        """Pokaż skróty klawiszowe"""
        shortcuts_text = """Skróty klawiszowe:

Ctrl+R - Rozpocznij/zatrzymaj nagrywanie
Ctrl+N - Nowa sesja
Ctrl+S - Zapisz transkrypcję
Ctrl+C - Kopiuj transkrypcję
Ctrl+L - Wyczyść transkrypcję
Ctrl+T - Test audio
Ctrl+, - Ustawienia
F1 - Pomoc
Esc - Wyjście
"""
        messagebox.showinfo("Skróty klawiszowe", shortcuts_text)
    
    def load_config(self):
        """Załaduj konfigurację z pliku"""
        config_file = Path("config.json")
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    saved_config = json.load(f)
                    self.config.update(saved_config)
            except Exception as e:
                logger.warning(f"Cannot load config: {e}")
    
    def save_config(self):
        """Zapisz konfigurację do pliku"""
        try:
            with open("config.json", 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            logger.warning(f"Cannot save config: {e}")
    
    def on_closing(self):
        """Obsługa zamknięcia aplikacji"""
        if self.is_recording:
            result = messagebox.askyesno(
                "Zamknięcie",
                "Nagrywanie jest aktywne. Czy na pewno chcesz zamknąć aplikację?"
            )
            if not result:
                return
            
            self.stop_recording()
        
        self.save_config()
        self.root.destroy()
    
    def run(self):
        """Uruchom aplikację"""
        self.root.mainloop()


class SettingsWindow:
    """Okno ustawień"""
    
    def __init__(self, parent, config: Dict[str, Any], callback):
        self.config = config.copy()
        self.callback = callback
        
        # Stwórz okno
        self.window = tk.Toplevel(parent)
        self.window.title("Ustawienia")
        self.window.geometry("400x500")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()
        
        self.create_interface()
    
    def create_interface(self):
        """Stwórz interface ustawień"""
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Model settings
        model_frame = ttk.LabelFrame(main_frame, text="Model STT", padding="10")
        model_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(model_frame, text="Model Whisper:").pack(anchor=tk.W)
        self.model_var = tk.StringVar(value=self.config["model"])
        model_combo = ttk.Combobox(
            model_frame,
            textvariable=self.model_var,
            values=["tiny", "base", "small", "medium", "large"],
            state="readonly"
        )
        model_combo.pack(fill=tk.X, pady=5)
        
        # VAD settings
        vad_frame = ttk.LabelFrame(main_frame, text="Voice Activity Detection", padding="10")
        vad_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(vad_frame, text="Tryb VAD:").pack(anchor=tk.W)
        self.vad_var = tk.StringVar(value=self.config["vad_mode"])
        vad_combo = ttk.Combobox(
            vad_frame,
            textvariable=self.vad_var,
            values=["permissive", "normal", "aggressive", "very_aggressive"],
            state="readonly"
        )
        vad_combo.pack(fill=tk.X, pady=5)
        
        # Timing settings
        timing_frame = ttk.LabelFrame(main_frame, text="Ustawienia czasowe", padding="10")
        timing_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(timing_frame, text="Min. długość segmentu (s):").pack(anchor=tk.W)
        self.min_duration_var = tk.DoubleVar(value=self.config["min_segment_duration"])
        min_duration_scale = ttk.Scale(
            timing_frame,
            from_=0.1,
            to=5.0,
            variable=self.min_duration_var,
            orient=tk.HORIZONTAL
        )
        min_duration_scale.pack(fill=tk.X, pady=5)
        
        ttk.Label(timing_frame, text="Timeout ciszy (s):").pack(anchor=tk.W)
        self.silence_timeout_var = tk.DoubleVar(value=self.config["silence_timeout"])
        silence_scale = ttk.Scale(
            timing_frame,
            from_=0.5,
            to=5.0,
            variable=self.silence_timeout_var,
            orient=tk.HORIZONTAL
        )
        silence_scale.pack(fill=tk.X, pady=5)
        
        # Interface settings
        ui_frame = ttk.LabelFrame(main_frame, text="Interfejs", padding="10")
        ui_frame.pack(fill=tk.X, pady=5)
        
        self.auto_save_var = tk.BooleanVar(value=self.config["auto_save"])
        ttk.Checkbutton(ui_frame, text="Automatyczne zapisywanie", variable=self.auto_save_var).pack(anchor=tk.W)
        
        self.show_confidence_var = tk.BooleanVar(value=self.config["show_confidence"])
        ttk.Checkbutton(ui_frame, text="Pokaż pewność transkrypcji", variable=self.show_confidence_var).pack(anchor=tk.W)
        
        self.show_timing_var = tk.BooleanVar(value=self.config["show_timing"])
        ttk.Checkbutton(ui_frame, text="Pokaż znaczniki czasu", variable=self.show_timing_var).pack(anchor=tk.W)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="OK", command=self.save_settings).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Anuluj", command=self.window.destroy).pack(side=tk.RIGHT)
        ttk.Button(button_frame, text="Domyślne", command=self.reset_to_defaults).pack(side=tk.LEFT)
    
    def save_settings(self):
        """Zapisz ustawienia"""
        self.config.update({
            "model": self.model_var.get(),
            "vad_mode": self.vad_var.get(),
            "min_segment_duration": self.min_duration_var.get(),
            "silence_timeout": self.silence_timeout_var.get(),
            "auto_save": self.auto_save_var.get(),
            "show_confidence": self.show_confidence_var.get(),
            "show_timing": self.show_timing_var.get()
        })
        
        self.callback(self.config)
        self.window.destroy()
    
    def reset_to_defaults(self):
        """Reset do ustawień domyślnych"""
        self.model_var.set("base")
        self.vad_var.set("normal")
        self.min_duration_var.set(1.0)
        self.silence_timeout_var.set(2.0)
        self.auto_save_var.set(True)
        self.show_confidence_var.set(True)
        self.show_timing_var.set(True)


def main():
    """Główna funkcja GUI"""
    try:
        app = STTGuiApplication()
        app.run()
    except Exception as e:
        logging.error(f"GUI Application error: {e}")
        messagebox.showerror("Błąd", f"Błąd aplikacji GUI:\n{e}")

if __name__ == "__main__":
    main()
