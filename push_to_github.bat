@echo off
echo 🚀 Push Real-time STT Polish to GitHub
echo =======================================

echo.
echo 📂 Current directory: %CD%
echo 🌐 Repository: https://github.com/fortenemy/realtime-stt-polish
echo.

echo 🔍 Checking git status...
git --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Git not found! Please install Git first.
    pause
    exit /b 1
)

echo ✅ Git found
echo.

echo 🔧 Initializing git repository...
git init
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️ Git already initialized or error occurred
)

echo.
echo 🔗 Adding remote repository...
git remote add origin https://github.com/fortenemy/realtime-stt-polish.git 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️ Remote already exists or error occurred
    echo 🔄 Trying to set remote URL...
    git remote set-url origin https://github.com/fortenemy/realtime-stt-polish.git
)

echo.
echo 📋 Checking current status...
git status

echo.
echo 📦 Adding all files...
git add .

echo.
echo 📊 Files to be committed:
git status --short

echo.
set /p CONTINUE="Continue with commit? (y/N): "
if /i "%CONTINUE%" NEQ "y" (
    echo ❌ Aborted by user
    pause
    exit /b 0
)

echo.
echo 💾 Creating commit...
git commit -m "feat: initial commit with complete real-time STT architecture

- Add AudioCapture module for real-time microphone recording
- Implement dual VAD system (SimpleVAD + WebRTC VAD)  
- Create RealtimePipeline orchestrator for audio processing
- Add comprehensive testing infrastructure (audio, VAD, integration)
- Include complete documentation (Polish + English)
- Set up GitHub repository with CI/CD pipeline
- Add professional README with architecture diagrams
- Configure development tools and contribution guidelines

Components implemented:
- AudioCapture: Thread-safe real-time recording with statistics
- SimpleVAD: Custom voice activity detection algorithm
- WebRTCVAD: Professional VAD with multiple sensitivity modes
- RealtimePipeline: Main orchestrator with speech segmentation
- Comprehensive test suite with audio device validation
- Multi-language documentation and development logs

Status: 22.5%% complete - Audio pipeline ready for STT integration"

if %ERRORLEVEL% NEQ 0 (
    echo ❌ Commit failed!
    pause
    exit /b 1
)

echo.
echo 🚀 Pushing to GitHub...
git branch -M main
git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Successfully pushed to GitHub!
    echo 🌐 Visit: https://github.com/fortenemy/realtime-stt-polish
    echo.
    echo 🔄 Next steps:
    echo   - Check GitHub Actions for CI/CD pipeline
    echo   - Review README.md display
    echo   - Create first release (v0.1.0)
    echo   - Set up branch protection rules
) else (
    echo.
    echo ❌ Push failed! 
    echo 💡 You may need to authenticate with GitHub
    echo    Try: git push -u origin main
    echo.
    echo 🔧 Troubleshooting:
    echo   - Check internet connection
    echo   - Verify GitHub credentials
    echo   - Check repository permissions
)

echo.
pause
