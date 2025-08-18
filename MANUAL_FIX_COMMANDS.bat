@echo off
echo 🛠️ RĘCZNE KOMENDY - KOPIUJ I WKLEJ
echo =================================
echo.

echo 📋 SKOPIUJ I WKLEJ TE KOMENDY JEDNA PO DRUGIEJ:
echo.

echo 1️⃣ Przejdź do folderu projektu:
echo cd /d "D:\projekty AI\rozkminianie"
echo.

echo 2️⃣ Sprawdź czy jesteś w dobrym miejscu:
echo dir src
echo.

echo 3️⃣ Sprawdź status git:
echo git status
echo.

echo 4️⃣ Skonfiguruj remote:
echo git remote remove origin
echo git remote add origin https://github.com/fortenemy/realtime-stt-polish.git
echo.

echo 5️⃣ Dodaj wszystkie pliki:
echo git add .
echo.

echo 6️⃣ Sprawdź co zostanie commitowane:
echo git status
echo.

echo 7️⃣ Utwórz commit:
echo git commit -m "feat: complete real-time STT system"
echo.

echo 8️⃣ Push do GitHub:
echo git branch -M main
echo git push --force origin main
echo.

echo ================================
echo 💡 ALTERNATYWNIE - JEDNA KOMENDA:
echo ================================
echo.
echo cd /d "D:\projekty AI\rozkminianie" ^&^& git remote remove origin ^&^& git remote add origin https://github.com/fortenemy/realtime-stt-polish.git ^&^& git add . ^&^& git commit -m "feat: complete STT system" ^&^& git branch -M main ^&^& git push --force origin main
echo.

pause
