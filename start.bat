@echo off
title Real-time Speech-to-Text Polish
color 0A
echo.
echo  ======================================================
echo    🎤 Real-time Speech-to-Text Polish v1.0.0
echo  ======================================================
echo.
echo  Wybierz opcję uruchomienia:
echo.
echo  [1] 🎨 GUI Application (Recommended)
echo  [2] 🎤 Command Line Demo  
echo  [3] 🔧 Audio System Test
echo  [4] 🧪 Complete System Test
echo  [5] 📦 Install Dependencies
echo  [6] 📖 Open Documentation
echo  [7] ❌ Exit
echo.
set /p choice="  Twój wybór (1-7): "

if "%choice%"=="1" (
    echo.
    echo  🚀 Uruchamianie GUI Application...
    python gui_launcher.py
) else if "%choice%"=="2" (
    echo.
    echo  🎤 Uruchamianie Command Line Demo...
    python main.py --mode demo
) else if "%choice%"=="3" (
    echo.
    echo  🔧 Testowanie systemu audio...
    python main.py --mode audio-test
) else if "%choice%"=="4" (
    echo.
    echo  🧪 Uruchamianie testów systemu...
    python test_complete_system.py
) else if "%choice%"=="5" (
    echo.
    echo  📦 Instalowanie dependencies...
    python install_complete_system.py
) else if "%choice%"=="6" (
    echo.
    echo  📖 Otwieranie dokumentacji...
    start START_HERE.md
    start README.md
) else if "%choice%"=="7" (
    echo.
    echo  👋 Do widzenia!
    exit /b 0
) else (
    echo.
    echo  ❌ Nieprawidłowy wybór. Spróbuj ponownie.
    pause
    goto :eof
)

echo.
echo  ✅ Zakończono.
pause
