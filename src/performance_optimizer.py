"""
Performance Optimizer for Real-time STT
Optymalizator wydajności dla Real-time STT

Autor: AI Assistant
Data: 2025-01-18
"""

import gc
import threading
import time
import psutil
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetrics:
    """Metryki wydajności systemu"""
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    memory_available_mb: float
    gpu_memory_used_mb: Optional[float]
    gpu_memory_total_mb: Optional[float]
    active_threads: int
    queue_sizes: Dict[str, int]
    processing_times: Dict[str, float]
    
    @property
    def memory_usage_ratio(self) -> float:
        """Stosunek używanej pamięci do dostępnej"""
        return self.memory_used_mb / max(self.memory_available_mb, 1)
    
    @property
    def is_memory_critical(self) -> bool:
        """Czy pamięć jest na krytycznym poziomie"""
        return self.memory_percent > 85.0
    
    @property
    def is_cpu_overloaded(self) -> bool:
        """Czy CPU jest przeciążony"""
        return self.cpu_percent > 80.0

class PerformanceOptimizer:
    """
    Optymalizator wydajności dla Real-time STT
    """
    
    def __init__(
        self,
        enable_monitoring: bool = True,
        optimize_memory: bool = True,
        optimize_threads: bool = True,
        monitoring_interval: float = 1.0
    ):
        """
        Inicjalizacja optimizera
        
        Args:
            enable_monitoring: Czy włączyć monitoring wydajności
            optimize_memory: Czy włączyć optymalizację pamięci
            optimize_threads: Czy włączyć optymalizację wątków
            monitoring_interval: Interwał monitoringu w sekundach
        """
        self.enable_monitoring = enable_monitoring
        self.optimize_memory = optimize_memory
        self.optimize_threads = optimize_threads
        self.monitoring_interval = monitoring_interval
        
        # Stan monitoringu
        self.is_monitoring = False
        self.monitoring_thread: Optional[threading.Thread] = None
        self.metrics_history: List[PerformanceMetrics] = []
        self.max_history_size = 60  # 1 minuta przy 1s interwale
        
        # Optymalizacje
        self.thread_pool: Optional[ThreadPoolExecutor] = None
        self.memory_threshold = 80.0  # %
        self.cpu_threshold = 75.0     # %
        
        # Callbacks
        self.performance_callbacks = []
        
        logger.info(f"🚀 PerformanceOptimizer zainicjalizowany")
    
    def start_monitoring(self):
        """Rozpocznij monitoring wydajności"""
        if self.is_monitoring:
            logger.warning("⚠️ Monitoring już uruchomiony")
            return
        
        if not self.enable_monitoring:
            logger.info("📊 Monitoring wyłączony")
            return
        
        self.is_monitoring = True
        self.monitoring_thread = threading.Thread(
            target=self._monitoring_loop,
            daemon=True,
            name="PerformanceMonitor"
        )
        self.monitoring_thread.start()
        
        logger.info("📊 Monitoring wydajności uruchomiony")
    
    def stop_monitoring(self):
        """Zatrzymaj monitoring wydajności"""
        if not self.is_monitoring:
            return
        
        self.is_monitoring = False
        
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            self.monitoring_thread.join(timeout=2.0)
        
        logger.info("📊 Monitoring wydajności zatrzymany")
    
    def _monitoring_loop(self):
        """Główna pętla monitoringu"""
        while self.is_monitoring:
            try:
                # Zbierz metryki
                metrics = self.collect_metrics()
                
                # Dodaj do historii
                self.metrics_history.append(metrics)
                if len(self.metrics_history) > self.max_history_size:
                    self.metrics_history.pop(0)
                
                # Sprawdź czy potrzeba optymalizacji
                self._check_optimization_triggers(metrics)
                
                # Wywołaj callbacks
                for callback in self.performance_callbacks:
                    try:
                        callback(metrics)
                    except Exception as e:
                        logger.error(f"❌ Performance callback error: {e}")
                
                # Oczekaj do następnego cyklu
                time.sleep(self.monitoring_interval)
                
            except Exception as e:
                logger.error(f"❌ Monitoring loop error: {e}")
                time.sleep(self.monitoring_interval)
    
    def collect_metrics(self) -> PerformanceMetrics:
        """Zbierz aktualne metryki wydajności"""
        try:
            # CPU i pamięć systemu
            cpu_percent = psutil.cpu_percent(interval=None)
            memory = psutil.virtual_memory()
            
            # GPU metrics (jeśli dostępne)
            gpu_memory_used = None
            gpu_memory_total = None
            
            try:
                import torch
                if torch.cuda.is_available():
                    gpu_memory_used = torch.cuda.memory_allocated() / 1024**2  # MB
                    gpu_memory_total = torch.cuda.get_device_properties(0).total_memory / 1024**2  # MB
            except ImportError:
                pass
            
            # Wątki
            active_threads = threading.active_count()
            
            # Queue sizes (jeśli dostępne)
            queue_sizes = self._get_queue_sizes()
            
            # Processing times (placeholder)
            processing_times = self._get_processing_times()
            
            return PerformanceMetrics(
                cpu_percent=cpu_percent,
                memory_percent=memory.percent,
                memory_used_mb=memory.used / 1024**2,
                memory_available_mb=memory.available / 1024**2,
                gpu_memory_used_mb=gpu_memory_used,
                gpu_memory_total_mb=gpu_memory_total,
                active_threads=active_threads,
                queue_sizes=queue_sizes,
                processing_times=processing_times
            )
            
        except Exception as e:
            logger.error(f"❌ Metrics collection error: {e}")
            # Zwróć domyślne metryki
            return PerformanceMetrics(
                cpu_percent=0.0,
                memory_percent=0.0,
                memory_used_mb=0.0,
                memory_available_mb=1000.0,
                gpu_memory_used_mb=None,
                gpu_memory_total_mb=None,
                active_threads=1,
                queue_sizes={},
                processing_times={}
            )
    
    def _get_queue_sizes(self) -> Dict[str, int]:
        """Pobierz rozmiary kolejek (implementacja specyficzna dla pipeline)"""
        # TODO: Integracja z RealtimePipeline
        return {}
    
    def _get_processing_times(self) -> Dict[str, float]:
        """Pobierz czasy przetwarzania"""
        # TODO: Integracja z komponentami
        return {}
    
    def _check_optimization_triggers(self, metrics: PerformanceMetrics):
        """Sprawdź czy potrzeba optymalizacji"""
        try:
            # Memory optimization
            if self.optimize_memory and metrics.is_memory_critical:
                logger.warning(f"⚠️ Krytyczny poziom pamięci: {metrics.memory_percent:.1f}%")
                self.optimize_memory_usage()
            
            # CPU optimization
            if metrics.is_cpu_overloaded:
                logger.warning(f"⚠️ Przeciążenie CPU: {metrics.cpu_percent:.1f}%")
                self.optimize_cpu_usage()
            
            # GPU memory optimization
            if (metrics.gpu_memory_used_mb and metrics.gpu_memory_total_mb and
                metrics.gpu_memory_used_mb / metrics.gpu_memory_total_mb > 0.9):
                logger.warning("⚠️ Krytyczny poziom pamięci GPU")
                self.optimize_gpu_memory()
                
        except Exception as e:
            logger.error(f"❌ Optimization trigger error: {e}")
    
    def optimize_memory_usage(self):
        """Optymalizuj użycie pamięci"""
        try:
            logger.info("🧹 Optymalizacja pamięci...")
            
            # Wymuś garbage collection
            collected = gc.collect()
            logger.info(f"🗑️ Garbage collection: {collected} obiektów")
            
            # GPU memory cleanup (jeśli dostępne)
            try:
                import torch
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                    logger.info("🔥 GPU cache wyczyszczony")
            except ImportError:
                pass
            
            # TODO: Dodatkowe optymalizacje specyficzne dla aplikacji
            
        except Exception as e:
            logger.error(f"❌ Memory optimization error: {e}")
    
    def optimize_cpu_usage(self):
        """Optymalizuj użycie CPU"""
        try:
            logger.info("⚡ Optymalizacja CPU...")
            
            # TODO: Implementacja optymalizacji CPU
            # - Redukcja częstotliwości próbkowania
            # - Zwiększenie chunk size
            # - Ograniczenie liczby wątków
            
        except Exception as e:
            logger.error(f"❌ CPU optimization error: {e}")
    
    def optimize_gpu_memory(self):
        """Optymalizuj pamięć GPU"""
        try:
            logger.info("🔥 Optymalizacja pamięci GPU...")
            
            import torch
            if torch.cuda.is_available():
                # Wyczyść cache
                torch.cuda.empty_cache()
                
                # TODO: Dodatkowe optymalizacje GPU
                # - Redukcja batch size
                # - Użycie half precision
                
        except ImportError:
            pass
        except Exception as e:
            logger.error(f"❌ GPU optimization error: {e}")
    
    def get_current_metrics(self) -> Optional[PerformanceMetrics]:
        """Pobierz aktualne metryki"""
        if self.metrics_history:
            return self.metrics_history[-1]
        return self.collect_metrics()
    
    def get_metrics_history(self, last_n: Optional[int] = None) -> List[PerformanceMetrics]:
        """Pobierz historię metryki"""
        if last_n is None:
            return self.metrics_history.copy()
        return self.metrics_history[-last_n:] if self.metrics_history else []
    
    def get_average_metrics(self, last_n: int = 10) -> Optional[PerformanceMetrics]:
        """Pobierz średnie metryki z ostatnich N pomiarów"""
        if not self.metrics_history:
            return None
        
        recent_metrics = self.get_metrics_history(last_n)
        if not recent_metrics:
            return None
        
        # Oblicz średnie
        avg_cpu = sum(m.cpu_percent for m in recent_metrics) / len(recent_metrics)
        avg_memory = sum(m.memory_percent for m in recent_metrics) / len(recent_metrics)
        avg_memory_used = sum(m.memory_used_mb for m in recent_metrics) / len(recent_metrics)
        avg_threads = sum(m.active_threads for m in recent_metrics) / len(recent_metrics)
        
        # GPU średnie (jeśli dostępne)
        gpu_metrics = [m for m in recent_metrics if m.gpu_memory_used_mb is not None]
        avg_gpu_used = (
            sum(m.gpu_memory_used_mb for m in gpu_metrics) / len(gpu_metrics)
            if gpu_metrics else None
        )
        avg_gpu_total = (
            recent_metrics[0].gpu_memory_total_mb 
            if recent_metrics and recent_metrics[0].gpu_memory_total_mb else None
        )
        
        return PerformanceMetrics(
            cpu_percent=avg_cpu,
            memory_percent=avg_memory,
            memory_used_mb=avg_memory_used,
            memory_available_mb=recent_metrics[-1].memory_available_mb,
            gpu_memory_used_mb=avg_gpu_used,
            gpu_memory_total_mb=avg_gpu_total,
            active_threads=int(avg_threads),
            queue_sizes=recent_metrics[-1].queue_sizes,
            processing_times=recent_metrics[-1].processing_times
        )
    
    def add_performance_callback(self, callback):
        """Dodaj callback dla metryki wydajności"""
        self.performance_callbacks.append(callback)
        logger.info("📊 Performance callback dodany")
    
    def remove_performance_callback(self, callback):
        """Usuń callback"""
        if callback in self.performance_callbacks:
            self.performance_callbacks.remove(callback)
            logger.info("📊 Performance callback usunięty")
    
    def get_optimization_recommendations(self) -> List[str]:
        """Pobierz rekomendacje optymalizacji"""
        recommendations = []
        
        current_metrics = self.get_current_metrics()
        if not current_metrics:
            return recommendations
        
        # Memory recommendations
        if current_metrics.memory_percent > 70:
            recommendations.append("💾 Rozważ zamknięcie innych aplikacji aby zwolnić pamięć")
            
        if current_metrics.memory_percent > 85:
            recommendations.append("🚨 Krytyczny poziom pamięci - restart aplikacji zalecany")
        
        # CPU recommendations
        if current_metrics.cpu_percent > 70:
            recommendations.append("⚡ Wysokie obciążenie CPU - rozważ użycie mniejszego modelu STT")
            
        if current_metrics.cpu_percent > 85:
            recommendations.append("🔥 Przeciążenie CPU - zamknij inne aplikacje")
        
        # GPU recommendations
        if (current_metrics.gpu_memory_used_mb and current_metrics.gpu_memory_total_mb):
            gpu_usage = current_metrics.gpu_memory_used_mb / current_metrics.gpu_memory_total_mb
            
            if gpu_usage > 0.8:
                recommendations.append("🔥 Wysokie użycie pamięci GPU - rozważ mniejszy model")
            
            if gpu_usage > 0.95:
                recommendations.append("🚨 Krytyczny poziom pamięci GPU - zmniejsz batch size")
        
        # Thread recommendations
        if current_metrics.active_threads > 20:
            recommendations.append("🧵 Duża liczba wątków - możliwa optymalizacja threading")
        
        return recommendations
    
    def generate_performance_report(self) -> Dict[str, Any]:
        """Wygeneruj raport wydajności"""
        current = self.get_current_metrics()
        average = self.get_average_metrics()
        recommendations = self.get_optimization_recommendations()
        
        return {
            "timestamp": time.time(),
            "current_metrics": current.__dict__ if current else None,
            "average_metrics": average.__dict__ if average else None,
            "recommendations": recommendations,
            "monitoring_active": self.is_monitoring,
            "history_size": len(self.metrics_history),
            "optimization_settings": {
                "memory_optimization": self.optimize_memory,
                "cpu_optimization": True,  # Always enabled
                "gpu_optimization": True   # If available
            }
        }
    
    def __enter__(self):
        """Context manager entry"""
        self.start_monitoring()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop_monitoring()


class MemoryManager:
    """
    Manager pamięci dla komponentów STT
    """
    
    def __init__(self):
        """Inicjalizacja memory managera"""
        self.cached_models = {}
        self.cache_limit_mb = 2000  # 2GB limit
        
    def cache_model(self, model_name: str, model_object):
        """Cachuj model w pamięci"""
        try:
            # Oszacuj rozmiar modelu
            model_size_mb = self._estimate_model_size(model_object)
            
            # Sprawdź czy mieści się w limicie
            if model_size_mb > self.cache_limit_mb:
                logger.warning(f"⚠️ Model {model_name} zbyt duży dla cache: {model_size_mb}MB")
                return False
            
            # Wyczyść cache jeśli potrzeba
            self._cleanup_cache_if_needed(model_size_mb)
            
            # Dodaj do cache
            self.cached_models[model_name] = {
                "model": model_object,
                "size_mb": model_size_mb,
                "last_used": time.time()
            }
            
            logger.info(f"💾 Model {model_name} cachowany ({model_size_mb}MB)")
            return True
            
        except Exception as e:
            logger.error(f"❌ Model caching error: {e}")
            return False
    
    def get_cached_model(self, model_name: str):
        """Pobierz model z cache"""
        if model_name in self.cached_models:
            self.cached_models[model_name]["last_used"] = time.time()
            return self.cached_models[model_name]["model"]
        return None
    
    def _estimate_model_size(self, model_object) -> float:
        """Oszacuj rozmiar modelu w MB"""
        try:
            import torch
            if hasattr(model_object, "parameters"):
                total_params = sum(p.numel() for p in model_object.parameters())
                # Załóż 4 bajty na parametr (float32)
                return (total_params * 4) / 1024**2
        except:
            pass
        
        # Fallback - domyślny rozmiar
        return 500.0  # MB
    
    def _cleanup_cache_if_needed(self, needed_mb: float):
        """Wyczyść cache jeśli potrzeba miejsca"""
        current_size = sum(info["size_mb"] for info in self.cached_models.values())
        
        if current_size + needed_mb > self.cache_limit_mb:
            # Sortuj według ostatniego użycia
            sorted_models = sorted(
                self.cached_models.items(),
                key=lambda x: x[1]["last_used"]
            )
            
            # Usuń najstarsze modele
            for model_name, info in sorted_models:
                del self.cached_models[model_name]
                current_size -= info["size_mb"]
                logger.info(f"🗑️ Usunięto z cache: {model_name}")
                
                if current_size + needed_mb <= self.cache_limit_mb:
                    break


# Singleton instance
performance_optimizer = PerformanceOptimizer()
memory_manager = MemoryManager()
