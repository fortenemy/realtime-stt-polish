# 🎯 Push do GitHub przez Cursor - Krok po kroku

## 📋 Instrukcje dla Cursor Git Extension

### **Krok 1: Otwórz projekt w Cursor**
1. **File → Open Folder**
2. **Wybierz:** `D:\projekty AI\rozkminianie`
3. **Sprawdź** czy widzisz wszystkie pliki w explorer

### **Krok 2: Sprawdź panel Source Control**
1. **Kliknij ikonę Git** w left sidebar (trzecia ikona)
2. **Lub naciśnij:** `Ctrl + Shift + G`
3. **Powinieneś zobaczyć:** listę zmian do commit

### **Krok 3: Zainicjuj Git (jeśli potrzeba)**
Jeśli widzisz "Initialize Repository":
1. **Kliknij:** "Initialize Repository"  
2. **Lub użyj Command Palette:** `Ctrl + Shift + P` → "Git: Initialize Repository"

### **Krok 4: Stage wszystkie pliki**
1. **W panelu Source Control** kliknij **"+"** obok "Changes"
2. **Lub** kliknij **"Stage All Changes"**
3. **Wszystkie pliki** powinny przejść do "Staged Changes"

### **Krok 5: Utwórz commit**
1. **W polu Message** wpisz:
```
feat: initial commit with complete real-time STT architecture

Complete real-time Speech-to-Text system for Polish language:
- AudioCapture: Thread-safe real-time recording
- Dual VAD system: SimpleVAD + WebRTC  
- RealtimePipeline: Main orchestrator
- Comprehensive testing suite
- Professional documentation (PL + EN)
- GitHub CI/CD pipeline

Status: Audio foundation ready for STT integration
```

2. **Kliknij:** ✓ "Commit" (lub `Ctrl + Enter`)

### **Krok 6: Dodaj remote repository**
1. **Otwórz Terminal w Cursor:** `Ctrl + `` (backtick)
2. **Wpisz:**
```bash
git remote add origin https://github.com/fortenemy/realtime-stt-polish.git
```

### **Krok 7: Push przez Cursor**
1. **W panelu Source Control** kliknij **"..."** (więcej opcji)
2. **Wybierz:** "Push to..."
3. **Lub:** Command Palette → "Git: Push"
4. **Jeśli pierwsz push:** wybierz "origin" i "main"

### **Alternatywne metody w Cursor:**

#### **Metoda A: Command Palette**
1. `Ctrl + Shift + P`
2. Wpisz: "Git: Push"
3. Wybierz remote i branch

#### **Metoda B: Terminal w Cursor**
1. `Ctrl + `` (otwórz terminal)
2. Wykonaj:
```bash
git branch -M main
git push -u origin main
```

#### **Metoda C: GitHub Authentication**
1. `Ctrl + Shift + P`
2. "GitHub: Sign in"
3. Zaloguj się do GitHub
4. Spróbuj push ponownie

## 🔧 Jeśli są problemy:

### **Problem: "Authentication failed"**
**Rozwiązanie:**
1. `Ctrl + Shift + P` → "GitHub: Sign in"
2. Zaloguj się przez browser
3. Spróbuj push ponownie

### **Problem: "Repository not found"**
**Sprawdź remote:**
```bash
git remote -v
```
**Powinno pokazać:**
```
origin  https://github.com/fortenemy/realtime-stt-polish.git (fetch)
origin  https://github.com/fortenemy/realtime-stt-polish.git (push)
```

### **Problem: "No upstream branch"**
**Rozwiązanie:**
```bash
git push --set-upstream origin main
```

## 🎯 Sprawdzenie sukcesu:

### **W Cursor:**
1. **Panel Source Control** powinien pokazać "No changes"
2. **Terminal** powinien pokazać sukces push
3. **Status bar** (dół) powinien pokazać sync icon

### **Na GitHub:**
1. **Odśwież:** https://github.com/fortenemy/realtime-stt-polish
2. **Sprawdź** czy pliki są widoczne
3. **Sprawdź** czy README.md się wyświetla

## 🚀 Expected Success Message:
```
To https://github.com/fortenemy/realtime-stt-polish.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

## 💡 Pro Tips for Cursor:

1. **Git Graph Extension:** Zainstaluj dla lepszej wizualizacji
2. **GitHub Pull Requests:** Automatycznie wykryje GitHub repo
3. **GitLens:** Pokaże blame, historię, itp.
4. **Auto-fetch:** Automatycznie pobierze zmiany z GitHub

## 🔄 Jeśli nadal nie działa:

**Ostateczne rozwiązanie - GitHub CLI:**
1. W terminalu Cursor:
```bash
# Zainstaluj GitHub CLI (jeśli nie masz)
winget install GitHub.cli

# Zaloguj się
gh auth login

# Push
git push -u origin main
```

---

**🎉 Po sukcesie sprawdź:**
- GitHub repo: https://github.com/fortenemy/realtime-stt-polish
- GitHub Actions w zakładce "Actions"
- README.md z badges i dokumentacją
