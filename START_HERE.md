# 🎤 Real-time Speech-to-Text Polish - START HERE

## 🚀 Quick Start Guide

### 1. **Complete Installation** (Recommended)
```bash
python install_complete_system.py
```
This will automatically install ALL dependencies and set up the entire system.

### 2. **Manual Installation** (Advanced users)
```bash
pip install -r requirements.txt
python install_whisper_dependencies.py
```

### 3. **Test Your System**
```bash
python test_complete_system.py
```

## 🎯 Usage Options

### **🎨 GUI Application** (Easiest)
```bash
python gui_launcher.py
```
- Full graphical interface
- Real-time transcription
- Export to multiple formats
- Performance monitoring

### **🎤 Command Line Demo**
```bash
python main.py --mode demo
```
- Quick start demo
- Terminal-based interface
- Real-time speech recognition

### **🔧 Advanced Options**
```bash
# Audio system test
python main.py --mode audio-test

# Full system test
python test_complete_system.py

# Custom model
python main.py --mode demo --model small

# Verbose logging
python main.py --mode demo --verbose
```

## 📊 System Requirements

### **Minimum:**
- Python 3.8+
- 4GB RAM
- 2GB free disk space
- Microphone

### **Recommended:**
- Python 3.9+
- 8GB RAM
- NVIDIA GPU (for faster processing)
- Good quality microphone

## 🛠️ Features

### ✅ **Core Features**
- **Real-time speech-to-text** from microphone
- **Polish language optimization** 
- **Voice Activity Detection** (VAD)
- **Multiple STT models** (tiny, base, small, medium, large)
- **High accuracy** transcription

### ✅ **Advanced Features**
- **GUI Application** with real-time visualization
- **Export formats**: TXT, JSON, CSV, SRT, VTT, XML, DOCX
- **Performance monitoring** and optimization
- **Configurable settings** and profiles
- **Batch processing** capabilities

### ✅ **Technical Features**
- **GPU acceleration** (CUDA support)
- **Memory management** and optimization
- **Thread-safe** audio processing
- **Error handling** and recovery
- **Comprehensive logging**

## 🆘 Troubleshooting

### **Common Issues:**

#### 1. **"Module not found" errors**
```bash
python install_complete_system.py
```

#### 2. **No audio input detected**
```bash
python main.py --mode audio-test
```

#### 3. **Whisper not working**
```bash
python install_whisper_dependencies.py
```

#### 4. **Performance issues**
- Use smaller model (tiny/base)
- Close other applications
- Check `python test_complete_system.py`

### **Get Help:**
1. Run system test: `python test_complete_system.py`
2. Check logs in `logs/` folder
3. See detailed documentation in `README.md`
4. Visit GitHub: https://github.com/fortenemy/realtime-stt-polish

## 📁 Project Structure

```
📦 realtime-stt-polish/
├── 🎨 gui_launcher.py          # GUI Application Launcher
├── 🎤 main.py                  # CLI Application
├── 🔧 install_complete_system.py # Complete Installer
├── 🧪 test_complete_system.py  # System Tests
├── 📋 start.bat               # Easy Windows Launcher
├── 📖 README.md               # Full Documentation
├── 📝 requirements.txt        # Python Dependencies
├── 📂 src/                    # Core System Modules
│   ├── 🎵 audio_capture.py
│   ├── 🗣️ voice_activity_detector.py
│   ├── 🤖 stt_engine.py
│   ├── 🔗 realtime_pipeline.py
│   ├── 📊 performance_optimizer.py
│   ├── 📤 export_manager.py
│   └── 🎨 gui_application.py
├── 📂 docs/                   # Documentation
├── 📂 logs/                   # Development Logs
└── 📂 tests/                  # Test Files
```

## 🎯 Next Steps

1. **First Time Setup:**
   ```bash
   python install_complete_system.py
   python test_complete_system.py
   python gui_launcher.py
   ```

2. **Daily Usage:**
   - Double-click `start.bat` (Windows)
   - Or run: `python gui_launcher.py`

3. **Advanced Usage:**
   - Customize settings in GUI
   - Export transcriptions
   - Monitor performance
   - Use different models

## 🎉 You're Ready!

**Real-time Speech-to-Text Polish** is now fully installed and ready to use!

Choose your preferred method:
- **Easy**: Double-click `start.bat`
- **GUI**: `python gui_launcher.py`  
- **CLI**: `python main.py --mode demo`

Happy transcribing! 🎤✨
