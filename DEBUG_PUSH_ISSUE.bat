@echo off
echo 🔍 Diagnoza problemu z push do GitHub
echo ====================================
echo.

cd /d "D:\projekty AI\rozkminianie"
echo 📂 Aktualny folder: %CD%
echo.

echo 🔧 Sprawdzanie stanu Git repository...
echo.

REM Sprawdź czy git jest zainicjalizowany
echo 1. Git status:
git status
echo.

REM Sprawdź remote
echo 2. Remote repositories:
git remote -v
echo.

REM Sprawdź branche
echo 3. Branche:
git branch -a
echo.

REM Sprawdź ostatnie commity
echo 4. Ostatnie commity:
git log --oneline -5
echo.

REM Sprawdź staged files
echo 5. Pliki w staging area:
git ls-files
echo.

REM Sprawdź czy są niestaged zmiany
echo 6. Niestaged zmiany:
git diff --name-only
echo.

REM Sprawdź czy są staged zmiany
echo 7. Staged zmiany:
git diff --cached --name-only
echo.

echo ====================================
echo 💡 MOŻLIWE PRZYCZYNY:
echo.
echo ❌ 1. Commit nie został utworzony
echo ❌ 2. Push nie przeszedł przez autoryzację
echo ❌ 3. Push poszedł do złego repository  
echo ❌ 4. Pliki nie zostały dodane do commit
echo ❌ 5. Błędy autoryzacji GitHub
echo.
echo 🔧 ROZWIĄZANIA:
echo.
echo ✅ A. Sprawdź czy commit istnieje: git log
echo ✅ B. Sprawdź remote URL: git remote -v
echo ✅ C. Spróbuj push ponownie: git push -u origin main
echo ✅ D. Sprawdź autoryzację GitHub
echo.

pause
echo.
echo 🚀 Czy chcesz spróbować naprawić automatycznie?
set /p FIX="Naprawa automatyczna? (tak/nie): "

if /i "%FIX%" NEQ "tak" (
    echo ❌ Anulowano
    exit /b 0
)

echo.
echo 🔄 Próba naprawy...
echo.

REM Sprawdź czy są pliki do dodania
echo 1. Dodawanie wszystkich plików...
git add .

REM Sprawdź status po add
echo 2. Status po git add:
git status --short

REM Jeśli są pliki do commit, zrób commit
git diff --cached --quiet
if %ERRORLEVEL% NEQ 0 (
    echo 3. Tworzenie commit...
    git commit -m "feat: initial commit - real-time STT architecture with AudioCapture, VAD, and Pipeline"
) else (
    echo 3. Brak zmian do commit
)

REM Sprawdź czy istnieje commit
git log --oneline -1 >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Brak commitów w repository!
    echo 💡 Musisz najpierw utworzyć commit
    pause
    exit /b 1
)

REM Ustaw main branch
echo 4. Ustawianie main branch...
git branch -M main

REM Sprawdź remote
git remote get-url origin >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo 5. Dodawanie remote origin...
    git remote add origin https://github.com/fortenemy/realtime-stt-polish.git
) else (
    echo 5. Remote origin już istnieje
)

REM Push
echo 6. Push do GitHub...
git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ ✅ ✅ SUKCES! ✅ ✅ ✅
    echo Push zakończony pomyślnie!
    echo.
    echo 🌐 Sprawdź: https://github.com/fortenemy/realtime-stt-polish
    echo.
) else (
    echo.
    echo ❌ Push nadal nie działa!
    echo.
    echo 🔐 Prawdopodobnie problem z autoryzacją GitHub
    echo.
    echo 💡 Spróbuj:
    echo   1. Otwórz GitHub Desktop
    echo   2. Zaloguj się do GitHub
    echo   3. Spróbuj push ponownie przez GitHub Desktop
    echo.
    echo Lub:
    echo   1. git config --global user.name "fortenemy"
    echo   2. git config --global user.email "your-email@example.com"
    echo   3. git push -u origin main
    echo.
)

pause
