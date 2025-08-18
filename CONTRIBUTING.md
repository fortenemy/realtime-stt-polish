# Contributing to Real-time Speech-to-Text Polish

First off, thank you for considering contributing to this project! 🎉

## Code of Conduct

This project adheres to a Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### 🐛 Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates.

**When submitting a bug report, please include:**
- Clear, descriptive title
- Steps to reproduce the issue
- Expected vs actual behavior
- Your environment (OS, Python version, hardware)
- Relevant logs or error messages
- Audio configuration (sample rate, device type)

### 💡 Suggesting Enhancements

Enhancement suggestions are welcome! Please provide:
- Clear description of the enhancement
- Explanation of why this would be useful
- Possible implementation approach
- Examples of usage

### 🔧 Code Contributions

#### Development Setup

1. **Fork and clone the repository**
```bash
git clone https://github.com/your-username/realtime-stt-polish.git
cd realtime-stt-polish
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install development dependencies**
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # When available
```

4. **Create a feature branch**
```bash
git checkout -b feature/your-feature-name
```

#### Coding Standards

**Python Style**
- Follow PEP 8
- Use type hints where possible
- Maximum line length: 88 characters (Black formatter)
- Use meaningful variable and function names

**Documentation**
- Add docstrings to all public functions and classes
- Include type information in docstrings
- Update README.md for significant changes
- Add comments for complex logic

**Code Example:**
```python
def process_audio_chunk(
    self, 
    audio_chunk: np.ndarray, 
    sample_rate: int = 16000
) -> Tuple[bool, Dict[str, Any]]:
    """
    Process audio chunk for voice activity detection.
    
    Args:
        audio_chunk: Audio data as numpy array
        sample_rate: Sample rate in Hz
        
    Returns:
        Tuple of (is_speech, analysis_data)
        
    Raises:
        ValueError: If audio_chunk is empty
    """
    # Implementation here
    pass
```

#### Testing

**Before submitting:**
- Run all existing tests: `python -m pytest tests/`
- Add tests for new functionality
- Ensure audio tests work with different hardware
- Test on different operating systems if possible

**Test Categories:**
- Unit tests for individual components
- Integration tests for component interaction
- Audio hardware tests (may require manual verification)
- Performance tests for real-time requirements

#### Performance Guidelines

**For real-time audio processing:**
- Target <500ms latency
- Memory usage should be bounded
- CPU usage <50% on modern hardware
- Handle audio dropouts gracefully

**Optimization priorities:**
1. Correctness
2. Real-time performance
3. Memory efficiency
4. Code readability

#### Commit Messages

Use conventional commit format:
```
type(scope): description

Examples:
feat(vad): add WebRTC VAD integration
fix(audio): resolve buffer overflow in AudioCapture
docs(readme): update installation instructions
test(pipeline): add integration tests for real-time processing
```

**Types:**
- `feat`: New features
- `fix`: Bug fixes
- `docs`: Documentation changes
- `test`: Test additions/modifications
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `chore`: Maintenance tasks

### 🌍 Language Support

**Polish Language Improvements:**
- Pronunciation variations
- Regional dialects
- Domain-specific terminology
- Accuracy improvements

**Additional Languages:**
- Follow the same architecture
- Create language-specific configurations
- Provide test samples
- Document language-specific considerations

### 📚 Documentation

**Areas needing documentation:**
- API reference
- Architecture decisions
- Performance tuning guides
- Deployment instructions
- Troubleshooting guides

### 🎯 Priority Areas

**High Priority:**
- STT engine integration (Whisper)
- Performance optimizations
- Cross-platform compatibility
- Error handling improvements

**Medium Priority:**
- GUI applications
- Additional audio formats
- Cloud deployment guides
- Mobile support

**Low Priority:**
- Additional VAD algorithms
- Advanced audio preprocessing
- Custom model training
- Hardware acceleration

## Pull Request Process

1. **Pre-submission checklist:**
   - [ ] Code follows style guidelines
   - [ ] Self-review completed
   - [ ] Tests added/updated
   - [ ] Documentation updated
   - [ ] No merge conflicts

2. **Pull request template:**
   - Clear description of changes
   - Link to related issues
   - Screenshots for UI changes
   - Performance impact assessment

3. **Review process:**
   - Automated tests must pass
   - Code review by maintainers
   - Manual testing for audio features
   - Documentation review

4. **Merging:**
   - Squash and merge for feature branches
   - Maintain clean commit history
   - Update version numbers if needed

## Development Guidelines

### Audio Testing

**Testing with different hardware:**
- USB microphones
- Built-in laptop microphones
- Professional audio interfaces
- Bluetooth headsets

**Testing environments:**
- Quiet environments
- Noisy backgrounds
- Different speaker accents
- Various audio quality levels

### Performance Testing

**Benchmarking:**
- Latency measurements
- CPU/memory profiling
- Long-running stability tests
- Stress testing with multiple audio sources

**Tools:**
- `cProfile` for performance profiling
- `memory_profiler` for memory usage
- Audio analysis tools for quality assessment

### Platform-Specific Considerations

**Windows:**
- WASAPI vs DirectSound
- Audio driver compatibility
- Permission handling

**Linux:**
- ALSA/PulseAudio configuration
- Real-time audio permissions
- Distribution-specific packages

**macOS:**
- Core Audio integration
- Security permissions
- M1/Intel compatibility

## Community

### Getting Help

- **Discord/Slack:** [Community chat link]
- **GitHub Discussions:** For questions and ideas
- **Stack Overflow:** Tag with `realtime-stt-polish`

### Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Credited in release notes
- Invited to contributor discussions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing! 🚀
