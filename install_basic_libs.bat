@echo off
echo 🚀 Instalacja podstawowych bibliotek Real-time STT
echo ===============================================

echo.
echo 📦 Instalowanie NumPy...
python -m pip install numpy
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Błąd instalacji NumPy
    pause
    exit /b 1
)

echo.
echo 📦 Instalowanie SoundDevice...
python -m pip install sounddevice
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Błąd instalacji SoundDevice
    pause
    exit /b 1
)

echo.
echo 📦 Instalowanie Colorama...
python -m pip install colorama
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Błąd instalacji Colorama
    pause
    exit /b 1
)

echo.
echo ✅ Podstawowe biblioteki zainstalowane!
echo.
echo 🧪 Uruchamiam test...
python simple_test.py

pause
