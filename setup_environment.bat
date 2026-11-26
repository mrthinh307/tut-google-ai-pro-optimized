@echo off
chcp 65001 >nul
title One-Click Environment Setup
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8

echo ============================================================
echo   Google Ultra / Pro One-Click Setup
echo   - Check Python installation
echo   - Install Frida 16.5.9
echo   - Detect or download ADB
echo   - Connect to MuMu emulator and run self-test
echo ============================================================
echo.
pause

python setup_env.py

echo.
echo ------------------------------------------------------------
echo   Done. If all checks passed green, run 12months-eft.bat to begin.
echo ------------------------------------------------------------
pause
