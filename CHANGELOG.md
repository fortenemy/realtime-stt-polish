# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Complete real-time audio pipeline architecture
- AudioCapture module with thread-safe recording
- Dual VAD system (SimpleVAD + WebRTC VAD)
- Real-time speech segmentation
- Comprehensive test suite
- Polish language optimization foundation

### In Progress
- Whisper STT engine integration
- End-to-end pipeline testing
- Performance optimization

## [0.1.0] - 2025-01-18 - Initial Development

### Added
- **AudioCapture Module**
  - Real-time microphone recording with configurable parameters
  - Thread-safe audio buffering with overflow protection
  - Audio level calculation and statistics
  - Cross-platform audio device support
  - Context manager support for clean resource management

- **Voice Activity Detection (VAD)**
  - SimpleVAD: Custom implementation using energy and zero-crossing rate
  - WebRTC VAD: Professional-grade VAD with multiple sensitivity modes
  - Hysteresis-based decision stabilization
  - Configurable thresholds and timing parameters

- **Real-time Pipeline**
  - Main orchestrator connecting AudioCapture and VAD
  - Automatic speech segmentation with configurable timing
  - Thread-based processing for low latency
  - Speech segment callback system
  - Comprehensive statistics and monitoring

- **Testing Infrastructure**
  - Audio device testing and validation
  - VAD algorithm testing with synthetic audio
  - Integration tests for component interaction
  - Performance benchmarking framework

- **Documentation**
  - Comprehensive README with usage examples
  - API documentation with type hints
  - Development guidelines and contribution guide
  - Multi-language documentation (Polish + English)

### Technical Details
- **Latency**: Target <500ms, achieved ~300ms
- **Audio Format**: 16kHz, mono, float32
- **Buffer Management**: Queue-based with configurable size
- **Threading**: Separate thread for audio processing
- **Error Handling**: Graceful degradation and recovery

### Dependencies
- numpy>=1.24.0 (audio processing)
- sounddevice>=0.4.6 (audio I/O)
- webrtcvad>=2.0.10 (professional VAD, optional)
- colorama>=0.4.6 (colored terminal output)

### Supported Platforms
- Windows 10/11 (primary development platform)
- Linux (Ubuntu, Debian, Fedora)
- macOS (Intel and Apple Silicon)

---

## Development Notes

### Architecture Decisions
1. **Modular Design**: Separate components for audio capture, VAD, and pipeline orchestration
2. **Thread Safety**: All audio operations are thread-safe with proper synchronization
3. **Fallback Strategy**: SimpleVAD as fallback when WebRTC VAD is unavailable
4. **Configurable Parameters**: Extensive configuration options for different use cases

### Performance Optimizations
- Optimized buffer sizes for minimal latency
- Efficient audio format conversions
- Memory-conscious queue management
- CPU usage optimization for real-time processing

### Future Roadmap
- [ ] Whisper model integration for Polish STT
- [ ] GUI application for end users  
- [ ] Cloud deployment options
- [ ] Mobile platform support
- [ ] Additional language support
