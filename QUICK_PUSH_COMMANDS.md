# 🚀 Quick Push Commands - Copy & Paste

## Otwórz terminal w folderze projektu i wykonaj:

```bash
# 1. Przejdź do folderu projektu
cd "D:\projekty AI\rozkminianie"

# 2. Inicjalizuj git (jeśli nie zrobione)
git init

# 3. Dodaj remote repository
git remote add origin https://github.com/fortenemy/realtime-stt-polish.git

# 4. Dodaj wszystkie pliki
git add .

# 5. Sprawdź status
git status

# 6. Utwórz commit
git commit -m "feat: initial commit with complete real-time STT architecture - AudioCapture, VAD, Pipeline ready"

# 7. Ustaw main branch i push
git branch -M main
git push -u origin main
```

## 🔧 Jeśli są problemy z autoryzacją:

```bash
# Ustaw swoją tożsamość Git
git config --global user.name "fortenemy"
git config --global user.email "your-email@example.com"

# Spróbuj ponownie
git push -u origin main
```

## ⚡ Jedna komenda (wszystko naraz):

```bash
cd "D:\projekty AI\rozkminianie" && git init && git remote add origin https://github.com/fortenemy/realtime-stt-polish.git && git add . && git commit -m "feat: initial commit with complete real-time STT architecture" && git branch -M main && git push -u origin main
```

## 🎯 Oczekiwany wynik:

```
Counting objects: 25, done.
Delta compression using up to 8 threads.
Compressing objects: 100% (23/23), done.
Writing objects: 100% (25/25), 45.67 KiB | 0 bytes/s, done.
Total 25 (delta 2), reused 0 (delta 0)
To https://github.com/fortenemy/realtime-stt-polish.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

**✅ Po sukcesie sprawdź: https://github.com/fortenemy/realtime-stt-polish**
