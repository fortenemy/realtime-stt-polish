@echo off
echo 🔍 DIAGNOZA PROBLEMU Z TERMINALEM
echo ==================================
echo.

REM Sprawdź gdzie jesteś
echo 📂 Aktualny folder:
cd
echo.

REM Sprawdź czy plik batch istnieje
echo 🔍 Sprawdzanie pliku AUTO_FIX_REPO.bat:
if exist "AUTO_FIX_REPO.bat" (
    echo ✅ Plik AUTO_FIX_REPO.bat znaleziony
) else (
    echo ❌ Plik AUTO_FIX_REPO.bat nie istnieje w tym folderze
    echo 💡 Sprawdź czy jesteś w folderze: D:\projekty AI\rozkminianie
)
echo.

REM Sprawdź czy jesteś w dobrym folderze
echo 🔍 Sprawdzanie plików projektu:
if exist "src\audio_capture.py" (
    echo ✅ src\audio_capture.py - ISTNIEJE
) else (
    echo ❌ src\audio_capture.py - BRAK
)

if exist "README.md" (
    echo ✅ README.md - ISTNIEJE
) else (
    echo ❌ README.md - BRAK
)

if exist "main.py" (
    echo ✅ main.py - ISTNIEJE
) else (
    echo ❌ main.py - BRAK
)
echo.

REM Sprawdź git
echo 🔍 Sprawdzanie Git:
git --version 2>nul
if %ERRORLEVEL% EQU 0 (
    echo ✅ Git jest zainstalowany
) else (
    echo ❌ Git nie jest dostępny
    echo 💡 Zainstaluj Git z: https://git-scm.com/
)
echo.

REM Sprawdź uprawnienia
echo 🔍 Sprawdzanie uprawnień:
echo TEST > test_file.txt 2>nul
if exist test_file.txt (
    echo ✅ Uprawnienia do zapisu - OK
    del test_file.txt
) else (
    echo ❌ Brak uprawnień do zapisu
)
echo.

echo 💡 MOŻLIWE PRZYCZYNY:
echo.
echo ❌ 1. Nie jesteś w folderze projektu
echo ❌ 2. Plik AUTO_FIX_REPO.bat nie istnieje
echo ❌ 3. Brak uprawnień do wykonania
echo ❌ 4. Git nie jest zainstalowany
echo ❌ 5. Antywirus blokuje wykonanie
echo.

echo 🛠️ ROZWIĄZANIA:
echo.
echo ✅ A. Przejdź do folderu projektu:
echo    cd /d "D:\projekty AI\rozkminianie"
echo.
echo ✅ B. Uruchom bezpośrednio git commands:
echo    git status
echo    git add .
echo    git commit -m "test"
echo.
echo ✅ C. Spróbuj PowerShell script:
echo    .\Fix-GitHubRepo.ps1
echo.

pause
