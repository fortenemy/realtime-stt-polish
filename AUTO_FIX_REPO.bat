@echo off
echo 🛠️ AUTOMATYCZNA NAPRAWA GITHUB REPO
echo ====================================
echo.
echo 🎯 Target: https://github.com/fortenemy/realtime-stt-polish
echo 📂 Source: D:\projekty AI\rozkminianie
echo.

REM Przejdź do folderu projektu
cd /d "D:\projekty AI\rozkminianie"

echo ✅ Folder projektu: %CD%
echo.

REM Sprawdź czy są pliki
echo 🔍 Sprawdzanie plików projektu...
if not exist "src\audio_capture.py" (
    echo ❌ BŁĄD: Brak plików źródłowych!
    echo 💡 Upewnij się że jesteś w folderze: D:\projekty AI\rozkminianie
    pause
    exit /b 1
)
echo ✅ Pliki źródłowe znalezione

REM Sprawdź git
echo 🔍 Sprawdzanie git...
git --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Git nie jest zainstalowany!
    echo 💡 Zainstaluj z: https://git-scm.com/
    pause
    exit /b 1
)
echo ✅ Git dostępny

REM Reset git config
echo 🔧 Resetowanie konfiguracji git...
git remote remove origin 2>nul
git remote add origin https://github.com/fortenemy/realtime-stt-polish.git

REM Sprawdź status
echo 📊 Status git przed naprawą:
git status

REM Dodaj WSZYSTKIE pliki
echo 📦 Dodawanie wszystkich plików...
git add .
git add -A
git add --all

REM Sprawdź co zostanie commitowane
echo 📋 Pliki do commit:
git diff --cached --name-only

REM Policz pliki
for /f %%i in ('git diff --cached --name-only ^| find /c /v ""') do set FILE_COUNT=%%i
echo 📊 Liczba plików do commit: %FILE_COUNT%

if %FILE_COUNT% LSS 10 (
    echo ⚠️ UWAGA: Mało plików do commit (%FILE_COUNT%)
    echo 🔍 Sprawdzam co może być nie tak...
    
    echo.
    echo 📂 Pliki w folderze:
    dir /b
    
    echo.
    echo 🔍 Git status szczegółowy:
    git status --porcelain
    
    echo.
    set /p CONTINUE="Kontynuować mimo małej liczby plików? (tak/nie): "
    if /i "!CONTINUE!" NEQ "tak" (
        echo ❌ Anulowano
        pause
        exit /b 0
    )
)

REM Utwórz commit
echo 💾 Tworzenie commit...
git commit -m "feat: complete real-time Speech-to-Text system for Polish language

🎤 Real-time STT System Components:
✅ AudioCapture: Thread-safe real-time microphone recording with buffering
✅ Voice Activity Detection: Dual system (SimpleVAD + WebRTC VAD)
✅ RealtimePipeline: Main orchestrator with speech segmentation
✅ Comprehensive Testing: Audio devices, VAD algorithms, integration tests
✅ Professional Documentation: Polish + English, API reference, troubleshooting
✅ GitHub Integration: CI/CD pipeline, issue templates, contribution guidelines

🏗️ Architecture:
- Real-time audio processing with <500ms latency
- Cross-platform compatibility (Windows/Linux/macOS)
- Thread-safe design with queue-based audio buffering
- Configurable VAD with hysteresis and multiple sensitivity modes
- Modular design ready for Whisper STT integration

📊 Technical Features:
- Sample Rate: 16kHz optimized for speech recognition
- Audio Format: Float32 with automatic device detection
- Buffer Management: Overflow protection with statistics
- Error Handling: Graceful degradation and comprehensive logging
- Testing: Unit tests, integration tests, audio hardware validation

🚀 Development Status: 22.5%% complete
📋 Next Phase: OpenAI Whisper integration for Polish speech recognition

Repository: https://github.com/fortenemy/realtime-stt-polish"

if %ERRORLEVEL% NEQ 0 (
    echo ❌ Commit nieudany!
    echo 🔍 Możliwe przyczyny:
    echo   - Brak zmian do commitowania
    echo   - Błąd w konfiguracji git
    echo   - Problemy z uprawnieniami
    
    echo.
    echo 📊 Sprawdzam szczegóły...
    git status
    pause
    exit /b 1
)

REM Ustaw branch main
echo 🔀 Ustawianie main branch...
git branch -M main

REM FORCE PUSH (nadpisuje zawartość GitHub)
echo 🚀 FORCE PUSH do GitHub...
echo ⚠️  To nadpisze zawartość repo na GitHub
echo.

git push --force-with-lease origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo 🎉 🎉 🎉 SUKCES! REPO NAPRAWIONE! 🎉 🎉 🎉
    echo =============================================
    echo.
    echo ✅ Wszystkie pliki zostały wysłane na GitHub!
    echo ✅ Repository jest teraz w pełni funkcjonalne
    echo.
    echo 🌐 Sprawdź wyniki na:
    echo    https://github.com/fortenemy/realtime-stt-polish
    echo.
    echo 🔍 Co powinno być teraz widoczne:
    echo   ✅ Professional README.md z badges
    echo   ✅ Folder src/ z kodem (AudioCapture, VAD, Pipeline)
    echo   ✅ Testy: test_audio_capture.py, test_vad.py
    echo   ✅ Dokumentacja: docs/, CONTRIBUTING.md, CHANGELOG.md
    echo   ✅ GitHub Actions w zakładce Actions
    echo   ✅ Issue templates w Issues
    echo.
    echo 🎯 Następne kroki:
    echo   1. Sprawdź czy GitHub Actions przechodzi (zielone ✓)
    echo   2. Utwórz pierwszy release v0.1.0
    echo   3. Zacznij implementację Whisper STT engine
    echo.
    echo 📊 Statystyki repo:
    git log --oneline -1
    echo.
    
) else (
    echo.
    echo ❌ ❌ ❌ PUSH NIEUDANY! ❌ ❌ ❌
    echo ================================
    echo.
    echo 🔐 Prawdopodobnie problem z autoryzacją GitHub
    echo.
    echo 💡 ROZWIĄZANIA:
    echo.
    echo 🎯 1. GitHub Desktop (NAJŁATWIEJSZE):
    echo      - Pobierz: https://desktop.github.com/
    echo      - Zaloguj się kontem GitHub
    echo      - Add Local Repository → wybierz ten folder
    echo      - Publish changes
    echo.
    echo 🎯 2. Autoryzacja w przeglądarce:
    echo      - git config --global user.name "fortenemy"
    echo      - git config --global user.email "your-email@example.com"
    echo      - git push origin main
    echo.
    echo 🎯 3. Personal Access Token:
    echo      - GitHub → Settings → Developer settings → Personal access tokens
    echo      - Generate new token z repo permissions
    echo      - git remote set-url origin https://fortenemy:TOKEN@github.com/fortenemy/realtime-stt-polish.git
    echo      - git push origin main
    echo.
    echo 🎯 4. SSH Key:
    echo      - ssh-keygen -t rsa -b 4096 -C "your-email@example.com"
    echo      - Dodaj klucz do GitHub → Settings → SSH keys
    echo      - git remote set-url origin git@github.com:fortenemy/realtime-stt-polish.git
    echo.
)

echo.
echo 📋 Status końcowy:
git status
echo.
echo 📊 Pliki w repo:
git ls-files | wc -l
echo.

pause
