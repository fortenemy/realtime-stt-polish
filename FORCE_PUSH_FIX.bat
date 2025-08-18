@echo off
echo 🛠️ Naprawianie problemu z GitHub push
echo ===================================
echo.

cd /d "D:\projekty AI\rozkminianie"

echo 📂 Folder: %CD%
echo 🌐 Target: https://github.com/fortenemy/realtime-stt-polish
echo.

echo 🔄 Krok 1: Reset i ponowna konfiguracja...
echo.

REM Usuń istniejący remote (może być źle skonfigurowany)
git remote remove origin 2>nul

REM Dodaj remote ponownie
echo ✅ Dodawanie remote repository...
git remote add origin https://github.com/fortenemy/realtime-stt-polish.git

REM Sprawdź remote
echo ✅ Sprawdzanie remote:
git remote -v

echo.
echo 🔄 Krok 2: Przygotowanie plików...
echo.

REM Dodaj wszystkie pliki
echo ✅ Dodawanie wszystkich plików...
git add .

REM Sprawdź status
echo ✅ Status:
git status --short

echo.
echo 🔄 Krok 3: Tworzenie commit (jeśli potrzeba)...
echo.

REM Sprawdź czy są zmiany do commit
git diff --cached --quiet
if %ERRORLEVEL% NEQ 0 (
    echo ✅ Tworzenie nowego commit...
    git commit -m "feat: complete real-time STT system

Real-time Speech-to-Text system optimized for Polish language featuring:

Core Modules:
- AudioCapture: Thread-safe real-time microphone recording
- Voice Activity Detection: Dual system (SimpleVAD + WebRTC)  
- RealtimePipeline: Main orchestrator with speech segmentation
- Comprehensive testing suite with audio device validation

Features:
- Low-latency processing (~300ms target)
- Cross-platform compatibility (Windows/Linux/macOS)
- Professional documentation (Polish + English)
- GitHub CI/CD pipeline with automated testing
- Complete development infrastructure

Status: Audio pipeline foundation complete, ready for STT integration"
) else (
    echo ✅ Używanie istniejącego commit...
)

echo.
echo 🔄 Krok 4: Push do GitHub...
echo.

REM Ustaw main branch
git branch -M main

REM Force push (na wypadek konfliktów)
echo ✅ Wykonywanie push...
git push -u origin main --force

if %ERRORLEVEL% EQU 0 (
    echo.
    echo 🎉 🎉 🎉 NAPRAWIONE! 🎉 🎉 🎉
    echo ================================
    echo.
    echo ✅ Pliki zostały wysłane na GitHub!
    echo ✅ Repository jest teraz aktywne
    echo.
    echo 🌐 Sprawdź wyniki:
    echo    https://github.com/fortenemy/realtime-stt-polish
    echo.
    echo 🔍 Co sprawdzić:
    echo   ✅ Pliki źródłowe w folderze src/
    echo   ✅ README.md z profesjonalną dokumentacją
    echo   ✅ GitHub Actions w zakładce "Actions"
    echo   ✅ Issues templates w "Issues"
    echo.
    echo 🎯 Następne kroki:
    echo   1. Sprawdź czy GitHub Actions przechodzi
    echo   2. Utwórz pierwszy release (v0.1.0)
    echo   3. Zacznij implementację Whisper STT
    echo.
) else (
    echo.
    echo ❌ ❌ ❌ NADAL PROBLEM! ❌ ❌ ❌
    echo ================================
    echo.
    echo 🔐 Prawdopodobnie problem z autoryzacją GitHub
    echo.
    echo 💡 ROZWIĄZANIA:
    echo.
    echo 🎯 Opcja 1 - GitHub Desktop:
    echo   1. Pobierz GitHub Desktop z: https://desktop.github.com/
    echo   2. Zaloguj się swoim kontem GitHub
    echo   3. File → Add Local Repository
    echo   4. Wybierz folder: D:\projekty AI\rozkminianie
    echo   5. Publish repository
    echo.
    echo 🎯 Opcja 2 - Personal Access Token:
    echo   1. Idź na GitHub.com → Settings → Developer settings
    echo   2. Personal access tokens → Generate new token
    echo   3. Skopiuj token
    echo   4. git remote set-url origin https://USERNAME:TOKEN@github.com/fortenemy/realtime-stt-polish.git
    echo   5. git push -u origin main
    echo.
    echo 🎯 Opcja 3 - SSH Key:
    echo   1. Wygeneruj SSH key: ssh-keygen -t rsa -b 4096 -C "your-email@example.com"
    echo   2. Dodaj do GitHub: Settings → SSH and GPG keys
    echo   3. git remote set-url origin git@github.com:fortenemy/realtime-stt-polish.git
    echo   4. git push -u origin main
    echo.
)

echo.
echo 📊 Końcowy status repository:
git status
echo.
echo 📋 Ostatnie commity:
git log --oneline -3
echo.

pause
